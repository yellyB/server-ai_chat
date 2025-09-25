from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import json
import asyncio
from typing import List, Dict, Optional
import uuid
from models import ChatMessage, ChatRoom, Character
from dialogue import dialogue_manager
from characters_data import create_character_objects

app = FastAPI(title="Escape Game Server", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3333"],  # React 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 채팅 관리자
class ChatManager:
    def __init__(self):
        self.rooms: Dict[str, ChatRoom] = {}
        self.message_queue: Dict[str, List[ChatMessage]] = {}  # room_id -> [messages]
        self.message_sequences: Dict[str, List[ChatMessage]] = {}  # room_id -> [pending_messages]
        self.current_sequence_index: Dict[str, int] = {}  # room_id -> current_index
        self.current_part_index: Dict[str, int] = {}  # room_id -> current_part (1부터 시작)
    
    async def create_room(self, room_id: str, room_name: str = None):
        """채팅방 생성"""
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(
                id=room_id,
                name=room_name or f"Room {room_id}",
                created_at=datetime.now()
            )
            self.message_queue[room_id] = []
    
    async def send_message_to_room(self, room_id: str, message: ChatMessage):
        """특정 방에 메시지 전송"""
        # 메시지를 큐에 저장
        if room_id not in self.message_queue:
            self.message_queue[room_id] = []
        self.message_queue[room_id].append(message)
    
    
    async def setup_message_sequence(self, room_id: str, messages: List[ChatMessage]):
        """메시지 시퀀스 설정"""
        if room_id not in self.message_sequences:
            self.message_sequences[room_id] = []
            self.current_sequence_index[room_id] = 0
            self.current_part_index[room_id] = 1  # 파트는 1부터 시작
        
        self.message_sequences[room_id] = messages
        self.current_sequence_index[room_id] = 0
        self.current_part_index[room_id] = 1
    
    async def get_next_message(self, room_id: str):
        """다음 메시지 가져오기"""
        if room_id not in self.message_sequences or room_id not in self.current_sequence_index:
            return None
        
        sequence = self.message_sequences[room_id]
        current_index = self.current_sequence_index[room_id]
        
        if current_index >= len(sequence):
            return None
        
        message = sequence[current_index]
        self.current_sequence_index[room_id] += 1
        
        return message
    
    
    async def send_next_part_messages(self, room_id: str):
        """다음 파트의 모든 메시지를 배열로 전송"""
        if room_id not in self.message_sequences or room_id not in self.current_part_index:
            return None
        
        current_part = self.current_part_index[room_id]
        
        # 현재 파트의 메시지들 찾기
        part_messages = [
            msg for msg in self.message_sequences[room_id] 
            if msg.part_number == current_part
        ]
        
        if not part_messages:
            return None
        
        # 파트 메시지들을 배열로 전송
        await self.send_message_to_room(room_id, {
            "type": "part_messages",
            "part_number": current_part,
            "messages": [msg.dict() for msg in part_messages],
            "is_dialogue_end": False  # 아직 끝인지 모름
        })
        
        # 다음 파트로 이동
        self.current_part_index[room_id] += 1
        
        # 더 이상 파트가 있는지 확인
        next_part_messages = [
            msg for msg in self.message_sequences[room_id] 
            if msg.part_number == self.current_part_index[room_id]
        ]
        
        if not next_part_messages:
            # 더 이상 파트가 없으면 대화 끝
            await self.send_message_to_room(room_id, {
                "type": "dialogue_end",
                "message": "대화가 끝났습니다"
            })
        
        return part_messages
    
    async def get_specific_part_messages(self, room_id: str, part_number: int):
        """특정 파트의 메시지들을 조회"""
        if room_id not in self.message_sequences:
            return None
        
        sequence = self.message_sequences[room_id]
        part_messages = [msg for msg in sequence if msg.part_number == part_number]
        
        if not part_messages:
            return None
        
        # 메시지들을 방에 전송
        for message in part_messages:
            await self.send_message_to_room(room_id, message)
        
        return part_messages
    

chat_manager = ChatManager()


class CharacterManager:
    """캐릭터 관리자"""
    
    def __init__(self):
        # 정적 데이터에서 캐릭터 객체 생성
        character_objects = create_character_objects()
        self.characters = character_objects
    
    def get_characters(self) -> List[Character]:
        """캐릭터 목록 반환"""
        return self.characters


character_manager = CharacterManager()

@app.get("/")
async def root():
    return {"message": "Escape Game Server is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 채팅 관련 API
@app.get("/chat/rooms")
async def get_chat_rooms():
    """채팅방 목록 조회"""
    return {"rooms": list(chat_manager.rooms.values())}


@app.get("/characters")
async def get_characters():
    """캐릭터 목록 조회"""
    characters = character_manager.get_characters()
    return {"characters": characters}


@app.post("/chat/rooms/{room_id}/setup-dialogue")
async def setup_dialogue(room_id: str, dialogue_id: str = "mina_dialogue"):
    """대화 시퀀스 설정"""
    # 채팅방 생성
    await chat_manager.create_room(room_id, "민아와의 대화")
    
    # 대화 시나리오 가져오기
    messages = dialogue_manager.get_dialogue(dialogue_id, room_id)
    
    # 메시지 시퀀스 설정
    await chat_manager.setup_message_sequence(room_id, messages)
    
    return {
        "status": "dialogue_setup",
        "total_messages": len(messages),
        "dialogue_id": dialogue_id
    }

@app.post("/chat/rooms/{room_id}/send")
async def send_message_to_room(room_id: str, message_data: dict = None):
    """다음 파트 자동 전송"""
    # 다음 파트 메시지 가져오기
    part_messages = await chat_manager.send_next_part_messages(room_id)
    
    if part_messages:
        return {
            "status": "sent", 
            "part_number": part_messages[0].part_number,
            "messages": [msg.dict() for msg in part_messages]
        }
    else:
        return {"status": "no_more_messages", "message": "대화가 끝났습니다"}


@app.post("/chat/rooms/{room_id}/next-part")
async def send_next_part_messages(room_id: str):
    """다음 파트의 모든 메시지를 배열로 전송"""
    part_messages = await chat_manager.send_next_part_messages(room_id)
    if part_messages:
        return {
            "status": "sent", 
            "part_number": part_messages[0].part_number,
            "messages": [msg.dict() for msg in part_messages]
        }
    else:
        return {"status": "no_more_messages", "message": "대화가 끝났습니다"}

@app.post("/chat/rooms/{room_id}/part/{part_number}")
async def get_specific_part_messages(room_id: str, part_number: int):
    """특정 파트의 메시지들을 조회"""
    part_messages = await chat_manager.get_specific_part_messages(room_id, part_number)
    if part_messages:
        return {
            "status": "sent", 
            "part_number": part_messages[0].part_number,
            "messages": [msg.dict() for msg in part_messages]
        }
    else:
        return {"status": "part_not_found", "message": f"파트 {part_number}를 찾을 수 없습니다"}

@app.get("/chat/rooms/{room_id}/sse")
async def chat_sse(room_id: str):
    """SSE 연결로 실시간 채팅 메시지 수신"""
    import asyncio
    from asyncio import Queue
    
    async def event_generator():
        # SSE 연결 생성
        queue = Queue()
        await chat_manager.add_sse_connection(room_id, queue)
        
        try:
            # 기존 메시지 히스토리 전송
            messages = await chat_manager.get_room_messages(room_id, 20)
            for msg in messages:
                yield f"data: {msg.json()}\n\n"
            
            # 새로운 메시지 대기
            while True:
                try:
                    message = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield f"data: {message.json()}\n\n"
                except asyncio.TimeoutError:
                    # Keep-alive 메시지
                    yield f"data: {json.dumps({'type': 'ping', 'timestamp': datetime.now().isoformat()})}\n\n"
        finally:
            await chat_manager.remove_sse_connection(room_id, queue)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
