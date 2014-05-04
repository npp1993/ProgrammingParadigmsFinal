# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# explosion.py provides explosion functionality

import pygame
import math

class Explosion(pygame.sprite.Sprite):
	def __init__(self, gs=None, enemy=None):
		pygame.sprite.Sprite.__init__(self)

		# initialize explosion
		self.gs = gs
		#self.delay = 100

		# initialize list of image names
		self.images = ["frames000a.png", "frames001a.png", "frames002a.png", "frames003a.png", "frames004a.png", "frames005a.png", "frames006a.png", "frames007a.png", "frames008a.png", "frames009a.png", "frames010a.png", "frames011a.png", "frames012a.png", "frames013a.png", "frames014a.png", "frames015a.png", "frames016a.png"]

		# initial image is the first image in the explosion
		self.i = 0
		self.imagePath = "explosion/" + self.images[self.i]
		self.image = pygame.image.load(self.imagePath)
		self.rect = self.image.get_rect()
		# place center at enemy's center
		self.enemy = enemy
		self.rect.center = self.enemy.rect.center

	def tick(self):
		# when the explosion occurs, the enemy no longer exists
		self.gs.enemyExists = False

		# add one to get the next image name in the sequence; if there is no next image, return
		self.i = self.i + 1
		if self.i>=len(self.images):
			self.gs.exploding = False
			return

		# load next image in sequence
		self.imagePath = "explosion/" + self.images[self.i]
		self.image = pygame.image.load(self.imagePath)
		self.rect = self.image.get_rect()
		self.rect.center = self.enemy.rect.center
