# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# player2.py provides player 2 functionality

import pygame
import math

class Player2(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)

		# initialize and load images
		self.gs = gs
		self.image = pygame.image.load("media/galaga_spaceship.png")
		self.rect = self.image.get_rect()
		self.angle = 0
		self.orig_image = self.image
