# Author:       Nathaniel Pawelczyk
# File:         main.py
# CSE 30332

import pygame
import math

class Player(pygame.sprite.Sprite):
        def __init__(self, gs=None):
                pygame.sprite.Sprite.__init__(self)
                
                self.gs = gs
                self.image = pygame.image.load("media/deathstar.png")
                self.rect = self.image.get_rect()
                self.rect.centerx = 51
                self.rect.centery = 51
                self.laser_sound = pygame.mixer.Sound("screammachine.wav")
                
                self.lasers = set()  # array of laser objects the player has shot
                self.nextlasers = set()
                
                self.dx = 0
                self.dy = 0
                
                self.angle = 0
                
                self.image_w, self.image_h = self.image.get_size()
                
                # keep original image to limit resize errors
                self.orig_image = self.image
                
                # if I can fire laser beams, this flag will say
                # whether I should be firing them /right now/
                self.tofire = False

        def tick(self):
                # get the mouse x and y position on the screen
                mx, my = pygame.mouse.get_pos()

                xdiff = mx - self.rect.centerx
                ydiff = my - self.rect.centery
                                                
                self.angle = -math.atan2(ydiff, xdiff)
                
                self.image = pygame.transform.rotate(self.orig_image, math.degrees(self.angle)-40)

                
                # this conditional prevents movement while firing
                if self.tofire == True:
                        laserx = self.rect.centerx + self.image_w/2 * math.cos(self.angle)
                        lasery = self.rect.centery + self.image_w/2 * -math.sin(self.angle)

                        laserdx = 5.0 * math.cos(self.angle)
                        laserdy = 5.0 * -math.sin(self.angle)
                                     
                        self.lasers.add(Laser(laserx, lasery, laserdx, laserdy, self.gs))
                        
                        self.laser_sound.play()
                else:
                        if self.rect.left >= 0 and self.rect.right <= self.gs.width:
                                self.rect.centerx += self.dx

                                if self.rect.left < 0:
                                        self.rect.left = 0
                                elif self.rect.right > self.gs.width:
                                        self.rect.right = self.gs.width
                                
                        if self.rect.top >= 0 and self.rect.bottom <= self.gs.height:
                                self.rect.centery += self.dy

                                if self.rect.top < 0:
                                        self.rect.top = 0
                                elif self.rect.bottom > self.gs.height:
                                        self.rect.bottom = self.gs.height
                        
        def draw(self):
        
                for laser in self.lasers:
                        laser.tick()
                        laser.draw()

                self.lasers = self.nextlasers
                self.nextlasers = set()
                
                self.gs.screen.blit(self.image, self.rect)

class Laser(pygame.sprite.Sprite):
        def __init__(self, x, y, xvel, yvel, gs=None):
                pygame.sprite.Sprite.__init__(self)

                self.gs = gs
                self.image = pygame.image.load("media/laser.png")
                self.rect = self.image.get_rect()
                
                self.rect.centerx = x  #position
                self.rect.centery = y
                self.dx = xvel  #x and y velocities
                self.dy = yvel
                
        def tick(self):
                self.rect.centerx += self.dx
                self.rect.centery += self.dy

                if math.hypot(self.rect.centerx - self.gs.planet.rect.centerx, self.rect.centery - self.gs.planet.rect.centery) < 190:  #radius of globe
                        self.gs.planet.health -= 1
                else:
                        self.gs.player.nextlasers.add(self)
        def draw(self):
                self.gs.screen.blit(self.image, self.rect)
                        
class Planet(pygame.sprite.Sprite):
        def __init__(self, gs=None):
                pygame.sprite.Sprite.__init__(self)

                self.gs = gs
                self.image = pygame.image.load("media/globe.png")
                self.rect = self.image.get_rect()
                self.explosion_sound = pygame.mixer.Sound("media/explode.wav")
                
                self.x = 330
                self.y = 300
                
                self.health = 100

                self.i = 0

                self.frames = ["000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015", "016"]

                self.rect.move_ip(self.x, self.y)

        def tick(self):
                if self.health == 0:
                        self.explosion_sound.play()
                        self.health -= 1
                
                if self.i < 16:
                        if self.health <= 0:
                                self.image = pygame.image.load("media/explosion/frames" + self.frames[self.i]+ "a.png")
                                self.i += 1
                        elif self.health <= 50:
                                self.image = pygame.image.load("media/globe_red100.png")
                else:
                        self.image = pygame.Surface((1, 1))

                        
                
        def draw(self):
                self.gs.screen.blit(self.image, self.rect)
                        
class GameSpace:
        def main(self):
                pygame.init()
                self.size = self.width, self.height = 640, 480
                self.black = 0, 0, 0
                self.screen = pygame.display.set_mode(self.size)
                
                self.clock = pygame.time.Clock()
                
                self.player = Player(self)
                self.planet = Planet(self)

                run = True
                
                while run:
                        self.clock.tick(60)  #set framerate
                
                        # 5) this is where you would handle user inputs...
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        run = False
                                elif event.type == pygame.MOUSEBUTTONUP:
                                        self.player.tofire = False
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                        self.player.tofire = True
                                if event.type == pygame.KEYDOWN:
                                        if (event.key == pygame.K_LEFT):
                                                self.player.dx = -1
                                        if (event.key == pygame.K_RIGHT):
                                                self.player.dx = 1
                                        if (event.key == pygame.K_UP):
                                                self.player.dy = -1
                                        if (event.key == pygame.K_DOWN):
                                                self.player.dy = 1
                                elif event.type == pygame.KEYUP:
                                        if (event.key == pygame.K_LEFT):
                                                self.player.dx = 0
                                        if (event.key == pygame.K_RIGHT):
                                                self.player.dx = 0
                                        if (event.key == pygame.K_UP):
                                                self.player.dy = 0
                                        if (event.key == pygame.K_DOWN):
                                                self.player.dy = 0
                                        
                
                        self.player.tick()  #send tick to player
                        self.planet.tick()  #send tick to planet
                
                        # 7) and finally, display the game objects
                        self.screen.fill(self.black)  #black out screen
                        
                        self.player.draw()  #player draws itself
                        self.planet.draw()  #planet draws itself
                        
                        pygame.display.flip()  #flip animation buffers


                pygame.quit()
                
if __name__ == '__main__':
        gs = GameSpace()
        gs.main()
