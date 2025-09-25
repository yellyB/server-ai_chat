"""
데이터 모델 정의
"""

from pydantic import BaseModel


class ChatMessage(BaseModel):
    id: str
    room_id: str
    message: str
    part_number: int = 1  # 파트 번호
    part_id: str = ""  # 파트 구분용 ID (예: "part_1", "part_2")


class Character(BaseModel):
    id: str
    name: str
