# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:43:23 2020

@author: Mukeshnath S
"""

import pathlib
import numpy as np
#import PIL
import pygame
pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("Joker_song.mp3")
pygame.mixer.music.play(-1, 0.0)

screen_len = 1300
screen_ht = 676
surface = 460

high_score = 0
lives = 3
stage = 1
stage_len = 0
level = 0
game_over = False

window = pygame.display.set_mode((screen_len,screen_ht), pygame.RESIZABLE)
window = pygame.display.set_mode()
pygame.display.set_caption("It's raining Mr. Beasts!")

currentDirectory = pathlib.Path("./dino")
currentPattern = "Run*.png"
sprite_imgs = []
for currentFile in currentDirectory.glob(currentPattern):
    sprite_imgs.append(currentFile)
req_images = []
for i in sprite_imgs:
    req_images.append('.\\' + '\\'.join(i._parts))


currentDirectory = pathlib.Path("./bg")
currentPattern_bg = "bg*.png"
bg_imgs = []
for currentFile in currentDirectory.glob(currentPattern_bg):
    bg_imgs.append(currentFile)
req_bg_images = []
for i in bg_imgs:
    req_bg_images.append('.\\' + '\\'.join(i._parts))

req_bg = []

levels = len(bg_imgs)

for i in range(1,levels+1):
    for index,b in enumerate(req_bg_images):
        if int(b[-6:-4]) == i:
            req_bg.append(b)
        else:
            continue

sprite_path = "./dino/"

walkRight = [pygame.image.load(img) for img in req_images]
walkLeft = [pygame.transform.flip(pygame.image.load(img),True,False) for img in req_images]
bg_l = [pygame.image.load(img) for img in req_bg]
bg = bg_l[level]
#bg = pygame.image.load(sprite_path + 'bg_3_resize.png')
#bg2 = pygame.transform.flip(bg,True,False)
#char = pygame.image.load(sprite_path + 'idle (1).png')
fireR = pygame.image.load(sprite_path + 'fireR.png')
fireL = pygame.image.load(sprite_path + 'fireL.png')

bgx = 0
bgx2 = bg.get_width()
score = 0
touch = 0

clock = pygame.time.Clock()


class player(object):
    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=1
        self.left=False
        self.right=False
        self.walkCount=0
        self.isJump=False
        self.jumpCount=10
        self.standing=True
        self.hitbox = (self.x+66, self.y+20, 125, 105)
        self.health=9
        self.isVisible=True

    def draw(self, window):

        if self.isVisible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if not(self.standing):
                if self.left:
                    window.blit(walkLeft[0], (self.x,self.y))
                    self.walkCount += 1
                elif self.right:
                    window.blit(walkRight[0], (self.x,self.y))
                    self.walkCount += 1
            else:
                if self.right:
                    window.blit(walkRight[0], (self.x,self.y))
                    self.walkCount += 1
                elif self.left:
                    window.blit(walkLeft[0], (self.x,self.y))
                    self.walkCount += 1
                else:
                    window.blit(walkLeft[0], (self.x, self.y))
                    self.walkCount += 1

            pygame.draw.rect(window, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 45, 9))
            pygame.draw.rect(window, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, (5 * self.health), 9))

            if self.right:
                self.hitbox = (self.x+9, self.y+20, 125, 105)
#                pygame.draw.rect(window, (255,0,0), self.hitbox, 2)
            else:
                self.hitbox = (self.x+66, self.y+20, 125, 105)
#                pygame.draw.rect(window, (255,0,0), self.hitbox, 2)

currentDirectory = pathlib.Path("./robot/")

currentPattern = "RunShoot*.png"
sprite_imgs_enemy = []

for currentFile in currentDirectory.glob(currentPattern):
    print(currentFile)
    sprite_imgs_enemy.append(currentFile)

#print(sprite_imgs)

req_images_enemy = []
for i in sprite_imgs_enemy:
    req_images_enemy.append(i._parts[0] + '\\' + i._parts[1:][0])
    print(i._parts[0])
    print('\\'.join(i._parts[1:]))
    print(req_images_enemy)


class enemy(object):

    walkRight = [pygame.image.load(img) for img in req_images_enemy]
    walkLeft = [pygame.transform.flip(pygame.image.load(img),True,False) for img in req_images_enemy]

    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.start=10
        self.end=screen_len
        self.path=[self.start, self.end]
        self.vel=5
        self.dropvel = 10
#        self.dropCount = 0
        self.walkCount=0
        self.hitbox = (self.x + 35, self.y+15, 87, 117)
        self.score=0
        self.health=9
        self.isVisible = True
        self.left = False
        self.right = False

    def draw(self, window):
#        self.move()
        if self.isVisible:
            if self.y >= surface:
                self.y=surface
                if self.walkCount + 1 >= 27:
                    self.walkCount = 0

                if self.vel>0:
                    window.blit(self.walkRight[0], (self.x,self.y))
                    self.walkCount += 1
                else:
                    window.blit(self.walkLeft[0], (self.x,self.y))
                    self.walkCount += 1

            else:
                if self.vel>0:
                    self.x += 2
                    self.y += self.dropvel
                    window.blit(self.walkRight[0], (self.x,self.y))

                else:
                    self.x += 2
                    self.y += self.dropvel
                    window.blit(self.walkLeft[0], (self.x,self.y))



            pygame.draw.rect(window, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 45, 9))
            pygame.draw.rect(window, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, (5 * self.health), 9))
            self.hitbox = (self.x + 35, self.y+15, 87, 117)
#            pygame.draw.rect(window, (255,0,0), self.hitbox, 2)

    def move(self):

        if self.vel > 0:
            self.left = False
            self.right = True
            if self.x + self.width + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            self.left = True
            self.right = False
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
            return True
        else:
            self.isVisible = False
            return False


class projectile(object):
    def __init__(self, x, y, width, height, facing):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, window):
        if self.facing < 0:
            window.blit(fireL, (self.x, self.y))
        else:
            window.blit(fireR, (self.x, self.y))

#        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


def redrawGameWindow():

    window.blit(bg, (bgx,0))
    window.blit(bg, (bgx2,0))
    score_text = font.render("SCORE: " + str(score), 1, (0,0,0))
    high_score_text = font.render("HIGH SCORE: " + str(high_score), 1, (0,0,0))
    stage_text = font.render("STAGE: " + str(stage), 1, (0,0,0))
    lives_text = font.render("LIVES: " + str(lives), 1, (0,0,0))
    start_text = font1.render("Press U key to play.", 1, (0,0,0))
#    start_new_text = font1.render("Press A key to Start a new game.", 1, (0,0,0))
    pause_text = font1.render("Press P key to pause.", 1, (0,0,0))
    revive_text = font1.render("Press R key to revive your DINO!", 1, (0,0,0))
    jump_text = font1.render("Press UP arrow key to jump.", 1, (0,0,0))
    fire_text = font1.render("Press SPACEBAR to breathe fire!", 1, (0,0,0))
    direc_text = font1.render("Press LEFT and RIGHT arrow keys to move left and right.", 1, (0,0,0))
    direc_text1 = font1.render("RUN TO THE RIGHT END OF THE TERRAIN!", 1, (0,0,0))
    gameover_text = font1.render("GAME OVER!!!", 1, (0,0,0))
    restart_text = font1.render("Press N key to Again start a new game.", 1, (0,0,0))

    window.blit(score_text, (550, 30))
    window.blit(high_score_text, (700, 30))
    window.blit(stage_text, (200, 30))
    window.blit(lives_text, (100, 30))

    if not(pause):
        window.blit(start_text, (200, 100))
        window.blit(pause_text, (200, 150))
        window.blit(revive_text, (200, 200))
        window.blit(jump_text, (200, 250))
        window.blit(fire_text, (200, 300))
        window.blit(direc_text, (200, 350))
        window.blit(direc_text1, (200, 400))

    if game_over:
        window.blit(gameover_text, (400, 350))
        window.blit(restart_text, (300, 225))

    dino.draw(window)
    for robot in robot_army:
        robot.draw(window)
    for bullet in bullets:
        bullet.draw(window)

    pygame.display.update()


#mainloop
font = pygame.font.SysFont('comicsans', 25, True, True)
font1 = pygame.font.SysFont('comicsans', 45, True, True)
pause = False
dino = player(580, surface, 201, 140)

num_enemy = 1
robot_army=[]
robot_army.append(enemy(50, surface, 142, 140))
bullets=[]
shootLoop = 0
run=True
while run:
    clock.tick(30)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    keys = pygame.key.get_pressed()

    if len(robot_army)<num_enemy:
        newx = np.random.randint(20, 1250)
        robot_army.append(enemy(newx, 50, 140, 140))

    for bullet in bullets:

        if dino.left:
            bullet_x = bullet.x
        else:
            bullet_x = bullet.x + bullet.width


        for robot in robot_army:

            if bullet.y < robot.hitbox[1] + robot.hitbox[3] and bullet.y > robot.hitbox[1]:
                if bullet_x >= robot.hitbox[0] and bullet_x < robot.hitbox[0]+robot.hitbox[2]:

                    if robot.hit():
                        if bullet in bullets:
                            bullets.pop(bullets.index(bullet))
                    else:
                        if robot in robot_army:
                            robot_army.pop(robot_army.index(robot))
                        score += 1
                        if bullet in bullets:
                            bullets.pop(bullets.index(bullet))


        if bullet.x<screen_len and bullet.x>0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if lives>0:
        if keys[pygame.K_p]:
            pause=False
            pygame.mixer.music.pause()

        if keys[pygame.K_u]:
            pause=True
            pygame.mixer.music.unpause()

    if game_over:
        if keys[pygame.K_n]:
            game_over = False
            dino = player(670, surface, 201, 140)
            for robot in robot_army[1:]:
                robot_army.pop(robot_army.index(robot))
            dino.isVisible = True
            dino.health = 9
            level=0
            stage=1
            lives = 3
            num_enemy=1
            bgx = 0
            bgx2 = bg.get_width()
            bg = bg_l[level]
            stage_len = 0
            if score>high_score:
                high_score = score
                score=0
            else:
                score=0
    #### CHEAT KEY "G" ####
    if keys[pygame.K_g]:
        dino = player(670, surface, 201, 140)
        dino.isVisible = True
        dino.health = 9
    #### CHEAT KEY "G" ####

    if pause:

        if not(dino.isVisible):
            if lives > 1:
                if keys[pygame.K_r]:
                    lives -= 1
                    dino = player(670, surface, 201, 140)
                    dino.isVisible = True
                    dino.health = 9
            else:
                game_over = True

        for robot in robot_army:
            robot.move()

            if shootLoop > 0:
                shootLoop += 1
            if shootLoop > 5:
                shootLoop = 0
            if keys[pygame.K_SPACE] and shootLoop==0:
                if dino.isVisible:
                    if dino.right:
                        facing = 1
                    else:
                        facing = -1
                    if len(bullets) < 3:
                        if dino.right:
                            bullets.append(projectile(round(dino.x+(dino.width//2))+(10*facing),round(dino.y+(dino.height//2) - 15), 64, 31, facing))
                        else:
                            bullets.append(projectile(round(dino.x+(dino.width//2))+(70*facing),round(dino.y+(dino.height//2) - 15), 64, 31, facing))
                        shootLoop = 1

            if robot.right:
                robot_x = robot.hitbox[0] + robot.hitbox[2]
            else:
                robot_x = robot.hitbox[0]


            if ((dino.hitbox[1]+dino.hitbox[3] >= robot.hitbox[1]) and (dino.hitbox[1]+dino.hitbox[3] <= robot.hitbox[1]+robot.hitbox[3])) or ((dino.hitbox[1] <= robot.hitbox[1]) and (dino.hitbox[1] >= robot.hitbox[1]+robot.hitbox[3])):

                if (robot_x > dino.hitbox[0]) and (robot_x < dino.hitbox[0]+dino.hitbox[2]):
                    touch -= 1
                    if touch <= -8:
                        dino.health -= 1
                        touch = 0



        if dino.health <= 0:
            dino.isVisible = False
        else:
            dino.isVisible = True

        if dino.isVisible:
            if keys[pygame.K_LEFT] and (dino.x > dino.vel):
                dino.vel=8
                dino.x -= dino.vel
                dino.left = True
                dino.right = False
                dino.standing = False
            elif keys[pygame.K_RIGHT] and (dino.x < screen_len - dino.width - dino.vel):
        #        elif keys[pygame.K_RIGHT] and (dino.x > 600):
                dino.vel = 1
                if dino.x > 5:
                    bgx -= 12
                    bgx2 -= 12
                    if bgx < bg.get_width() * -1:
                        bgx = bg.get_width()
        #                    print("bgx - " + str(bgx))
                    if bgx2 < bg.get_width() * -1:
                        bgx2 = bg.get_width()
        #                    print("bgx2 - " + str(bgx2))
                        stage_len += 1

                dino.x += dino.vel
                dino.left = False
                dino.right = True
                dino.standing = False
            else:
                dino.standing = True
                dino.walkCount = 0

            if not(dino.isJump):
                if keys[pygame.K_UP] and not(dino.y==0):
                    dino.isJump=True
            else:
                if dino.jumpCount >= -10:
                    neg = 1
                    if dino.jumpCount<0:
                        neg = -(neg)
                    dino.y -= (dino.jumpCount ** 2) * 0.5 * neg
                    dino.jumpCount -= 1
                else:
                    dino.isJump=False
                    dino.jumpCount = 10

    if stage_len == 2:
        pause = False

        if stage == 16:
            game_over = True
        else:
            if keys[pygame.K_u]:
                if not(game_over):
                    stage += 1
                    level += 1

                    if level <=4 :
                        num_enemy = np.random.randint(2,4)
                    if 10 >= level > 4 :
                        num_enemy = np.random.randint(3,5)
                    if 15 >= level > 10 :
                        num_enemy = np.random.randint(4,6)

                    bg = bg_l[level]
                    stage_len = 0
                    pause = True

#    if keys[pygame.K_a]:
#        game_over = False
#        stage = 1
#        level = 0
#        lives = 4
#        score = 0

    redrawGameWindow()

pygame.mixer.music.stop()

pygame.display.quit

pygame.quit()
