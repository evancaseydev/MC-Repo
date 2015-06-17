import pygame, random
from pygame.locals import *

pygame.init()

class Explosion(pygame.sprite.Sprite):
    growthRate = 7  #smaller is faster
    growthTime = 18  #number of times radius will increment
    origTime = growthTime
    incr = 1
    increasing = True
    tick = 0
    score = 0
    def __init__(self, pos, friendly, variation, big, radius, cities, missiles, powerups, launchsites):
        self.pos = pos
        self.friendly = friendly
        self.image = pygame.image.load("Images/explosion.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        if variation == "nuke":
            self.radius = 100
            self.growthRate = 1
            self.growthTime = 100
        self.variation = variation
        self.radius = radius
        if big:
            self.radius = radius * 2
        self.cities = cities
        self.powerups = powerups
        self.launchsites = launchsites
        self.missiles = missiles

    def collisionCheck(self, score, possibleCoords, activePower, cities, missiles, powerups, launchsites, explosions, radius, pointorbs):
        for city in cities:
            if self.rect.colliderect(city) and not self.friendly:
                city.image = pygame.image.load("Images/city_dest.png").convert_alpha()
                city.dead = True
                if city.xCoord + 21 in possibleCoords:
                    possibleCoords.remove(city.xCoord + 21)
                
        for missile in missiles:
            if self.rect.colliderect(missile) and not missile.friendly and not missile.done:
                missile.done = True
                if missile.addToScore:
                   score[0] += 10 
                missile.addToScore = False
                if self.variation == "norm":
                    explosions.append(Explosion((int(missile.trueX), int(missile.trueY)), True, "norm", False, radius[0], cities, missiles, powerups, launchsites))
                
        for power in powerups:
            if self.rect.colliderect(power) and self.friendly:
                activePower.append(power.powertype)
                self.powerups.remove(power)
                score[0] += 100

        for site in launchsites:
            if self.rect.colliderect(site) and not self.friendly:
                site.dead = True
                site.image = pygame.image.load("Images/launchsitedead.png").convert_alpha()
                if site.xCoord + (63 / 2) in possibleCoords:
                    possibleCoords.remove(site.xCoord + (63 / 2))

        for orb in pointorbs:
            if self.rect.colliderect(orb) and self.friendly:
                score[0] += 200
                pointorbs.remove(orb)
                explosions.append(Explosion((int(orb.xCoord + 5), int(orb.yCoord + 5)), True, "norm", False, radius[0] + 5, cities, missiles, powerups, launchsites))


        
    def update(self, cities, missiles, powerups, launchsites, explosions, score, possibleCoords, activePower, pointorbs):
        self.rect = Rect(self.pos[0] - self.radius - 1, self.pos[1] - self.radius - 1, self.radius * 2, self.radius * 2)

        self.collisionCheck(score, possibleCoords, activePower, cities, missiles, powerups, launchsites, explosions, [self.radius], pointorbs)
        
        if self.radius == 0:
            explosions.remove(self)
            if self.variation == "nuke":
                missiles[:] = []
                explosions[:] = []

        if self.growthTime == self.origTime / 2:
            self.increasing = False
            if self.variation != "nuke":
                self.growthRate -= 1

        self.tick += 1
        if self.tick % self.growthRate == 0 and self.increasing:
            self.radius += self.incr
            self.growthTime -= 1
        elif self.tick % self.growthRate == 0 and not self.increasing and not self.radius == 0:
            self.radius -= self.incr
            self.growthTime -= 1
            
        return ((random.randrange(70, 250), 10, random.randrange(50, 200)), self.pos, self.radius, 0)

