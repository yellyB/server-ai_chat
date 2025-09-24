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
