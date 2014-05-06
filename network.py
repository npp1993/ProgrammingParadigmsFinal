# Author:       Nathaniel Pawelczyk and Stephanie Tilden
# File:         main.py
# CSE 30332

from twisted.internet.protocol import Protocol, Factory, ClientFactory, ReconnectingClientFactory
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.internet import protocol, reactor
import pygame
import cPickle as pickle
from gamespace import GameSpace

gs = 0  #define global variable gamespace 

def startGameSpace(conn):  #initialize gamespace, start looping call for gamespace main loop
	global gs
	gs = GameSpace(conn)
	gs.main()
	
	tick = LoopingCall(gs.tick)  #set up looping call to run gamespace tick
	tick.start(1.0/60)  #set to run tick every 60th of a second
	
def updateGameSpace(data):  #update player2 object with network data
	unpacked = pickle.loads(data)
	gs.player2.rect = unpacked["rect"]  #get other player data
	gs.player2.angle = unpacked["angle"]
		
	if "newBullet" in unpacked:
		gs.bullets.append(unpacked["newBullet"])
	

class ClientConnection(Protocol):

	def dataReceived(self, data):
		updateGameSpace(data)
		
	def connectionMade(self):
		startGameSpace(self)
		
class ClientConnectionFactory(Factory):
	def buildProtocol(self, addr):
		return ClientConnection()
		

class ServerConnection(Protocol):

	def dataReceived(self, data):
		updateGameSpace(data)

	def connectionMade(self):
		startGameSpace(self)
	

class ServerConnectionFactory(ReconnectingClientFactory):
	def buildProtocol(self, addr):
		self.resetDelay()
		return ServerConnection()

	def clientConnectionLost(self, connector, reason):  #exit game if connection to server is lost
		reactor.stop()


	def clientConnectionFailed(self, connector, reason):
		print "Connection failed. Reason:", reason
		ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
		
		
