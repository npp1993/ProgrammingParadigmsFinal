# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# player2.py provides player 2 functionality

import pygame
import math

class Player2(pygame.sprite.Sprite):  #class representing player 2
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)

		# initialize and load images
		self.gs = gs
		self.image = pygame.image.load("media/galaga_spaceship2.png")
		self.rect = self.image.get_rect()
		self.angle = 0
		
		self.i = 1
		self.exploding = False
		self.remove = False
	
	def blit(self):
		if not self.remove:
			if self.exploding:
				# add one to get the next image name in the sequence; if there is no next image, return
				if self.i == 15:
					self.remove = True  #flag explosion for removal from enemies list
					return
		
				imagePath = "media/explosion/galaga_enemy1_explosion" + str(self.i) + ".png"
				self.image = pygame.image.load(imagePath)
				self.i = self.i + 1  #increment explosion sequence image counter
				
			self.gs.screen.blit(self.image, self.rect)  #display local player
