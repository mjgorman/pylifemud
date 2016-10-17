import yaml
from systems.models import Character
from areas import rooms
from passlib.hash import sha256_crypt


def login_manager(player, command):
    players = player.factory.players
    player_status = players[player.id]
    if player_status["state"] == "LOGIN_NAME":
        if len(command) < 3:
            player.send("Please choose a name of at least 3 characters")
        else:
            player.send("{0}, is that right? (y/n)".format(command))
            player_status["player"] = command
            player_status["state"] = "LOGIN_CONFIRM"


    elif player_status["state"] == "LOGIN_CONFIRM":
        if command == "y":
            try:
                with open("save/{0}".format(player_status["player"]), "r") as load_player:
                    loaded_player = yaml.load(load_player.read())
                    player_status["state"] = "LOGIN_PASSWORD"
            except Exception as e:
                player_status["player"] = Character(player_status["player"])
                player_status["state"] = "CREATION_PASS1"
            finally:
                player.send("Great. what's your password? ")
        else:
            player.send("No? Okay what name would you like then?")
            player_status["state"] = "LOGIN_NAME"



    elif player_status["state"] == "LOGIN_PASSWORD":
        with open("save/{0}".format(player_status["player"]), "r") as load_player:
            loaded_player = yaml.load(load_player.read())
        if sha256_crypt.verify("{0}".format(command), loaded_player["password"]):
            player_status["player"] = Character(loaded_player["name"], load=True)
            player_status["player"].password = loaded_player["password"]
            player_status["player"].sex = loaded_player["sex"]
            player_status["player"].height = loaded_player["height"]
            player_status["player"].weight = loaded_player["weight"]
            player_status["player"].understanding = loaded_player["understanding"]
            player_status["player"].courage = loaded_player["courage"]
            player_status["player"].diligence = loaded_player["diligence"]
            player_status["player"].knowledge = loaded_player["knowledge"]
            player_status["player"].expression = loaded_player["expression"]
            player_status["player"].actions = loaded_player["actions"]
            player_status["state"] = "ONLINE"
            for id, pl in players.items():
                if player is not id:
                    pl['con'].send("\r\n{0} entered the game".format(player_status["player"]))
            player.send("Welcome back!")
            player.send(rooms[player_status["room"]]["description"])
        else:
            player.send("Incorrect Password.")

    elif player_status["state"] == "CREATION_PASS1":
        player_status["player"].password = sha256_crypt.encrypt("{0}".format(command))
        player_status["state"] = "CREATION_SEX"
        player.send("Are you a Male or Female?")
        print("User: {0} Client: {1} Host: {2}".format(player_status["player"],
                                                       player_status["con"].transport.sessionno,
                                                       player_status["con"].transport.hostname))

    elif player_status["state"] == "CREATION_SEX":
        if command in ["male", "m"]:
            player_status["player"].sex = "Male"
        elif command in ["female", "f"]:
            player_status["player"].sex = "Female"
        else:
            player.send("Are you a Male or Female?")
            return

        player_status["state"] = "ONLINE"
        for id, pl in players.items():
            if player is not id:
                pl['con'].send("\r\n{0} entered the game".format(player_status["player"]))

        player.send("\n\rWelcome to the game, {0}. Type 'help' for a list of commands. Have fun!".format(
            str(player_status["player"])[:1].upper() + str(player_status["player"])[1:]))
