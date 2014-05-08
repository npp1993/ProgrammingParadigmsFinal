# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# bullet.py provides bullet functionality

import pygame
import math

class Bullet(pygame.sprite.Sprite):
	def __init__(self, gs, angle=None, enemy=None):
		pygame.sprite.Sprite.__init__(self)
		
		self.enemy = False
		self.player = ""  #owner of bullet
		
		if enemy:
			self.enemy = True

		# initialize bullet info
		if self.enemy:
			self.rect = gs.enemyBulletImage.get_rect()
			self.rect.center = enemy.data.rect.center
		else:
			self.rect = gs.bulletImage.get_rect()
			self.rect.center = gs.player.rect.center

		self.angle = angle
		self.remove = False

		# find horizontal and vertical speed according to the angle
		self.hspeed = math.cos(self.angle)
		self.vspeed = 12 * math.sin(self.angle)
		
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
			if not bullet.remove and bullet.rect.centery < self.gs.height:
				bullet.tick()
				nextBullets.append(bullet)
				
		self.bullets = nextBullets  #updated bullets list

	def blit(self):  #draw all bullets to screen
		for bullet in self.bullets:
			if bullet.enemy:
				self.gs.screen.blit(self.gs.enemyBulletImage, bullet.rect)
			else:
				self.gs.screen.blit(self.gs.bulletImage, bullet.rect)

				
				
				
