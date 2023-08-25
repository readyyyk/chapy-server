from typing import Dict
from fastapi import WebSocket
from _types.HubId import HubId
from _types.Name import Name


class HubModel:
    id: str
    clients: Dict[str, WebSocket]

    def __init__(self, _id: HubId):
        self.id = str(_id)
        self.clients = dict[str, WebSocket]()

    async def connect(self, ws: WebSocket, name: Name):
        await ws.accept()
        self.clients[str(name)] = ws

    def disconnect(self, name: Name):
        del self.clients[str(name)]

    @staticmethod
    async def send_exact(ws: WebSocket, message: dict):
        await ws.send_json(message)

    async def broadcast(self, sender: WebSocket, message: dict):
        for ws in self.clients.values():
            if ws == sender:
                continue
            await ws.send_json(message)
