"""
민아와의 대화 시나리오 관리
"""

from typing import List, Dict
from datetime import datetime
import uuid
from models import ChatMessage


class DialogueManager:
    """대화 시나리오 관리자"""
    
    def __init__(self):
        self.dialogues = {
            "mina_dialogue": self._create_mina_dialogue()
        }
    
    def _create_mina_dialogue(self) -> List[ChatMessage]:
        """민아와의 대화 시나리오 생성"""
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
                    room_id="",  # 나중에 설정됨
                    message=message_text,
                    timestamp=datetime.now(),
                    message_type="chat",
                    sender="민아",
                    is_last=is_last_in_part,
                    part_number=part_index + 1,  # 파트 번호 추가
                    part_id=f"part_{part_index + 1}"  # 파트 구분용 ID
                ))
        
        return messages
    
    def get_dialogue(self, dialogue_id: str, room_id: str) -> List[ChatMessage]:
        """대화 시나리오 가져오기 (room_id 설정)"""
        if dialogue_id not in self.dialogues:
            raise ValueError(f"Unknown dialogue: {dialogue_id}")
        
        # room_id를 설정한 새로운 메시지 리스트 생성
        messages = []
        for msg in self.dialogues[dialogue_id]:
            new_msg = ChatMessage(
                id=str(uuid.uuid4()),
                room_id=room_id,
                message=msg.message,
                timestamp=datetime.now(),
                message_type=msg.message_type,
                sender=msg.sender,
                is_last=msg.is_last,
                part_number=msg.part_number,
                part_id=msg.part_id
            )
            messages.append(new_msg)
        
        return messages
    
    def add_dialogue(self, dialogue_id: str, messages: List[ChatMessage]):
        """새로운 대화 시나리오 추가"""
        self.dialogues[dialogue_id] = messages
    
    def list_dialogues(self) -> List[str]:
        """사용 가능한 대화 시나리오 목록"""
        return list(self.dialogues.keys())


# 전역 대화 관리자 인스턴스
dialogue_manager = DialogueManager()
