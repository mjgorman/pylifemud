import yaml
from time import sleep
from systems.mudserver import MudServer
from models import Character
from areas import rooms
from commands import execute_command
from passlib.hash import sha256_crypt


def run_server():
    mud = MudServer()

    while True:
        sleep(0.2)
        mud.update()

        for id in mud.get_new_players():
            mud.players[id] = {
                "player": None,
                "state": "LOGIN",
                "room": 1,
            }
            mud.send_message(id,"\n\n\r")
            mud.send_message(id,"    / /                                 / /              //  ) )")
            mud.send_message(id,"   / /        ( )          ___         / /        ( ) __//__  ___")
            mud.send_message(id,"  / /        / / ||  / / //___) )     / /        / /   //   //___) )")
            mud.send_message(id," / /        / /  || / / //           / /        / /   //   //")
            mud.send_message(id,"/ /____/ / / /   ||/ / ((____       / /____/ / / /   //   ((____")
            mud.send_message(id,"\n\n\n\r")
            mud.send_message(id,"What is your name?")
            mud.send_prompt(id)

        for id in mud.get_disconnected_players():
            if id not in mud.players: continue
            for pid,pl in mud.players.items():
                if pid is not id:
                    mud.send_message(pid,"{0} quit the game".format(
                        str(mud.players[id]["player"])[:1].upper() + str(mud.players[id]["player"])[1:]))
            del(mud.players[id])

        for id,command,params in mud.get_commands():
            if id not in mud.players: continue

            if mud.players[id]["state"] == "ONLINE":
                execute_command(mud, id, command, params)

            elif mud.players[id]["state"] == "LOGIN":
                if len(command) < 3:
                    mud.send_message(id, "Please choose a name of at least 3 characters")
                else:
                    try:
                        with open("save/{0}".format(command), "r") as load_player:
                            loaded_player = yaml.load(load_player.read())
                            mud.players[id]["state"] = "LOGIN_PASSWORD"
                    except Exception as e:
                        mud.players[id]["player"] = Character(command)
                        mud.players[id]["state"] = "CREATION_PASS1"
                    finally:
                        mud.send_message(id,"Great. what's your password? ")

            elif mud.players[id]["state"] == "LOGIN_PASSWORD":
                if sha256_crypt.verify("{0}".format(command), loaded_player["password"]):
                    mud.players[id]["player"] = Character(loaded_player["name"], load=True)
                    mud.players[id]["player"].password = loaded_player["password"]
                    mud.players[id]["player"].sex = loaded_player["sex"]
                    mud.players[id]["player"].height = loaded_player["height"]
                    mud.players[id]["player"].weight = loaded_player["weight"]
                    mud.players[id]["player"].understanding = loaded_player["understanding"]
                    mud.players[id]["player"].courage = loaded_player["courage"]
                    mud.players[id]["player"].diligence = loaded_player["diligence"]
                    mud.players[id]["player"].knowledge = loaded_player["knowledge"]
                    mud.players[id]["player"].expression = loaded_player["expression"]
                    mud.players[id]["state"] = "ONLINE"
                    mud.send_message(id,"Welcome back!")
                    mud.send_message(id,rooms[mud.players[id]["room"]]["description"])
                else:
                    mud.send_message(id,"Incorrect Password.")

            elif mud.players[id]["state"] == "CREATION_PASS1":
                mud.players[id]["player"].password = sha256_crypt.encrypt("{0}".format(command))
                mud.players[id]["state"] = "ONLINE"

                for pid,pl in mud.players.items():
                    if pid is not id:
                        mud.send_message(pid,"\n\r{0} entered the game".format(mud.players[id]["player"]))
                        mud.send_prompt(id)

                mud.send_message(id,"\n\rWelcome to the game, {0}. Type 'help' for a list of commands. Have fun!".format(
                    str(mud.players[pid]["player"])[:1].upper() + str(mud.players[pid]["player"])[1:]))
                mud.send_message(id,rooms[mud.players[id]["room"]]["description"])
                mud.send_prompt(id)


if __name__ == "__main__":
    run_server()
