# Build Pac-Man from Scratch in Python with PyGame!!
from collections import deque
import copy
from board import boards
import pygame
import math

pygame.init()

aims_food = (24, 15)

WIDTH = 900
HEIGHT = 950 
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 120
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = 'blue'
PI = math.pi
player_images = []
for i in range(0, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))
num1 = ((HEIGHT - 50) // 32)
num2 = (WIDTH // 30)
player_x = 450
player_y = 663
#num1 = 28, num2 = 30
direction = 0
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
counter = 5
flicker = False
find = True
ways = []
d = 0
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 4
player_dead = False
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
class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
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
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        # R, L, U, D
        #num1 = 28, num2 = 30
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
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
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
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
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
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
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
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
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (50, 500))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (50 + i * 40, 330))
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
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num3 = 15
    #num1 = 28, num2 = 30
    # centerx = 473
    # centery = 686
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def draw_board():
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
                
class Player:
    def __init__(self, x_coord, y_coord, direct, find_coord, ways_coord, d, blink_x, blink_y, blinky_dead, ink_x, ink_y, inky_dead, pink_x, pink_y, pinky_dead, clyd_x, clyd_y, clyde_dead, powerup):
        self.num1 = (HEIGHT - 50) // 32
        self.num2 = WIDTH // 30
        self.num3 = 15
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.blinky_x = (blink_x + 23) // num2
        self.blinky_y = (blink_y + 24) // num1
        self.inky_x = (ink_x + 23) // num2
        self.inky_y = (ink_y + 24) // num1
        self.pinky_x= (pink_x + 23) // num2
        self.pinky_y = (pink_y + 24) // num1
        self.clyde_x = (clyd_x + 23) // num2
        self.clyde_y = (clyd_y + 24) // num1
        self.p = powerup
        self.x = x_coord + 23
        self.y = y_coord + 24
        self.direction = direct
        self.find = find_coord
        self.ways = ways_coord
        self.i = d
        min_PG = 1e9
        self.min_gost = (-99, -99)
        if(not powerup and not(14 <= (blink_y + 23) // num2 <= 16 and 12 <= (blink_x + 24) // num1 <= 17) and not blinky_dead and min_PG > math.sqrt((x_coord - blink_x)*(x_coord - blink_x) + (y_coord - blink_y)*(y_coord - blink_y))):
            min_PG = math.sqrt((x_coord - blink_x)*(x_coord - blink_x) + (y_coord - blink_y)*(y_coord - blink_y))
            self.min_gost = (blink_y, blink_x)
        if(not powerup and not(14 <= (ink_y + 23) // num2 <= 16 and 12 <= (ink_x + 24) // num1 <= 17) and not inky_dead and min_PG > math.sqrt((x_coord - ink_x)*(x_coord - ink_x) + (y_coord - ink_y)*(y_coord - ink_y))):
            min_PG = math.sqrt((x_coord - ink_x)*(x_coord - ink_x) + (y_coord - ink_y)*(y_coord - ink_y))
            self.min_gost = (ink_y, ink_x)
        if(not powerup and not(14 <= (pink_y + 23) // num2 <= 16 and 12 <= (pink_x + 24) // num1 <= 17) and not pinky_dead and min_PG > math.sqrt((x_coord - pink_x)*(x_coord - pink_x) + (y_coord - pink_y)*(y_coord - pink_y))):
            min_PG = math.sqrt((x_coord - pink_x)*(x_coord - pink_x) + (y_coord - pink_y)*(y_coord - pink_y))
            self.min_gost = (pink_y, pink_x)
        if(not powerup and not(14 <= (clyd_y + 23) // num2 <= 16 and 12 <= (clyd_x + 24) // num1 <= 17) and not clyde_dead and min_PG > math.sqrt((x_coord - clyd_x)*(x_coord - clyd_x) + (y_coord - clyd_y)*(y_coord - clyd_y))):
            min_PG = math.sqrt((x_coord - clyd_x)*(x_coord - clyd_x) + (y_coord - clyd_y)*(y_coord - clyd_y))
            self.min_gost = (clyd_y, clyd_x)
            

        self.rect = self.draw_player()

    def draw_player(self):
        # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        if self.direction == 0:
            screen.blit(player_images[counter // 5], (player_x, player_y))
        elif self.direction == 1:
            screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
        elif self.direction == 2:
            screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
        elif self.direction == 3:
            screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

    def move_player(self, b, aims):
        # print(aims)
        # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        start = self.get_position(self.y_pos, self.x_pos)
        if self.find == True or math.sqrt((self.get_position(self.y_pos, self.x_pos)[1] - self.get_position(self.min_gost[0], self.min_gost[1])[1])*(self.get_position(self.y_pos, self.x_pos)[1] - self.get_position(self.min_gost[0], self.min_gost[1])[1]) + (self.get_position(self.y_pos, self.x_pos)[0] - self.get_position(self.min_gost[0], self.min_gost[1])[0])*(self.get_position(self.y_pos, self.x_pos)[0] - self.get_position(self.min_gost[0], self.min_gost[1])[0])) == 3.0:
            #print("FIND")
            aims = self.near_food(b)
            self.i = 0
            if(start != aims and aims != None and 0 <= aims[0] < 33 and 0 <= aims[1] < 30):
                self.ways = self.find_food(start, aims)
                self.find = False
        else:
            if(self.i < len(self.ways)):
                if self.ways[self.i] == aims:
                    self.find = True
                else:
                    if(self.i < len(self.ways) - 1):
                        if self.ways[self.i+1][1] - self.ways[self.i][1] == 1:
                            self.x_pos += player_speed
                            self.direction = 0
                        elif self.ways[self.i+1][1] - self.ways[self.i][1] == -1:
                            self.x_pos -= player_speed
                            self.direction = 1
                        elif self.ways[self.i+1][0] - self.ways[self.i][0] == -1:
                            self.y_pos -= player_speed
                            self.direction = 2
                        elif self.ways[self.i+1][0] - self.ways[self.i][0] == 1:
                            self.y_pos += player_speed
                            self.direction = 3
                            
                    if self.direction == 0 and self.x - ways[self.i][1]*self.num2 >= 45:
                        self.i = self.i+1
                    elif self.direction == 1 and self.x - ways[self.i][1]*self.num2 <= -10:
                        self.i = self.i+1
                    elif self.direction == 2 and self.y - ways[self.i][0]*self.num1 <= -10:
                        self.i = self.i+1
                    elif self.direction == 3 and self.y - ways[self.i][0]*self.num1 >= 40:
                        self.i = self.i+1

        return self.x_pos, self.y_pos, aims,self.direction, self.find, self.ways, self.i
    
    def find_food(self, start, goal):
        frontier = deque([start])
        visited = set()
        came_from = {}

        while frontier:
            current = frontier.popleft()
            visited.add(current)

            if current == goal:
                break

            for next_node in self.get_neighbors(current):
                if next_node not in visited:
                    frontier.append(next_node)
                    came_from[next_node] = current

        path = self.reconstruct_path(came_from, start, goal)
        return path

    def get_neighbors(self, node):
        neighbors = []
        x, y = node
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if (math.sqrt((new_x - self.blinky_x) ** 2 + (new_y - self.blinky_y) ** 2) >= 1.0) and \
                (math.sqrt((new_x - self.pinky_x) ** 2 + (new_y - self.pinky_y) ** 2) >= 1.0) and \
                (math.sqrt((new_x - self.inky_x) ** 2 + (new_y - self.inky_y) ** 2) >= 1.0) and \
                (math.sqrt((new_x - self.clyde_x) ** 2 + (new_y - self.clyde_y) ** 2) >= 1.0):
                if 0 <= new_x < len(level) and 0 <= new_y < len(level[0]) and level[new_x][new_y] < 3:
                    neighbors.append((new_x, new_y))
        return neighbors

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path
    # def next_foof(self):
    #     das = 0
    def get_position(self, y , x):

        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        return (y+23) // num1, (x+24) // num2
    def near_food(self, board):
        aimsfood_x = self.x // num2
        aimsfood_y = self.y // num1
        blink_x = self.blinky_x
        blink_y = self.blinky_y
        ink_x = self.inky_x
        ink_y = self.inky_y
        pink_x = self.pinky_x
        pink_y = self.pinky_y
        clyd_x = self.clyde_x
        clyd_y = self.clyde_y
        powerup = self.p
        check = [[0 for col in range(30)] for row in range(33)]
        start = (aimsfood_y ,aimsfood_x)
        def dfs(board, aimsfood_x , aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check):
            if 0 < board[aimsfood_y][aimsfood_x] < 3 and aimsfood_y != start[0] and aimsfood_x != start[1]:
                return aimsfood_y, aimsfood_x
            check[aimsfood_y][aimsfood_x] = 1
            min_PG = 1e9
            if(min_PG > math.sqrt((aimsfood_x - blink_x)*(aimsfood_x - blink_x) + (aimsfood_y - blink_y)*(aimsfood_y - blink_y))):
                min_PG = math.sqrt((aimsfood_x - blink_x)*(aimsfood_x - blink_x) + (aimsfood_y - blink_y)*(aimsfood_y - blink_y))
                min_gost = (blink_y, blink_x)
            if(min_PG > math.sqrt((aimsfood_x - ink_x)*(aimsfood_x - ink_x) + (aimsfood_y - ink_y)*(aimsfood_y - ink_y))):
                min_PG = math.sqrt((aimsfood_x - ink_x)*(aimsfood_x - ink_x) + (aimsfood_y - ink_y)*(aimsfood_y - ink_y))
                min_gost = (ink_y, ink_x)
            if(min_PG > math.sqrt((aimsfood_x - pink_x)*(aimsfood_x - pink_x) + (aimsfood_y - pink_y)*(aimsfood_y - pink_y))):
                min_PG = math.sqrt((aimsfood_x - pink_x)*(aimsfood_x - pink_x) + (aimsfood_y - pink_y)*(aimsfood_y - pink_y))
                min_gost = (pink_y, pink_x)
            if(min_PG > math.sqrt((aimsfood_x - clyd_x)*(aimsfood_x - clyd_x) + (aimsfood_y - clyd_y)*(aimsfood_y - clyd_y))):
                min_PG = math.sqrt((aimsfood_x - clyd_x)*(aimsfood_x - clyd_x) + (aimsfood_y - clyd_y)*(aimsfood_y - clyd_y))
                min_gost = (clyd_y, clyd_x)
                
            if min_gost[0] - aimsfood_y <= 0:
                if(min_gost[1] - aimsfood_x >= 0):
                    # print(min_gost)
                    # print("DL")
                    if 0 <= aimsfood_y+1 < 33 and board[aimsfood_y+1][aimsfood_x] < 3 and check[aimsfood_y+1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y+1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y+1][aimsfood_x] = 0
                    if 0 <= aimsfood_x-1 < 30 and board[aimsfood_y][aimsfood_x-1] < 3 and check[aimsfood_y][aimsfood_x-1] == 0:
                        temp = dfs(board, aimsfood_x-1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x-1] = 0
                    if 0 <= aimsfood_x+1 < 30 and board[aimsfood_y][aimsfood_x+1] < 3 and check[aimsfood_y][aimsfood_x+1] == 0:
                        temp = dfs(board, aimsfood_x+1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x+1] = 0
                    if 0 <= aimsfood_y-1 < 33 and board[aimsfood_y-1][aimsfood_x] < 3 and check[aimsfood_y-1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y-1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y-1][aimsfood_x] = 0
                else:
                    # print(min_gost)
                    # print("DR")
                    if 0 <= aimsfood_y+1 < 33 and board[aimsfood_y+1][aimsfood_x] < 3 and check[aimsfood_y+1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y+1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y+1][aimsfood_x] = 0
                    if 0 <= aimsfood_x+1 < 30 and board[aimsfood_y][aimsfood_x+1] < 3 and check[aimsfood_y][aimsfood_x+1] == 0:
                        temp = dfs(board, aimsfood_x+1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x+1] = 0
                    if 0 <= aimsfood_x-1 < 30 and board[aimsfood_y][aimsfood_x-1] < 3 and check[aimsfood_y][aimsfood_x-1] == 0:
                        temp = dfs(board, aimsfood_x-1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x-1] = 0
                    if 0 <= aimsfood_y-1 < 33 and board[aimsfood_y-1][aimsfood_x] < 3 and check[aimsfood_y-1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y-1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y-1][aimsfood_x] = 0
                    
            if min_gost[0] - aimsfood_y >= 0:
                if(min_gost[1] - aimsfood_x >= 0):
                    # print(min_gost)
                    # print("UL")
                    if 0 <= aimsfood_y-1 < 33 and board[aimsfood_y-1][aimsfood_x] < 3 and check[aimsfood_y-1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y-1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y-1][aimsfood_x] = 0
                    if 0 <= aimsfood_x-1 < 30 and board[aimsfood_y][aimsfood_x-1] < 3 and check[aimsfood_y][aimsfood_x-1] == 0:
                        temp = dfs(board, aimsfood_x-1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x-1] = 0
                    if 0 <= aimsfood_x+1 < 30 and board[aimsfood_y][aimsfood_x+1] < 3 and check[aimsfood_y][aimsfood_x+1] == 0:
                        temp = dfs(board, aimsfood_x+1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x+1] = 0
                    if 0 <= aimsfood_y+1 < 33 and board[aimsfood_y+1][aimsfood_x] < 3 and check[aimsfood_y+1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y+1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y+1][aimsfood_x] = 0
                else:
                    # print(min_gost)
                    # print("UR")
                    if 0 <= aimsfood_y-1 < 33 and board[aimsfood_y-1][aimsfood_x] < 3 and check[aimsfood_y-1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y-1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y-1][aimsfood_x] = 0
                    if 0 <= aimsfood_x+1 < 30 and board[aimsfood_y][aimsfood_x+1] < 3 and check[aimsfood_y][aimsfood_x+1] == 0:
                        temp = dfs(board, aimsfood_x+1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x+1] = 0
                    if 0 <= aimsfood_x-1 < 30 and board[aimsfood_y][aimsfood_x-1] < 3 and check[aimsfood_y][aimsfood_x-1] == 0:
                        temp = dfs(board, aimsfood_x-1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x-1] = 0
                    if 0 <= aimsfood_y+1 < 33 and board[aimsfood_y+1][aimsfood_x] < 3 and check[aimsfood_y+1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y+1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y+1][aimsfood_x] = 0
            if min_gost[1] - aimsfood_x >= 0:
                if(min_gost[0] - aimsfood_y <= 0):
                    # print(min_gost)
                    # print("LD")
                    if 0 <= aimsfood_x-1 < 30 and board[aimsfood_y][aimsfood_x-1] < 3 and check[aimsfood_y][aimsfood_x-1] == 0:
                        temp = dfs(board, aimsfood_x-1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x-1] = 0
                    if 0 <= aimsfood_y+1 < 33 and board[aimsfood_y+1][aimsfood_x] < 3 and check[aimsfood_y+1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y+1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y+1][aimsfood_x] = 0
                    if 0 <= aimsfood_y-1 < 33 and board[aimsfood_y-1][aimsfood_x] < 3 and check[aimsfood_y-1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y-1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y-1][aimsfood_x] = 0
                    if 0 <= aimsfood_x+1 < 30 and board[aimsfood_y][aimsfood_x+1] < 3 and check[aimsfood_y][aimsfood_x+1] == 0:
                        temp = dfs(board, aimsfood_x+1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x+1] = 0
                else:
                    # print(min_gost)
                    # print("LU")
                    if 0 <= aimsfood_x-1 < 30 and board[aimsfood_y][aimsfood_x-1] < 3 and check[aimsfood_y][aimsfood_x-1] == 0:
                        temp = dfs(board, aimsfood_x-1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x-1] = 0
                    if 0 <= aimsfood_y-1 < 33 and board[aimsfood_y-1][aimsfood_x] < 3 and check[aimsfood_y-1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y-1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y-1][aimsfood_x] = 0
                    if 0 <= aimsfood_y+1 < 33 and board[aimsfood_y+1][aimsfood_x] < 3 and check[aimsfood_y+1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y+1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y+1][aimsfood_x] = 0
                    if 0 <= aimsfood_x+1 < 30 and board[aimsfood_y][aimsfood_x+1] < 3 and check[aimsfood_y][aimsfood_x+1] == 0:
                        temp = dfs(board, aimsfood_x+1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x+1] = 0
            if min_gost[1] - aimsfood_x <= 0:
                if(min_gost[0] - aimsfood_y <= 0):
                    # print(min_gost)
                    # print("RD")
                    if 0 <= aimsfood_x+1 < 30 and board[aimsfood_y][aimsfood_x+1] < 3 and check[aimsfood_y][aimsfood_x+1] == 0:
                        temp = dfs(board, aimsfood_x+1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x+1] = 0
                    if 0 <= aimsfood_y+1 < 33 and board[aimsfood_y+1][aimsfood_x] < 3 and check[aimsfood_y+1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y+1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y+1][aimsfood_x] = 0
                    if 0 <= aimsfood_y-1 < 33 and board[aimsfood_y-1][aimsfood_x] < 3 and check[aimsfood_y-1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y-1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y-1][aimsfood_x] = 0
                    if 0 <= aimsfood_x-1 < 30 and board[aimsfood_y][aimsfood_x-1] < 3 and check[aimsfood_y][aimsfood_x-1] == 0:
                        temp = dfs(board, aimsfood_x-1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x-1] = 0
                else:
                    # print(min_gost)
                    # print("RU")
                    if 0 <= aimsfood_x+1 < 30 and board[aimsfood_y][aimsfood_x+1] < 3 and check[aimsfood_y][aimsfood_x+1] == 0:
                        temp = dfs(board, aimsfood_x+1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x+1] = 0
                    if 0 <= aimsfood_y-1 < 33 and board[aimsfood_y-1][aimsfood_x] < 3 and check[aimsfood_y-1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y-1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y-1][aimsfood_x] = 0
                    if 0 <= aimsfood_y+1 < 33 and board[aimsfood_y+1][aimsfood_x] < 3 and check[aimsfood_y+1][aimsfood_x] == 0:
                        temp = dfs(board, aimsfood_x , aimsfood_y+1, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y+1][aimsfood_x] = 0
                    if 0 <= aimsfood_x-1 < 30 and board[aimsfood_y][aimsfood_x-1] < 3 and check[aimsfood_y][aimsfood_x-1] == 0:
                        temp = dfs(board, aimsfood_x-1, aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)
                        if(temp != None):
                                return temp
                        else:
                            check[aimsfood_y][aimsfood_x-1] = 0
            return None
            
        if(powerup):
            q = deque()
            q.append(start)
    # R, L, U, D
            while(True):
                cur = q.popleft()
                if((board[cur[0]][cur[1]] == 1 or level[cur[0]][cur[1]] == 2) and cur != start):
                    return cur
            
                if(0 <= cur[0] + 1 < 33 and board[cur[0] + 1][cur[1]] < 3 and check[cur[0] + 1][cur[1]] == 0):
                    q.append((cur[0] + 1,cur[1]))
                    check[cur[0] + 1][cur[1]] = 1

                if(0 <= cur[0] - 1 < 33 and board[cur[0] - 1][cur[1]] < 3 and check[cur[0] - 1][cur[1]] == 0):
                    q.append((cur[0] - 1,cur[1]))
                    check[cur[0] - 1][cur[1]] = 1

                if(0 <= cur[1] + 1 < 30 and board[cur[0]][cur[1] + 1] < 3 and check[cur[0]][cur[1] + 1] == 0):
                    q.append((cur[0],cur[1] + 1))
                    check[cur[0]][cur[1] + 1] = 1

                if(0 <= cur[1] - 1 < 30 and board[cur[0]][cur[1] - 1] < 3 and check[cur[0]][cur[1] - 1] == 0):
                    q.append((cur[0],cur[1] - 1))
                    check[cur[0]][cur[1] - 1] = 1
        else:
            return dfs(board, aimsfood_x , aimsfood_y, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, check)


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
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]


run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 5
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_board()
    center_x = player_x + 23
    center_y = player_y + 24
    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)

    turns_allowed = check_position(center_x, center_y)

    player = Player(player_x, player_y, direction, find, ways, d, blinky_x, blinky_y, blinky_dead, inky_x, inky_y, inky_dead, pinky_x, pinky_y, pinky_dead, clyde_x, clyde_y, clyde_dead, powerup)

    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                   blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead,
                 inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead,
                  pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead,
                  clyde_box, 3)
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

    if moving:
        player_x, player_y, aims_food, direction, find, ways, d = player.move_player(level, aims_food)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)
    # add to if not powerup to check if eaten ghosts
    if not powerup:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                (player_circle.colliderect(inky.rect) and not inky.dead) or \
                (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                (player_circle.colliderect(clyde.rect) and not clyde.dead):
            if lives > 0:
                print("DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD_DEAD")
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 450
                player_y = 663
                center_x = player_x + 23
                center_y = player_y + 24
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
                find = True
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
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead:
        if lives > 0:
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
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.dead:
        if lives > 0:
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
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:
        blinky_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]:
        inky_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:
        pinky_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:
        clyde_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (game_over or game_won):
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
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False

    draw_misc()

    pygame.display.flip()
pygame.quit()


# sound effects, restart and winning messages
