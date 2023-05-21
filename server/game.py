from . import models
from .models.game import BOARD_SIZE
import uuid
from loguru import logger
from fastapi import WebSocket

HORIZONTAL_LINE = "\n" + "-" * (BOARD_SIZE * 5) + "\n"
SYMBOLS = list("OX")

class KnoughtsAndCrosses:
    def __init__(self, player1: models.Player, player2: models.Player):
        self._model = models.Game(
            player1=player1,
            player2=player2,
        )
        
    def game_id(self) -> str:
        return self._model._id

    async def broadcast(self, message: dict) -> None:
        for player in self.players:
            await player.websocket.send_json(message)

    def _symbol(self, player_id: uuid.UUID | None) -> str:
        match player_id:
            case self._model.player1._id:
                return SYMBOLS[0]
            case self._model.player2._id:
                return SYMBOLS[1]
            case _:
                return " "

    def current_player(self) -> models.Player:
        cur_player = self._model.player2 if self._model.current_player_index else self._model.player1
        logger.debug(f"Current player: {cur_player}")
        return cur_player

    def _increment_player(self) -> None:
        self._model.current_player_index = (self._model.current_player_index + 1) % 2
        logger.debug(f"New current player index: {self._model.current_player_index}")

    def add_symbol(self, player: models.Player, location: int) -> str:
        assert player == self.current_player()
        assert self._model.board[location] is None
        self._model.board[location] = player._id
        self._increment_player()
        return self._symbol(player._id)

    def render(self) -> None:
        board = HORIZONTAL_LINE
        for location, player_id in enumerate(self._model.board):
            board += f"| {self._symbol(player_id)} |"
            if not (location + 1) % BOARD_SIZE:
                board += HORIZONTAL_LINE
        print(board)
        
    @property
    def players(self):
        yield self._model.player1
        yield self._model.player2

    def player_from_ws(self, ws: WebSocket)->models.Player:
        return next(p for p in self.players if p.websocket is ws)