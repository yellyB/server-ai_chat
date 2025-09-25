from typing import List
from models import Character

CHARACTERS_DATA = [
    {
        "id": "friend",
        "name": "수정",
    },
    {
        "id": "mother",
        "name": "엄마",
    },
    {
        "id": "colleague",
        "name": "민영씨",
    },
    {
        "id": "sister",
        "name": "여동생",
    },
    {
        "id": "future_self",
        "name": "미래의 나",
    }
]

def create_character_objects() -> List[Character]:
    characters = []
    for char_data in CHARACTERS_DATA:
        characters.append(Character(**char_data))
    return characters
