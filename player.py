# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# player.py provides player functionality

import pygame
import math
from datetime import datetime

from bullet import *

class PlayerController():
	def __init__(self, gs):
		self.gs = gs
	
		self.player1 = Player(self)
		self.player2 = Player(self)
		
		self.data.image = pygame.image.load("media/galaga_spaceship.png")
		
	def tick(self):
		self.player1.tick()
		self.player2.tick()
		
class PlayerData():
	def __init__(self):  #class to hold data about enemy position and appearance
		self.data.rect = None
		self.exploding = False
		self.data.i = 1
		self.exploding = False
		self.remove = False

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, controller)
		
		self.data = PlayerData()  #instantiate player data
		self.data.rect = self.controller.image.get_rect()
		
		# place at bottom right of screen
		self.data.rect.center = (self.gs.width-50, self.gs.height-50)

		# initialize variables
		self.tofire = False
		self.speed = 0
		self.hspeed = 9
		self.vspeed = 3
		
		self.bulletLastFiredAt = datetime.now()  #used to limit rate of bullet fire
		
	def blit(self):    #display player
		if not self.remove:
			self.controller.gs.screen.blit(self.image, self.data.rect)

	def tick(self):
		self.data.rect = self.data.rect.move(self.speed, 0)  #move the ship

		if not self.data.exploding:
			if self.tofire == True:
				currentTime = datetime.now()  #get current time
			
				timeDiff = currentTime - self.bulletLastFiredAt  #get time since last bullet was fired
			
				if (timeDiff.seconds*1000000) + timeDiff.microseconds > 500000:  #allow for one bullet to be fired every 0.5 seconds
					self.bulletLastFiredAt = currentTime  #update time that last bullet was fired
				
					newBullet = Bullet(self.controller.gs, -math.pi/2)  #create new bullet
				
					if hasattr(self.controller.gs, "bulletController"):  #if player is server
						self.controller.gs.bulletController.addBullet(newBullet)  #add it to bullets list
				
					self.controller.gs.bulletNoise.play()
			
					return newBullet
			
				bullets = []
			
			if hasattr(self.controller.gs, "bulletController"):  #get all bullets from gamespace
				bullets = self.gs.bulletController.bullets
			else:
				bullets = self.gs.bullets
				
			for bullet in bullets:  #checks for any bullets that have hit this player
				if bullet.enemy and self.data.rect.colliderect(bullet.rect):
					bullet.remove = True
					self.exploding = True
					return
		else:
			# add one to get the next image name in the sequence; if there is no next image, return
			if self.data.i == 15:
				self.remove = True  #flag explosion for removal from enemies list
				return
			
			imagePath = "media/explosion/galaga_enemy1_explosion" + str(self.data.i) + ".png"
			self.data.image = pygame.image.load(imagePath)
			
			self.data.i = self.data.i + 1  #increment explosion sequence image counter
			
		self.tofire = False

	def move(self, event):  #only want 2-dimensional motion
		# handle key events to move player and fire
		if event.type == pygame.KEYDOWN:
                        if (event.key == pygame.K_RIGHT):
				self.speed = self.hspeed
                        elif (event.key == pygame.K_LEFT):
				self.speed = -self.hspeed
                        if (event.key == pygame.K_SPACE):
				self.tofire = True;
                if event.type == pygame.KEYUP:
                        if (event.key == pygame.K_RIGHT):
                                self.speed = 0
                        elif (event.key == pygame.K_LEFT):
                                self.speed = 0

		
		#if key == pygame.K_UP:
		#	self.data.rect = self.data.rect.move(0, -self.vspeed)
		#elif key == pygame.K_DOWN:
		#	self.data.rect = self.data.rect.move(0, self.vspeed)

