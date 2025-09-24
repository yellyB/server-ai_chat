from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import asyncio
from typing import List, Dict
import uuid

app = FastAPI(title="Escape Game Server", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3333"],  # React 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 게임 상태 관리
class GameManager:
    def __init__(self):
        self.rooms: Dict[str, Dict] = {}
        self.connections: Dict[str, List[WebSocket]] = {}
    
    async def create_room(self, room_id: str):
        """새로운 게임 방 생성"""
        self.rooms[room_id] = {
            "id": room_id,
            "players": [],
            "status": "waiting",
            "game_data": {}
        }
        self.connections[room_id] = []
    
    async def join_room(self, room_id: str, player_name: str, websocket: WebSocket):
        """플레이어가 방에 참가"""
        if room_id not in self.rooms:
            await self.create_room(room_id)
        
        player_id = str(uuid.uuid4())
        player = {
            "id": player_id,
            "name": player_name,
            "websocket": websocket
        }
        
        self.rooms[room_id]["players"].append(player)
        self.connections[room_id].append(websocket)
        
        return player_id
    
    async def broadcast_to_room(self, room_id: str, message: dict):
        """방의 모든 플레이어에게 메시지 전송"""
        if room_id in self.connections:
            for connection in self.connections[room_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    pass
    
    async def remove_player(self, room_id: str, websocket: WebSocket):
        """플레이어 제거"""
        if room_id in self.rooms:
            self.rooms[room_id]["players"] = [
                p for p in self.rooms[room_id]["players"] 
                if p["websocket"] != websocket
            ]
            if websocket in self.connections[room_id]:
                self.connections[room_id].remove(websocket)

game_manager = GameManager()

@app.get("/")
async def root():
    return {"message": "Escape Game Server is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    
    try:
        # 플레이어 이름 받기
        data = await websocket.receive_text()
        player_data = json.loads(data)
        player_name = player_data.get("player_name", "Anonymous")
        
        # 방에 참가
        player_id = await game_manager.join_room(room_id, player_name, websocket)
        
        # 다른 플레이어들에게 새 플레이어 알림
        await game_manager.broadcast_to_room(room_id, {
            "type": "player_joined",
            "player_id": player_id,
            "player_name": player_name,
            "room_info": game_manager.rooms[room_id]
        })
        
        # 게임 루프
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # 메시지 타입에 따른 처리
                if message["type"] == "game_action":
                    # 게임 액션 처리
                    await game_manager.broadcast_to_room(room_id, {
                        "type": "game_update",
                        "action": message["action"],
                        "player_id": player_id,
                        "data": message.get("data", {})
                    })
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"Error processing message: {e}")
                break
                
    except WebSocketDisconnect:
        pass
    finally:
        # 플레이어 제거
        await game_manager.remove_player(room_id, websocket)
        await game_manager.broadcast_to_room(room_id, {
            "type": "player_left",
            "player_id": player_id,
            "room_info": game_manager.rooms.get(room_id, {})
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
