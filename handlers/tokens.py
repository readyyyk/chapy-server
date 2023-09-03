import os
import datetime
import time

from dotenv import load_dotenv
import uuid
import jwt

from _consts import JWT_LIVE_TIME

load_dotenv()

current_tokens = []


def create(name: str):
    token_id = str(uuid.uuid4())

    jwt_payload = jwt.encode({
        "name": name,
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
