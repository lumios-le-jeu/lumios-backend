from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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
    print(f"Client connecté : {websocket.client}")
    try:
        while True:
            # Réception des données depuis un client
            data = await websocket.receive_text()
            print(f"Message reçu : {data}")
            # Envoi des données à tous les clients connectés
            for client in connected_clients:
                await client.send_text(data)
    except WebSocketDisconnect:
        print(f"Client déconnecté : {websocket.client}")
        connected_clients.remove(websocket)
    except Exception as e:
        print(f"Erreur inattendue : {e}")
    finally:
        await websocket.close()
