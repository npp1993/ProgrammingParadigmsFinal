# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# bullet.py provides bullet functionality

import pygame
import math

class Bullet(pygame.sprite.Sprite):
	def __init__(self, gs, angle=None):
		pygame.sprite.Sprite.__init__(self)

		# initialize bullet info
		self.rect = gs.bulletImage.get_rect()
		# start bullet behind the player at the center
		self.rect.center = gs.player.rect.center

		self.angle = angle
		self.remove = False

		# find horizontal and vertical speed according to the angle
		self.hspeed = math.cos(self.angle)
		self.vspeed = math.sin(self.angle)
		
		self.hspeed = self.hspeed*10
		self.vspeed = -self.vspeed*10
		
	def tick(self):
		# on tick, move the bullet hspeed and vspeed
		self.rect = self.rect.move(self.hspeed, self.vspeed)
		
class BulletController():
	def __init__(self, gs):
		self.gs = gs
		self.bullets = []
		
	def addBullet(self, bullet):
		self.bullets.append(bullet)
		
	def tick(self):  #animate all bullets on map
		nextBullets = []
		
		for bullet in self.bullets:  #remove all bullets from bullets array that are flagged to be removed
			if not bullet.remove:
				bullet.tick()
				nextBullets.append(bullet)
				
		self.bullets = nextBullets  #updated bullets list

	def blit(self):  #draw all bullets to screen
		for bullet in self.bullets:
			self.gs.screen.blit(self.gs.bulletImage, bullet.rect)

				
				
				
