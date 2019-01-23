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
screen = (screenWidth ,screenHeight)
win = pygame.display.set_mode(screen,  pygame.RESIZABLE)
clock = pygame.time.Clock()
shieldMax = 100
shieldMeter = 100
click = 1


isQuitting = False
menuScreen = True
gameScreen = False
GameRun = False
isShield = False
Boss = False
youLoose = False

BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

#Loading Assets =========================================
bg = pygame.image.load("Assets/space.png")
quitPompt = pygame.image.load("Assets/quit prompt.png")
enemy1 = pygame.image.load("Assets/enemy1 - 128.png")
enemy2 = pygame.image.load("Assets/enemy2 - 128.png")
enemy3 = pygame.image.load("Assets/enemy3 - 128.png")
spaceShip = pygame.image.load("Assets/SpaceShip - 128.png")
shieldSprite = pygame.image.load("Assets/Shield.png")
enemySprites = [enemy1, enemy2, enemy3]

#Classes =================================================

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
class Player(object):
    def __init__(self,x ,y, width=128, height=128, sprite = spaceShip, hp = 40):
        self.x = x
        self.y = y
        self.vel  = 20
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.sprite = sprite
        self.hp = hp


    def draw(self):
        win.blit(self.sprite,(self.x,self.y))
        pygame.draw.rect(win, (255, 0, 0),(self.x, self.y, self.width, self.height),2)
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
    def __init__(self, x, y, radius, color,dmg):
        self.x = x
        self.y = y
        self.dmg = dmg
        self.radius = radius
        self.color = color
        self.vel = 50
        self.damage = 2

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Shield(object):
    def __init__(self,x,y,sprite = shieldSprite,):
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self,x,y):
        self.x = x
        self.y = y
        win.blit(self.sprite,(self.x,self.y))
    def shieldBarDraw(self):
        pygame.draw.rect(win,RED,(screenWidth//4 ,screenHeight//4,200,10))
        pygame.draw.rect(win, GREEN, (screenWidth//4 ,screenHeight//4, 200 *(shieldMeter/100), 10))


#Functions================================================

def quitGame():
    global isRuning
    isRuning = False


def redrawGameWindow():
    """ This function draws EVERYTHING (or calls methods to draw objects on each frame)"""
    win.blit(bg, (0, 0))

    if isQuitting:
        """ Draws the quit prompt whit quit buttons"""
        win.blit(quitPompt, (screenCenterX - 300 ,screenCenterY - 200)) # Draws "Quit Prompt
        quitText = myfont.render("Are you sure you want to quit?", True, BLACK) # Setting Text variable
        win.blit(quitText,(screenCenterX - 250 ,screenCenterY - 100)) # Printing text variable
        yesButton.draw() # Drawing Yes button
        noButton.draw()# Drawing No Button

    elif GameRun:
        game.draw()
        player.draw()
        shield.shieldBarDraw()
        if youLoose:
            win.blit(quitPompt, (screenCenterX - 300, screenCenterY - 200))
            looseText = myfont.render("You Loose! Play Again?", True, BLACK)  # Setting Text variable
            win.blit(looseText, (screenCenterX - 250, screenCenterY - 100))  # Printing text variable
            yesButton.draw()  # Drawing Yes button
            noButton.draw()  # Drawing No Button
        if Boss:
            bossText = bossFont.render("BOSS!!!!", True, (255, 255, 255))
            win.blit(bossText, (screenWidth // 2, screenHeight // 2))


        for bullet in PlayerBullets:
            bullet.draw()
        for mob in Mobs:
            mob.draw()
        for mobbullet in MobBullets:
            mobbullet.draw()

    else:

        if menuScreen:
            startButton.draw()
            quitButton.draw()

    if isShield:
        shield.draw(player.x,player.y)
    pygame.display.update()
    return



#Main loop below =========================================

#Definining objects ======================================

startButton = Button((screenWidth//10),(screenHeight//4)*3, 200, 75,WHITE,"START")
quitButton = Button((screenWidth//10)*3,(screenHeight//4)*3, 200, 75,RED,"QUIT")
yesButton = Button(screenCenterX - 250, screenCenterY + 90, 200, 75,BLUE,"YES")
noButton = Button(screenCenterX + 70, screenCenterY + 90, 200, 75,BLUE,"NO")
buttons = [startButton, quitButton,yesButton,noButton]
game = GameEvent("Score", "No of lives left:")
player = Player(64, 64)
#mob1 = Enemy(screenWidth,screenHeight)
#mob2 = Enemy(screenWidth,screenHeight)
#mob3 = Enemy(screenWidth,screenHeight)
shield = Shield(player.x, player.y)
Mobs = []
PlayerBullets = []
MobBullets = []
timers = []

#Main LOOP ===============================================
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

    for event in events:
        #print(events)


        if event.type == pygame.QUIT:
            isRuning= False

        if keys[pygame.K_ESCAPE]:
            isQuitting = True

        # Quit menu screen

        if event.type == pygame.MOUSEBUTTONDOWN:

            if  startButton.isClick():
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
                    a = 0
                    GameRun = True
                    youLoose = False
                elif noButton.isClick():
                    youLoose = False
                    menuScreen = True
                    a = 0

            elif noButton.isClick():
                isQuitting = False
            else:
                pass

    if GameRun and youLoose:
        a = 0
        player = Player(64, 64)
        shield = Shield(player.x, player.y)
        Mobs = []
        PlayerBullets = []
        MobBullets = []
        timers = []

    else:
        #Event timer
        a = pygame.time.get_ticks()
        bossTime = 1
        if a >= bossTime:
            Boss = True

        if clicktimer1 > 0:
            clicktimer1 += 1
        if clicktimer1 > 3:
            clicktimer1 = 0

        if clicktimer2 > 0:
            clicktimer2 += 1
        if clicktimer2 > 3:
            clicktimer2 = 0
        # Enemy spawn
        if mobtimer > 0:
            mobtimer += 1
        if mobtimer > 50:
            mobtimer = 0

        if mobtimer == 0:
            mob = Enemy(screenWidth + 128,random.randint(0, screenHeight-128),enemySprites[random.randint(0,2)])
            Mobs.append(mob)
            mobtimer = 1

        for mob in Mobs:

            if mob.time():
                mobbullet = projectile(mob.x - 128, mob.y +64, 5, BLUE, 10)
                MobBullets.append(mobbullet)
        # Moving==================================================
        if keys[pygame.K_UP] and player.y >= game.y:
            #print("Pressing UP, Event :",event)
            player.y -= player.vel

        if keys[pygame.K_DOWN] and player.y <= (game.height - player.height):
            #print("Pressing DOWN, Event :", event.type)
            player.y += player.vel
            #Shooting================================================
        if keys[pygame.K_h] and clicktimer1 == 0:
            bullet = projectile(player.x + 128, player.y + 64,5,RED, 10)
            PlayerBullets.append(bullet)
            clicktimer1 = 1
            #Shield==================================================
        if keys[pygame.K_j] and clicktimer2 == 0:
           if isShield:
               isShield = False
           else: isShield = True
           clicktimer2  = 1
        if isShield:
            if shieldMeter <= 0:
                shieldMeter = 0
                isShield = False
            else:
                shieldMeter -= 1
        else:
            if shieldMeter <= shieldMax:
                shieldMeter += .5
            else:
                shieldMeter = shieldMax
            #Mobs ====================================================
        for mob in Mobs:
            for bullet in PlayerBullets:
                if (mob.width + mob.x)> bullet.x > mob.x and (mob.y+mob.height)> bullet.y > mob.y :
                    print("Mob hit")
                    Mobs.pop(Mobs.index(mob))
                    PlayerBullets.pop(PlayerBullets.index(bullet))
            mob.x -= mob.vel
            if mob.x <= (-128):
                Mobs.pop(Mobs.index(mob))


            #Bullets =================================================
        for bullet in PlayerBullets:
            bullet.x += bullet.vel
            if bullet.x >= (game.width + 50):
                PlayerBullets.pop(PlayerBullets.index(bullet))

        for mobbullet in MobBullets:
            mobbullet.x -= mobbullet.vel
            if (player.x + player.width) > mobbullet.x > player.x and (player.y + player.height) > mobbullet.y > player.y:
                player.takeDamage(mobbullet.dmg)
                MobBullets.pop(MobBullets.index(mobbullet))
                #print("Colision detected, Ship hp : {}".format(player.hp),"You loose = ", youLoose)
            if mobbullet.x <= (- 50):
                MobBullets.pop(MobBullets.index(mobbullet))

    #Crtanje svaki frejm igre, sta se nalazi na ekranu
    redrawGameWindow()
    #print(mobtimer)



pygame.quit()