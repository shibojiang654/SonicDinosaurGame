import pygame
import os
import random
from Main import main
from Functions import *

class Sprite:
    XPOSITION = 80
    YPOSITION = 300
    YPOSITIONDUCK = 310
    JUMP_HEIGHT = 9.5

    def __init__(self):
        self.run_picture = SPRITE_RUNNING
        self.jump_picture = SPRITE_JUMPING
        self.duck_picture = SPRITE_DUCKING

        self.running = True
        self.jumping = False
        self.ducking = False

        self.steps = 0
        self.jump_height = self.JUMP_HEIGHT
        self.image = self.run_picture[0]
        self.sprite_hitbox = self.image.get_rect()
        self.sprite_hitbox.x = self.XPOSITION
        self.sprite_hitbox.y = self.YPOSITION

    def update(self, input):

        if (input[pygame.K_UP] and not self.ducking) and not self.jumping:
            self.running = False
            self.jumping = True
            self.ducking = False
       
        if (input[pygame.K_SPACE] and not self.ducking) and not self.jumping:
            self.running = False
            self.jumping = True
            self.ducking = False

        if input[pygame.K_DOWN] and not self.jumping:
            self.running = False
            self.jumping = False
            self.ducking = True

        if self.ducking and input[pygame.K_UP]:
            self.running = False
            self.jumping = False
            self.ducking = True

        if self.ducking and input[pygame.K_SPACE]:
            self.running = False
            self.jumping = False
            self.ducking = True
        
        if not (self.jumping or input[pygame.K_DOWN]):
            self.running = True
            self.jumping = False
            self.ducking = False

        if self.running:
            self.run()

        if self.jumping:
            self.jump()

        if self.ducking:
            self.duck()

        if self.steps >= 10:
            self.steps = 0
            
    def run(self):
        self.image = self.run_picture[self.steps // 5]
        self.sprite_hitbox = self.image.get_rect()
        self.sprite_hitbox.x = self.XPOSITION
        self.sprite_hitbox.y = self.YPOSITION
        self.steps += 1

    def duck(self):
        self.image = self.duck_picture[self.steps // 5]
        self.sprite_hitbox = self.image.get_rect()
        self.sprite_hitbox.x = self.XPOSITION
        self.sprite_hitbox.y = self.YPOSITIONDUCK
        self.steps += 1
    
    def jump(self):
        self.image = self.jump_picture
        if self.jumping:
            self.sprite_hitbox.y -= self.jump_height * 3
            self.jump_height -= 0.9
        if self.jump_height < - self.JUMP_HEIGHT:
            self.jumping = False
            self.jump_height = self.JUMP_HEIGHT

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.sprite_hitbox.x, self.sprite_hitbox.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = WIDTH_OF_SCREEN

    def update(self):
        self.rect.x -= map_speed
        if self.rect.x < -self.rect.width:
            main.obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class Pterodactyl(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(100, 242)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
                self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class Pterodactyl2(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 300
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class SmallCacti(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 315