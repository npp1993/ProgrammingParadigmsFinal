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

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, gs = None, controller = None, newSpeed = None):
		pygame.sprite.Sprite.__init__(self)

		# initialize enemy sprite
		self.gs = gs
		self.controller = controller
		
		imageNum = randint(1,2)
		
		self.rect = self.gs.enemyImage.get_rect()
		self.rect.center = (x,y)  # place in bottom center of screen


		
		self.i = 1  #used to keep track of which explosion sprite to display
		
		self.new = (newSpeed != None)
		self.newSpeed = newSpeed
		
		self.exploding = False
		self.remove = False

	def tick(self):
		if not self.exploding:
			for bullet in self.gs.bulletController.bullets:  #checks for any bullets that have hit this enemy
				if self.rect.colliderect(bullet.rect):
					bullet.remove = True
					self.exploding = True
					return

			# keeps the enemy moving back and forth
			if not self.new:
				self.rect = self.rect.move(self.controller.hspeed, 0)
			else:
				self.rect = self.rect.move(self.newSpeed, 0)
				
				enemyRects = []
				
				for enemy in self.controller.enemies:
					if self != enemy:
						enemyRects.append(enemy.rect)
				
				nextRect = self.rect
				nextRect.centerx += self.newSpeed - self.controller.hspeed
				
				if  nextRect.collidelist(enemyRects) < 0 and self.rect.centerx > self.gs.width/4:
					self.new = False
				elif self.rect.left > self.gs.width:
					self.remove = True
					
			# if the enemy hits the edge of the screen, begin moving in the opposite direction
			if not self.new and self.rect.left < 20 or self.rect.right > self.gs.width - 20:
				self.controller.hspeed = -self.controller.hspeed
				
		else:
			# add one to get the next image name in the sequence; if there is no next image, return
			if self.i == 15:
				self.remove = True  #flag explosion for removal from enemies list
				return
			
			self.i = self.i + 1  #increment explosion sequence image counter


class EnemyController:
	def __init__(self, gs = None):
		self.gs = gs
		
		self.enemies = []
		
		self.lastEnemyAddedAt = datetime.now()
		
		self.enemyAddFrequency = 2
		
		# one enemy is 26 x 29 pixels
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

	def addEnemy(self):
		newEnemyLeft = Enemy(self.leftEnemy.rect.center.x-50, self.gs.height/8, self.gs)
		newEnemyRight = Enemy(self.rightEnemy.rect.center.y+50, self.gs.height/8, self.gs)
		

	def blit(self):  #draw all enemies to screen
		for enemy in self.enemies:
			if not enemy.exploding:  #draw regular image if not exploding
				self.gs.screen.blit(self.gs.enemyImage, enemy.rect)
			else:  #draw exploding image
				imagePath = "media/explosion/galaga_enemy1_explosion" + str(enemy.i) + ".png"
				self.gs.screen.blit(pygame.image.load(imagePath), enemy.rect)
				
				

