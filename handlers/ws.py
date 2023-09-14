import binascii

from Crypto.Cipher.AES import block_size
from fastapi import WebSocket, WebSocketDisconnect
import json

from _types.HubId import HubId
from _types.Name import Name
from handlers import tokens
from handlers.encoding import AESCipher, get_random_string

from models.WsMessageModel import MessageModel, ConnectionMessageModel
from models.HubModel import HubModel
from models.HubsModel import hubs


async def handle_message(data: str, hub: HubModel, name: str, conn: WebSocket):
    try:
        message: dict = json.loads(data)
    except json.decoder.JSONDecodeError:
        await hub.send_exact(conn, MessageModel("Invalid ws message", "server").__dict__)
        return

    try:
        decoded: str = hub.encoder.decrypt(message["data"], message["iv"]).decode("utf-8")
        message: dict = json.loads(decoded)
    except (binascii.Error, KeyError) as e:
        await hub.send_exact(conn, MessageModel(f"Error parsing message: {e}", "server").__dict__)
        return
    except Exception as e:
        await hub.send_exact(conn, MessageModel(f"Unhandled error: {e}", "server").__dict__)
        return

    try:
        ev = message["event"]
        data = json.loads(message["data"])
    except KeyError:
        await hub.send_exact(conn, MessageModel("Field 'data' or 'event' was not provided", "server").__dict__)
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


async def ws(hub_id: str, ws: WebSocket, token: str):
    try:
        HubId(hub_id)
    except Exception:
        await ws.close(reason="Invalid hub id")
        return

    if hub_id not in hubs.hubs:
        hubs.hubs[hub_id] = HubModel(HubId(hub_id), AESCipher(get_random_string(block_size)))
    hub: HubModel = hubs.hubs[hub_id]

    token_data = tokens.get_payload(token)

    if "error" in token_data:
        await ws.close(reason=token_data["error"])
        return

    if token_data["id"] not in tokens.current_tokens:
        await ws.close(reason="Token is already used!")
        return

    name = token_data["name"]
    tokens.current_tokens.remove(token_data["id"])

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
