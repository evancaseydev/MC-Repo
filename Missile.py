import pygame, Vector, Explosion, random
from pygame.locals import *

pygame.init()

class Missile(pygame.sprite.Sprite):
    addToScore = True
    done = False
    width = 1
    def __init__(self, pos, start, friendly, superSonic, bigExplosions, variant, enemyspeed):
        self.image = pygame.image.load("Images/missile.png").convert_alpha() # load image
        self.rect = self.image.get_rect()
        self.trueX = start[0]
        self.trueY = start[1]
        self.rect.center = (self.trueX, self.trueY)
        if friendly:
            self.speed = enemyspeed[1]
        else:
            self.speed = enemyspeed[0]
            
        if superSonic and friendly:
            self.speed = 30
            
        if pos[1] > 450 and friendly:
            pos = list(pos)
            pos[1] = 450
            
        self.target = pos
        self.friendly = friendly
        self.start = start
        if friendly:
            self.color = (0, 0, 255)
        else:
            self.color = (255, 0, 0)
        self.big = bigExplosions
        self.variant = variant
        if variant == 1:
            self.width = 2
            self.speed = .5
        self.enemyspeed = enemyspeed

    def get_direction(self, target):
        if self.target:
            position = Vector.Vector(self.rect.centerx, self.rect.centery) 
            target = Vector.Vector(target[0], target[1]) 
            self.dist = target - position 

            direction = self.dist.normalize() 
            return direction
        
    def distance_check(self, dist):
        dist_x = dist[0] ** 2
        dist_y = dist[1] ** 2 
        t_dist = dist_x + dist_y 
        speed = self.speed ** 2 

        if t_dist < (speed): 
            return True

    def update(self, explosions, height, radius, cities, missiles, powerups, launchsites, possibleCoords):
        self.dir = self.get_direction(self.target)
        if self.dir: 
            if self.distance_check(self.dist): 
                self.rect.center = self.target 
                
            else: 
                self.trueX += (self.dir[0] * self.speed) 
                self.trueY += (self.dir[1] * self.speed)
                self.rect.center = (round(self.trueX),round(self.trueY))

        if self.variant == 1:
            self.color = (random.randrange(200), 0, 0)
            
        if list(self.rect.center) == list(self.target):
            explosions.append(Explosion.Explosion(self.target, self.friendly, "norm", self.big, radius[0], cities, missiles, powerups, launchsites))
            self.done = True
            missiles.remove(self)

        if self.variant == 1 and self.trueY > height / 3:
            self.speed = 0
            choices = []
            poss = random.choice(possibleCoords)
            numMirv = 3
            if len(possibleCoords) < 3:
                numMirv = len(possibleCoords)
            for i in range(numMirv):
                while poss in choices:
                    poss = random.choice(possibleCoords)
                choices.append(poss)
                missiles.append(Missile((poss, height - 5), (self.trueX, self.trueY), False, False, False, 0, self.enemyspeed))
            missiles.remove(self)

        return (self.color, (self.start[0], self.start[1]), self.rect.topleft, self.width)

