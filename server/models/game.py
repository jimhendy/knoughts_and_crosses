import uuid

from pydantic import Field, PrivateAttr

from .common import Model
from .player import Player

BOARD_SIZE = 3



def _empty_board() -> list[uuid.UUID]:
    return [None] * BOARD_SIZE**2


def _new_id() -> str:
    return str(uuid.uuid4())


class Game(Model):
    player1: Player
    player2: Player

    board: list[uuid.UUID | None] = Field(default_factory=_empty_board)
    _id: str = PrivateAttr(default_factory=_new_id)
    current_player_index = Field(default=0)

