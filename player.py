# Nathaniel Pawelczyk & Stephanie Tilden
# CSE 30332
# Pygame + Twisted Final Project
# Due May 7, 2014

# player.py provides player functionality

import pygame
import math

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
		self.hspeed = 3
		self.vspeed = 3

	def tick(self):
		#mx, my = pygame.mouse.get_pos()
		#px = self.rect.centerx
		#py = self.rect.centery
		# calculate angle to rotate & shoot bullet
		#self.angle = -math.atan2(my-py, mx-px)
		
		self.rect = self.rect.move(self.speed, 0)


		# create new bullet and add to bullets[]
		if self.tofire == True:
			#self.gs.laserNoise.play()
			newBullet = Bullet(self.gs, math.pi/2)
			self.gs.bullets.append(newBullet)
			self.tofire = False
			
			return newBullet
		else:
			# rotate image to face mouse
			#self.angle = math.degrees(self.angle) - 30
			#self.image = pygame.transform.rotate(self.orig_image, self.angle)
			#rotate_rect = self.image.get_rect()
			#rotate_rect.center = self.rect.center
			#self.rect = rotate_rect
			
			return None

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

