from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, Request

from handlers.connect import connect
from handlers.names import names
from handlers.ws import ws


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get():
    return {
        'message': 'Hello, World',
        'docs': '/docs'
    }


@app.get("/{hub}/connect")
async def _connect(request: Request, hub: str, name: str):
    return connect(request.url._url, hub, name)


@app.get("/{hub}/names")
async def _names(hub: str):
    return names(hub)


@app.websocket("/{hub}/ws")
async def _ws(hub: str, websocket: WebSocket, token: str):
    await ws(hub, websocket, token)
