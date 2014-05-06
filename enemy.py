# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# enemy.py provides enemy functionality

import pygame
import math

from bullet import *

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, gs = None, controller = None):
		pygame.sprite.Sprite.__init__(self)

		# initialize enemy sprite
		self.gs = gs
		self.controller = controller
		self.image = pygame.image.load("media/galaga_enemy1.png")
		self.rect = self.image.get_rect()
		# place in bottom center of screen
		self.rect.center = (x,y)

		# initialize variables
		#self.hits = 0
		
		self.i = 1  #used to keep track of which explosion sprite to display
		
		self.exploding = False
		self.remove = False

	def tick(self):
		if not self.exploding:
			# create bulletRects to check for collisions
			#bulletRects = []
			for bullet in self.gs.bullets:
				if self.rect.colliderect(bullet.rect):
					bullet.remove = True
					self.exploding = True
					return

			#	bulletRects.append(bullet.rect)

			# if a bullet has collided, add 1
			#if self.rect.collidelist(bulletRects) >= 0:
			#	self.hits +=1
			#for bulletRect in bulletRects:
			#	if self.rect.collidepoint(bulletRect.

			# if the enemy has been 5 times, explode
			#if self.hits >= 5:
			#	self.exploding = True
			#	return;
			
			# if the enemy hits the edge of the screen, begin moving in the opposite direction
			if self.rect.collidepoint(self.gs.width-20, self.gs.height/8) or self.rect.collidepoint(20, self.gs.height/8):
				self.controller.hspeed = -self.controller.hspeed;

			# keeps the enemy moving back and forth
			self.rect = self.rect.move(self.controller.hspeed, 0)
		else:
			# add one to get the next image name in the sequence; if there is no next image, return
			if self.i > 15:
				self.remove = True  #flag explosion for removal from explosions list
				return

			# load next image in sequence
			self.imagePath = "media/explosion/galaga_enemy1_explosion" + str(self.i) + ".png"
			self.image = pygame.image.load(self.imagePath)
			
			self.i = self.i + 1


class enemyController:
	def __init__(self, gs = None):
		self.gs = gs
		# one enemy is 26 x 29 pixels
		leftEnemy = Enemy(self.gs.width/2-50, self.gs.height/8, self.gs, self)
		middleEnemy = Enemy(self.gs.width/2, self.gs.height/8, self.gs, self)
		rightEnemy = Enemy(self.gs.width/2+50, self.gs.height/8, self.gs, self)

		self.enemies = []
		self.enemies.append(leftEnemy)
		self.enemies.append(middleEnemy)
		self.enemies.append(rightEnemy)
		
		self.hspeed = 2
		
	def tick(self):
		nextEnemies = []
	
		for enemy in self.enemies:
			enemy.tick()
			
			if not enemy.remove:
				nextEnemies.append(enemy)
				
		self.enemies = nextEnemies

	def addEnemy(self):
		newEnemyLeft = Enemy(self.leftEnemy.rect.center.x-50, self.gs.height/8, self.gs)
		newEnemyRight = Enemy(self.rightEnemy.rect.center.y+50, self.gs.height/8, self.gs)
		

	def blit(self):
		for enemy in self.enemies:
			self.gs.screen.blit(enemy.image, enemy.rect)
		
