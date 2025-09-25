from pydantic import BaseModel


class ChatMessage(BaseModel):
    id: str
    character_id: str
    message: str
    part_number: int = 1  # 파트 번호


class Character(BaseModel):
    id: str
    name: str
