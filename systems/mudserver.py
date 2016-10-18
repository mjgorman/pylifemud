from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from systems.commands import execute_command
from systems.login_manager import login_manager
from datetime import datetime, timedelta
import yaml


class MudServer(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.id = None

    def connectionMade(self):
        self.id = self.transport.sessionno
        self.factory.players[self.id] = {
                "player": None,
                "con": self,
                "state": "LOGIN_NAME",
                "room": 1,
            }
        print("New Client: {0} Host: {1}".format(self.transport.sessionno, self.transport.hostname))
        self.send("What's your name?")

    def dataReceived(self, data):
        self.command_parser(data)

    def command_parser(self, data):
        data = data.strip()
        command = data.split(" ")[0].lower()
        params = " ".join(data.split(" ")[1:])
        if self.factory.players[self.id]["state"] == "ONLINE":
            execute_command(self, command, params)
            self.send("<<  {0} | Actions: {1} >>".format(self.factory.timeofday[self.factory.mudtime.hour],
                                                         self.factory.players[self.id]["player"].actions))
            return
        login_manager(self, command)
        self.send(">>")

    def send(self, msg):
        self.transport.write("\r\n{0} ".format(msg))

    def connectionLost(self, reason):
        for id, player in self.factory.players.items():
            if player['con'] is not self:
                player['con'].send("{0} has quit\r\n".format(self.factory.players[self.id]["player"]))
        self.factory.players.pop(self.transport.sessionno)

class MudServerFactory(Factory):
    def __init__(self):
        self.players = {}
        self.timeofday = {
                0: "Night",
                1: "Night",
                2: "Night",
                3: "Night",
                4: "Early Morning",
                5: "Early Morning",
                6: "Early Morning",
                7: "Early Morning",
                8: "Morning",
                9: "Morning",
                10: "Morning",
                11: "Morning",
                12: "Afternoon",
                13: "Afternoon",
                14: "Afternoon",
                15: "Afternoon",
                16: "Late Afternoon",
                17: "Late Afternoon",
                18: "Late Afternoon",
                19: "Late Afternoon",
                20: "Evening",
                21: "Evening",
                22: "Evening",
                23: "Evening",
                24: "Night",
                }
        try:
            with open('save/mud.time', 'r') as mudtime:
                self.mudtime = yaml.load(mudtime.read())
        except:
            self.mudtime = datetime(1,1,1)
        print("The Time is: {0}".format(self.mudtime))

    def buildProtocol(self, addr):
        return MudServer(self)

    def update(self):
        try:
            self.mudtime = self.mudtime + timedelta(seconds=1)
        except:
            print("Failed to update time")
        with open('save/mud.time', 'w') as mudtime:
            yaml.dump(self.mudtime, mudtime, default_flow_style=True)

        if self.mudtime.hour % 4 == 0 and self.mudtime.minute == 0 and self.mudtime.second == 0:
            for id, pl in self.players.items():
                if pl["state"] == "ONLINE":
                    pl["con"].send("The Time of day has advanced\r\n")
                    if pl["player"].actions == 0:
                        pl["player"].actions = 1
