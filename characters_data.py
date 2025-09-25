"""
캐릭터 정적 데이터
"""

from typing import Dict, List
from models import Character

# 캐릭터 데이터 정의
CHARACTERS_DATA = {
    "friend": {
        "id": "friend",
        "name": "Friend",
        "name_korean": "친구",
        "description": "친한 친구이자 동창회에서 만난 인물",
        "relationship": "친구",
        "is_available": True
    },
    "mother": {
        "id": "mother",
        "name": "Mother",
        "name_korean": "엄마",
        "description": "가족 중 가장 가까운 존재",
        "relationship": "가족",
        "is_available": True
    },
    "colleague": {
        "id": "colleague",
        "name": "Colleague",
        "name_korean": "직장동료",
        "description": "직장 후배로 함께 일하는 동료",
        "relationship": "직장동료",
        "is_available": True
    },
    "sister": {
        "id": "sister",
        "name": "Sister",
        "name_korean": "여동생",
        "description": "가족 중 한 명인 여동생",
        "relationship": "가족",
        "is_available": True
    },
    "future_self": {
        "id": "future_self",
        "name": "Future Self",
        "name_korean": "미래의 나",
        "description": "미래의 자신과의 대화",
        "relationship": "자기 자신",
        "is_available": True
    }
}

def get_characters_data() -> Dict[str, dict]:
    """캐릭터 데이터 반환"""
    return CHARACTERS_DATA

def create_character_objects() -> List[Character]:
    """캐릭터 객체 리스트 생성"""
    characters = []
    for char_data in CHARACTERS_DATA.values():
        characters.append(Character(**char_data))
    return characters
