# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# enemy.py provides enemy functionality

import pygame
import math
from random import randint
from datetime import datetime

from bullet import *

class EnemyData():
	def __init__(self, imageNum, exploding, i):  #class to hold data about enemy position and appearance
		self.rect = None
		self.imageNum = imageNum
		self.exploding = exploding
		self.i = i
		

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, gs, controller, newSpeed = None):
		pygame.sprite.Sprite.__init__(self)

		# initialize enemy sprite
		self.gs = gs
		self.controller = controller
		
		self.data = EnemyData(randint(1,2), False, 1)
		self.image = pygame.image.load("media/galaga_enemy" + str(self.data.imageNum) + ".png")  #pick random image for enemy
		
		self.data.rect = self.image.get_rect()
		self.data.rect.center = (x,y)  # place in top of screen
		
		self.new = (newSpeed != None)
		self.newSpeed = newSpeed
		
		self.remove = False  #flag to determine whether or not to remove enemy on next tick

	def tick(self):
		if not self.data.exploding:
			for bullet in self.gs.bulletController.bullets:  #checks for any bullets that have hit this enemy
				if self.data.rect.colliderect(bullet.rect):
					bullet.remove = True
					self.data.exploding = True
					return

			# keeps the enemy moving back and forth
			if not self.new:
				self.data.rect = self.data.rect.move(self.controller.hspeed, 0)
			else:
				self.data.rect = self.data.rect.move(self.newSpeed, 0)
				
				enemyRects = []
				
				for enemy in self.controller.enemies:
					if self != enemy:
						enemyRects.append(enemy.data.rect)
				
				nextRect = self.data.rect
				nextRect.centerx += self.newSpeed - self.controller.hspeed
				
				if  nextRect.collidelist(enemyRects) < 0 and self.data.rect.centerx > self.gs.width/4:
					self.new = False
				elif self.data.rect.left > self.gs.width:
					self.remove = True
					
			# if the enemy hits the edge of the screen, begin moving in the opposite direction
			if not self.new and self.data.rect.left < 20 or self.data.rect.right > self.gs.width - 20:
				self.controller.hspeed = -self.controller.hspeed
				
		else:
			# add one to get the next image name in the sequence; if there is no next image, return
			if self.data.i == 15:
				self.remove = True  #flag explosion for removal from enemies list
				return
			
			imagePath = "media/explosion/galaga_enemy1_explosion" + str(self.data.i) + ".png"
			self.image = pygame.image.load(imagePath)
			
			self.data.i = self.data.i + 1  #increment explosion sequence image counter


class EnemyController:
	def __init__(self, gs):
		self.gs = gs
		
		self.enemies = []
		
		self.lastEnemyAddedAt = datetime.now()
		
		self.enemyAddFrequency = 2
		
		#one enemy is 26 x 29 pixels
		leftEnemy = Enemy(self.gs.width/2-50, self.gs.height/8, self.gs, self)
		middleEnemy = Enemy(self.gs.width/2, self.gs.height/8, self.gs, self)
		rightEnemy = Enemy(self.gs.width/2+50, self.gs.height/8, self.gs, self)

		self.enemies.append(leftEnemy)
		self.enemies.append(middleEnemy)
		self.enemies.append(rightEnemy)
	
		self.hspeed = 2
		
	def tick(self):  #animate all enemies on map
		nextEnemies = []
	
		for enemy in self.enemies:  #remove all enemies done exploding
			enemy.tick()
		
			if not enemy.remove:  #enemy still alive or exploding
				nextEnemies.append(enemy)
				
		currentTime = datetime.now()  #get current time
		timeDiff = currentTime - self.lastEnemyAddedAt  #get time since last enemy was added
		
		if timeDiff.seconds > self.enemyAddFrequency:  #allow for one enemy to be fired every 2 seconds
			self.lastEnemyAddedAt = currentTime  #update time that last bullet was fired
			
			randHeight = randint(-1, 1) * 50
			newEnemy = Enemy(-50, self.gs.height/8 + randHeight, self.gs, self, 4)
			nextEnemies.append(newEnemy)  #add new enemy to enemies list
	
		self.enemies = nextEnemies


	def blit(self):  #draw all enemies to screen
		for enemy in self.enemies:
			self.gs.screen.blit(enemy.image, enemy.data.rect)
				
				

