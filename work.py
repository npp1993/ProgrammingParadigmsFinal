# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# work.py provides twisted functionality

# command port is 40061
# data port is 80061
# service port is 22

from twisted.internet import protocol, reactor
from twisted.internet.defer import DeferredQueue

#class init_work(self, work_connections):
#	def __init__(self, work_connections):
#		connections = work_connections		

class work_CommandConn(protocol.Protocol):
	def __init__(self):
		print 'work created command connection to home'	

	def connectionMade(self):
		work_connections['command_conn'] = self

	def dataReceived(self, data):
		reactor.connectTCP('student00.cse.nd.edu', 80061, work_DataConnFactory())
		reactor.connectTCP('student00.cse.nd.edu', 22, work_ServiceConnFactory())

class work_CommandConnFactory(protocol.ReconnectingClientFactory):
	def buildProtocol(self, addr):
		self.resetDelay()
		return work_CommandConn()

	def clientConnectionLost(self, connector, reason):
		print "Lost connection. Reason:", reason
		ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

	def clientConnectionFailed(self, connector, reason):
		print "Lost connection. Reason:", reason
		ReconnectingClientFactory.clientConnectionLost(self, connector, reason)


class work_DataConn(protocol.Protocol):
	def __init__(self):
		print 'data connection established'	
		self.queue = DeferredQueue()

	def connectionMade(self):
		work_connections['data_conn'] = self
		self.queue.get().addCallback(self.forwardData)

	def dataReceived(self, data):
		self.queue.put(data)

	def forwardData(self, data):
		work_connections['service_conn'].transport.write(data)
		self.queue.get().addCallback(self.forwardData)

class work_DataConnFactory(protocol.ClientFactory):
	def buildProtocol(self, addr):
		return work_DataConn()


class work_ServiceConn(protocol.Protocol):
	def __init__(self):
		print 'service connection established'
		self.queue = DeferredQueue()

	def connectionMade(self):
		work_connections['service_conn'] = self
		self.queue.get().addCallback(self.forwardData)

	def dataReceived(self, data):
		self.queue.put(data)

	def forwardData(self, data):
		work_connections['data_conn'].transport.write(data)
		self.queue.get().addCallback(self.forwardData)

class work_ServiceConnFactory(protocol.ClientFactory):
	def buildProtocol(self, addr):
		return work_ServiceConn()




