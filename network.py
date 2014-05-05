# Author:       Nathaniel Pawelczyk and Stephanie Tilden
# File:         main.py
# CSE 30332

from twisted.internet.protocol import Protocol, ClientFactory, ReconnectingClientFactory
from twisted.internet import reactor
from twisted.internet import protocol, reactor
import pygame
import cPickle as pickle

def startGamespace(conn):
	global gs
	gs = GameSpace(conn)
	gs.main()  #initialize gamespace
	
	tick = LoopingCall(gs.tick())  #set up looping call to run gamespace tick
	tick.start(1.0/60)  #set to run tick every 60th of a second
			
	reactor.run()

class ClientConnection(Protocol):

	def dataReceived(self, data):
		print "got data from client" + data
		gs.player2.rect = pickle.loads(data)
		
	def connectionMade(self):
		print "connected to client"
		startGamespace(self)
		
class ClientConnectionFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return ClientConnection()
		
		

class ServerConnection(Protocol):

	def dataReceived(self, data):
		print "got data from server"
		gs.player2.rect = pickle.loads(data)

	def connectionMade(self):
		print "connected to server"
		startGamespace(self)
	

class ServerConnectionFactory(ReconnectingClientFactory):
	def buildProtocol(self, addr):
		self.resetDelay()
		return ServerConnection()

	def clientConnectionLost(self, connector, reason):
		print "Lost connection.  Reason:", reason
		ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

	def clientConnectionFailed(self, connector, reason):
		print "Connection failed. Reason:", reason
		ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
		
		