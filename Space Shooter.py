import pygame, sys
import time
import random

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS',25)
bossFont = pygame.font.SysFont('Comic Sans MS', 150)
#Variables ===============================================
screenWidth = 1920
screenHeight = 1080
screenCenterX = screenWidth//2
screenCenterY = screenHeight//2
screen = (screenWidth, screenHeight)
win = pygame.display.set_mode(screen,  pygame.RESIZABLE)
clock = pygame.time.Clock()
shieldMax = 100
score = 0


isQuitting = False
menuScreen = True
gameScreen = False
GameRun = False
isShield = False
BossBool = False
youLoose = False

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Loading Assets ========================================================================================================
bg = pygame.image.load("Assets/space.png").convert_alpha()
gamebg = pygame.image.load("Assets/SpaceBg.png").convert_alpha()
quitPompt = pygame.image.load("Assets/quit prompt.png").convert_alpha()
enemy1 = pygame.image.load("Assets/enemy1 - 128.png").convert_alpha()
enemy2 = pygame.image.load("Assets/enemy2 - 128.png").convert_alpha()
enemy3 = pygame.image.load("Assets/enemy3 - 128.png").convert_alpha()
spaceShip = pygame.image.load("Assets/SpaceShip - 128.png").convert_alpha()
shieldSprite = pygame.image.load("Assets/Shield.png").convert_alpha()
enemySprites = [enemy1, enemy2, enemy3]
bossSprites = [pygame.image.load("Assets/Boss/Boss_Undamaged.png").convert_alpha(), pygame.image.load("Assets/Boss/Boss_Rwing_Dmg.png").convert_alpha(),pygame.image.load("Assets/Boss/Boss_Lwing_Dmg.png").convert_alpha(),pygame.image.load("Assets/Boss/Boss_Rwing_Destroyed.png").convert_alpha(),
               pygame.image.load("Assets/Boss/Boss_Lwing_Destroyed.png").convert_alpha(),pygame.image.load("Assets/Boss/Boss_Body_Damage.png").convert_alpha(),pygame.image.load("Assets/Boss/Boss_No_Wings.png").convert_alpha()]
explosion = [pygame.image.load("Assets/Explosion/explosion_transparent-0.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-1.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-2.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-3.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-4.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-5.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-6.png").convert_alpha(),
             pygame.image.load("Assets/Explosion/explosion_transparent-7.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-8.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-9.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-10.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-11.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-12.png").convert_alpha(),
             pygame.image.load("Assets/Explosion/explosion_transparent-13.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-14.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-15.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-16.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-17.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-18.png").convert_alpha(),
             pygame.image.load("Assets/Explosion/explosion_transparent-19.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-20.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-21.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-22.png").convert_alpha()]
#Classes  ==============================================================================================================

class GameEvent(object):
    def __init__(self, eventTitle, eventText ,x=0 ,y=0, width=screenWidth, height=screenHeight, colour=(0,0,0), Lives = 4):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.eventText = eventText
        self.eventTitle = eventTitle
        self.Lives = Lives

    def draw(self):
        eventBg = pygame.Surface((self.width,self.height)) # crate BG surface
        eventBg.fill(self.colour)                        # Fill BG surface with collor (WHITE)
        eventText = myfont.render(self.eventText, True,BLACK)
        eventTitle = myfont.render(self.eventTitle, True,BLACK)
        win.blit(eventBg,(self.x,self.y))
        win.blit(eventText, (self.x+100, self.y+100))
        win.blit(eventTitle, (self.x+50, self.y+50))

class Background(object):
    def __init__(self,x,y,sprite = gamebg):
        self.x = x
        self.y = y
        self.sprite = sprite
    def move(self):
        self.x -=1
        if self.x == -1920:
            self.x = 1920

    def draw(self):
        win.blit(self.sprite,(self.x, self.y))


class Player(object):
    def __init__(self, x, y, width=128, height=128, sprite=spaceShip, hp=1000, dmg = 50):
        self.x = x
        self.y = y
        self.vel = 20
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.sprite = sprite
        self.hp = hp
        self.dmg = dmg


    def draw(self):
        win.blit(self.sprite, (self.x, self.y))
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)
    def takeDamage(self,dmg):
        self.hp -= dmg
        if self.hp < 0:
            global youLoose
            youLoose = True

