# Knoughts And Crosses

### Simple test for using FastAPI WebSockets

I wanted to understand how to use WebSockets to interface a python backend with a javascript frontend. This simple example uses `FastAPI`'s WebSockets to communicate between the client and server allowing clean separation between the two.

### ToDo
* [ ] Landing Page to start new games
* [ ] Strategy for initial connection. How to hit the FastAPI websocket route if not from localhost?
* [ ] Error comminucation card to the client
* [ ] Game winning/ending logic
* [ ] Model ownership is messy, currently create `Player`s and pass to `Game`. Badness.
