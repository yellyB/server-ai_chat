#!/usr/bin/env python3
"""
게임 서버 실행 스크립트
"""
import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Escape Game Server 시작 중...")
    print("📡 서버 주소: http://localhost:8000")
    print("📖 API 문서: http://localhost:8000/docs")
    print("🛑 종료하려면 Ctrl+C를 누르세요")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 개발 모드에서 자동 재시작
        log_level="info"
    )
