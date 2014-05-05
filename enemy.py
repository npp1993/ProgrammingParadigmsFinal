# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# enemy.py provides enemy functionality

import pygame
import math

from bullet import *
from explosion import *

class Enemy(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)

		# initialize enemy sprite
		self.gs = gs
		self.image = pygame.image.load("globe.png")
		self.rect = self.image.get_rect()
		# place in bottom center of screen
		self.rect.center = (self.gs.width/2, self.gs.height)

		# initialize variables
		self.hspeed = 2
		self.hits = 0
		self.explosion = None

	def tick(self):
		# create bulletRects to check for collisions
		bulletRects = []
		for bullet in self.gs.bullets:
			bulletRects.append(bullet.rect)

		# if a bullet has collided, add 1
		if self.rect.collidelist(bulletRects) >= 0:
			self.hits +=1
		
		# if the enemy has been hit 130 times, make it red
		if self.hits == 130:
			self.image = pygame.image.load("globe_red100.png")

		# if the enemy has been hit 200 times, explode
		if self.hits == 200:
			self.explosion = Explosion(self.gs, self) # create explosion object
			self.gs.exploding = True

		# if the enemy hits the edge of the screen, begin moving in the opposite direction
		if self.rect.collidepoint(self.gs.width+20, self.gs.height) or self.rect.collidepoint(-20, self.gs.height):
			self.hspeed = -self.hspeed;

		# keeps the enemy moving back and forth
		self.rect = self.rect.move(self.hspeed, 0)
