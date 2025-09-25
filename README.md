# Escape Game Server

FastAPI 기반의 실시간 멀티플레이어 게임 서버입니다.

## 🚀 빠른 시작

### 1. 가상환경 활성화
```bash
# 가상환경 활성화
source venv/bin/activate
```

### 2. 의존성 설치
```bash
# 필요한 패키지 설치
pip3 install -r requirements.txt
```

### 3. 서버 실행
```bash
# 개발 모드로 서버 실행
python3 run.py
```

## 📋 시스템 요구사항

- Python 3.9+
- pip3
- 가상환경 (venv)

## 🛠️ 설치 및 설정

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd server-ai_chat
```

### 2. 가상환경 생성 (이미 생성되어 있다면 생략)
```bash
python3 -m venv venv
```

### 3. 가상환경 활성화
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. 의존성 설치
```bash
pip3 install -r requirements.txt
```

### 5. 서버 실행
```bash
python3 run.py
```

## 🌐 서버 접속 정보

서버가 성공적으로 실행되면 다음 주소로 접속할 수 있습니다:

- **서버 주소**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs (Swagger UI)
- **상태 확인**: http://localhost:8000/health

## 🎮 API 엔드포인트

### REST API
- `GET /` - 서버 상태 확인
- `GET /health` - 헬스 체크

### 채팅 API
- `GET /chat/rooms` - 채팅방 목록 조회
- `GET /chat/rooms/{room_id}/messages` - 방의 메시지 히스토리 조회
- `POST /chat/rooms/{room_id}/send` - 방에 메시지 전송 (서버용)
- `POST /chat/rooms/{room_id}/setup-dialogue` - 민아와의 대화 시퀀스 설정
- `POST /chat/rooms/{room_id}/next` - 다음 메시지 전송
- `POST /chat/rooms/{room_id}/next-part` - 다음 파트의 모든 메시지를 배열로 전송
- `GET /chat/rooms/{room_id}/sse` - SSE 연결로 실시간 메시지 수신

### WebSocket
- `ws://localhost:8000/ws/{room_id}` - 게임 방에 연결

## 🔧 개발 모드

서버는 개발 모드로 실행되며, 파일 변경 시 자동으로 재시작됩니다.

### 서버 중지
터미널에서 `Ctrl+C`를 눌러 서버를 중지할 수 있습니다.

## 📦 주요 의존성

- **FastAPI**: 웹 프레임워크
- **Uvicorn**: ASGI 서버
- **WebSockets**: 실시간 통신
- **python-socketio**: Socket.IO 지원

## 🎯 게임 서버 기능

- 다중 플레이어 게임 방 관리
- 실시간 WebSocket 통신
- 플레이어 참가/퇴장 처리
- 게임 액션 브로드캐스팅
- SSE 기반 실시간 채팅 시스템

## 💬 채팅 API 사용 예시

### 1. 프론트엔드에서 SSE 연결
```javascript
// SSE 연결로 실시간 메시지 수신
const eventSource = new EventSource('http://localhost:8000/chat/rooms/room1/sse');

eventSource.onmessage = function(event) {
    const message = JSON.parse(event.data);
    console.log('새 메시지:', message);
    // 로컬스토리지에 저장
    localStorage.setItem('chat_messages', JSON.stringify(message));
};

eventSource.onerror = function(event) {
    console.error('SSE 연결 오류:', event);
};
```

### 2. 서버에서 메시지 전송
```bash
# 특정 방에 메시지 전송
curl -X POST "http://localhost:8000/chat/rooms/room1/send" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "안녕하세요!",
       "type": "chat"
     }'
```

### 3. 메시지 히스토리 조회
```bash
# 방의 메시지 히스토리 조회
curl "http://localhost:8000/chat/rooms/room1/messages?limit=20"
```

### 4. 채팅방 목록 조회
```bash
# 모든 채팅방 목록 조회
curl "http://localhost:8000/chat/rooms"
```

### 5. 민아와의 대화 시퀀스 설정
```bash
# 민아와의 대화 시퀀스 설정
curl -X POST "http://localhost:8000/chat/rooms/mina_dialogue/setup-dialogue"
```

