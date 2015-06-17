import pygame, random, sys, math, time, Vector, City, Powerup, Explosion, Missile, PointOrb
from pygame.locals import *

pygame.init()
pygame.font.init()

def shop(DISPLAYSURF, myClock, coefficient, shootCooldown, radius, enemyspeed, launchAmmo, score, prices, duration):
    running = True
    fontObj = pygame.font.Font("Fonts/airstrikelaser.ttf", 60)
    smallfontObj = pygame.font.Font("Fonts/freesansbold.ttf", 40)
    options = ["Missile Speed +", "Explosion Size +", "Firing Speed +", "Starting Missiles +", "Powerup Duration +"]
    textList = []
    priceText = []
    printy = [200, 240, 280, 320, 360, 400]
    title = fontObj.render("SHOP", True, (193, 2, 2))
    index = 0
    ammoplus = 10
    timePlus = 30

    SELBLUE = (10, 210, 226)
    NONBLUE = (5, 73, 231)
    SELORNG = (236, 71, 0)

    for i in range(len(options)):
        textList.append(smallfontObj.render(options[i], True, NONBLUE))
        priceText.append(smallfontObj.render(str(prices[i]), True, SELBLUE))
    
    while running:
        good = False
        scoreText = fontObj.render(str(score[0]), True, NONBLUE)
        DISPLAYSURF.fill((255, 255, 255))
        DISPLAYSURF.blit(title, (135, 100))
        DISPLAYSURF.blit(scoreText, (5, 0))
        textList[index] = smallfontObj.render(str(options[index]), True, SELORNG)
        for i in range(len(textList)):
            DISPLAYSURF.blit(textList[i], (110, printy[i]))
            DISPLAYSURF.blit(priceText[i], (10, printy[i]))
            
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_UP:
                    if index == 0:
                        index = len(options) - 1
                    else:
                        index -= 1
                if event.key == K_LEFT or event.key == K_DOWN:
                    if index == len(options) - 1:
                        index = 0
                    else:
                        index += 1
                if event.key == K_RETURN:
                    if prices[index] <= score[0]:
                        score[0] -= prices[index]
                        good = True
                    if index == 0 and good:
                        enemyspeed[1] *= coefficient
                        prices[index] *= coefficient
                        prices[index] = int(prices[index])
                    elif index == 1 and good:
                        radius[0] *= coefficient
                        prices[index] *= coefficient
                        prices[index] = int(prices[index])
                        radius[0] = int(radius[0])
                    elif index == 2 and good and shootCooldown[0] > 10:
                        shootCooldown[0] -= 5
                        prices[index] *= coefficient
                        prices[index] = int(prices[index])
                    elif index == 2 and not shootCooldown[0] > 10:
                        score[0] += prices[index]
                    elif index == 3 and good:
                        launchAmmo[0] += ammoplus
                        prices[index] *= coefficient
                        prices[index] = int(prices[index])
                    elif index == 4 and good:
                        duration[0] += timePlus
                        prices[index] *= coefficient
                        prices[index] = int(prices[index])
                    
        textList[:] = []
        priceText[:] = []
        for i in range(len(options)):
            textList.append(smallfontObj.render(options[i], True, NONBLUE))
            priceText.append(smallfontObj.render(str(prices[i]), True, SELBLUE))
        
        myClock.tick(60)
        pygame.display.update()


def enemyFire(possible, variant, missiles, height, width, enemyspeed):
    missiles.append(Missile.Missile((random.choice(possible), height - 5), (random.randrange(width), 0), False, False, False, variant, enemyspeed))
    
class LaunchSite(pygame.sprite.Sprite):
    dead = False
    def __init__(self, location, numMissiles, height):
        self.xCoord = location[0]
        self.yCoord = location[1]
        self.location = location
        self.numMissiles = numMissiles
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/launchsite.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.xCoord, self.yCoord]
        self.height = height
        
    def shoot(self, destination, superSonic, bigExplosions, variant, missiles, enemyspeed):
        self.numMissiles -= 1
        missiles.append(Missile.Missile(destination, (251, self.height - 29), True, superSonic, bigExplosions, variant, enemyspeed))
     
