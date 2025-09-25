from typing import List
import uuid
from models import ChatMessage


class DialogueManager:
    def __init__(self):
        self.dialogues = {
            "mina_dialogue": self._create_mina_dialogue()
        }
    
    def _create_mina_dialogue(self) -> List[ChatMessage]:
        dialogue_parts = {
            1: [
                "너 왜 동창회 안왔어?",
                "안온다는거 겨우 설득해놨더니 갑자기 잠수타버려서",
                "다들 걱정했잖아!"
            ],
            2: [
                "엥",
                "뭔 소리야",
                "오늘도 주희가 썰렁한 개그 엄청 했는데",
                "그거 웃기다고 웃어주는 사람이 없어서 반응하느라 힘들었다구ㅠ.ㅠ"
            ],
            3: [
                "당연하지",
                "남 말에 리액션 해주고 들어주는게 얼마나 큰건데",
                "너는 항상 친구들 고민도 침착하게 잘 들어줘서",
                "우리가 친해진것도 내가 너한테 고민상담하다가 그런거였잖아"
            ],
            4: [
                "암튼",
                "왜 안온거야? 무슨 일 있던거 아니지?"
            ]
        }
        
        messages = []
        for part_number, part_messages in dialogue_parts.items():
            for msg_index, message_text in enumerate(part_messages):
                messages.append(ChatMessage(
                    id=str(uuid.uuid4()),
                    room_id="",
                    message=message_text,
                    part_number=part_number,
                    part_id=str(part_number)
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
                part_number=msg.part_number,
                part_id=msg.part_id
            )
            messages.append(new_msg)
        
        return messages
    


# 전역 대화 관리자 인스턴스
dialogue_manager = DialogueManager()
