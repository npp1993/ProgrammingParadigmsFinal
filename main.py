# Author:       Nathaniel Pawelczyk and Stephanie Tilden
# File:         main.py
# CSE 30332

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from network import *
from gamespace import *

import math
import sys

gs = 0 #variable to hold local gamespace
                
if __name__ == '__main__':
	if(len(sys.argv) < 2):  #get number of command line args
		print "usage: main.py <server|client> <hostname>"
		exit(1)
		
	if(sys.argv[1] == "server"):  #if player has specified himself as server, listen for connection
		reactor.listenTCP(40046, ClientConnectionFactory())
	elif(sys.argv[1] == "client"):  #if player has specified himself as client, connect to server
		if(len(sys.argv) == 3):
			reactor.connectTCP(sys.argv[2], 40046, ServerConnectionFactory()) 

	#wait for connection to be created before creating gamespace, see network.py

