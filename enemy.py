# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# enemy.py provides enemy functionality

import pygame
import math
from random import randint

from bullet import *

class EnemyData():
	def __init__(self, imageNum):  #class to hold data about enemy position and appearance
		self.rect = None
		self.imageNum = imageNum
		self.exploding = False
		self.i = 1
		

class Enemy(pygame.sprite.Sprite):
	def __init__(self, row, col, gs, controller):
		pygame.sprite.Sprite.__init__(self)

		# initialize enemy sprite
		self.gs = gs
		self.controller = controller
		
		self.data = EnemyData(randint(1,2))
		self.image = pygame.image.load("media/galaga_enemy" + str(self.data.imageNum) + ".png")  #pick random image for enemy
		
		self.row = row
		self.col = col
		
		self.fireFrequency = randint(40, 200)  #frequency with which enemy fires  
		
		self.data.rect = self.controller.rects[self.row][self.col]  #get rect from rects array in controller
		
		self.remove = False  #flag to determine whether or not to remove enemy on next tick

	def tick(self):
		if not self.data.exploding:
			for bullet in self.gs.bulletController.bullets:  #checks for any bullets that have hit this enemy
				if not bullet.enemy and self.data.rect.colliderect(bullet.rect):
					bullet.remove = True
					self.data.exploding = True
					return

			if self.controller.ticks % self.fireFrequency == 0:  #check if enemy is going to fire
				newBullet = Bullet(self.gs, math.pi/2, self)  #create new enemy bullet
				
				self.gs.bulletController.addBullet(newBullet)  #add it to bullets list
				self.gs.bulletNoise.play()
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
		
		self.ticks = 1  #counts number of ticks, used for timing
		
		self.enemies = []  #list of enemies
		self.rects = []  #2 dimensional array of rects to hold enemies
		self.filled = []  #2 dimensional array to keep track of which rects are filled
		
		width = 26  #width of all enemy sprites
		height = 31  #height of all enemy sprites
		
		startLeft = 25
		left = startLeft
		top = 100
		
		leftStep = 35
		topStep = 40
		
		for i in range(0, 3):  #instantiate rects array
			self.rects.append(list())
			self.filled.append(list())
			for j in range(0, 12):
				self.rects[i].append(pygame.Rect(left, top, width, height))  #create new rect and place in rects array
				left = left + leftStep  #incrment width
				self.filled[i].append(False)
			left = startLeft  #reset width to original width
			top = top + topStep  #increment height
		
		self.enemyAddFrequency = 120
	
		self.hspeed = 2
		
	def tick(self):  #animate all enemies on map
		nextEnemies = []
		newBullets = []
	
		for enemy in self.enemies:  #remove all enemies done exploding
			enemy.tick()			
		
			if not enemy.remove:  #enemy still alive or exploding
				nextEnemies.append(enemy)
			else:
				self.filled[enemy.row][enemy.col] = False  #free rect in filled array
				
		self.enemies = nextEnemies  #update enemies arrary
		
		if self.ticks % self.enemyAddFrequency == 0:  #allow for one enemy to be added
			row = randint(0, len(self.filled)-1)  #get random point in rects array, still need to make sure point is not already occupied
			col = randint(0, len(self.filled[0])-1)
			
			if self.filled[row][col] == False:  #only create enemy if random spot is free
				newEnemy = Enemy(row, col, self.gs, self)  #place enemy in random spot on rects array
				self.enemies.append(newEnemy)  #add new enemy to enemies list
				self.filled[row][col] = True
		
		for i, rectList in enumerate(self.rects):  #move all rects together
			for j, rect in enumerate(rectList):
				self.rects[i][j] = rect.move(self.hspeed, 0)
				
		if self.ticks % 130 == 0:  #reverse speed
			self.hspeed = -self.hspeed
			
		if self.enemyAddFrequency > 10 and self.ticks % 300 == 0:  #increase enemy add frequency
			self.enemyAddFrequency = self.enemyAddFrequency - 10
			
		self.ticks = self.ticks + 1  #increment ticks
				

	def blit(self):  #draw all enemies to screen
		for enemy in self.enemies:
			rect = self.rects[enemy.row][enemy.col]
			enemy.data.rect = rect
			self.gs.screen.blit(enemy.image, enemy.data.rect)
				
				

