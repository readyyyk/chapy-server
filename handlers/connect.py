from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import re

from _consts import PROD_URL

from _types.HubId import HubId
from _types.Name import Name
from models.HubModel import HubModel

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
        hubs.hubs[hub_id] = HubModel(HubId(hub_id))

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
    ws_url = ws_url + f"?name={name}"
    return JSONResponse(
        content=jsonable_encoder({"wsLink": ws_url}),
        status_code=status.HTTP_200_OK
    )
