import pygame, random
from pygame.locals import *

pygame.init()

class PointOrb(pygame.sprite.Sprite):
    def __init__(self, height, width):
        self.xCoord = random.choice([-18, width])
        if self.xCoord == -18:
            self.increasing = True
        else:
            self.increasing = False
        self.yCoord = random.randrange(25, height / 2)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/pointOrb.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.xCoord, self.yCoord]

    def update(self, pointorbs, DISPLAYSURF, height, width):
        if self.increasing:
            self.xCoord += 1
        else:
            self.xCoord -= 1

        if self.increasing and self.xCoord > width:
            pointorbs.remove(self)
        elif not self.increasing and self.xCoord < -18:
            pointorbs.remove(self)
            
        self.rect.topleft = [self.xCoord, self.yCoord]
        DISPLAYSURF.blit(self.image, (self.xCoord, self.yCoord))

