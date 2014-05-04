# Author: Nathaniel Pawelczyk
# CSE 30332
# work.py

from twisted.internet.protocol import Protocol, ClientFactory, ReconnectingClientFactory
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

commandconn = 0  #initialze globals
dataconn = 0
serviceconn = 0

class Command(Protocol):
	def dataReceived(self, data):
		if(data == "begin data connect"):
			reactor.connectTCP("student02.cse.nd.edu", 40246, DataConnectionFactory())
		elif(data == "begin service connect"):
			reactor.connectTCP("localhost", 22, ServiceConnectionFactory())
			

			

class CommandConnectionFactory(ReconnectingClientFactory):
	def startedConnecting(self, connector):
		print "Command connection created!"

	def buildProtocol(self, addr):
		self.resetDelay()
		commandconn = Command()
		return commandconn

	def clientConnectionLost(self, connector, reason):
		print "Lost connection.  Reason:", reason
		ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

	def clientConnectionFailed(self, connector, reason):
		print "Connection failed. Reason:", reason
		ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
		
		
		
class Data(Protocol):
	def dataReceived(self, data):
		serviceconn.transport.write(data)  #data connection writes to service connection


class DataConnectionFactory(ClientFactory):
	def startedConnecting(self, connector):
		print "Data connection created!"

	def buildProtocol(self, addr):
		global dataconn
		dataconn = Data()
		return dataconn
		

class Service(Protocol):
	def __init__(self):
		self.queue = DeferredQueue()
		self.queue.get().addCallback(self.writeData)

	def dataReceived(self, data):
		self.queue.put(data)
		
	def writeData(self, data):
		dataconn.transport.write(data)  #service connection writes to data connection
		self.queue.get().addCallback(self.writeData)


class ServiceConnectionFactory(ClientFactory):
	def startedConnecting(self, connector):
		print "Service connection created!"

	def buildProtocol(self, addr):
		global serviceconn
		serviceconn = Service()
		return serviceconn	


reactor.connectTCP("student02.cse.nd.edu", 40046, CommandConnectionFactory())
reactor.run()

