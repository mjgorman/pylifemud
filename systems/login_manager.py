import yaml
from models import Character
from areas import rooms
from passlib.hash import sha256_crypt


def login_manager(mud, id, command, params):
    if mud.players[id]["state"] == "LOGIN":
        if len(command) < 3:
            mud.send_message(id, "Please choose a name of at least 3 characters")
        else:
            try:
                with open("save/{0}".format(command), "r") as load_player:
                    loaded_player = yaml.load(load_player.read())
                    mud.players[id]["player"] = command
                    mud.players[id]["state"] = "LOGIN_PASSWORD"
            except Exception as e:
                mud.players[id]["player"] = Character(command)
                mud.players[id]["state"] = "CREATION_PASS1"
            finally:
                mud.send_message(id,"Great. what's your password? ")
                mud.send_prompt(id)

    elif mud.players[id]["state"] == "LOGIN_PASSWORD":
        with open("save/{0}".format(mud.players[id]["player"]), "r") as load_player:
            loaded_player = yaml.load(load_player.read())
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
            mud.send_prompt(id)
        else:
            mud.send_message(id,"Incorrect Password.")
            mud.send_prompt(id)

    elif mud.players[id]["state"] == "CREATION_PASS1":
        mud.players[id]["player"].password = sha256_crypt.encrypt("{0}".format(command))
        mud.players[id]["state"] = "ONLINE"

        for pid,pl in mud.players.items():
            if pid is not id:
                mud.send_message(pid,"\n\r{0} entered the game".format(mud.players[id]["player"]))
                mud.send_prompt(id)

        mud.send_message(id,"\n\rWelcome to the game, {0}. Type 'help' for a list of commands. Have fun!".format(
            str(mud.players[pid]["player"])[:1].upper() + str(mud.players[pid]["player"])[1:]))
