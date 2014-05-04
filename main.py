# Author:       Nathaniel Pawelczyk and Stephanie Tilden
# File:         main.py
# CSE 30332

from twisted.internet.protocol import Protocol, ClientFactory, ReconnectingClientFactory
from twisted.internet import reactor
from twisted.internet import protocol, reactor
import pygame
import cPickle as pickle

from gamespace import *

import math
import sys

gs = 0 #variable to hold local gamespace

class ClientConnection(Protocol):

	def dataReceived(self, data):
		print "got data from client" + data
		gs.player2.rect = pickle.loads(data)
		
	def connectionMade(self):
		print "connected to client"
		gs = GameSpace(self)
		gs.main()  #start gamespac
		
class ClientConnectionFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return ClientConnection()
		
		

class ServerConnection(Protocol):

	def dataReceived(self, data):
		print "got data from server"
		gs.player2.rect = pickle.loads(data)

	def connectionMade(self):
		print "connected to server"
		gs = GameSpace(self)
		gs.main()  #start gamespac
	

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

