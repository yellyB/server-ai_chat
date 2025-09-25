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
    def __init__(self):
        character_objects = create_character_objects()
        self.characters = character_objects
    
    def get_characters(self) -> List[Character]:
        return self.characters

character_manager = CharacterManager()

@app.get("/")
async def root():
    return {"message": "Chat Server is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/characters")
async def get_characters():
    characters = character_manager.get_characters()
    return characters

@app.get("/dialogue/{character_id}/part/{part_number}")
async def get_dialogue_part(character_id: str, part_number: int):
    try:
        messages = dialogue_manager.get_dialogue(character_id)
        
        part_messages = [msg for msg in messages if msg.part_number == part_number]
        
        if not part_messages:
            return {"status": "part_not_found", "message": f"캐릭터 {character_id}의 파트 {part_number}를 찾을 수 없습니다"}
        
        return {
            "status": "success",
            "character_id": character_id,
            "part_number": part_number,
            "messages": [{"id": msg.id, "message": msg.message} for msg in part_messages]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)