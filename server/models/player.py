import uuid

from fastapi import WebSocket
from pydantic import PrivateAttr

from .common import Model


class Player(Model):
    name: str
    websocket: WebSocket
    _id: uuid.UUID = PrivateAttr(default_factory=uuid.uuid4)

    class Config:
        arbitrary_types_allowed = True
