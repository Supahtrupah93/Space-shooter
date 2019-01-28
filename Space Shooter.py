import pygame, sys
import time
import random

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS',25//2)
bossFont = pygame.font.SysFont('Comic Sans MS', 150//2)
#Variables ===============================================
screenWidth = 1280
screenHeight = 720
scale_x = 960/1920
scale_y = 540/1080
print(scale_x, scale_y)
screenCenterX = screenWidth//2
screenCenterY = screenHeight//2
screen = (screenWidth, screenHeight)
win = pygame.display.set_mode(screen,  pygame.HWSURFACE)
clock = pygame.time.Clock()
shieldMax = 100
score = 0
t0 = 0
t1 = 0
t2 = 0

clicktimer1 = 0
clicktimer2 = 0
mobtimer = 0
bullettimer = 0

isRuning = True
godmode = False
isQuitting = False
menuScreen = True
GameRun = False
isShield = False
BossBool = False
youLoose = False
GameOver = False
ChooseAccount = False
TextPrompt = False
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Loading Assets ========================================================================================================
bg = pygame.image.load("Assets/space.png").convert_alpha()
gamebg = pygame.image.load("Assets/SpaceBg.png").convert_alpha()
quitPompt = pygame.image.load("Assets/quit prompt.png").convert_alpha()
quitPompt1 = pygame.transform.scale(quitPompt,(300,200))
enemy1 = pygame.image.load("Assets/enemy1 - 128.png").convert_alpha()
enemy2 = pygame.image.load("Assets/enemy2 - 128.png").convert_alpha()
enemy3 = pygame.image.load("Assets/enemy3 - 128.png").convert_alpha()
spaceShip = pygame.image.load("Assets/SpaceShip - 128.png").convert_alpha()
spaceShip1 = pygame.transform.scale(spaceShip,(64,64))
shieldSprite = pygame.image.load("Assets/Shield.png").convert_alpha()
shieldSprite1 = pygame.transform.scale(shieldSprite,(64,64))
enemySprites = [enemy1, enemy2, enemy3]
enemySprites1 = []
for enemy in enemySprites:
    a =pygame.transform.scale(enemy,(64,64))
    enemySprites1.append(a)
bossSprites = [pygame.image.load("Assets/Boss/Boss_Undamaged.png").convert_alpha(), pygame.image.load("Assets/Boss/Boss_Rwing_Dmg.png").convert_alpha(),pygame.image.load("Assets/Boss/Boss_Lwing_Dmg.png").convert_alpha(),pygame.image.load("Assets/Boss/Boss_Rwing_Destroyed.png").convert_alpha(),
               pygame.image.load("Assets/Boss/Boss_Lwing_Destroyed.png").convert_alpha(),pygame.image.load("Assets/Boss/Boss_Body_Damage.png").convert_alpha(),pygame.image.load("Assets/Boss/Boss_No_Wings.png").convert_alpha()]
bossSprites1 = []
for sprite in bossSprites:
    a = pygame.transform.scale(sprite, (540, 540))
    bossSprites1.append(a)
explosion = [pygame.image.load("Assets/Explosion/explosion_transparent-0.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-1.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-2.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-3.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-4.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-5.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-6.png").convert_alpha(),
             pygame.image.load("Assets/Explosion/explosion_transparent-7.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-8.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-9.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-10.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-11.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-12.png").convert_alpha(),
             pygame.image.load("Assets/Explosion/explosion_transparent-13.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-14.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-15.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-16.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-17.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-18.png").convert_alpha(),
             pygame.image.load("Assets/Explosion/explosion_transparent-19.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-20.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-21.png").convert_alpha(),pygame.image.load("Assets/Explosion/explosion_transparent-22.png").convert_alpha()]

pygame.mixer.init()
pew1 = pygame.mixer.Sound("Assets/Music/pew1.wav")
pew2 = pygame.mixer.Sound("Assets/Music/pew2.wav")
pew3 = pygame.mixer.Sound("Assets/Music/pew3.wav")
victorytune ="Assets/Music/Victory Tune.wav"
gameovertune = "Assets/Music/Game Over Tune.wav"
bosstheme = "Assets/Music/Boss Theme.wav"
gameplaymusic = "Assets/Music/GameplaySong.wav"
menusong = "Assets/Music/MainMenu.wav"
#Classes  ==============================================================================================================

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
    def __init__(self, x, y, width=64, height=64, sprite=spaceShip1, hp=600, dmg = 100):
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
    def __init__(self,x ,y, sprite, width=64, height=64, cooldown = 10, neg = 1):
        self.x = x
        self.y = y
        self.vel  = 20
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.sprite = sprite
        self.cooldown = cooldown
        self.a = self.cooldown
        self.neg = neg * random.randrange(-1, 1, 2)
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
    def __init__(self, x, y, radius, color, dmg, vel = 50):
        self.x = x
        self.y = y
        self.dmg = dmg
        self.radius = radius
        self.color = color
        self.vel = vel

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Shield(object):
    def __init__(self, x, y, sprite=shieldSprite1, shieldMeter=100):
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
        pygame.draw.rect(win, RED, (50/2, 50/2, 200, 10))
        pygame.draw.rect(win, GREEN, (50/2, 50/2, 200 * (self.shieldMeter/100), 10))

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
    def __init__(self, x, y, sprites = bossSprites1, width = 1080/2, height = 1080/2, L_wingHP = 500, R_wingHP = 500, Main_BodyHP = 1000, L_wingBool = True, R_wingBool = True,
                 M_mainBool = True , R_wingHit = False, L_wingHit = False, M_mainHit = False, setup = False, Rw = 0, Lw = 15, Mn = 0,Mcd = 90, Wcd =30):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.width = width
        self.height = height
        self.R_wingHP = R_wingHP
        self.L_wingHP = L_wingHP
        self.L_wingBool = L_wingBool
        self.R_wingBool = R_wingBool
        self.M_mainBool = M_mainBool
        self.Main_BodyHP = Main_BodyHP
        self.R_hitbox = (self.x + 25/2, self.y + 75//2, 240//2, 240//2)
        self.L_hitbox = (self.x + 25/2, self.y + 780//2, 240//2, 240//2)
        self.M_hitbox = (self.x + 25/2, self.y + 315//2, 800//2, 465//2)
        self.R_wingHit = R_wingHit
        self.L_wingHit = L_wingHit
        self.M_mainHit = M_mainHit
        self.setup = setup
        self.Rw = Rw
        self.Lw = Lw
        self.Mn = Mn
        self.Mcd = Mcd
        self.Wcd = Wcd

        self.Bx = x
        self.By = y
        self.Bsprites = sprites
        self.Bwidth = width
        self.Bheight = height
        self.BR_wingHP = R_wingHP
        self.BL_wingHP = L_wingHP
        self.BL_wingBool = L_wingBool
        self.BR_wingBool = R_wingBool
        self.BM_mainBool = M_mainBool
        self.BMain_BodyHP = Main_BodyHP
        self.BR_hitbox = (self.x + 25/2, self.y + 75//2, 240//2, 240//2)
        self.BL_hitbox = (self.x + 25/2, self.y + 780//2, 240//2, 240//2)
        self.BM_hitbox = (self.x + 25/2, self.y + 315//2, 800//2, 465//2)
        self.BR_wingHit = R_wingHit
        self.BL_wingHit = L_wingHit
        self.BM_mainHit = M_mainHit
        self.Bsetup = setup

    def reset(self):
        self.x = self.Bx
        self.y = self.By
        self.sprites = self.Bsprites
        self.width = self.Bwidth
        self.height = self.Bheight
        self.R_wingHP = self.BR_wingHP
        self.L_wingHP = self.BL_wingHP
        self.L_wingBool = self.BL_wingBool
        self.R_wingBool = self.BR_wingBool
        self.M_mainBool = self.BM_mainBool
        self.Main_BodyHP = self.BMain_BodyHP
        self.R_hitbox = (self.x + 25, self.y + 75, 240, 240)
        self.L_hitbox = (self.x + 25, self.y + 780, 240, 240)
        self.M_hitbox = (self.x + 25, self.y + 315, 800, 465)
        self.R_wingHit = self.BR_wingHit
        self.L_wingHit = self.BL_wingHit
        self.M_mainHit = self.BM_mainHit
        self.setup =self.Bsetup
    def draw(self):
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, self.width, self.height), 2)
        pygame.draw.rect(win, (255, 0, 0), (self.x + 25/2, self.y + 75//2, 240//2, 240//2), 2)
        pygame.draw.rect(win, (255, 0, 0), (self.x + 25/2, self.y + 780//2, 240//2, 240//2), 2)
        pygame.draw.rect(win, (255, 0, 0), (self.x + 25/2, self.y + 315//2, 800//2, 465//2), 2)
        if self.L_wingBool and self.R_wingBool:
            win.blit(self.sprites[0], (self.x, self.y))
            if self.R_wingHit:
                win.blit(self.sprites[1], (self.x, self.y))
                self.R_wingHit = False
            elif self.L_wingHit:
                win.blit(self.sprites[2], (self.x, self.y))
                self.L_wingHit = False
        elif self.R_wingBool and not self.L_wingBool:
            win.blit(self.sprites[4], (self.x, self.y))
            if self.R_wingHit:
                win.blit(self.sprites[1], (self.x, self.y))
                self.R_wingHit = False
        elif self.L_wingBool and not self.R_wingBool:
            win.blit(self.sprites[3], (self.x, self.y))
            if self.L_wingHit:
                win.blit(self.sprites[2], (self.x, self.y))
                self.L_wingHit = False
        elif self.M_mainBool:
            win.blit(self.sprites[6], (self.x, self.y))
            if self.M_mainHit:
                win.blit(self.sprites[5], (self.x, self.y))
                self.M_mainHit = False
        else:
            win.blit(self.sprites[6], (self.x, self.y))

    def RwingHit(self, dmg):
        win.blit(self.sprites[1], (self.x, self.y))
        self.R_wingHP -= dmg
        self.R_wingHit = True
        print(self.R_wingHP)
        if self.R_wingHP <=0:
            print("Right wing destroyed")
            self.R_wingBool = False

    def LwingHit(self, dmg):
        win.blit(self.sprites[2],(self.x, self.y))
        self.L_wingHP -= dmg
        self.L_wingHit = True
        print(self.L_wingHP)
        if self.L_wingHP <=0:
            print("Left wing destroyed")
            self.L_wingBool = False

    def MainHit(self, dmg):
        win.blit(self.sprites[5],(self.x, self.y))
        self.Main_BodyHP -= dmg
        self.M_mainHit = True
        print(self.Main_BodyHP)
        if self.Main_BodyHP <= 0:
            print("Boss defeated")
            self.M_mainBool = False
    def RwingShot(self):
        if self.Rw == 0:
            self.Rw = self.Wcd
            return True
        else:
            self.Rw -= 1
            return False
    def LwingShot(self):
        if self.Lw == 0:
            self.Lw = self.Wcd
            return True
        else:
            self.Lw -= 1
            return False
    def Mshot(self):
        if self.Mn == 0:
            self.Mn = self.Mcd
            return True
        else:
            self.Mn -= 1
            return False
#Functions =============================================================================================================

def quitGame():
    global isRuning
    isRuning = False
    return

def redrawGameWindow():


    if isQuitting:
        """ Draws the quit prompt whit quit buttons"""
        win.blit(quitPompt1, (screenCenterX - 300//2, screenCenterY - 200//2))  # Draws "Quit Prompt
        quitText = myfont.render("Are you sure you want to quit?", True, BLACK)  # Setting Text variable
        win.blit(quitText, (screenCenterX - 250//2, screenCenterY - 100//2))  # Printing text variable
        yesButton.draw()   # Drawing Yes button
        noButton.draw()  # Drawing No Button
    else:
        if menuScreen:
            win.blit(bg, (0, 0))
            startButton.draw()
            quitButton.draw()

        if GameRun:
            background1.draw()
            background2.draw()
            background1.move()
            background2.move()
            player.draw()
            shield.shieldBarDraw()
            scoreText = myfont.render("Score: {}".format(score), True, WHITE)
            win.blit(scoreText, (screenWidth - 200//2, 50//2))
            if BossBool:
                # bossText = bossFont.render("BOSS!!!!", True, (255, 255, 255))
                # win.blit(bossText, (screenWidth // 2, screenHeight // 2))
                boss.draw()

            if isShield:
                shield.draw(player.x, player.y)

            for bullet in PlayerBullets:
                bullet.draw()
            for mob in Mobs:
                mob.draw()
            for mobbullet in MobBullets:
                mobbullet.draw()
            for i in explosions:
                i.explode()
            for bullet in BossBullets:
                bullet.draw()

        if youLoose or GameOver:
            win.blit(quitPompt1, (screenCenterX - 300//2, screenCenterY - 200//2))
            looseText = myfont.render("You Loose! Play Again?", True, BLACK)  # Setting Text variable
            winText = myfont.render("You Win! Play Again?", True, BLACK)
            if youLoose:
                win.blit(looseText, (screenCenterX - 250//2, screenCenterY - 100//2))  # Printing text variable
            if GameOver:
                win.blit(winText, (screenCenterX - 250//2, screenCenterY - 100//2))
            yesButton.draw()  # Drawing Yes button
            noButton.draw()  # Drawing No Button

    pygame.display.update()

#Main loop below  ======================================================================================================

#Definining objects  ===================================================================================================

background1 = Background(0,0)
background2 = Background(screenWidth,0)
startButton = Button((screenWidth // 10)//2, ((screenHeight // 4) * 3)//2, 200//2, 75//2, WHITE, "START")
quitButton = Button(((screenWidth // 10) * 3)//2, ((screenHeight // 4) * 3)//2, 200//2, 75//2, RED, "QUIT")
yesButton = Button(screenCenterX - 250//2, screenCenterY + 90//2, 200//2, 75//2, BLUE, "YES")
noButton = Button(screenCenterX + 70//2, screenCenterY + 90//2, 200//2, 75//2, BLUE, "NO")
buttons = [startButton, quitButton, yesButton, noButton]
player = Player(64, 64)
boss = Boss(screenWidth + 400//2, 0)
shield = Shield(player.x, player.y)
Mobs = []
PlayerBullets = []
MobBullets = []
BossBullets = []
timers = []
explosions = []
neg = -1



#Main LOOP  ============================================================================================================
while isRuning:

    clock.tick(30)
    events = pygame.event.get()
    mousepos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()


    if GameOver or youLoose or startButton.isClick(): # Reset game, if game over bcs player lost or won, or game has started
        background1 = Background(0, 0)
        background2 = Background(screenWidth, 0)
        startButton = Button((screenWidth // 10)//2, ((screenHeight // 4) * 3)//2, 200//2, 75//2, WHITE, "START")
        quitButton = Button(((screenWidth // 10) * 3)//2, ((screenHeight // 4) * 3)//2, 200//2, 75//2, RED, "QUIT")
        yesButton = Button(screenCenterX - 250//2, screenCenterY + 90//2, 200//2, 75//2, BLUE, "YES")
        noButton = Button(screenCenterX + 70//2, screenCenterY + 90//2, 200//2, 75//2, BLUE, "NO")
        buttons = [startButton, quitButton, yesButton, noButton]
        player = Player(64, 64)
        boss = Boss(screenWidth + 400//2, 0)
        shield = Shield(player.x, player.y)
        Mobs = []
        PlayerBullets = []
        MobBullets = []
        timers = []
        explosions = []
        neg = -1
        t0 = pygame.time.get_ticks()
        BossBool = False
    #Game logic ========================================================================================================
    if GameRun:

        a = pygame.time.get_ticks()

        if a - (t2 - t1) - t0 >= 10000 and not BossBool and not isQuitting:
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
            if not BossBool or boss.setup and boss.M_mainBool:
                mob = Enemy(screenWidth + 128//2, random.randint(0, screenHeight-128//2),enemySprites1[random.randint(0,2)])
                Mobs.append(mob)
                mobtimer = 1
        if not BossBool:
            for mob in Mobs:  # Make bullets for mobs (While Not boss, and game run)
                if mob.time():
                    mobbullet = projectile(mob.x - 128//2, mob.y + 64//2, 5, BLUE, 50)
                    MobBullets.append(mobbullet)

        if BossBool:
            if boss.setup: #IF boss is setup then spawn bullets
                for mob in Mobs:  # Make bullets for mobs
                    if mob.time():
                        mobbullet = projectile(mob.x - 128//2, mob.y + 64//2, 5, BLUE, 50)
                        MobBullets.append(mobbullet)

            if boss.x >= (screenWidth - screenWidth//5) and boss.M_mainBool:
                boss.x -= 5
            else:
                boss.setup = True

            if not boss.M_mainBool:
                if boss.x <= (screenWidth + 400//2):
                    boss.x += 5
                else:
                    GameOver = True
                    BossBool = False
            else:
                boss.y += neg*2
                if boss.y <= -100//2:
                    neg = neg*(-1)
                if boss.y+boss.height >= 1180//2:
                    neg = neg*(-1)
            if boss.setup:
                if boss.RwingShot() and boss.R_wingBool:
                    r = projectile(boss.x + 25//2, boss.y + 75//2 + 120//2, 10, GREEN, 50)
                    BossBullets.append(r)
                if boss.LwingShot() and boss.L_wingBool:
                    a = projectile(boss.x + 25//2,boss.y + 780//2 + 120//2, 10, GREEN, 50)
                    BossBullets.append(a)
                if boss.Mshot() and boss.M_mainBool:
                    m = projectile(boss.x + 25//2,boss.y + 315//2 + 230//2, 20, GREEN, 50, 20)
                    BossBullets.append(m)

            for bullet in PlayerBullets:
                if boss.setup:
                    if (boss.x + screenHeight//4) > bullet.x > (boss.x + screenHeight//43) and (boss.y + screenHeight//3) > bullet.y > (boss.y + (screenHeight//43)*3) and boss.R_wingBool:
                        print("Boss hit, Right wing")
                        boss.RwingHit(player.dmg)
                        PlayerBullets.pop(PlayerBullets.index(bullet))
                        if not boss.R_wingBool:
                            explosions.append(Explosion((boss.x + 265//4 + random.randint(0,100)*random.randint(-1,1)), (boss.y + 320//4 + random.randint(0,100)*random.randint(-1,1))))
                    if (boss.x + 265//2) > bullet.x > (boss.x + 25//2) and (boss.y + 1020//2) > bullet.y > (boss.y + 780//2) and boss.L_wingBool:
                        print("Boss hit, Left wing")
                        boss.LwingHit(player.dmg)
                        PlayerBullets.pop(PlayerBullets.index(bullet))
                        if not boss.L_wingBool:
                            explosions.append(Explosion((boss.x + 265//4//2 + random.randint(0,100)*random.randint(-1,1)), (boss.y + 780//2 + 240//4//2 + random.randint(0,100)*random.randint(-1,1))))
                    if (boss.x + 825//2) > bullet.x > (boss.x + 25//2) and (boss.y + 800//2) > bullet.y > (boss.y +265//2) and not boss.L_wingBool and not boss.R_wingBool and boss.M_mainBool:
                        print("Boss hit, Main body")
                        boss.MainHit(player.dmg)
                        try:
                            PlayerBullets.pop(PlayerBullets.index(bullet))
                        except:
                            print("Object_Out_Of_List_Error")
                        if not boss.M_mainBool:
                            explosions.append(
                                Explosion((boss.x + 825//4//2 + random.randint(0, 100) * random.randint(-1, 1)), (boss.y + 320//2 + 460//4//2 + random.randint(0, 300) * random.randint(-1, 1))))


        # Moving / Player controls =====================================================================================
        if GameRun:
            if keys[pygame.K_UP] and player.y >= 0:
                #print("Pressing UP, Event :",event)
                player.y -= player.vel
            if keys[pygame.K_DOWN] and player.y <= (screenHeight - player.height):
                #print("Pressing DOWN, Event :", event.type)
                player.y += player.vel
                #Shooting ==============================================================================================
            if keys[pygame.K_h] and clicktimer1 == 0:
                #pew1.play()
                bullet = projectile(player.x + 128//2, player.y + 64//2, 5, RED, player.dmg)
                PlayerBullets.append(bullet)
                clicktimer1 = 1
                #Shield ================================================================================================
            if keys[pygame.K_j] and clicktimer2 == 0:
               if isShield:
                   isShield = False
               else:
                   isShield = True
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
        elif isQuitting:
            pass
        elif youLoose:
            pass
        elif GameOver:
            pass
        #Mobs  ========================================================================================================

        # Checking lists  ==============================================================================================

        for mob in Mobs: # Moving MOBs======================
            mob.x -= mob.vel
            mob.y -= mob.vel//2 * mob.neg
            if mob.x <= (-128):
                Mobs.pop(Mobs.index(mob))
            if 0 >= mob.y or mob.y >= (screenHeight-128//2):
                mob.neg *= -1

            for bullet in PlayerBullets: #Checkign colision on Mobs with player bullets

                if (mob.width + mob.x) > bullet.x > mob.x and (mob.y+mob.height) > bullet.y > mob.y:
                    score += 10
                    explosions.append(Explosion((mob.x + mob.width//4),(mob.y + mob.height//4)))
                    Mobs.pop(Mobs.index(mob))
                    PlayerBullets.pop(PlayerBullets.index(bullet))


        for bullet in PlayerBullets: #Moving plater bullets
            bullet.x += bullet.vel
            if bullet.x >= (screenWidth + 50//2):
                PlayerBullets.pop(PlayerBullets.index(bullet))

        for i in explosions: #Removing explosions from list
            if i.done:
                explosions.pop(explosions.index(i))

        for mobbullet in MobBullets: #Moving Mob Bullets  and checking colision with player
            mobbullet.x -= mobbullet.vel
            if (player.x + player.width) > mobbullet.x > player.x and (player.y + player.height) > mobbullet.y > player.y:
                if isShield:
                    shield.takeDamage(mobbullet.dmg)
                else:
                    player.takeDamage(mobbullet.dmg)
                    MobBullets.pop(MobBullets.index(mobbullet))
                    print("Colision detected, Ship hp : {}".format(player.hp),"You loose = ", youLoose)
            if mobbullet.x <= (- 50//2):
                MobBullets.pop(MobBullets.index(mobbullet))

        for bullet in BossBullets:
            bullet.x -= bullet.vel
            if bullet.radius == 20:
                if bullet.y < player.y:
                    for i in range (5):
                        bullet.y -= 5-i
                        bullet.y += 5
                elif bullet.y > player.y + 128//2:
                    for i in range(5):
                        bullet.y += 5-i
                        bullet.y -= 5
                else:
                    pass
            if (player.x + player.width) > bullet.x > player.x and (player.y + player.height) > bullet.y > player.y:
                if isShield:
                    shield.takeDamage(bullet.dmg)
                else:
                    player.takeDamage(bullet.dmg)
                    BossBullets.pop(BossBullets.index(bullet))
                    print("Colision detected, Ship hp : {}".format(player.hp),"You loose = ", youLoose)
            if bullet.x <= (- 50//2):
                BossBullets.pop(BossBullets.index(bullet))
    elif isQuitting:
        pass
    elif youLoose:
        pass
    elif GameOver:
        pass

    #Checking Events ===================================================================================================
    for event in events:

        if event.type == pygame.QUIT:
            isRuning = False

        if keys[pygame.K_ESCAPE]:
            isQuitting = True
            t1 = pygame.time.get_ticks()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if startButton.isClick():
                t0 = pygame.time.get_ticks()
                print("Start CLicked")
                menuScreen = False
                GameRun = True
                Mobs = []
                PlayerBullets = []
                MobBullets = []
                BossBullets = []
                timers = []
                boss.reset()
                explosions = []
                isShield = False

            if quitButton.isClick():
                isQuitting = True

            if isQuitting:
                if yesButton.isClick():
                    if menuScreen:
                        quitGame()

                    else:
                        menuScreen = True
                        GameOver = False
                        youLoose = False
                        GameRun = False
                        isQuitting = False
                        BossBool = False

                elif noButton.isClick():
                    isQuitting = False
                    GameRun = True
                    t2 = pygame.time.get_ticks()

            if GameRun and (youLoose or GameOver):
                if yesButton.isClick():
                    t0 = pygame.time.get_ticks()
                    youLoose = False
                    GameOver = False
                    score = 0
                    player = Player(64, 64)
                    shield = Shield(player.x, player.y)
                    Mobs = []
                    PlayerBullets = []
                    MobBullets = []
                    timers = []
                    explosions = []
                    boss.reset()
                elif noButton.isClick():
                    youLoose = False
                    GameOver = False
                    GameRun = False
                    menuScreen = True
                    score = 0
                    boss.reset()
                    Mobs = []
                    PlayerBullets = []
                    MobBullets = []
                    timers = []
                    explosions = []
            else:
                pass

    redrawGameWindow()
pygame.quit()