from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from _types.HubId import HubId


def names(hub: str):
    try:
        hub = HubId(hub)
    except Exception:
        return JSONResponse(
            content=jsonable_encoder({"message": "Invalid hub id"}),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return f"{hub}/names"
