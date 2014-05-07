# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# gamespace.py starts the game

from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import cPickle as pickle

from player import Player
from player2 import Player2
from enemy import *
from bullet import Bullet

import pygame
import math
import sys, getopt

class GameSpace:
	def __init__(self, connection):
		self.connection = connection
	
	def main(self):
		# basic initialization
		pygame.init()
		pygame.mixer.init()
		self.size = self.width, self.height = 740, 580
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()
		
		# set repeat
		pygame.key.set_repeat(1,1)
		
		# set up game objects
		self.player = Player(self)
		self.player2 = Player2(self)
		
		self.bulletImage = pygame.image.load("media/bullet.png")  #store bullet sprite in local gamespace so it is not sent over the network
		self.enemyImage = pygame.image.load("media/galaga_enemy1.png")

		self.bulletController = BulletController(self)  #manages all enemies
		self.enemyController = EnemyController(self)  #manages all bullets

		# set up sounds
		self.bulletNoise = pygame.mixer.Sound("media/bullet.wav")
		#self.explodeNoise = pygame.mixer.Sound("media/explode.wav")
		
	def tick(self): #called every 1/60th of second by LoopingCall in main
		# clock tick regulation (framerate) is handled by LoopingCall
		# event handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				reactor.stop() #stop twisted reactor
			else:
				self.player.move(event)
		
		#tick bullets, player, enemy, explosions
		newBullet = self.player.tick()  #if player created a bullet in this tick, save it to send across network
		self.enemyController.tick()
		self.bulletController.tick()  #tick all bullets
		
		self.sendData(newBullet)  #send all appropriate data to other player

		# blit to screen
		self.screen.fill(self.black)  #clear screen
		
		self.screen.blit(self.player.image, self.player.rect)  #display local player
		self.screen.blit(self.player2.image, self.player2.rect)  #display player 2
		self.enemyController.blit()  #blit all enemies
		self.bulletController.blit()  #blit all bullets

		pygame.display.flip()  #flip display buffers


class ClientGameSpace(GameSpace):
	def __init__(self, connection):
		GameSpace.__init__(self, connection)
		
	def sendData(self, newBullet = None):  #send data to other player
		unpacked = dict()  #create data structure to send to other player
		unpacked["rect"] = self.player.rect
		unpacked["angle"] = self.player.angle
		
		if newBullet:
			unpacked["newBullet"] = newBullet
		
		data = pickle.dumps(unpacked)
		self.connection.transport.write(data)
		
	def update(self, data):
		unpacked = pickle.loads(data)
		self.player2.rect = unpacked["rect"]  #get other player data
		self.player2.angle = unpacked["angle"]
		
		if "newBullet" in unpacked:
			self.bulletController.addBullet(unpacked["newBullet"])


class ServerGameSpace(GameSpace):
	def __init__(self, connection):
		GameSpace.__init__(self, connection)
		
	def sendData(self, newBullet = None):  #send data to other player
		unpacked = dict()  #create data structure to send to other player
		unpacked["rect"] = self.player.rect
		unpacked["angle"] = self.player.angle
		
		if newBullet:
			unpacked["newBullet"] = newBullet
		
		data = pickle.dumps(unpacked)
		self.connection.transport.write(data)
		
	def update(self, data):
		unpacked = pickle.loads(data)
		self.player2.rect = unpacked["rect"]  #get other player data
		self.player2.angle = unpacked["angle"]
		
		if "newBullet" in unpacked:
			self.bulletController.addBullet(unpacked["newBullet"])