### 6. 다음 메시지 전송
```bash
# 시퀀스에서 다음 메시지 전송
curl -X POST "http://localhost:8000/chat/rooms/mina_dialogue/next"
```

### 7. 다음 파트 메시지 전송
```bash
# 다음 파트 전송 (자동으로 순서대로)
curl -X POST "http://localhost:8000/chat/rooms/mina_dialogue/next-part"

# 계속 호출하면 파트 1, 2, 3, 4 순서로 전송
# 더 이상 파트가 없으면 "대화가 끝났습니다" 응답
```

## 🎭 민아와의 대화 시나리오

### 대화 흐름 (4개 파트로 나누어진 민아의 메시지):

**파트 1** (3개 메시지):
1. "너 왜 동창회 안왔어?"
2. "안온다는거 겨우 설득해놨더니 갑자기 잠수타버려서"
3. "다들 걱정했잖아!"

**파트 2** (4개 메시지):
4. "엥"
5. "뭔 소리야"
6. "오늘도 주희가 썰렁한 개그 엄청 했는데"
7. "그거 웃기다고 웃어주는 사람이 없어서 반응하느라 힘들었다구ㅠ.ㅠ"

**파트 3** (4개 메시지):
8. "당연하지"
9. "남 말에 리액션 해주고 들어주는게 얼마나 큰건데"
10. "너는 항상 친구들 고민도 침착하게 잘 들어줘서"
11. "우리가 친해진것도 내가 너한테 고민상담하다가 그런거였잖아"

**파트 4** (2개 메시지):
12. "그래서 암튼"
13. "왜 안온거야? 무슨 일 있던거 아니지?" ← **전체 대화 마지막**

### 주인공 대사 (프론트엔드에서 처리):
- "……난 그냥 없어져도 아무도 모를 줄 알았어."
- "내가 평소에 잘 웃었던건 진짜로 웃겨서가 아니라..."
- "나 같은 애는 웃는거라도 잘해야"
- "다른 사람들이 좋아하기 때문이었어"
- "…그게 그렇게 중요했어?"

### 프론트엔드 구현 예시:
```javascript
// SSE 연결
const eventSource = new EventSource('http://localhost:8000/chat/rooms/mina_dialogue/sse');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.type === 'part_messages') {
        // 파트별 메시지 배열 처리
        data.messages.forEach(message => {
            displayMessage(message);
            saveToLocalStorage(message);
        });
        
        // 대화가 끝났는지 확인
        if (data.is_dialogue_end) {
            showDialogueEndMessage();
        }
    }
};

// 다음 파트 메시지 요청
function requestNextPartMessages() {
    fetch('/chat/rooms/mina_dialogue/next-part', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'sent') {
                // 파트 메시지들이 SSE로 자동 전송됨
                console.log(`파트 ${data.part_number} 전송됨`);
            } else if (data.status === 'no_more_messages') {
                console.log('대화가 끝났습니다');
            }
        });
}

// 사용 예시
requestNextPartMessages(); // 파트 1 전송
requestNextPartMessages(); // 파트 2 전송
requestNextPartMessages(); // 파트 3 전송
requestNextPartMessages(); // 파트 4 전송 (마지막)
requestNextPartMessages(); // "대화가 끝났습니다" 응답
```

## 🐛 문제 해결

### Python 명령어를 찾을 수 없는 경우
```bash
# python3 사용
python3 run.py
```

### pip 명령어를 찾을 수 없는 경우
```bash
# pip3 사용
pip3 install -r requirements.txt
```

### 포트가 이미 사용 중인 경우
`run.py` 파일에서 포트 번호를 변경할 수 있습니다:
```python
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8001,  # 포트 번호 변경
    reload=True,
    log_level="info"
)
```

## 📝 로그 확인

서버 실행 시 다음과 같은 로그를 확인할 수 있습니다:
- 서버 시작 메시지
- 요청 로그
- 에러 메시지

## 🔄 자동 재시작

개발 모드에서는 파일이 변경될 때마다 서버가 자동으로 재시작됩니다.
