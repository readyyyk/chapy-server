import json
from typing import Dict
from fastapi import WebSocket
from _types.HubId import HubId
from _types.Name import Name
from handlers.encoding import AESCipher


class HubModel:
    id: str
    encoder: AESCipher
    clients: Dict[str, WebSocket]

    def __init__(self, _id: HubId, encoder: AESCipher):
        self.id = str(_id)
        self.encoder = encoder
        self.clients = dict[str, WebSocket]()

    async def connect(self, ws: WebSocket, name: Name):
        await ws.accept()
        self.clients[str(name)] = ws

    def disconnect(self, name: Name):
        del self.clients[str(name)]

    async def send_exact(self, ws: WebSocket, message: dict):
        data, iv = self.encoder.encrypt(json.dumps(message))
        await ws.send_json({"data": data.decode("utf-8"), "iv": iv})

    async def broadcast(self, sender: WebSocket, message: dict):
        data, iv = self.encoder.encrypt(json.dumps(message))
        for ws in self.clients.values():
            if ws == sender:
                continue
            await ws.send_json({"data": data.decode("utf-8"), "iv": iv})
