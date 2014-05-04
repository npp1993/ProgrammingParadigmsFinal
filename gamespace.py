# Stephanie Tilden
# CSE 30332
# Pygame Primer
# Due April 16, 2013

import pygame
import math
import sys

from twisted.internet import protocol, reactor
from twisted.internet.defer import DeferredQueue

from work import *
from home import *

class GameSpace:
	def main(self):
		# basic initialization
		pygame.init()
		pygame.mixer.init()
		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size) 

		# set up game objects
		self.clock = pygame.time.Clock()
		self.player = Player(self)
		self.enemy = Enemy(self)

		# set repeat and initialize variables
		pygame.key.set_repeat(1,1)
		self.bullets = []
		self.exploding = False
		self.enemyExists = True

		# set up sounds
		self.laserNoise = pygame.mixer.Sound("screammachine.wav")
		self.explodeNoise = pygame.mixer.Sound("explode.wav")

		# start game loop 
		while 1:
			# clock tick regulation (framerate)
			self.clock.tick(60)

			# if exploding, play explodeNoise and go to next scene in explosion
			if self.exploding:
				self.enemy.explosion.tick()
				self.laserNoise.stop()
				self.explodeNoise.play()

			# event handler
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					self.player.move(event.key)
				elif event.type == pygame.QUIT:
					exit()
			
			# tick bullets, player, enemy
			for bullet in self.bullets:
				bullet.tick()

			self.player.tick()
			self.enemy.tick()

			# blit to screen
			self.screen.fill(self.black)
			for bullet in self.bullets:
				self.screen.blit(bullet.image, bullet.rect)
			self.screen.blit(self.player.image, self.player.rect)
			# if statement to only show enemy before explosion
			if self.enemyExists:
				self.screen.blit(self.enemy.image, self.enemy.rect)
			if self.exploding:
				self.screen.blit(self.enemy.explosion.image, self.enemy.explosion.rect)
	
			pygame.display.flip()


class Enemy(pygame.sprite.Sprite):
	def __init__(self, gs = None):
		pygame.sprite.Sprite.__init__(self)

		# initialize enemy sprite
		self.gs = gs
		self.image = pygame.image.load("globe.png")
		self.rect = self.image.get_rect()
		# place in bottom center of screen
		self.rect.center = (self.gs.width/2, self.gs.height)

		# initialize variables
		self.hspeed = 2
		self.hits = 0
		self.explosion = None

	def tick(self):
		# create bulletRects to check for collisions
		bulletRects = []
		for bullet in self.gs.bullets:
			bulletRects.append(bullet.rect)

		# if a bullet has collided, add 1
		if self.rect.collidelist(bulletRects) >= 0:
			self.hits +=1
		
		# if the enemy has been hit 130 times, make it red
		if self.hits == 130:
			self.image = pygame.image.load("globe_red100.png")

		# if the enemy has been hit 200 times, explode
		if self.hits == 200:
			self.explosion = Explosion(self.gs, self) # create explosion object
			self.gs.exploding = True

		# if the enemy hits the edge of the screen, begin moving in the opposite direction
		if self.rect.collidepoint(self.gs.width+20, self.gs.height) or self.rect.collidepoint(-20, self.gs.height):
			self.hspeed = -self.hspeed;

		# keeps the enemy moving back and forth
		self.rect = self.rect.move(self.hspeed, 0)


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


class Explosion(pygame.sprite.Sprite):
	def __init__(self, gs=None, enemy=None):
		pygame.sprite.Sprite.__init__(self)

		# initialize explosion
		self.gs = gs
		#self.delay = 100

		# initialize list of image names
		self.images = ["frames000a.png", "frames001a.png", "frames002a.png", "frames003a.png", "frames004a.png", "frames005a.png", "frames006a.png", "frames007a.png", "frames008a.png", "frames009a.png", "frames010a.png", "frames011a.png", "frames012a.png", "frames013a.png", "frames014a.png", "frames015a.png", "frames016a.png"]

		# initial image is the first image in the explosion
		self.i = 0
		self.imagePath = "explosion/" + self.images[self.i]
		self.image = pygame.image.load(self.imagePath)
		self.rect = self.image.get_rect()
		# place center at enemy's center
		self.enemy = enemy
		self.rect.center = self.enemy.rect.center

	def tick(self):
		# when the explosion occurs, the enemy no longer exists
		self.gs.enemyExists = False

		# add one to get the next image name in the sequence; if there is no next image, return
		self.i = self.i + 1
		if self.i>=len(self.images):
			self.gs.exploding = False
			return

		# load next image in sequence
		self.imagePath = "explosion/" + self.images[self.i]
		self.image = pygame.image.load(self.imagePath)
		self.rect = self.image.get_rect()
		self.rect.center = self.enemy.rect.center

if __name__ == '__main__':
	

	if player == "player1": # home
		home_connections = {}
		reactor.listenTCP(40061, home_CommandConnFactory())
		reactor.listenTCP(9001, home_ClientConnFactory())
		reactor.run()
	elif player == "player2": # work
		work_connections = {}
		reactor.connectTCP('student00.cse.nd.edu', 40061, work_CommandConnFactory())
		reactor.run()

	# play 
	gs = GameSpace()
	gs.main()


