"""
캐릭터 정적 데이터
"""

from typing import List
from models import Character

# 캐릭터 데이터 정의
CHARACTERS_DATA = {
    "friend": {
        "id": "friend",
        "name": "수정",
    },
    "mother": {
        "id": "mother",
        "name": "엄마",
    },
    "colleague": {
        "id": "colleague",
        "name": "민영씨",
    },
    "sister": {
        "id": "sister",
        "name": "여동생",
    },
    "future_self": {
        "id": "future_self",
        "name": "미래의 나",
    }
}

def create_character_objects() -> List[Character]:
    """캐릭터 객체 리스트 생성"""
    characters = []
    for char_data in CHARACTERS_DATA.values():
        characters.append(Character(**char_data))
    return characters
