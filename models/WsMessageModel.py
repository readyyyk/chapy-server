from pydantic import BaseModel
from typing import Literal
import json

from _consts import ALLOWED_CONNECTION_DETAILS
from _types.Name import Name


class WsMessageModel(BaseModel):
    event: str
    data: str


class ConnectionMessageData(BaseModel):
    detail: str
    name: str | None


class MessageData(BaseModel):
    text: str
    sender: str | None


class ConnectionMessageModel:
    event = "connection"
    data: str

    def __init__(self, detail: str, name: str | None = None):
        self.event = "connection"

        data = {}

        if detail not in ALLOWED_CONNECTION_DETAILS:
            return

        data["detail"] = detail

        if detail != "trying to connect":
            data["name"] = name

        self.data = json.dumps(data, separators=(',', ':'))
# print(ConnectionMessageModel("trying to connect").__dict__)


class MessageModel:
    event = "message"
    data: str

    def __init__(self, text: str, sender: str | None = None):
        self.event = "message"

        data = {}

        if sender is not None:
            try:
                Name(sender)
            except Exception as e:
                print(e)
                return
            data["sender"] = sender

        data["text"] = text

        self.data = json.dumps(data, separators=(',', ':'))
# print(MessageModel("trying to connect", "asd").__dict__)