class Enemy(object):
    def __init__(self,x ,y, sprite, width=128, height=128, cooldown = 10):
        self.x = x
        self.y = y
        self.vel  = 20
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.sprite = sprite
        self.cooldown = cooldown
        self.a = self.cooldown

    def draw(self):
        win.blit(self.sprite,(self.x,self.y))
        pygame.draw.rect(win, (255, 0, 0),(self.x, self.y, self.width, self.height),2)
    def time(self):
        if self.a == 0:
            self.a = self.cooldown
            return True
        else:
            self.a -= 1
            return False

class Button(object):
    def __init__(self,x,y,width,height,colour,text):
        self.x = x
        self.y = y
        self.width = width
        self.height= height
        self.colour = colour
        self.text = text
    def draw(self):

        buttontext = myfont.render(self.text, True,BLACK)

        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        win.blit(buttontext, (self.x + self.width//3, self.y+self.height//3))


    def isClick(self):
        if self.x < mousepos[0] < (self.x + self.width) and self.y < mousepos[1] < (self.y +self.height) :
            return True
        else:
            return False



class projectile(object):
    def __init__(self, x, y, radius, color, dmg):
        self.x = x
        self.y = y
        self.dmg = dmg
        self.radius = radius
        self.color = color
        self.vel = 50

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Shield(object):
    def __init__(self, x, y, sprite=shieldSprite, shieldMeter=100):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.shieldMeter = shieldMeter

    def draw(self,x,y):
        self.x = x
        self.y = y
        win.blit(self.sprite,(self.x,self.y))
    def takeDamage(self,dmg):
        self.shieldMeter -= dmg
    def shieldBarDraw(self):
        pygame.draw.rect(win, RED, (50, 50, 200, 10))
        pygame.draw.rect(win, GREEN, (50, 50, 200 * (self.shieldMeter/100), 10))

class Explosion(object):
    def __init__(self, x, y,done = False, counter = 22, explosionList = explosion):
        self.x = x
        self.y = y
        self.counter = counter
        self.exlosionList = explosionList
        self.done = done
    def explode(self):
        if self.counter <= 66:
            win.blit(self.exlosionList[self.counter//3],(self.x,self.y))
            self.counter +=1
        else:
            self.done = True

class Boss(object):
    def __init__(self, x, y, sprites = bossSprites, width = 1080, height = 1080, L_wingHP = 100, R_wingHP = 100, Main_BodyHP = 1000, L_wingBool = True, R_wingBool = True):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.width = width
        self.height = height
        self.R_wingHP = R_wingHP
        self.L_wingHP = L_wingHP
        self.L_wingBool = L_wingBool
        self.R_wingBool = R_wingBool
        self.Main_BodyHP = Main_BodyHP
        self.R_hitbox = (self.x + 25, self.y + 75, 240, 240)
        self.L_hitbox = (self.x + 25, self.y + 780, 240, 240)

    def draw(self):
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, self.width, self.height), 2)
        pygame.draw.rect(win, (255, 0, 0), (self.x + 25, self.y + 780, 240, 240), 2)
        pygame.draw.rect(win, (255, 0, 0), (self.x + 25, self.y + 75, 240, 240), 2)
        if self.L_wingBool and self.R_wingBool:
            win.blit(self.sprites[0], (self.x, self.y))
        elif self.R_wingBool and not self.L_wingBool:
            win.blit(self.sprites[4], (self.x, self.y))
        elif self.L_wingBool and not self.R_wingBool:
            win.blit(self.sprites[3], (self.x, self.y))
        else:
            win.blit(self.sprites[6], (self.x, self.y))

    def RwingHit(self,dmg):
        win.blit(self.sprites[1], (self.x, self.y))
        self.R_wingHP -= dmg
        print(self.R_wingHP)
        if self.R_wingHP <=0:
            print("Right wing destroyed")
            self.R_wingBool = False

    def LwingHit(self,dmg):
        win.blit(self.sprites[2],(self.x, self.y))
        self.L_wingHP -= dmg
        print(self.L_wingHP)
        if self.L_wingHP <=0:
            print("Left wing destroyed")
            self.L_wingBool = False


#Functions =============================================================================================================

def quitGame():
    global isRuning
    isRuning = False
    return

def redrawGameWindow():
    win.blit(bg, (0, 0))

    if isQuitting:
        """ Draws the quit prompt whit quit buttons"""
        win.blit(quitPompt, (screenCenterX - 300, screenCenterY - 200))  # Draws "Quit Prompt
        quitText = myfont.render("Are you sure you want to quit?", True, BLACK)  # Setting Text variable
        win.blit(quitText, (screenCenterX - 250, screenCenterY - 100))  # Printing text variable
        yesButton.draw()   # Drawing Yes button
        noButton.draw()  # Drawing No Button

    elif GameRun:
        background1.draw()
        background2.draw()
        background1.move()
        background2.move()
        #game.draw()
        player.draw()
        shield.shieldBarDraw()
        scoreText = myfont.render("Score: {}".format(score), True, WHITE)
        win.blit(scoreText, (screenWidth - 200, 50))
        if youLoose:
            win.blit(quitPompt, (screenCenterX - 300, screenCenterY - 200))
            looseText = myfont.render("You Loose! Play Again?", True, BLACK)  # Setting Text variable
            win.blit(looseText, (screenCenterX - 250, screenCenterY - 100))  # Printing text variable
            yesButton.draw()  # Drawing Yes button
            noButton.draw()  # Drawing No Button
        if BossBool:
                bossText = bossFont.render("BOSS!!!!", True, (255, 255, 255))
                win.blit(bossText, (screenWidth // 2, screenHeight // 2))
                boss.draw()
        for bullet in PlayerBullets:
            bullet.draw()
        for mob in Mobs:
            mob.draw()
        for mobbullet in MobBullets:
            mobbullet.draw()
        for i in explosions:
            i.explode()

    else:

        if menuScreen:
            startButton.draw()
            quitButton.draw()

    if isShield:
        shield.draw(player.x, player.y)
    pygame.display.update()





#Main loop below  ======================================================================================================

#Definining objects  ===================================================================================================
background1 = Background(0,0)
background2 = Background(1920,0)
startButton = Button((screenWidth//10),(screenHeight//4)*3, 200, 75,WHITE,"START")
quitButton = Button((screenWidth//10)*3,(screenHeight//4)*3, 200, 75,RED,"QUIT")
yesButton = Button(screenCenterX - 250, screenCenterY + 90, 200, 75,BLUE,"YES")
noButton = Button(screenCenterX + 70, screenCenterY + 90, 200, 75,BLUE,"NO")
buttons = [startButton, quitButton,yesButton,noButton]
game = GameEvent("Score", "No of lives left:")
player = Player(64, 64)
boss = Boss(screenWidth + 400, 0)
#mob1 = Enemy(screenWidth,screenHeight)
#mob2 = Enemy(screenWidth,screenHeight)
#mob3 = Enemy(screenWidth,screenHeight)
shield = Shield(player.x, player.y)
Mobs = []
PlayerBullets = []
MobBullets = []
timers = []
explosions = []
neg = -1

#Main LOOP  ============================================================================================================

isRuning = True
boolswitch = False
timer = 0.0
clicktimer1 = 0
clicktimer2 = 0
mobtimer = 0
bullettimer = 0

while isRuning:
    clock.tick(30)
    events = pygame.event.get()
    mousepos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    if GameRun:
        a = pygame.time.get_ticks()
        if a >= 0 and not BossBool:
            BossBool = True

        if clicktimer1 > 0:
            clicktimer1 += 1
        if clicktimer1 > 6:
            clicktimer1 = 0

        if clicktimer2 > 0:
            clicktimer2 += 1
        if clicktimer2 > 6:
            clicktimer2 = 0
        # Enemy spawn
        if mobtimer > 0:
            mobtimer += 1
        if mobtimer > 50:
            mobtimer = 0

        if mobtimer == 0:
            if not BossBool:
                mob = Enemy(screenWidth + 128,random.randint(0, screenHeight-128),enemySprites[random.randint(0,2)])
                Mobs.append(mob)
                mobtimer = 1
        if BossBool:
            if boss.x >= (screenWidth - 400):
                boss.x -= 5
            else:
                boss.y += neg*2
                if boss.y <= -100:
                    neg = neg*(-1)
                if boss.y+boss.height >= 1180:
                    neg = neg*(-1)
            for bullet in PlayerBullets:
                #print(bullet.x, bullet.y , "Boss target", boss.x + 25, boss.x + 265, boss.y + 75, boss.y + 320)
                if (boss.x + 265) > bullet.x > (boss.x + 25) and (boss.y + 320) > bullet.y > (boss.y + 75):
                    print("Boss hit, Right wing")
                    boss.RwingHit(player.dmg)
                    PlayerBullets.pop(PlayerBullets.index(bullet))
                    if not boss.R_wingBool:
                        explosions.append(Explosion((boss.x + 265//4 + random.randint(0,100)*random.randint(-1,1)),(boss.y + 320//4 + random.randint(0,100)*random.randint(-1,1))))
                if (boss.x + 265) > bullet.x > (boss.x + 25) and (boss.y + 1020) > bullet.y > (boss.y + 780):
                    print("Boss hit, Left wing")
                    boss.LwingHit(player.dmg)
                    PlayerBullets.pop(PlayerBullets.index(bullet))
                    if not boss.L_wingBool:
                        explosions.append(Explosion((boss.x + 265//4 + random.randint(0,100)*random.randint(-1,1)),(boss.y + 780 + 240//4 + random.randint(0,100)*random.randint(-1,1))))




        for mob in Mobs:
            if mob.time():
                mobbullet = projectile(mob.x - 128, mob.y +64, 5, BLUE, 50)
                MobBullets.append(mobbullet)
        # Moving =======================================================================================================
        if keys[pygame.K_UP] and player.y >= game.y:
            #print("Pressing UP, Event :",event)
            player.y -= player.vel

        if keys[pygame.K_DOWN] and player.y <= (game.height - player.height):
            #print("Pressing DOWN, Event :", event.type)
            player.y += player.vel
            #Shooting ==================================================================================================
        if keys[pygame.K_h] and clicktimer1 == 0:
            bullet = projectile(player.x + 128, player.y + 64, 5, RED, player.dmg)
            PlayerBullets.append(bullet)
            clicktimer1 = 1
            #Shield ====================================================================================================
        if keys[pygame.K_j] and clicktimer2 == 0:
           if isShield:
               isShield = False
           else: isShield = True
           clicktimer2  = 1

        if isShield:
            if shield.shieldMeter <= 0:
                shield.shieldMeter = 0
                isShield = False
        else:
            if shield.shieldMeter < shieldMax:
                shield.shieldMeter += 1
            else:
                shieldMeter = shieldMax
            #Mobs  =====================================================================================================
        # Checking lists  ==============================================================================================

        for mob in Mobs:
            mob.x -= mob.vel
            if mob.x <= (-128):
                Mobs.pop(Mobs.index(mob))

            for bullet in PlayerBullets:

                if (mob.width + mob.x) > bullet.x > mob.x and (mob.y+mob.height) > bullet.y > mob.y:
                    score += 10
                    explosions.append(Explosion((mob.x + mob.width//4),(mob.y + mob.height//4)))
                    Mobs.pop(Mobs.index(mob))
                    PlayerBullets.pop(PlayerBullets.index(bullet))


        for bullet in PlayerBullets:
            bullet.x += bullet.vel
            if bullet.x >= (game.width + 50):
                PlayerBullets.pop(PlayerBullets.index(bullet))

        for i in explosions:
            if i.done:
                explosions.pop(explosions.index(i))

        for mobbullet in MobBullets:
            mobbullet.x -= mobbullet.vel
            if (player.x + player.width) > mobbullet.x > player.x and (player.y + player.height) > mobbullet.y > player.y:
                if isShield:
                    shield.takeDamage(mobbullet.dmg)
                else:
                    player.takeDamage(mobbullet.dmg)
                    MobBullets.pop(MobBullets.index(mobbullet))
                    print("Colision detected, Ship hp : {}".format(player.hp),"You loose = ", youLoose)
            if mobbullet.x <= (- 50):
                MobBullets.pop(MobBullets.index(mobbullet))


    for event in events:

        if event.type == pygame.QUIT:
            isRuning= False

        if keys[pygame.K_ESCAPE]:
            isQuitting = True

        # Quit menu screen

        if event.type == pygame.MOUSEBUTTONDOWN:

            if startButton.isClick():
                print("Start CLicked")
                menuScreen = False
                gameScreen = True
                GameRun = True

            if quitButton.isClick():
                    isQuitting = True

            if isQuitting and yesButton.isClick():
                if menuScreen:
                    #print("menuscreen = ",menuScreen, "gamescreen =", gameScreen)
                    quitGame()

                elif gameScreen:
                    #print("menuscreen = ", menuScreen, "gamescreen =", gameScreen)
                    gameScreen = False
                    menuScreen=True
                    GameRun = False
                    isQuitting = False

            if GameRun and youLoose:
                GameRun = False
                if yesButton.isClick():
                    GameRun = True
                    youLoose = False
                    score = 0
                    player = Player(64, 64)
                    shield = Shield(player.x, player.y)
                    Mobs = []
                    PlayerBullets = []
                    MobBullets = []
                    timers = []
                elif noButton.isClick():
                    youLoose = False
                    menuScreen = True
                    score = 0

            elif noButton.isClick():
                isQuitting = False
            else:
                pass

    redrawGameWindow()
pygame.quit()