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

from work import *
from home import *

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

		# set repeat and initialize variables
		pygame.key.set_repeat(1,1)
		self.bullets = []
		self.exploding = False
		self.enemyExists = True

		# set up sounds
		self.laserNoise = pygame.mixer.Sound("screammachine.wav")
		self.explodeNoise = pygame.mixer.Sound("explode.wav")

		# start game loop 
		while 1:
			# clock tick regulation (framerate)
			self.clock.tick(60)

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
					exit()
			
			# tick bullets, player, enemy
			for bullet in self.bullets:
				bullet.tick()

			self.player.tick()
			self.enemy.tick()

			data = pickle.dumps(self.player.rect)
			self.connection.transport.write(data)

			# blit to screen
			self.screen.fill(self.black)
			for bullet in self.bullets:
				self.screen.blit(bullet.image, bullet.rect)
			self.screen.blit(self.player.image, self.player.rect)
			self.screen.blit(self.player2.image, self.player2.rect)
			# if statement to only show enemy before explosion
			if self.enemyExists:
				self.screen.blit(self.enemy.image, self.enemy.rect)
			if self.exploding:
				self.screen.blit(self.enemy.explosion.image, self.enemy.explosion.rect)
	
			pygame.display.flip()



