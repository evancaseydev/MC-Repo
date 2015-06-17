import pygame
from pygame.locals import *

pygame.init()

availPowers = ["Missile +10", "ATOMIC BOMB", "Rapid Fire", "Huge Explosions", "Supersonic Missiles", "Flak Cannon"]

class Powerup(pygame.sprite.Sprite):
    def __init__(self, xpos, powertype, limit, bases):
        self.xpos = xpos
        self.ypos = 0
        self.powertype = availPowers[powertype]
        if self.powertype == "Missile +10" and bases == 3:
            self.powertype = "Missile +15"
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/powerup.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.xpos, self.ypos]
        self.limit = limit

    def update(self, powerups):
        self.ypos += 1
        self.rect.topleft = [self.xpos, self.ypos]
        if self.ypos > self.limit:
            powerups.remove(self)
        return (self.image, (self.xpos, self.ypos))
