from time import sleep
from commands import execute_command
from systems.login_manager import login_manager


def gameloop(mud):
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
        else:
            login_manager(mud, id, command, params)
