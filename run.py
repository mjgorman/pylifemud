from twisted.application import internet, service
from twisted.internet import task, reactor
from systems.mudserver import MudServerFactory

port = 8080
application = service.Application('MudServer')
factory = MudServerFactory()
mudService = internet.TCPServer(port,factory)
mudService.setServiceParent(application)

gameloop = task.LoopingCall(factory.update)
gameloop.start(.06)