def play():
    SCREEN_SIZE = (500, 500)
    height = SCREEN_SIZE[1]
    width = SCREEN_SIZE[0]
    DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    pygame.display.set_caption("Missile Command")
    pygame.mouse.set_visible(True)
    fontObj = pygame.font.Font("Fonts/freesansbold.ttf", 30)
    smallfontObj = pygame.font.Font("Fonts/freesansbold.ttf", 18)

    FPS = 60
    myClock = pygame.time.Clock()
    shootCooldown = 50
    origCooldown = 50
    powercooldown = 0
    tick = shootCooldown
    counter = 0
    rapidCool = 5
    missileTimer = 75
    missilesToFire = 10
    missilesFired = 0
    score = [0]
    launchAmmo = 15
    levelCount = 0
    enemyspeed = [1, 10]
    supersonic = bigexplosions = rapid = flak = False
    prices = [750, 500, 400, 450, 500]
    duration = 300

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    cityXCoords = [25, 75, 125, 250 + 125 + 63, 250 + 75 + 63, 250 + 25 + 63]
    launchx = (width / 2) - (63 / 2)
    launchy = height - 29

    missiles = []
    launchsites = []
    cities = []
    explosions = []
    powerups = []
    pointorbs = []
    radius = [10]
    availPowers = ["Missile +10", "ATOMIC BOMB", "Rapid Fire", "Huge Explosions", "Supersonic Missiles", "Flak Cannon"]
    possibleCoords = cityXCoords[:]
    for i in range(len(possibleCoords)):
        possibleCoords[i] += 21
                
    possibleCoords.append(launchx + (63 / 2))
    activePower = []

    launchsite = LaunchSite((launchx, launchy), launchAmmo, height)
    launchsites.append(launchsite)
    gameover = fontObj.render("GAME OVER", True, RED)
    nextlevel = fontObj.render("LEVEL 1", True, BLUE)

    for x in cityXCoords:
        cities.append(City.City((x, launchy + 2)))
        
    while True:
        rad = 0
        if tick > shootCooldown:
            rad = 5
        nomissilesleft = True
        variant = 0

        if levelCount >= 2:
            if random.randrange(20) == 1:
                variant = 1

        if powercooldown == 0:
            supersonic = bigexplosions = rapid = flak = False
            
        missilesLeft = fontObj.render(str(launchsite.numMissiles), True, RED)
        scoreText = fontObj.render(str(score[0]), True, BLUE)
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(launchsite.image, launchsite.location)
        DISPLAYSURF.blit(missilesLeft, (width - (20 * len(str(launchsite.numMissiles))), 0))
        DISPLAYSURF.blit(scoreText, (0, 0))
        pygame.draw.circle(DISPLAYSURF, RED, (launchsite.rect.center[0] + 1, launchsite.rect.center[1]), rad, 0)

        if powercooldown > 0:
            if powercooldown <= 254:
                color = powercooldown
            else:
                color = 255
            pygame.draw.circle(DISPLAYSURF, (0, color, 0), (width / 2, 11), 10, 0)

            
        if random.randrange(500) == 1 and len(powerups) == 0 and powercooldown == 0:  
            powerups.append(Powerup.Powerup(random.randrange(width - 20), random.randrange(0, len(availPowers)), height, 1))

        if random.randrange(1250) == 1 and len(pointorbs) == 0:
            pointorbs.append(PointOrb.PointOrb(height, width))

        for power in activePower:
            powercooldown = duration
            powertext = fontObj.render(power + "!", True, GREEN)
            if power == "Supersonic Missiles":
                supersonic = True
            elif power == "Missile +10":
                launchsite.numMissiles += 10
            elif power == "ATOMIC BOMB":
                explosions.append(Explosion.Explosion((width / 2, height / 2), True, "nuke", False, radius[0], cities, missiles, powerups, launchsites))
                score[0] += 100
            elif power == "Huge Explosions":
                bigexplosions = True
            elif power == "Rapid Fire":
                rapid = True
            elif power == "Flak Cannon":
                flak = True
            activePower.remove(power)

        if counter % missileTimer == 0 and not missilesFired == missilesToFire:
            enemyFire(possibleCoords, variant, missiles, height, width, enemyspeed)
            missilesFired += 1
            
        for city in cities:
            DISPLAYSURF.blit(city.image, city.location)

        if flak and random.randrange(20) == 1:
            explosions.append(Explosion.Explosion((random.randrange(10, width - 10), random.randrange(10, height - 50)), True, "norm", False, radius[0], cities, missiles, powerups, launchsites))
            explosions[-1].growthTime += 10
            
        for missile in missiles:
            if not missile.done:
                display = missile.update(explosions, height, radius, cities, missiles, powerups, launchsites, possibleCoords)
                nomissilesleft = False
                pygame.draw.line(DISPLAYSURF, display[0], display[1], display[2], display[3])
                    
        for explosion in explosions:
            display = explosion.update(cities, missiles, powerups, launchsites, explosions, score, possibleCoords, activePower, pointorbs)
            pygame.draw.circle(DISPLAYSURF, display[0], display[1], display[2], display[3])

        for power in powerups:
            display = power.update(powerups)
            DISPLAYSURF.blit(display[0], display[1])

        for orb in pointorbs:
            orb.update(pointorbs, DISPLAYSURF, height, width)

        if powercooldown > 225:
            DISPLAYSURF.blit(powertext, ((width / 2) - 100, (height / 2)))
        
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                outfile = open("Data/highscores.txt", "a")
                outfile.write(str(score[0] * (levelCount + 1)) + ", ")
                outfile.close()
                import MainMenu
                MainMenu.startMenu()
            if event.type == pygame.MOUSEBUTTONDOWN and not rapid:
                pos = pygame.mouse.get_pos()
                if not launchsite.numMissiles == 0 and tick > shootCooldown and not launchsite.dead:
                    launchsite.shoot(pos, supersonic, bigexplosions, 0, missiles, enemyspeed)
                    tick = 0

        if rapid and tick % rapidCool == 0:
            launchsite.shoot(pygame.mouse.get_pos(), supersonic, bigexplosions, 0, missiles, enemyspeed)
            launchsite.numMissiles += 1
            
        if launchsite.dead:
            deadCount = 0
            for city in cities:
                if city.dead:
                    deadCount += 1
            if deadCount == len(cities):
                finalscore = fontObj.render("Score: " + str(score[0] * (levelCount + 1)), True, RED)
                time.sleep(3)
                DISPLAYSURF.fill(BLACK)
                DISPLAYSURF.blit(gameover, (width / 2 - 85, (height / 2) - 35))
                DISPLAYSURF.blit(finalscore, (width / 2 - 85, height / 2))
                pygame.display.update()
                time.sleep(3)
                outfile = open("Data/highscores.txt", "a")
                outfile.write(str(score[0] * (levelCount + 1)) + ", ")
                outfile.close()
                import MainMenu
                MainMenu.startMenu()

        if missilesFired == missilesToFire and nomissilesleft and len(explosions) == 0:
            time.sleep(2)
            levelCount += 1
            viewscores = True
            aliveCount = 0
            launchsite.dead = False
            for city in cities:
                if not city.dead:
                    aliveCount += 1

            citybonus = smallfontObj.render("Cities Alive:  " + str(aliveCount), True, BLUE)
            missilesbonus = smallfontObj.render("Missiles Left: " + str(launchsite.numMissiles), True, BLUE)
            finalbonus = smallfontObj.render("Bonus: " + str(aliveCount * 50) + " + " + str(launchsite.numMissiles * 5) + " = " + str((launchsite.numMissiles * 5) + (aliveCount * 50)), True, BLUE)
            nextlevel = fontObj.render("LEVEL " + str(levelCount), True, BLUE)

            powercooldown = 0
            supersonic = bigexplosions = rapid = False
            shootCooldown = origCooldown
            score[0] += (aliveCount * 50)
            score[0] += (launchsite.numMissiles * 5)
            cities[:] = []
            missiles[:] = []
            explosions[:] = []
            powerups[:] = []
            activePower[:] = []
            launchsites[:] = []
            pointorbs[:] = []
            possibleCoords[:] = cityXCoords
            for x in cityXCoords:
                cities.append(City.City((x, launchy + 2)))

            for i in range(len(possibleCoords)):
                possibleCoords[i] += 21
            possibleCoords.append(launchx + (63 / 2))

            while viewscores:
                DISPLAYSURF.fill((255, 255, 255))
                DISPLAYSURF.blit(nextlevel, ((width / 2) - 85, (height / 2) - 80))
                DISPLAYSURF.blit(citybonus, ((width / 2) - 85, (height / 2) - 40))
                DISPLAYSURF.blit(missilesbonus, ((width / 2) - 85, (height / 2) - 20))
                DISPLAYSURF.blit(finalbonus, ((width / 2) - 85, (height / 2)))
                for event in pygame.event.get():
                    if event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        viewscores = False
                myClock.tick(FPS)
                pygame.display.update()

            shootCooldown = [shootCooldown]
            launchAmmo = [launchAmmo]
            duration = [duration]
            shop(DISPLAYSURF, myClock, 1.2, shootCooldown, radius, enemyspeed, launchAmmo, score, prices, duration)
            launchAmmo = launchAmmo[0]
            shootCooldown = shootCooldown[0]
            duration = duration[0]
            
            missilesFired  = 0
            missilesToFire = int(1.3 * float(missilesToFire))
            launchAmmo = int(1.2 * float(launchAmmo))
            launchsite = LaunchSite((launchx, launchy), launchAmmo, height)
            launchsites.append(launchsite)
            if levelCount % 2 == 0: # every other level enemy missile speed increases
                enemyspeed[0] += .5
            if levelCount % 3 == 0 and missileTimer >= 45: # every second level enemy missile frequency increases
                missileTimer -= 5

            pygame.display.update()
            
        if powercooldown > 0:
            powercooldown -= 1
        tick += 1
        counter += 1
        myClock.tick(FPS)
        pygame.display.update()

           

