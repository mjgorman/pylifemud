import textwrap
import yaml
from areas import rooms
from help import help_files


def execute_command(player, command, params):
    players = player.factory.players
    player_status = players[player.id]
    commands = {
        "help": cmd_help,
        "score": cmd_score,
        "look": cmd_look,
        "go": cmd_go,
        "say": cmd_say,
        "emote": cmd_emote,
        "quit": cmd_quit,
        "watch": cmd_watch,
        "save": cmd_save,
        "who": cmd_who,
    }
    if command in commands:
        commands[command](player, params, player_status, players)
    elif len(command) > 0:
       player.send("Unknown command '{0}'".format(command))

def cmd_help(player, params, player_status, players):
    if not params:
        player.send("Commands:")
        for command in help_files:
           player.send("{0} - {1}".format(command, help_files[command]['short']))
    else:
       if params in help_files:
           player.send("--------------------")
           player.send("{0}".format(params))
           player.send("--------------------")
           for line in help_files[params]['long']:
               player.send("{0}".format(textwrap.fill(line, 75)))
           player.send("--------------------")

def cmd_who(player, params, player_status, players):
    player.send("---------Players-----------")
    for id, pl in players.items():
        if pl["player"] is not player_status["player"]:
            player.send("   {0}".format(str(pl["player"].name[:1].upper()) + str(pl["player"].name[1:])))
    player.send("---------------------------")

def cmd_save(player, params, player_status, players):
    player_save = { "name": "{0}".format(player_status["player"].name),
                    "password": "{0}".format(player_status["player"].password),
                    "sex": "{0}".format(player_status["player"].sex),
                    "height": player_status["player"].height,
                    "weight": player_status["player"].weight,
                    "understanding": player_status["player"].understanding,
                    "courage": player_status["player"].courage,
                    "diligence": player_status["player"].diligence,
                    "knowledge": player_status["player"].knowledge,
                    "expression": player_status["player"].expression,
                    "actions": player_status["player"].actions
                  }
    with open('save/{0}'.format(player_status["player"]), 'w') as player_file:
        yaml.dump(player_save, player_file, default_flow_style=False)
    player.send("Saved..")

def cmd_watch(player, params, player_status, players):
    player.send("{0}".format(player.factory.mudtime.ctime()))

def cmd_quit(player, params, player_status, players):
    player.send("Thanks for playing. Come back soon.")
    cmd_save(player, params, player_status, players)
    player.transport.loseConnection()

def cmd_score(player, params, player_status, players):
    player.send("--------------------")
    player.send(" {}".format(str(player_status["player"])[:1].upper() + str(player_status["player"])[1:]))
    player.send("--------------------")
    player.send(" {}".format(player_status["player"].sex))
    player.send(" {} lbs".format(player_status["player"].height))
    player.send(" {} inches".format(player_status["player"].weight))
    player.send("--------------------")
    player.send(" {} Understanding".format(player_status["player"].understanding))
    player.send(" {} Courage".format(player_status["player"].courage))
    player.send(" {} Diligence".format(player_status["player"].diligence))
    player.send(" {} Knowledge".format(player_status["player"].knowledge))
    player.send(" {} Expression".format(player_status["player"].expression))
    player.send("--------------------")

def cmd_say(player, params, player_status, players):
    for id, pl in players.items():
        if pl["room"] == player_status["room"]:
            if player_status["player"] is pl["player"]:
                player.send("You say: {0}".format(params))
            else:
                pl['con'].send("{0} says: {1}".format(str(player_status["player"])[:1].upper() + str(player_status["player"])[1:],params))

def cmd_emote(player, params, player_status, players):
    for id, pl in players.items():
        if pl["room"] == player_status["room"]:
            if player_status["player"] is pl["player"]:
                player.send("{0}".format(
                    params.replace("<me>", "you")))
            else:
                pl['con'].send("{0}".format(
                    params.replace("<me>", "{0}".format(
                        str(player_status["player"])[:1].upper() + str(player_status["player"])[1:]))))

def cmd_look(player, params, player_status, players):
    rm = rooms[player_status["room"]]
    playershere = []

    player.send(rm["description"])
    for id,pl in players.items():
        if pl["room"] == player_status["room"]:
            if player_status["player"] is not pl["player"]:
                playershere.append(str(players[id]["player"])[:1].upper() + str(players[id]["player"])[1:])
    player.send( "Players here: {0}".format(", ".join(playershere)))
    player.send( "Exits are: {0}".format(", ".join(rm["exits"])))

def cmd_go(player, params, player_status, players):
    ex = params.lower()
    rm = rooms[player_status["room"]]

    if ex in rm["exits"]:
        for id,pl in players.items():
            if pl["room"] == player_status["room"] and player_status["player"] is not pl["player"]:
                pl["con"].send("{0} left via exit '{1}'".format(
                    str(player_status["player"])[:1].upper() + str(player_status["player"])[1:],
                    ex))

        player_status["room"] = rm["exits"][ex]
        rm = rooms[player_status["room"]]

        for id,pl in players.items():
            if pl["room"] == player_status["room"] and player_status["player"] is not pl["player"]:
                pl["con"].send("{0} arrived via exit '{1}'".format(
                    str(player_status["player"])[:1].upper() + str(player_status["player"])[1:],
                    ex))

        player.send("You arrive at '{0}'".format(rooms[player_status["room"]]["name"]))
        cmd_look(player, params, player_status, players)

    else:
        player.send( "Unknown exit '{0}'".format(ex))
