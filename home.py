# Stephanie Tilden
# cse30332
# twisted
# Due April 30, 2014

# home.py

# command port is 40061
# data port is 80061
# client port is 9001

from twisted.internet import protocol, reactor
from twisted.internet.defer import DeferredQueue

class home_ClientConn(protocol.Protocol):
	def __init__(self):
		print 'client connection established'
		self.queue = DeferredQueue()

	def connectionMade(self):
		home_connections['client_conn'] = self
		home_connections['command_conn'].transport.write('begin data connect')
		reactor.listenTCP(80061, DataConnFactory())
		self.queue.get().addCallback(self.forwardData)

	def dataReceived(self, data):
		self.queue.put(data)

	def forwardData(self, data):
		home_connections['data_conn'].transport.write(data)
		self.queue.get().addCallback(self.forwardData)
		

class home_ClientConnFactory(protocol.ClientFactory):
	def buildProtocol(self, addr):
		return home_ClientConn()


class home_CommandConn(protocol.Protocol):
	def __init__(self):
		print 'command connection established'

	def connectionMade(self):
		home_connections['command_conn'] = self

class home_CommandConnFactory(protocol.ClientFactory):
	def buildProtocol(self, addr):
		return home_CommandConn()



class home_DataConn(protocol.Protocol):
	def __init__(self):
		print 'home listening for data connection from work'
		self.queue = DeferredQueue()

	def connectionMade(self):
		home_connections['data_conn'] = self
		self.queue.get().addCallback(self.forwardData)

	def dataReceived(self, data):
		self.queue.put(data)

	def forwardData(self, data):
		home_connections['client_conn'].transport.write(data)
		self.queue.get().addCallback(self.forwardData)


class home_DataConnFactory(protocol.ClientFactory):
	def buildProtocol(self, addr):
		print "in data conn factory in home"
		return home_DataConn()
