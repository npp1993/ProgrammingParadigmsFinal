# Author:       Nathaniel Pawelczyk and Stephanie Tilden
# File:         main.py
# CSE 30332

from twisted.internet.protocol import Protocol, Factory, ClientFactory, ReconnectingClientFactory
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.internet import protocol, reactor
import pygame
from gamespace import *

gs = None  #define global variable gamespace 

def startGameSpace(conn, player):  #initialize gamespace, start looping call for gamespace main loop
	global gs

	if player == "server":  #create different gamespaces depending on which end of the connection game is on
		gs = ServerGameSpace(conn)
	else:
		gs = ClientGameSpace(conn)
	
	tick = LoopingCall(gs.tick)  #set up looping call to run gamespace tick
	tick.start(1.0/60)  #set to run tick every 60th of a second
	

class ClientConnection(Protocol):

	def dataReceived(self, data):
		gs.updateData(data)
		
	def connectionMade(self):
		startGameSpace(self, "server")
		
class ClientConnectionFactory(Factory):
	def buildProtocol(self, addr):
		return ClientConnection()
		

class ServerConnection(Protocol):

	def dataReceived(self, data):
		gs.updateData(data)

	def connectionMade(self):
		startGameSpace(self, "client")
	

class ServerConnectionFactory(ReconnectingClientFactory):
	def buildProtocol(self, addr):
		self.resetDelay()
		return ServerConnection()

	def clientConnectionLost(self, connector, reason):  #exit game if connection to server is lost
		reactor.stop()


	def clientConnectionFailed(self, connector, reason):
		print "Connection failed. Reason:", reason
		ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
		
		
