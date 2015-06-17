import pygame, sys, random, MC_onebase, MC_threebase, Missile, Explosion, City, PointOrb
from pygame.locals import *

pygame.init()
pygame.font.init()

def highScores(DISPLAYSURF, myClock):
    fontObj = pygame.font.Font("Fonts/airstrikelaser.ttf", 60)
    smallfontObj = pygame.font.Font("Fonts/freesansbold.ttf", 40)
    highscores = open("Data/highscores.txt", "r")
    scores = highscores.readlines()
    highscores.close()
    if len(scores) == 0:
        startMenu()
    newstr = scores[0]
    scores = newstr.split(", ")
    scores.remove(scores[-1])
    for i in range(len(scores)):
        scores[i] = int(scores[i])
    scores = sorted(scores)[::-1]
    textList = []
    running = True
    printy = [200, 240, 280, 320, 360]
    title = fontObj.render("High Scores", True, (193, 2, 2))
    if len(scores) < 5:
        counter = len(scores)
    else:
        counter = 5

    ctrl = 0
    while ctrl < counter:
        textList.append(smallfontObj.render(str(ctrl + 1) + ": " + str(scores[ctrl]), True, (0, 0, 255)))
        ctrl += 1
        
    while running:
        DISPLAYSURF.fill((255, 255, 255))
        DISPLAYSURF.blit(title, (225, 100))
        for i in range(len(textList)):
            DISPLAYSURF.blit(textList[i], (220, printy[i]))
            
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                startMenu()

        myClock.tick(60)
        pygame.display.update()
        
def transition(DISPLAYSURF, index, explosions, cities, launchsites, powerups, missiles, height, width, score, possibleCoords, activePower, myClock, pointorbs):
    explosions[:] = []
    timer = 0
    interval = 12
    FPS = 55
    cities[:] = powerups[:] = launchsites[:] = missiles[:] = []
    fontObj = pygame.font.Font("Fonts/airstrike.ttf", 48)
    loading = fontObj.render("Loading...", True, (0, 0, 255))
    for i in range(250):
        DISPLAYSURF.fill((255, 255, 255))
        x = random.randrange(width)
        y = random.randrange(height)
        radius = random.randrange(5, 20)
        if timer % interval == 0:
            explosions.append(Explosion.Explosion((x, y), True, "norm", False, radius, cities, missiles, powerups, launchsites))

        for explosion in explosions:
            display = explosion.update(cities, missiles, powerups, launchsites, explosions, score, possibleCoords, activePower, pointorbs)
            pygame.draw.circle(DISPLAYSURF, display[0], display[1], display[2], display[3])

        DISPLAYSURF.blit(loading, (width / 2 - 100, height / 2))
        myClock.tick(FPS)
        pygame.display.update()
        timer += 1
            
    if index == 0:
        MC_onebase.play()
        pygame.quit()
        sys.exit()
    else:
        MC_threebase.play()
        pygame.quit()
        sys.exit()
    
class LaunchSite(pygame.sprite.Sprite):
    dead = False
    def __init__(self, location, numMissiles, height, width):
        self.xCoord = location[0]
        self.yCoord = location[1]
        self.location = location
        self.numMissiles = numMissiles
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/launchsite.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.xCoord, self.yCoord]
        self.height = height
        self.width = width
        
    def shoot(self, destination, superSonic, bigExplosions, variant, missiles, enemyspeed):
        self.numMissiles -= 1
        missiles.append(Missile.Missile(destination, (self.width / 2, self.height - 29), True, superSonic, bigExplosions, variant, enemyspeed))
     
