from typing import List
import uuid
from models import ChatMessage

DIALOGUE_DATA = {
    "friend": [
        [
            "너 왜 동창회 안왔어?",
            "안온다는거 겨우 설득해놨더니 갑자기 잠수타버려서",
            "다들 걱정했잖아!"
        ],
        [
            "엥",
            "뭔 소리야",
            "오늘도 주희가 썰렁한 개그 엄청 했는데",
            "그거 웃기다고 웃어주는 사람이 없어서 반응하느라 힘들었다구ㅠ.ㅠ"
        ],
        [
            "당연하지",
            "남 말에 리액션 해주고 들어주는게 얼마나 큰건데",
            "너는 항상 친구들 고민도 침착하게 잘 들어줘서",
            "우리가 친해진것도 내가 너한테 고민상담하다가 그런거였잖아"
        ],
        [
            "암튼",
            "왜 안온거야? 무슨 일 있던거 아니지?"
        ]
    ],
    "sister": [
        [
            "풉.",
            "쟤 참 착하다.",
            "네 웃음소리가 그리웠대.",
            "웃기지 않냐? 언니는 제대로 웃은 적도 없는데."
        ],
        [
            "사랑받으려고 맨날 '인기 많아지는법' 같은거 검색하고",
            "앞으로 리액션 좋은 사람이 되어야겠다고 하던거",
            "진짜 찌질이 그자체였는데 말이야.",
            "가면 쓴 모습으로 받는 사랑이 의미가 있나?"
        ],
        [
            "뭐, 됐고",
            "여기 들어오기 전에 엄마랑 한바탕 한거 기억나지?",
            "그것때문에 나한테 \"열등감폭발\"해서 날 가두려던거잖아",
            "언니가 그동안 엄마 속였던거, 그건 죄책감 안들어?",
            "나처럼 엄마한테 기쁨만 주는 착한 딸은",
            "상상도 못하는 일이네~~"
        ],
        [
            "들었냐?",
            "엄마는 널 자랑스러웠다고 말하는데 그거 믿는거 아니지?",
            "너 하나로 충분했으면 왜 날 만들었을까? ㅋㅋ",
            "답 나왔지? 네 머릿속 환상일 뿐이니까."
        ],
        [
            "너가 좋은 회사 다닌다고 되게 자랑하고 다니시던데,",
            "회사에서 맨날 실수하고 인정 못받는 폐급이라는거 알면 어떠시려나?",
            "웃기지 않냐?",
            "네가 남긴 쪼가리 종이 하나가 뭐라고.",
            "그 정도로 보잘것없는 게 네 \"성과\"야.",
            "대~~단하다, 진짜. ㅋㅋ"
        ],
        [
            "근데 말이야, 네가 그렇게 대단하다면",
            "왜 스스로는 못 살리냐?",
            "고작 이 작은 방 하나도 나가지 못하는데"
        ],
        [
            "넌 날 미워했잖아.",
            "내가 행복하던 시절이 네겐 꼴 보기 싫었지.",
            "그래서 날 가두려고 했잖아."
        ],
        [
            "간단하지.",
            "난 네 머릿속에만 있으니까.",
            "넌 나를 버리고, 미워하고, 저주했어.",
            "그래서 너 스스로를 가둔 거야."
        ],
        [
            "난 네 어린 날이야.",
            "네가 제일 부러워했고, 제일 싫어했던…",
            "너 자신."
        ],
        [
            "흥, 그래.",
            "날 혐오하든 뭐든, 난 네 일부야.",
            "마찬가지로 못난 네 모습도 너이고.",
            "그러니까 자꾸 숨기려고 하지마.",
            "나 없인 네가 네가 아니니까."
        ]
    ],
    "mother": [
        [
            "딸",
            "생각해보니까 요즘에 엄마가 잘 못챙겨준것 같네",
            "자취하면서 밥은 잘 챙겨 먹고 있니?"
        ],
        [
            "그런 소리 말아.",
            "재능도 있는데 열심히 노력해서",
            "원하는 학과 진학하고 좋은 디자인 회사에서 일하는데",
            "그게 어떻게 아무것도 아니니?"
        ],
        [
            "나랑 아빠랑 둘다 맞벌이하느라 집에 없을때가 대부분이었는데",
            "다 클때까지 불만도 한번 없이",
            "외로울텐데도 혼자서도 몇 시간을 꼬박 앉아 있던 네 모습",
            "엄마한텐 너무 든든했어."
        ],
        [
            "하나밖에 없는 딸이 이렇게 잘 커줘서",
            "엄마는 너무 자랑스러워",
            "너는 아무것도 아닌게 아니야",
            "절대로"
        ]
    ],
    "colleague": [
        [
            "선배?!",
            "왜이렇게 길게 휴가를 쓰셨어요?",
            "휴가는 하루 이상으로 절대 안쓰시던분이.."
        ],
        [
            "네?? 갑자기요??!!",
            "저한텐요.",
            "선배가 제 얘기 들어주고,",
            "제가 실수라도 하면, 그럴수도 있다면서",
            "몰래 책상에 응원 포스트잇 붙여주던 거…",
            "그 덕분에 버틴 날이 얼마나 많은데요."
        ],
        [
            "작은 거라도 누군가한테는 세상을 버티게 하는 이유가 돼요."
        ]
    ],
    "future_self": [
        [
            "이제 알겠지?",
            "문은 밖에서 잠긴 적 없어.",
            "네가 스스로 잠근 거야."
        ],
        [
            "열쇠도 네가 가지고 있어.",
            "그냥 이런 널 받아들여"
        ]
    ]
}


class DialogueManager:
    def __init__(self):
        self.dialogues = {}
        for character_id in DIALOGUE_DATA.keys():
            self.dialogues[character_id] = self._create_dialogue(character_id)
    
    def _create_dialogue(self, character_id: str) -> List[ChatMessage]:
        if character_id not in DIALOGUE_DATA:
            raise ValueError(f"Unknown character: {character_id}")
        
        dialogue_parts = DIALOGUE_DATA[character_id]
        messages = []
        
        for part_index, part_messages in enumerate(dialogue_parts):
            part_number = part_index + 1  # 1부터 시작
            for msg_index, message_text in enumerate(part_messages):
                messages.append(ChatMessage(
                    id=str(uuid.uuid4()),
                    room_id=character_id,
                    character_id=character_id,
                    message=message_text,
                    part_number=part_number
                ))
        
        return messages
    
    def get_dialogue(self, character_id: str) -> List[ChatMessage]:
        if character_id not in self.dialogues:
            raise ValueError(f"Unknown character: {character_id}")
        
        return self.dialogues[character_id]


# 전역 대화 관리자 인스턴스
dialogue_manager = DialogueManager()