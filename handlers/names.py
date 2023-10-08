from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from _types.HubId import HubId

from models.HubsModel import hubs


def names(hub: str):
    try:
        hub = HubId(hub)
        return JSONResponse(
            content=jsonable_encoder([*hubs.hubs[str(hub)].clients.keys()]),
            status_code=status.HTTP_200_OK,
            headers={"Cache-Control": "no-cache"},
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            content=jsonable_encoder({"message": "Invalid hub id"}),
            status_code=status.HTTP_400_BAD_REQUEST,
            headers={"Cache-Control": "no-cache"},
        )

