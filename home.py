# Author: Nathaniel Pawelczyk
# CSE 30332
# home.py

from twisted.internet import protocol, reactor
from twisted.internet.defer import DeferredQueue

commandconn = 0  #initialze globals
clientconn = 0
dataconn = 0

class Command(protocol.Protocol):
	def dataReceived(self, data):
		print "data received: " + data
		#self.transport.write(data)
		
	def connectionMade(self):
		global commandconn
		print "Command connection created!"
		reactor.listenTCP(40246, DataFactory())
		self.transport.write("begin data connect")
		commandconn = self

class CommandFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return Command()
		
		
class Client(protocol.Protocol):
	def __init__(self):
		self.queue = DeferredQueue()
		self.queue.get().addCallback(self.writeData)

	def dataReceived(self, data):
		self.queue.put(data)
		
	def writeData(self, data):
		dataconn.transport.write(data)  #client connection writes to data connection
		self.queue.get().addCallback(self.writeData)
		
	def connectionMade(self):
		global clientconn
		print "Client connection created!"
		clientconn = self
		commandconn.transport.write("begin service connect")

		
class ClientFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return Client()


class DataFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return Data()
		
class Data(protocol.Protocol):
	def __init__(self):
		self.queue = DeferredQueue()
		self.queue.get().addCallback(self.writeData)

	def dataReceived(self, data):
		self.queue.put(data)
		
	def writeData(self, data):
		clientconn.transport.write(data)  #data connection writes to client connection
		self.queue.get().addCallback(self.writeData)
		
	def connectionMade(self):
		global dataconn
		print "Data connection created!"
		reactor.listenTCP(40146, ClientFactory())
		dataconn = self	
		
reactor.listenTCP(40046, CommandFactory())

print "Listening for command and client connections..."

reactor.run()
