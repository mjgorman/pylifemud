from time import sleep
from systems.mudserver import MudServer
from models import Character
from areas import rooms
from commands import execute_command


def run_server():
    mud = MudServer()

    while True:
        sleep(0.25)
        mud.update()
        for id in mud.get_new_players():
            mud.players[id] = { 
                "player": None,
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
        
            if mud.players[id]["player"] is None:
                mud.players[id]["player"] = Character(command)
                
                for pid,pl in mud.players.items():
                    if pid is not id:
                        mud.send_message(pid,"\n\r{0} entered the game".format(mud.players[id]["player"]))
                        mud.send_prompt(id)
                
                mud.send_message(id,"\n\rWelcome to the game, {0}. Type 'help' for a list of commands. Have fun!".format(
                    str(mud.players[pid]["player"])[:1].upper() + str(mud.players[pid]["player"])[1:]))
                mud.send_message(id,rooms[mud.players[id]["room"]]["description"])
                mud.send_prompt(id)
            else:
                execute_command(mud, id, command, params)
    

if __name__ == "__main__":
    run_server()
