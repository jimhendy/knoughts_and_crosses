import uuid

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from loguru import logger

from .game import KnoughtsAndCrosses
from .models import Player

app = FastAPI()

# WebSocket json format: {'event': "...", 'data': {} }


class GameController:
    def __init__(self):
        self.waiting_players = []
        self.games: dict[uuid.UUID, KnoughtsAndCrosses] = {}

    async def deal_with_websocket_message(self, message: dict, ws: WebSocket):
        try:
            return await getattr(self, message["event"])(message.get("data"), ws=ws)
        except Exception as e:
            logger.error(e)
            #raise HTTPException(400) from e

    async def new_player(self, data: dict, ws: WebSocket) -> dict:
        self.waiting_players.append(Player(name=data["player_name"], websocket=ws))

        match len(self.waiting_players):
            case 2:
                game = KnoughtsAndCrosses(*self.waiting_players)
                self.waiting_players.clear()
                _id = game.game_id()
                self.games[_id] = game
                await game.broadcast(
                    {"event": "game_created", "data": {"game_id": _id}}
                )
            case 1:
                return {
                    "event": "game_pending",
                }
            case _:
                raise HTTPException("Too many players waiting")

    async def add_symbol(self, data: dict, ws: WebSocket) -> dict:
        logger.info(f"Adding symbol for {data}")
        game = self.games[data["game_id"]]
        player = game.player_from_ws(ws=ws)
        symbol = game.add_symbol(player, data["location"])
        game.render()
        await game.broadcast(
            {
                "event": "add_symbol",
                "data": {"location": data["location"], "symbol": symbol},
            }
        )
        

    def disconnect_websocket(self, ws: WebSocket):
        # ToDo: Be better
        self.games.clear()
        self.waiting_players.clear()


gc = GameController()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    logger.info(f"Starting new websocket to client: {client_id}")
    await websocket.accept()

    try:
        while True:
            incoming = await websocket.receive_json()
            logger.debug(f"Recieved json from {client_id}: {incoming}")
            outgoing = await gc.deal_with_websocket_message(
                message=incoming, ws=websocket
            )
            logger.debug(f"Sending json to client {client_id}: {outgoing}")
            if outgoing:
                await websocket.send_json(outgoing)
    except WebSocketDisconnect:
        logger.info(f"Disconnecting client: {client_id}")
        gc.disconnect_websocket(websocket)
