import pygame
import random
import math
from pygame import mixer



pygame.init()

#Screen create and logo
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Sharif's Space games")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)


#background Image
bgImage = pygame.image.load('background.png')


#Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

#Player
playerImg = pygame.image.load('rocket.png')
playerX = 380
playerY = 490
moveChangeX=0
moveChangeY=0

#Enemy
enemyImg=[]
enemX=[]
enemY=[]
enemMoveChangeX = []
enemMoveChangeY = []
enemNumber = 5
for i in range(enemNumber):
    enemyImg.append(pygame.image.load('enemyBoss.png'))
    enemX.append(random.randint(0,688))
    enemY.append(random.randint(0,150))
    enemMoveChangeX.append(7)
    enemMoveChangeY.append(6)

#Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX=0
bulletY=490
bulletChangeX=0
bulletChangeY=10
bulletState = "ready"

def fire_bullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg,(x+26,y+13))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def player(x,y):
    screen.blit(playerImg,(x,y))

def is_collision(enX,enY,buX,buY):
    distance = math.sqrt((math.pow(enX-buX,2))+(math.pow(enY-buY,2)))
    if distance <= 24:
        return True
    return False


#Show score:
score = 0
font = pygame.font.Font('freesansbold.ttf',32)
fontX= 20
fontY= 15

def fontShow(x,y):
    scoreValue = font.render("Score : "+str(score),True,(255,123,255))
    screen.blit(scoreValue,(x,y))
#GameOverText
over_font=pygame.font.Font('freesansbold.ttf',64)

def game_over():
    ovet_text = font.render("Game Over",True,(255,255,255))
    screen.blit(ovet_text,(350,250))


running = True
while running:
    screen.fill((128,128,128))
    screen.blit(bgImage,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveChangeX = -10
            if event.key == pygame.K_RIGHT:
                moveChangeX = 10
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                if bulletState is "ready":
                    bulletX = playerX
                    bulletY = 490
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                moveChangeX = 0
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_UP:
        #         moveChangeY =-0.4
        #     if event.key == pygame.K_DOWN:
        #         moveChangeY =0.4
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
        #         moveChangeY = 0
    
    playerX+=moveChangeX
    playerY+=moveChangeY
    if playerX<=0:
        playerX=0
    if playerX>=736:
        playerX=736

    # if playerY>=536:
    #     playerY=536
    # if playerY <=100:
    #     playerY =100

    if bulletY <=0:
        bulletX = playerX
        bulletY = 490
        bulletState = "ready"
    if bulletState is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletChangeY
    

    for i in range(enemNumber):
        if enemY[i] > 450:
            for j in range(enemNumber):
                enemY[j]=2000
            game_over()
            break


        enemX[i] += enemMoveChangeX[i]
        if enemX[i] <= 0:
            enemMoveChangeX[i] = 7
            enemY[i] += enemMoveChangeY[i]
        elif enemX[i] >= 736:
            enemMoveChangeX[i] = -7
            enemY[i] += enemMoveChangeY[i]
        collision = is_collision(enemX[i],enemY[i],bulletX,bulletY)
        if collision:
            col_sound = mixer.Sound('explosion.wav')
            col_sound.play()
            enemX[i] = random.randint(49,688)
            enemY[i] = random.randint(50,250)
            bulletState = "ready"
            bulletY = 490
            score += 1
        enemy(enemX[i],enemY[i],i)
        
    
    player(playerX,playerY)
    fontShow(fontX,fontY)
    pygame.display.update()