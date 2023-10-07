from pydantic import BaseModel
import json
import uuid

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

    def __init__(self, _id: uuid.UUID, detail: str, name: str | None = None):
        self.event = "connection"

        data = {}

        if detail not in ALLOWED_CONNECTION_DETAILS:
            return

        data["id"] = str(_id)
        data["detail"] = detail

        if detail != "trying to connect":
            data["name"] = name

        self.data = json.dumps(data, separators=(',', ':'))


class MessageModel:
    event = "message"
    data: str

    def __init__(self, _id: uuid.UUID, text: str, sender: str | None = None):
        self.event = "message"

        data = {}

        if sender is not None:
            try:
                Name(sender)
            except Exception as e:
                print(e)
                return
            data["sender"] = sender

        data["id"] = str(_id)
        data["text"] = text

        self.data = json.dumps(data, separators=(',', ':'))


class HistoryMessageModel:
    event = "history"
    data: str

    def __init__(self, sender: str, data: str):
        self.event = "history"

        data = {
            "name": sender,
            "data": data,
        }

        self.data = json.dumps(data, separators=(',', ':'))
