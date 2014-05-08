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
from bullet import *

import pygame
import math
import sys, getopt

class GameSpace:
	def __init__(self, connection):
		self.connection = connection

		# basic initialization
		pygame.init()
		pygame.mixer.init()
		self.size = self.width, self.height = 700, 700
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()
		
		# set repeat
		pygame.key.set_repeat(1,1)
		
		# set up game objects
		self.player = Player(self)
		self.player2 = Player2(self)
		
		self.bulletImage = pygame.image.load("media/bullet.png")  #store bullet sprite in local gamespace so it is not sent over the network
		self.enemyBulletImage = pygame.image.load("media/enemyBullet.png")

		# set up sounds
		self.bulletNoise = pygame.mixer.Sound("media/bullet.wav")
		self.welcomeNoise = pygame.mixer.Sound("media/galagaWelcome.wav")
		
		self.welcomeNoise.play()  #play welcome noise

		#self.startScreen()

	def startScreen(self):
		self.font = pygame.font.Font(None, 30)
		textImg = self.font.render("PRESS SPACE TO START GAME", 1, (255,0,0))
		self.screen.blit(textImg, (self.width/2, self.height/2))

		while True:  #get all events from user
			event = pygame.event.wait()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				return
				
		
	def tick(self): #called every 1/60th of second by LoopingCall in main
		# clock tick regulation (framerate) is handled by LoopingCall
		# event handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				reactor.stop() #stop twisted reactor
			else:
				self.player.move(event)


class ClientGameSpace(GameSpace):
	def __init__(self, connection):
		GameSpace.__init__(self, connection)
		self.enemies = []  #holds the enemies
		self.bullets = []  #holds the bullets
		pygame.display.set_caption("Galaga client")
		
	def tick(self):  #tick bullets, player, enemy, explosions
		GameSpace.tick(self)
		newBullet = self.player.tick()  #if player created a bullet in this tick, save it to send across network
		
		#enemies and bullets are not stored locally and ticked because they contain a server-controlled AI
		
		self.sendData(newBullet)  #send all appropriate data to other player

		# blit to screen
		self.screen.fill(self.black)  #clear screen

		self.player.blit()  #blit local player
		
		if not self.player2.remove:  #blit other player
			self.gs.screen.blit(self.player2.image, self.player2.rect)
		
		
		self.displayEnemies()  #display all enemies based on server data
		self.displayBullets()  #display all bullets based on server data

		pygame.display.flip()  #flip display buffers
		
	def displayEnemies(self):  #display all enemies based on data from server
		for enemy in self.enemies:
			if not enemy.exploding:  #enemy not exploding
				imagePath = "media/galaga_enemy" + str(enemy.imageNum) + ".png"
				image = pygame.image.load(imagePath)
				self.screen.blit(image, enemy.rect)
			else:  #enemy is exploding
				imagePath = "media/explosion/galaga_enemy1_explosion" + str(enemy.i) + ".png"	
				image = pygame.image.load(imagePath)
				self.screen.blit(image, enemy.rect)
				
	def displayBullets(self):  #display all bullets
		for bullet in self.bullets:
			if bullet.enemy:  #enemy bullet
				self.screen.blit(self.enemyBulletImage, bullet.rect)
			else:  #player bullet
				self.screen.blit(self.bulletImage, bullet.rect)
		
	def sendData(self, newBullet = None):  #send data to other player
		unpacked = dict()  #create data structure to send to other player
		unpacked["rect"] = self.player.rect
		
		if newBullet:
			unpacked["newBullet"] = newBullet
		
		data = pickle.dumps(unpacked)
		self.connection.transport.write(data)
		
	def updateData(self, data):
		unpacked = pickle.loads(data)
		self.player2.rect = unpacked["rect"]  #get other player data	
		self.enemies = unpacked["enemies"]  #get all enemy data from server
		self.bullets = unpacked["bullets"]


class ServerGameSpace(GameSpace):
	def __init__(self, connection):
		GameSpace.__init__(self, connection)
		self.enemyController = EnemyController(self)  #manages all enemies
		self.bulletController = BulletController(self)  #manages all bullets
		
		pygame.display.set_caption("Galaga server")

		
	def tick(self):  #tick bullets, player, enemy, explosions
		GameSpace.tick(self)
		
		self.playerController.tick()  #tick players
		self.enemyController.tick()  #tick all server-controlled enemies, get bullets from enemies
		self.bulletController.tick()  #tick all bullets
		
		self.sendData()  #send all appropriate data to other player

		# blit to screen
		self.screen.fill(self.black)  #clear screen
		
		self.playerController.blit()

		self.screen.blit(self.player.image, self.player.rect)  #display local player
		self.screen.blit(self.player2.image, self.player2.rect)  #display player 2
		
		self.enemyController.blit()  #blit all enemies
		self.bulletController.blit()  #blit all bullets
		
		pygame.display.flip()  #flip display buffers

		
	def sendData(self):  #send data to other player
		unpacked = dict()  #create data structure to send to other player
		unpacked["rect"] = self.player.rect
		
		unpacked["enemies"] = list()
		
		for enemy in self.enemyController.enemies:  #send all enemy data
			enemy.data.rect = self.enemyController.rects[enemy.row][enemy.col]  #get updated rect from rects array in enemy controller
			unpacked["enemies"].append(enemy.data)
		
		unpacked["bullets"] = self.bulletController.bullets  #send all bullets
		
		data = pickle.dumps(unpacked)
		self.connection.transport.write(data)
		
	def updateData(self, data):
		unpacked = pickle.loads(data)
		self.player2.rect = unpacked["rect"]  #get other player data
		
		if "newBullet" in unpacked:
			self.bulletController.addBullet(unpacked["newBullet"])



