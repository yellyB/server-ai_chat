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
- `POST /chat/rooms/{character_id}/send` - 다음 파트 자동 전송
- `POST /chat/rooms/{character_id}/setup-dialogue` - 대화 시퀀스 설정
- `POST /chat/rooms/{character_id}/next-part` - 다음 파트의 모든 메시지를 배열로 전송
- `POST /chat/rooms/{character_id}/part/{part_number}` - 특정 파트의 메시지들을 조회

### 대화 시나리오 API
- `GET /dialogues` - 사용 가능한 대화 시나리오 목록 조회

### 캐릭터 API
- `GET /characters` - 캐릭터 목록 조회


## 🔧 개발 모드

서버는 개발 모드로 실행되며, 파일 변경 시 자동으로 재시작됩니다.

### 서버 중지
터미널에서 `Ctrl+C`를 눌러 서버를 중지할 수 있습니다.
