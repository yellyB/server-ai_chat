from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Character
from dialogue import dialogue_manager
from characters_data import create_character_objects

app = FastAPI(title="Chat Server", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CharacterManager:
    """캐릭터 관리자"""
    
    def __init__(self):
        # 정적 데이터에서 캐릭터 객체 생성
        character_objects = create_character_objects()
        self.characters = character_objects
    
    def get_characters(self) -> List[Character]:
        """캐릭터 목록 반환"""
        return self.characters

# 매니저 인스턴스 생성
character_manager = CharacterManager()

@app.get("/")
async def root():
    """서버 상태 확인"""
    return {"message": "Chat Server is running"}

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}

@app.get("/characters")
async def get_characters():
    """캐릭터 목록 조회"""
    characters = character_manager.get_characters()
    return {"characters": characters}

@app.get("/dialogue/{room_id}/part/{part_number}")
async def get_dialogue_part(room_id: str, part_number: int):
    """특정 파트의 대화 데이터 조회"""
    try:
        # 대화 시나리오 가져오기
        messages = dialogue_manager.get_dialogue("mina_dialogue", room_id)
        
        # 특정 파트의 메시지들 필터링
        part_messages = [msg for msg in messages if msg.part_number == part_number]
        
        if not part_messages:
            return {"status": "part_not_found", "message": f"파트 {part_number}를 찾을 수 없습니다"}
        
        return {
            "status": "success",
            "part_number": part_number,
            "messages": [msg.dict() for msg in part_messages]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)