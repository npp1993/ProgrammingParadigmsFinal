# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# gamespace.py starts the game

from twisted.internet.protocol import Protocol
import cPickle as pickle

from player import Player
from player2 import Player2
from enemy import Enemy
from explosion import Explosion
from bullet import Bullet

import pygame
import math
import sys, getopt

from bullet import *
from explosion import *
from enemy import *

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

		# set up game objects
		self.clock = pygame.time.Clock()
		self.player = Player(self)
		self.player2 = Player2(self)
		self.enemy = Enemy(self)
		
		self.bulletImage = pygame.image.load("media/laser.png")  #store bullet sprite in local gamespace so it is not sent over the network

		# set repeat and initialize variables
		pygame.key.set_repeat(1,1)
		self.bullets = []
		self.exploding = False
		self.enemyExists = True

		# set up sounds
		#self.laserNoise = pygame.mixer.Sound("media/screammachine.wav")
		#self.explodeNoise = pygame.mixer.Sound("media/explode.wav")

	def tick(self): #called every 1/60th of second by LoopingCall in main
		# clock tick regulation (framerate) is handled by LoopingCall

		# if exploding, play explodeNoise and go to next scene in explosion
		if self.exploding:
			self.enemy.explosion.tick()
			self.laserNoise.stop()
			self.explodeNoise.play()

		# event handler
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				self.player.move(event.key)
			elif event.type == pygame.QUIT:
				reactor.stop() #stop twisted reactor
		
		# tick bullets, player, enemy
		for bullet in self.bullets:
			bullet.tick()

		newBullet = self.player.tick()
		self.player2.tick()  #update player 2 based on network data
		self.enemy.tick()

		unpacked = dict()  #create data structure to send to other player
		unpacked["rect"] = self.player.rect
		unpacked["angle"] = self.player.angle
		
		if newBullet:
			unpacked["newBullet"] = newBullet
		
		data = pickle.dumps(unpacked)
		self.connection.transport.write(data)

		# blit to screen
		self.screen.fill(self.black)
		
		for bullet in self.bullets:  #display all bullets
			self.screen.blit(self.bulletImage, bullet.rect)
			
		self.screen.blit(self.player.image, self.player.rect)  #display local player
		self.screen.blit(self.player2.image, self.player2.rect)  #display player 2
		
		# if statement to only show enemy before explosion
		if self.enemyExists:
			self.screen.blit(self.enemy.image, self.enemy.rect)
		if self.exploding:
			self.screen.blit(self.enemy.explosion.image, self.enemy.explosion.rect)

		pygame.display.flip()  #flip display buffers



