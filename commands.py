import textwrap
from areas import rooms
from help import help_files


def execute_command(mud, id, command, params):
    
    commands = {
        "help": cmd_help,
        "score": cmd_score,
        "look": cmd_look,
        "go": cmd_go,
        "say": cmd_say,
        "emote": cmd_emote,
        "quit": cmd_quit,
        "watch": cmd_watch,
    }
    if command in commands:
        commands[command](mud, id, params)
    else:
       #send back an 'unknown command' message
       mud.send_message(id, "Unknown command '{0}'".format(command))
    mud.send_prompt(id)
       
def cmd_help(mud, id, params):
    if not params:
        mud.send_message(id,"Commands:")
        for command in help_files:
           mud.send_message(id,"{0} - {1}".format(command, help_files[command]['short']))
    else:
       if params in help_files:
           mud.send_message(id,"--------------------")
           mud.send_message(id, "{0}".format(params))
           mud.send_message(id,"--------------------")
           for line in help_files[params]['long']:
               mud.send_message(id, "{0}".format(textwrap.fill(line, 75)))
           mud.send_message(id,"--------------------")

def cmd_watch(mud, id, params):
    mud.send_message(id,"{0}".format(mud.atomic_clock))

def cmd_quit(mud, id, params):
    mud.send_message(id,"Thanks for playing. Come back soon.")
    mud._clients[id].socket.close()
    
def cmd_score(mud, id, params):
    mud.send_message(id,"--------------------")
    mud.send_message(id," {}".format(str(mud.players[id]["player"])[:1].upper() + str(mud.players[id]["player"])[1:]))
    mud.send_message(id,"--------------------")
    mud.send_message(id," {}".format(mud.players[id]["player"].sex))
    mud.send_message(id," {} lbs".format(mud.players[id]["player"].height))
    mud.send_message(id," {} inches".format(mud.players[id]["player"].weight))
    mud.send_message(id,"--------------------")
    mud.send_message(id," {} Understanding".format(mud.players[id]["player"].understanding))
    mud.send_message(id," {} Courage".format(mud.players[id]["player"].courage))
    mud.send_message(id," {} Diligence".format(mud.players[id]["player"].diligence))
    mud.send_message(id," {} Knowledge".format(mud.players[id]["player"].knowledge))
    mud.send_message(id," {} Expression".format(mud.players[id]["player"].expression))
    mud.send_message(id,"--------------------")

def cmd_say(mud, id, params):
    for pid,pl in mud.players.items():
        if mud.players[pid]["room"] == mud.players[id]["room"]:
            if pid is id:
                mud.send_message(pid,"You say: {0}".format(params))
            else:
                mud.send_message(pid,"{0} says: {1}".format(str(mud.players[id]["player"])[:1].upper() + str(mud.players[id]["player"])[1:],params))
            
def cmd_emote(mud, id, params):
    for pid,pl in mud.players.items():
        if mud.players[pid]["room"] == mud.players[id]["room"]:
            if pid is id:
                mud.send_message(pid,"{0}".format(
                    params.replace("<me>", "you")))
            else:
                mud.send_message(pid,"{0}".format(
                    params.replace("<me>", "{0}".format(
                        str(mud.players[id]["player"])[:1].upper() + str(mud.players[id]["player"])[1:]))))

def cmd_look(mud, id, params):
    rm = rooms[mud.players[id]["room"]]
    playershere = []

    mud.send_message(id, rm["description"])
    for pid,pl in mud.players.items():
        if mud.players[pid]["room"] == mud.players[id]["room"]:
            if pid is not id:
                playershere.append(str(mud.players[pid]["player"])[:1].upper() + str(mud.players[pid]["player"])[1:])
    mud.send_message(id, "Players here: {0}".format(", ".join(playershere)))
    mud.send_message(id, "Exits are: {0}".format(", ".join(rm["exits"])))
                
def cmd_go(mud, id, params):
    ex = params.lower()
    rm = rooms[mud.players[id]["room"]]
    
    if ex in rm["exits"]:
        for pid,pl in mud.players.items():
            if mud.players[pid]["room"] == mud.players[id]["room"] and pid!=id:
                mud.send_message(pid,"{0} left via exit '{1}'".format(
                    str(mud.players[pid]["player"])[:1].upper() + str(mud.players[pid]["player"])[1:],
                    ex))
                
        mud.players[id]["room"] = rm["exits"][ex]
        rm = rooms[mud.players[id]["room"]]
        
        for pid,pl in mud.players.items():
            if mud.players[pid]["room"] == mud.players[id]["room"] and pid!=id:
                mud.send_message(pid,"{0} arrived via exit '{1}'".format(
                    str(mud.players[pid]["player"])[:1].upper() + str(mud.players[pid]["player"])[1:],
                    ex))
                
        mud.send_message(id,"You arrive at '{0}'".format(rooms[mud.players[id]["room"]]["name"]))
        cmd_look(mud, id, params)
        
    else:
        mud.send_message(id, "Unknown exit '{0}'".format(ex))
