# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# player.py provides player functionality

import pygame
import math
from datetime import datetime

from bullet import *

class Player(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)

		# initialize and load images
		self.gs = gs
		self.image = pygame.image.load("media/galaga_spaceship.png")
		self.rect = self.image.get_rect()
		# place at bottom right of screen
		self.rect.center = (self.gs.width-50, self.gs.height-50)

		self.angle = 0
		self.orig_image = self.image

		# initialize variables
		self.tofire = False
		self.speed = 0
		self.hspeed = 9
		self.vspeed = 3
		
		self.exploding = False
		self.remove = False
		
		self.i = 1
		
		self.bulletLastFiredAt = datetime.now()
		
	def blit(self):
		if not self.remove:
			self.gs.screen.blit(self.image, self.rect)  #display local player

	def tick(self):
		if not self.exploding:
			self.rect = self.rect.move(self.speed, 0)  #move the ship
		
			if self.tofire == True:
				currentTime = datetime.now()  #get current time
			
				timeDiff = currentTime - self.bulletLastFiredAt  #get time since last bullet was fired
			
				if (timeDiff.seconds*1000000) + timeDiff.microseconds > 500000:  #allow for one bullet to be fired every 0.5 seconds
					self.bulletLastFiredAt = currentTime  #update time that last bullet was fired
				
					newBullet = Bullet(self.gs, -math.pi/2)  #create new bullet
					newBullet.id = self.gs.id
				
					if self.gs.id == "server":  #if player is server
						self.gs.bulletController.addBullet(newBullet)  #add it to bullets list
				
					self.gs.bulletNoise.play()
			
					return newBullet
			
			bullets = []
			
			if self.gs.id == "server":  #get all bullets from gamespace
				bullets = self.gs.bulletController.bullets
			else:
				bullets = self.gs.bullets
				
			for bullet in bullets:  #checks for any bullets that have hit this player
				if bullet.enemy and self.rect.colliderect(bullet.rect):
					self.exploding = True
					return
		else:
			# add one to get the next image name in the sequence; if there is no next image, return
			if self.i == 15:
				self.remove = True  #flag explosion for removal from enemies list
				return
			
			imagePath = "media/explosion/galaga_enemy1_explosion" + str(self.i) + ".png"
			self.image = pygame.image.load(imagePath)
			
			self.i = self.i + 1  #increment explosion sequence image counter
			
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
		#	self.rect = self.rect.move(0, -self.vspeed)
		#elif key == pygame.K_DOWN:
		#	self.rect = self.rect.move(0, self.vspeed)

