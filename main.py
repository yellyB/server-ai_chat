from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from datetime import datetime
import json
import asyncio
from typing import List, Dict, Optional
import uuid

app = FastAPI(title="Escape Game Server", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3333"],  # React 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 채팅 메시지 모델
class ChatMessage(BaseModel):
    id: str
    room_id: str
    message: str
    timestamp: datetime
    message_type: str = "chat"  # chat, system, notification 등
    sender: str = "system"  # 민아, 주인공, system
    is_last: bool = False  # 이 메시지가 시퀀스의 마지막인지 여부
    part_number: int = 1  # 파트 번호

# 채팅 방 모델
class ChatRoom(BaseModel):
    id: str
    name: str
    created_at: datetime
    is_active: bool = True

# 게임 상태 관리
class GameManager:
    def __init__(self):
        self.rooms: Dict[str, Dict] = {}
        self.connections: Dict[str, List[WebSocket]] = {}

# 채팅 관리자
class ChatManager:
    def __init__(self):
        self.rooms: Dict[str, ChatRoom] = {}
        self.sse_connections: Dict[str, List] = {}  # room_id -> [connection_list]
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
            self.sse_connections[room_id] = []
            self.message_queue[room_id] = []
    
    async def add_sse_connection(self, room_id: str, connection):
        """SSE 연결 추가"""
        if room_id not in self.sse_connections:
            await self.create_room(room_id)
        self.sse_connections[room_id].append(connection)
    
    async def remove_sse_connection(self, room_id: str, connection):
        """SSE 연결 제거"""
        if room_id in self.sse_connections and connection in self.sse_connections[room_id]:
            self.sse_connections[room_id].remove(connection)
    
    async def send_message_to_room(self, room_id: str, message: ChatMessage):
        """특정 방에 메시지 전송"""
        if room_id in self.sse_connections:
            # 메시지를 큐에 저장
            if room_id not in self.message_queue:
                self.message_queue[room_id] = []
            self.message_queue[room_id].append(message)
            
            # SSE 연결된 클라이언트들에게 전송
            for connection in self.sse_connections[room_id]:
                try:
                    await connection.put(message)
                except:
                    # 연결이 끊어진 경우 제거
                    await self.remove_sse_connection(room_id, connection)
    
    async def get_room_messages(self, room_id: str, limit: int = 50):
        """방의 메시지 히스토리 조회"""
        if room_id in self.message_queue:
            return self.message_queue[room_id][-limit:]
        return []
    
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
    
    async def send_next_message_in_sequence(self, room_id: str):
        """시퀀스에서 다음 메시지 전송"""
        message = await self.get_next_message(room_id)
        if message:
            await self.send_message_to_room(room_id, message)
            return message
        return None
    
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
    
    async def join_room(self, room_id: str, player_name: str, websocket: WebSocket):
        """플레이어가 방에 참가"""
        if room_id not in self.rooms:
            await self.create_room(room_id)
        
        player_id = str(uuid.uuid4())
        player = {
            "id": player_id,
            "name": player_name,
            "websocket": websocket
        }
        
        self.rooms[room_id]["players"].append(player)
        self.connections[room_id].append(websocket)
        
        return player_id
    
    async def broadcast_to_room(self, room_id: str, message: dict):
        """방의 모든 플레이어에게 메시지 전송"""
        if room_id in self.connections:
            for connection in self.connections[room_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    pass
    
    async def remove_player(self, room_id: str, websocket: WebSocket):
        """플레이어 제거"""
        if room_id in self.rooms:
            self.rooms[room_id]["players"] = [
                p for p in self.rooms[room_id]["players"] 
                if p["websocket"] != websocket
            ]
            if websocket in self.connections[room_id]:
                self.connections[room_id].remove(websocket)

game_manager = GameManager()
chat_manager = ChatManager()

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

@app.get("/chat/rooms/{room_id}/messages")
async def get_room_messages(room_id: str, limit: int = 50):
    """특정 방의 메시지 히스토리 조회"""
    messages = await chat_manager.get_room_messages(room_id, limit)
    return {"messages": messages}

@app.post("/chat/rooms/{room_id}/send")
async def send_message_to_room(room_id: str, message_data: dict):
    """특정 방에 메시지 전송 (서버에서 사용)"""
    message = ChatMessage(
        id=str(uuid.uuid4()),
        room_id=room_id,
        message=message_data.get("message", ""),
        timestamp=datetime.now(),
        message_type=message_data.get("type", "chat"),
        sender=message_data.get("sender", "system"),
        is_last=message_data.get("is_last", False)
    )
    
    await chat_manager.send_message_to_room(room_id, message)
    return {"status": "sent", "message_id": message.id}

@app.post("/chat/rooms/{room_id}/setup-dialogue")
async def setup_dialogue(room_id: str):
    """민아와의 대화 시퀀스 설정"""
    # 채팅방 생성
    await chat_manager.create_room(room_id, "민아와의 대화")
    
    # 4개 파트로 나누어진 민아의 메시지들
    dialogue_parts = [
        # 파트 1
        [
            "너 왜 동창회 안왔어?",
            "안온다는거 겨우 설득해놨더니 갑자기 잠수타버려서",
            "다들 걱정했잖아!"
        ],
        # 파트 2
        [
            "엥",
            "뭔 소리야",
            "오늘도 주희가 썰렁한 개그 엄청 했는데",
            "그거 웃기다고 웃어주는 사람이 없어서 반응하느라 힘들었다구ㅠ.ㅠ"
        ],
        # 파트 3
        [
            "당연하지",
            "남 말에 리액션 해주고 들어주는게 얼마나 큰건데",
            "너는 항상 친구들 고민도 침착하게 잘 들어줘서",
            "우리가 친해진것도 내가 너한테 고민상담하다가 그런거였잖아"
        ],
        # 파트 4
        [
            "그래서 암튼",
            "왜 안온거야? 무슨 일 있던거 아니지?"
        ]
    ]
    
    # 파트별로 ChatMessage 객체 생성
    messages = []
    for part_index, part_messages in enumerate(dialogue_parts):
        for msg_index, message_text in enumerate(part_messages):
            is_last_in_part = msg_index == len(part_messages) - 1
            messages.append(ChatMessage(
                id=str(uuid.uuid4()),
                room_id=room_id,
                message=message_text,
                timestamp=datetime.now(),
                message_type="chat",
                sender="민아",
                is_last=is_last_in_part,
                part_number=part_index + 1  # 파트 번호 추가
            ))
    
    # 메시지 시퀀스 설정
    await chat_manager.setup_message_sequence(room_id, messages)
    
    return {"status": "dialogue_setup", "total_messages": len(messages)}

@app.post("/chat/rooms/{room_id}/next")
async def send_next_message(room_id: str):
    """다음 메시지 전송"""
    message = await chat_manager.send_next_message_in_sequence(room_id)
    if message:
        return {"status": "sent", "message": message, "is_last": message.is_last}
    else:
        return {"status": "no_more_messages"}

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

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    
    try:
        # 플레이어 이름 받기
        data = await websocket.receive_text()
        player_data = json.loads(data)
        player_name = player_data.get("player_name", "Anonymous")
        
        # 방에 참가
        player_id = await game_manager.join_room(room_id, player_name, websocket)
        
        # 다른 플레이어들에게 새 플레이어 알림
        await game_manager.broadcast_to_room(room_id, {
            "type": "player_joined",
            "player_id": player_id,
            "player_name": player_name,
            "room_info": game_manager.rooms[room_id]
        })
        
        # 게임 루프
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # 메시지 타입에 따른 처리
                if message["type"] == "game_action":
                    # 게임 액션 처리
                    await game_manager.broadcast_to_room(room_id, {
                        "type": "game_update",
                        "action": message["action"],
                        "player_id": player_id,
                        "data": message.get("data", {})
                    })
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"Error processing message: {e}")
                break
                
    except WebSocketDisconnect:
        pass
    finally:
        # 플레이어 제거
        await game_manager.remove_player(room_id, websocket)
        await game_manager.broadcast_to_room(room_id, {
            "type": "player_left",
            "player_id": player_id,
            "room_info": game_manager.rooms.get(room_id, {})
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
