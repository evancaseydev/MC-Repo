import pygame
from pygame.locals import *

pygame.init()

class City(pygame.sprite.Sprite):
    dead = False
    def __init__(self, location):
        self.location = location
        self.xCoord = location[0]
        self.yCoord = location[1]
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/city.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.xCoord, self.yCoord]
