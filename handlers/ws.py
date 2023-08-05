from fastapi import WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json

from _types.HubId import HubId
from _types.Name import Name

from models.HubsModel import hubs
from models.HubModel import HubModel
from models.WsMessageModel import MessageModel, ConnectionMessageModel


async def handle_message(data: str, hub: HubModel, name: str, conn: WebSocket):
    try:
        message: dict = json.loads(data)
    except json.decoder.JSONDecodeError:
        await hub.send_exact(conn, MessageModel("Invalid ws message", "server").__dict__)
        return

    ev = message.get("event")
    try:
        data = json.loads(message.get("data"))
    except TypeError:
        await hub.send_exact(conn, MessageModel("Data field was not provided", "server").__dict__)
        return
    except json.decoder.JSONDecodeError:
        await hub.send_exact(conn, MessageModel("Invalid data was provided", "server").__dict__)
        return

    match ev:
        case "connection":
            try:
                match data["detail"]:
                    case "trying to connect":
                        await hub.broadcast(conn, ConnectionMessageModel(data["detail"]).__dict__)
                    case "connected":
                        await hub.send_exact(conn, ConnectionMessageModel(data["detail"], name).__dict__)
                        await hub.broadcast(conn, ConnectionMessageModel(data["detail"], name).__dict__)
                    case "disconnected":
                        await hub.broadcast(conn, ConnectionMessageModel(data["detail"], name).__dict__)
                    case _:
                        await hub.send_exact(conn, MessageModel("Invalid detail field", "server").__dict__)
            except KeyError:
                await hub.send_exact(conn, MessageModel("Detail was not provided", "server").__dict__)
                return
        case "message":
            try:
                await hub.send_exact(conn, MessageModel(data["text"]).__dict__)
                await hub.broadcast(conn, MessageModel(data["text"], name).__dict__)
            except KeyError:
                await hub.send_exact(conn, MessageModel("Text was not provided", "server").__dict__)
                return
        case _:
            await hub.send_exact(conn, MessageModel("Invalid event", "server").__dict__)


async def ws(hub_id: str, ws: WebSocket, name: str):
    try:
        HubId(hub_id)
    except Exception:
        return JSONResponse(
            content=jsonable_encoder({"message": "Invalid hub id"}),
            status_code=status.HTTP_400_BAD_REQUEST
        )

    hub: HubModel = hubs.hubs.get(hub_id)
    # name: Name = Name(name)

    await hub.connect(ws, Name(name))

    await hub.send_exact(ws, ConnectionMessageModel("connected", name).__dict__)
    await hub.broadcast(ws, ConnectionMessageModel("connected", name).__dict__)

    try:
        while True:
            data = await ws.receive_text()
            await handle_message(data, hub, name, ws)
    except WebSocketDisconnect:
        hub.disconnect(Name(name))
        await hub.broadcast(ws, ConnectionMessageModel("disconnected", name).__dict__)