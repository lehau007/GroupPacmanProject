# Build Pac-Man from Scratch in Python with PyGame!!
import copy
from board_modified import boards
import pygame
import math
from enum import Enum
import numpy as np
from random import random
from random import randint
from collections import deque
pygame.init()

WIDTH = 900 
HEIGHT = 950 
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 30
class Action(Enum):
   RIGHT = 0;
   LEFT = 1;
   UP = 2;
   DOWN = 3;
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = 'blue'
PI = math.pi
player_images = []
for i in range(1, 5):
    image = (pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (30, 30)))
    player_images.append(image)
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (30,30))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (30, 30))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (30,30))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (30, 30))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (30, 30))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (30, 30))
player_x = 465
player_y = 686
direction = 0
blinky_x = 75
blinky_y = 70
blinky_direction = 0
inky_x = 495
inky_y = 462
inky_direction = 2
pinky_x = 435
pinky_y = 406
pinky_direction = 2
clyde_x = 435
clyde_y = 406
clyde_direction = 2
counter = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
moving = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
lives = 3
game_over = False
game_won = False
epsilon = 1
epsilon_decay = 0.998
epsilon_min = 0.1
gamma = 0.9
alpha = 0.2


arr = level
def bfs(player_x,player_y):
   q = deque()
   num1 = (HEIGHT - 50) // 32
   num2 = WIDTH // 30
   check = np.zeros((33,30),np.int32)
   start = (player_y // num1 ,player_x // num2,-1)
   q.append(start)
#    print(start,end= " ")
   while((len(q))):
      cur = q.popleft()
      if((arr[cur[0]][cur[1]] == 1 or arr[cur[0]][cur[1]] == 2) and cur != start):
         return cur[2]
      if(arr[cur[0] + 1][cur[1]] < 3 and check[cur[0] + 1][cur[1]] == 0):
          if cur == start : q.append((cur[0] + 1,cur[1],3))
          else : q.append((cur[0] + 1,cur[1],cur[2]))
          check[cur[0] + 1][cur[1]] = 1

      if(arr[cur[0] - 1][cur[1]] < 3 and check[cur[0] - 1][cur[1]] == 0):
           if cur == start : q.append((cur[0] - 1,cur[1],2))
           else : q.append((cur[0] - 1,cur[1],cur[2]))
           check[cur[0] - 1][cur[1]] = 1

      if(arr[cur[0]][cur[1] + 1] < 3 and check[cur[0]][cur[1] + 1] == 0):
           if cur == start : q.append((cur[0],cur[1] + 1,0))
           else : q.append((cur[0],cur[1] + 1,cur[2]))
           check[cur[0]][cur[1] + 1] = 1

      if(arr[cur[0]][cur[1] - 1] < 3 and check[cur[0]][cur[1] - 1] == 0):
           if cur == start : q.append((cur[0],cur[1] - 1,1))
           else : q.append((cur[0],cur[1] - 1,cur[2]))
           check[cur[0]][cur[1] - 1] = 1


def check_ghost(blinky_x,blinky_y,pinky_x,pinky_y,player_x,player_y):
    global HEIGHT,WIDTH
    check = [False,False,False,False]
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    pos_blinky = (blinky_y//num1,blinky_x//num2)
    pos_pinky = (pinky_y // num1,pinky_x // num2)
    pos_player = (player_y // num1,player_x // num2)
    if abs(pos_player[0] - pos_blinky[0]) <= 1 or abs(pos_player[0] - pos_pinky[0]) <= 1 :
        if  (pos_blinky[1] - pos_player[1] <= 4 and pos_blinky[1] - pos_player[1] >= 0 ) or (pos_pinky[1] - pos_player[1] <=4 and pos_pinky[1] - pos_player[1] >= 0) :
            #  print(pos_pinky[1] - pos_player[1])
             check[0] = True
        if ( pos_player[1] - pos_blinky[1] <= 4 and pos_player[1] - pos_blinky[1] >= 0 )or (pos_player[1] - pos_pinky[1] <= 4  and pos_player[1] - pos_pinky[1] >= 0):
            #  print(pos_player[1] - pos_pinky[1])
             check[1] = True
    if abs(pos_player[1] - pos_blinky[1]) <= 1 or abs(pos_player[1] - pos_pinky[1]) <= 1 :
        if (pos_blinky[0] - pos_player[0] <=4 and 0 < pos_blinky[0] - pos_player[0] >= 0) or  (pos_pinky[0] - pos_player[0] <=4 and pos_pinky[0] - pos_player[0] >= 0) :
             check[3] = True
        if (pos_player[0] - pos_blinky[0] <= 4 and pos_player[0] - pos_blinky[0] >= 0) or (pos_player[0] - pos_pinky[0] <= 4 and pos_player[0] - pos_pinky[0] >= 0) :
             check[2] = True
    return check


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos
        self.center_y = self.y_pos
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img,self.img.get_rect(center= (self.x_pos,self.y_pos)))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, spooked_img.get_rect(center= (self.x_pos,self.y_pos)))
        else:
            screen.blit(dead_img, dead_img.get_rect(center = (self.x_pos,self.y_pos)))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        # R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y) // num1 - 1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x) // num2 - 1] < 3 \
                    or (level[self.center_y // num1][(self.center_x) // num2 - 1] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x) // num2 + 1] < 3 \
                    or (level[self.center_y // num1][(self.center_x) // num2 + 1] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y) // num1 + 1][self.center_x // num2] < 3 \
                    or (level[(self.center_y) // num1 + 1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y) // num1 - 1][self.center_x // num2] < 3 \
                    or (level[(self.center_y) // num1 - 1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y) // num1 + 1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y) // num1 - 1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x) // num2 - 1] < 3 \
                            or (level[self.center_y // num1][(self.center_x) // num2 - 1] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x) // num2 + 1] < 3 \
                            or (level[self.center_y // num1][(self.center_x) // num2 + 1] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y) // num1 + 1][self.center_x // num2] < 3 \
                            or (level[(self.center_y) // num1 + 1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y) // num1 - 1][self.center_x // num2] < 3 \
                            or (level[(self.center_y) // num1 - 1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x) // num2 - 1] < 3 \
                            or (level[self.center_y // num1][(self.center_x) // num2 - 1] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x) // num2 + 1] < 3 \
                            or (level[self.center_y // num1][(self.center_x) // num2 + 1] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
       
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed[1]
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                else:
                    self.x_pos += self.speed[1]
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed[1]
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                else:
                    self.x_pos -= self.speed[1]
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed[1]
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed[0]
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                else:
                    self.y_pos -= self.speed[0]
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed[0]
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                else:
                    self.y_pos += self.speed[0]
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed[1]
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
            elif self.turns[0]:
                self.x_pos += self.speed[1]
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed[1]
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
            elif self.turns[1]:
                self.x_pos -= self.speed[1]
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed[0]
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
            elif self.turns[2]:
                self.y_pos -= self.speed[0]
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed[0]
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
            elif self.turns[3]:
                self.y_pos += self.speed[0]
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed[1]
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                else:
                    self.x_pos += self.speed[1]
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed[1]
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                else:
                    self.x_pos -= self.speed[1]
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed[0]
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
            elif self.turns[2]:
                self.y_pos -= self.speed[0]
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed[0]
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
            elif self.turns[3]:
                self.y_pos += self.speed[0]
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed[1]
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
            elif self.turns[0]:
                self.x_pos += self.speed[1]
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed[1]
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
            elif self.turns[1]:
                self.x_pos -= self.speed[1]
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed[1]
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed[0]
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed[0]
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                else:
                    self.y_pos -= self.speed[0]
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed[0]
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed[0]
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed[1]
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed[1]
                else:
                    self.y_pos += self.speed[0]
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))


def check_collisions(scor, power, power_count, eaten_ghosts):
    global reward
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
            reward = 1
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
            reward = 2
    return scor, power, power_count, eaten_ghosts,reward


def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_images[counter // 5]).get_rect(center = (player_x,player_y)))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False),(player_images[counter // 5]).get_rect(center = (player_x,player_y)))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90),(player_images[counter // 5]).get_rect(center = (player_x,player_y)))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_images[counter // 5]).get_rect(center = (player_x,player_y)))

reward = -1

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx) // num2 + 1] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx ) // num2 - 1] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery) // num1 + 1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery) // num1 + 1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery) // num1 + 1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery) // num1 - 1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery) // num1 + 1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery) // num1 - 1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx) // num2 - 1] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx) // num2 + 1] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns



def move_player(play_x, play_y):
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += num2
    elif direction == 1 and turns_allowed[1]:
        play_x -= num2
    if direction == 2 and turns_allowed[2]:
        play_y -= num1
    elif direction == 3 and turns_allowed[3]:
        play_y += num1
    return play_x, play_y


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target

    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
    return [blink_target, -1, pink_target, -1]

action = 1
episode = 0
run = True




while run:
    
    terminated = 0
    reward = -1
    timer.tick(fps)
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]

    moving = True

    screen.fill('black')
    draw_board()
    center_x = player_x 
    center_y = player_y
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    if powerup:
        ghost_speeds = [(num1,num2), (num1,num2), (num1,num2), (num1,num2)]
    else:
        ghost_speeds =  [(num1,num2), (num1,num2), (num1,num2), (num1,num2)]
    if eaten_ghost[0]:
        ghost_speeds[0] = (num1,num2)
    if eaten_ghost[1]:
        ghost_speeds[1] = (num1,num2)
    if eaten_ghost[2]:
        ghost_speeds[2] = (num1,num2)
    if eaten_ghost[3]:
        ghost_speeds[3] = (num1,num2)
    if blinky_dead:
        ghost_speeds[0] = (num1,num2)
    if inky_dead:
        ghost_speeds[1] = (num1,num2)
    if pinky_dead:
        ghost_speeds[2] = (num1,num2)
    if clyde_dead:
        ghost_speeds[3] = (num1,num2)

    game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
    draw_player()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                   blinky_box, 0)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead,
                  pinky_box, 2)
    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

    turns_allowed = check_position(center_x, center_y)

    direction_command = action

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        # if not inky_dead and not inky.in_box:
        #     inky_x, inky_y, inky_direction = inky.move_inky()
        # else:
        #     inky_x, inky_y, inky_direction = inky.move_clyde()
        # clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    score, powerup, power_counter, eaten_ghost,reward = check_collisions(score, powerup, power_counter, eaten_ghost)
    # add to if not powerup to check if eaten ghosts
    if not powerup:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                (player_circle.colliderect(pinky.rect) and not pinky.dead) :
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 465
                player_y = 686
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                level = copy.deepcopy(boards)
                reward = -100 
                terminated = 1
                episode += 1
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 465
            player_y = 686
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
            reward = -100
            level = copy.deepcopy(boards)
            terminated = 1
            episode += 1
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 465
            player_y = 686
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
            reward = -100 
            terminated = 1
            episode += 1
            level = copy.deepcopy(boards)
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:
        blinky_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:
        pinky_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    
    if  (game_over or game_won):
                draw_misc()
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False

    

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False


    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    # current_state = (((player_y + 23) // num1,(player_x + 24) // num2),((blinky_y + 22) // num1,(blinky_x + 22) // num2),((pinky_y + 22) // num1,(pinky_x + 22) // num2))
    # if current_state != prev_state :
    #  food = (bfs(player_x + 23,player_y + 24))
    #  ghost_right,ghost_left,ghost_up,ghost_down = check_ghost(blinky_x+22,blinky_y+22,pinky_x+22,pinky_y + 22,player_x + 23,player_y + 24)
    #  turn_next = check_position(player_x + 23,player_y + 24)
    #  if food == 0 and (ghost_right):
    #     if turn_next[2] and not ghost_up: action = 2
    #     elif turn_next[1] and not ghost_left: action = 1
    #     elif turn_next[3] and not ghost_down: action = 3
    #  elif food  == 1 and (ghost_left):
    #     if turn_next[3] and not ghost_down : action = 3
    #     elif turn_next[0] and not ghost_right : action = 0
    #     elif turn_next[2] and not ghost_left : action = 2
    #  elif food == 2 and (ghost_up):
    #     if turn_next[1] and not ghost_left : action = 1 
    #     elif turn_next[3] and not ghost_down : action = 3
    #     elif turn_next[0] and not ghost_right : action = 0
    #  elif food == 3 and (ghost_down):
    #     if turn_next[0] and not ghost_right : action = 0
    #     elif turn_next[2] and not ghost_up : action = 2
    #     elif turn_next[1] and not ghost_left : action = 1 
    #  else:
    #     action = food
    turn_next = check_position(player_x,player_y)
    food = (bfs(player_x,player_y))
    ghost_right,ghost_left,ghost_up,ghost_down = check_ghost(blinky_x,blinky_y,pinky_x,pinky_y,player_x,player_y)
    
    if food == 0 and (turn_next[0] and ghost_right):
        if turn_next[2] and not ghost_up: action = 2
        elif turn_next[1] and not ghost_left: action = 1
        elif turn_next[3] and not ghost_down: action = 3
    elif food  == 1 and (turn_next[1] and ghost_left):
        if turn_next[3] and not ghost_down : action = 3
        elif turn_next[0] and not ghost_right : action = 0
        elif turn_next[2] and not ghost_up : action = 2
    elif food == 2 and (turn_next[2] and ghost_up):
        if turn_next[1] and not ghost_left : action = 1 
        elif turn_next[3] and not ghost_down : action = 3
        elif turn_next[0] and not ghost_right : action = 0
    elif food == 3 and (turn_next[3] and ghost_down):
        if turn_next[0] and not ghost_right : action = 0
        elif turn_next[2] and not ghost_up : action = 2
        elif turn_next[1] and not ghost_left : action = 1 
    else:
        action = food
    
    
    # print(((blinky_y + 22) // num1,(blinky_x + 22) // num2),end = " ")
    # # print(((pinky_y + 22) // num1,(pinky_x + 22) // num2),end = " ")
    # print(food,end=" ")
    # print(turn_next,end=" ")
    # print(action)
    # print(ghost_right,end = " ")
    # print(ghost_left,end= " ")
    # print(ghost_up,end= " ")
    # print(ghost_down)
    
    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False
    if game_won == True:
        draw_misc()
    pygame.display.flip()
    


pygame.quit()


# sound effects, restart and winning messages
