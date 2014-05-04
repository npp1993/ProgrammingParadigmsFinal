# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# bullet.py provides bullet functionality

import pygame
import math

class Bullet(pygame.sprite.Sprite):
	def __init__(self, gs=None, angle=None):
		pygame.sprite.Sprite.__init__(self)

		# initialize bullet info
		self.gs = gs
		self.image = pygame.image.load("laser.png")
		self.rect = self.image.get_rect()
		# start bullet behind the player at the center
		self.rect.center = self.gs.player.rect.center

		self.angle = angle

		# find horizontal and vertical speed according to the angle
		self.hspeed = math.cos(self.angle)
		self.vspeed = math.sin(self.angle)
		
		self.hspeed = self.hspeed*4
		self.vspeed = -self.vspeed*4
		
	def tick(self):
		# on tick, move the bullet hspeed and vspeed
		self.rect = self.rect.move(self.hspeed, self.vspeed)
