# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# explosion.py provides explosion functionality

import pygame
import math

class Explosion(pygame.sprite.Sprite):
	def __init__(self, gs=None, enemyRect=None):
		pygame.sprite.Sprite.__init__(self)

		# initialize explosion
		self.gs = gs
		#self.delay = 100

		# initial image is the first image in the explosion
		self.i = 0
		
		self.imagePath = None
		self.image = None
		self.rect = None
		
		# place center at enemy's center
		self.center = enemyRect.center
		
		self.done = False

	def tick(self):

