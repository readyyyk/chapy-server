import os
import datetime
import time
from typing import Dict

import uuid
import jwt

from _consts import JWT_LIVE_TIME


current_tokens = []


def create(data: Dict[str, str]):
    token_id = str(uuid.uuid4())

    jwt_payload = jwt.encode({
        **data,
        "id": token_id,
        "exp": time.time() + datetime.timedelta(seconds=JWT_LIVE_TIME).total_seconds(),
    }, os.getenv("JWT_SECRET"))

    current_tokens.append(token_id)

    return jwt_payload


def get_payload(token: str):
    try:
        return jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except jwt.exceptions.ExpiredSignatureError:
        return {"error": "ExpiredSignatureError"}
