import re
import urllib.parse
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from Crypto.Cipher.AES import block_size

from _consts import PROD_URL
from handlers import tokens
from handlers.encoding import AESCipher, get_random_string

from models.HubModel import HubModel
from _types.HubId import HubId
from _types.Name import Name

from models.HubsModel import hubs


def connect(url: str, hub_id: str, name: str):
    try:
        HubId(hub_id)
    except Exception:
        return JSONResponse(
            content=jsonable_encoder({"message": "Invalid hub id"}),
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if hub_id not in hubs.hubs:
        hubs.hubs[hub_id] = HubModel(HubId(hub_id), AESCipher(get_random_string(block_size)))

    hub: HubModel = hubs.hubs[hub_id]

    try:
        Name(name)
    except Exception:
        return JSONResponse(
            content=jsonable_encoder({"message": "Invalid name"}),
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if name in hub.clients.keys():
        return JSONResponse(
            content=jsonable_encoder({"message": "Name already used"}),
            status_code=status.HTTP_400_BAD_REQUEST
        )

    ws_url = re.sub(r"^http", "ws", url)
    if PROD_URL in url:
        ws_url = re.sub(r"^.+://", "wss://", url)  # force wss protocol
    ws_url = re.sub("/[^/]+$", "/ws", ws_url)

    data = {
        "name": name,
        "key": hub.encoder.key
    }
    ws_url = ws_url + f"?token={urllib.parse.quote(tokens.create(data))}"

    return JSONResponse(
        content=jsonable_encoder({"wsLink": ws_url}),
        status_code=status.HTTP_200_OK
    )
