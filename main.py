# Author:       Nathaniel Pawelczyk and Stephanie Tilden
# File:         main.py
# CSE 30332

from twisted.internet.protocol import Protocol, Factory, ClientFactory, ReconnectingClientFactory
from twisted.internet import protocol, reactor
from twisted.internet.defer import DeferredQueue
import pygame
import math
import sys

connection = 0 #global to hold either client or server connection


class ClientConnection(Protocol):
	def __init__(self):
		self.queue = DeferredQueue()
		self.queue.get().addCallback(self.writeData)

	def dataReceived(self, data):
		print data
		self.queue.put(data)
		
	def writeData(self, data):
		self.queue.get().addCallback(self.writeData)
		
	def connectionMade(self):
		global clientconn
		print "Client connection created!"
		self.transport.write("connected")
		connection = self
		
class ClientConnectionFactory(Factory):
	def buildProtocol(self, addr):
		return Client()
		
		
		

class ServerConnection(Protocol):
	def __init__(self):
		self.queue = DeferredQueue()
		self.queue.get().addCallback(self.writeData)

	def dataReceived(self, data):
		print data;
		self.queue.put(data)
		
	def writeData(self, data):
		self.queue.get().addCallback(self.writeData)
		
	def connectionMade(self):
		global connection
		print "Server connection created!"
		connection = self
	

class ServerConnectionFactory(ReconnectingClientFactory):
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
		
		
                
if __name__ == '__main__':

	if(len(sys.argv) < 2):  #get number of command line args
		print "usage: main.py <server|client> <hostname>"
		exit(1)
		
	if(sys.argv[1] == "server"):  #if player has specified himself as server, listen for connection
		reactor.listenTCP(40046, ClientConnectionFactory())
	elif(sys.argv[1] == "client"):  #if player has specified himself as client, connect to server
		if(len(sys.argv) == 3):
			reactor.connectTCP(sys.argv[2], 40046, ServerConnectionFactory()) 

	reactor.run()

