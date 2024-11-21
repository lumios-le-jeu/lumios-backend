import os
from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()
connected_clients: List[WebSocket] = []

# Route HTTP pour vérifier que le backend est actif
@app.get("/")
def read_root():
    return {"message": "Backend is running and WebSocket is ready!"}

# Endpoint WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in connected_clients:
                await client.send_text(data)
    except:
        connected_clients.remove(websocket)

# Ajout de cette ligne pour utiliser le port défini par Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Utilise le port défini par Render, par défaut 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
