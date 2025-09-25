"""
데이터 모델 정의
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChatMessage(BaseModel):
    id: str
    room_id: str
    message: str
    timestamp: datetime
    message_type: str = "chat"  # chat, system, notification 등
    sender: str = "system"  # 민아, 주인공, system
    is_last: bool = False  # 이 메시지가 시퀀스의 마지막인지 여부
    part_number: int = 1  # 파트 번호
    part_id: str = ""  # 파트 구분용 ID (예: "part_1", "part_2")


class ChatRoom(BaseModel):
    id: str
    name: str
    created_at: datetime
    is_active: bool = True


class Character(BaseModel):
    id: str
    name: str
    name_korean: str
    description: str
    relationship: str
    is_available: bool = True
