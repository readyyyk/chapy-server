import json
from typing import Dict
from fastapi import WebSocket
from starlette.websockets import WebSocketState
from websockets.exceptions import ConnectionClosedError

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
        try:
            await ws.send_json({"data": data.decode("utf-8"), "iv": iv})
        except ConnectionClosedError:
            print("Tried to `send exact` to closed socket")

    async def broadcast(self, sender: WebSocket, message: dict):
        data, iv = self.encoder.encrypt(json.dumps(message))
        for name in self.clients.keys():
            ws = self.clients[name]
            if ws == sender:
                continue
            try:
                await ws.send_json({"data": data.decode("utf-8"), "iv": iv})
            except Exception as e:
                print(e)
                print("Tried to `broadcast` to closed socket")
                self.disconnect(Name(name))