def startMenu():
    SCREEN_SIZE = (800, 500)
    height = SCREEN_SIZE[1]
    width = SCREEN_SIZE[0]
    DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    pygame.display.set_caption("Missile Command")
    pygame.mouse.set_visible(True)
    bigfontObj = pygame.font.Font("Fonts/airstrikelaser.ttf", 72)
    fontObj = pygame.font.Font("Fonts/airstrike.ttf", 48)
    smallfontObj = pygame.font.Font("Fonts/airstrike.ttf", 18)
    FPS = 60
    myClock = pygame.time.Clock()
    options = ["One Base", "Three Bases", "High Scores"]
    index = 0
    tick = 0
    coolDown = 50
    cityXCoords = [50, 125, 200, 275, (width / 2) + 125 - (63 / 2) - 5, (width / 2) + 200 - (63 / 2) - 5, (width / 2) + 275 - (63 / 2) - 5, width - 50 - (63 / 2) - 5]
    cities = []
    missiles = []
    launchsites = []
    explosions = []
    powerups = []
    activePower = []
    pointorbs = []
    radius = [10]
    score = [0]
    for x in cityXCoords:
        cities.append(City.City((x, height - 27)))

    possibleCoords = cityXCoords[:]
    for i in range(len(possibleCoords)):
        possibleCoords[i] += 21
    possibleCoords.append((width / 2))
        
    WHITE = (255, 255, 255)
    NONBLUE = (5, 73, 231)
    SELBLUE = (10, 210, 226)
    SELORNG = (236, 71, 0)
    DEEPRED = (193, 2, 2)

    missileCommand = bigfontObj.render("MISSILE COMMAND", True, DEEPRED)

    launchsite = LaunchSite(((width / 2) - (63 / 2), height - 29), 10, height, width)
    launchsites.append(launchsite)
    while True:
        DISPLAYSURF.fill(WHITE)
        
        if index == 0:   
            ONEoptText = fontObj.render(options[0], True, SELORNG)
        else:
            ONEoptText = fontObj.render(options[0], True, NONBLUE)
            
        if index == 1:
            THREEoptText = fontObj.render(options[1], True, SELORNG)
        else:
            THREEoptText = fontObj.render(options[1], True, NONBLUE)

        if index == 2:
            HIGHoptText = fontObj.render(options[2], True, SELORNG)
        else:
            HIGHoptText = fontObj.render(options[2], True, NONBLUE)

        DISPLAYSURF.blit(launchsite.image, launchsite.location)

        if tick % 100 == 0:
            missiles.append(Missile.Missile((random.choice(possibleCoords), height - 7), (random.randrange(width), 0), False, False, False, 0, [1.5]))

        if tick % coolDown== 0 and not launchsite.dead:
            launchsite.shoot((random.randrange(width), random.randrange(height)), False, False, 0, missiles, [1.5, 10])
        
        for city in cities:
            DISPLAYSURF.blit(city.image, city.location)

        if random.randrange(500) == 1 and len(pointorbs) == 0:
            pointorbs.append(PointOrb.PointOrb(height, width))

        for missile in missiles:
            if not missile.done:
                display = missile.update(explosions, height, radius, cities, missiles, powerups, launchsites, possibleCoords)
                nomissilesleft = False
                pygame.draw.line(DISPLAYSURF, display[0], display[1], display[2], display[3])

        for explosion in explosions:
            display = explosion.update(cities, missiles, powerups, launchsites, explosions, score, possibleCoords, activePower, pointorbs)
            pygame.draw.circle(DISPLAYSURF, display[0], display[1], display[2], display[3])

        for orb in pointorbs:
            orb.update(pointorbs, DISPLAYSURF, height, width)

        DISPLAYSURF.blit(missileCommand, (35, 35))
        DISPLAYSURF.blit(ONEoptText, (width / 2 - 115, 210))
        DISPLAYSURF.blit(THREEoptText, (width / 2 - 160, 260))
        DISPLAYSURF.blit(HIGHoptText, (width / 2 - 145, 350))
        
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_UP:
                    if index == 0:
                        index = len(options) - 1
                    else:
                        index -= 1
                        
                if event.key == K_RIGHT or event.key == K_DOWN:
                    if index == len(options) - 1:
                        index = 0
                    else:
                        index += 1

                if event.key == K_RETURN:
                    if index == 0 or index == 1:
                        transition(DISPLAYSURF, index, explosions, cities, launchsites, powerups, missiles, height, width, score, possibleCoords, activePower, myClock, pointorbs)
                    else:
                        highScores(DISPLAYSURF, myClock)
                        
        if launchsite.dead:
            alive = False
            for city in cities:
                if not city.dead:
                    alive = True
            if not alive:
                cities[:] = []
                missiles[:] = []
                explosions[:] = []
                launchsites[:] = []
                pointorbs[:] = []
                launchsite = LaunchSite(((width / 2) - (63 / 2), height - 29), 10, height, width)
                launchsites.append(launchsite)
                possibleCoords = cityXCoords[:]
                for i in range(len(possibleCoords)):
                    possibleCoords[i] += 21
                possibleCoords.append((width / 2))

                for x in cityXCoords:
                    cities.append(City.City((x, height - 27)))
            
        myClock.tick(FPS)
        pygame.display.update()
        tick += 1

startMenu()
