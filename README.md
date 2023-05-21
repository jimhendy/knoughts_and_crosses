# Knoughts And Crosses

### Simple test for using FastAPI WebSockets

I wanted to understand how to use WebSockets to interface a python backend with a javascript frontend. This simple example uses `FastAPI`'s WebSockets to communicate between the client and server allowing clean separation between the two.

## Usage

### Client 

Simply open [index.html](client/index.html) or server using a simple python server
```sh
python -m http.server 9000 --directory client/
```
To access from outside `localhost` you must alter the websocket connection to use you local IP address (use `ifconfig`).

### Server
```sh
uvicorn server.main:app --host 0.0.0.0
```

## Development

This project uses `poetry`.

1. Use `conda`/`mamba` to create a new virtual env: 
```sh
mamba create -n knoughts_n_crosses "python>3.11,<3.12" poerty
```
2. Activate the virtual env
```sh
mamba activate knoughts_n_crosses
```
3. Install the poerty dependencies (will install directly into the current virtual env.)
```sh
poetry install
```
4. Whenever you wish to use this code, simply activate the `conda` env (step 2.). No `poetry` commands are required after initial setup.


### ToDo
* [ ] Landing Page to start new games
* [ ] Strategy for initial connection. How to hit the FastAPI websocket route if not from localhost?
* [ ] Error comminucation card to the client
* [ ] Game winning/ending logic
* [ ] Model ownership is messy, currently create `Player`s and pass to `Game`. Badness.
* [ ] Dockerise
