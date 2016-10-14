from systems.mudserver import MudServer
from systems.gameloop import gameloop


def run_server():
    mud = MudServer()
    while True:
        gameloop(mud)


if __name__ == "__main__":
    run_server()
