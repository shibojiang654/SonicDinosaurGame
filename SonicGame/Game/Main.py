import pygame
import os
import random
import shelve
from pygame import display

from pygame.constants import K_SPACE
pygame.init()

# Global Constants
#Sets ups the dimensions for the screen
HEIGHT_OF_SCREEN = 720
WIDTH_OF_SCREEN = 1280
GAME_DISPLAY = pygame.display.set_mode((WIDTH_OF_SCREEN, HEIGHT_OF_SCREEN))

#All of the Global Constants for the images used in game. Them being in a list allows us to switch between pictures easier later on, and to randomize the obtacles that appear.
GROUND = pygame.image.load(os.path.join("Things/Background", "Ground.png"))
SMALL_CACTI = [pygame.image.load(os.path.join("Things/Cactus", "SmallOne-Cacti.png")), pygame.image.load(os.path.join("Things/Cactus", "SmallTwo-Cacti.png")), pygame.image.load(os.path.join("Things/Cactus", "SmallThree-Cacti.png"))]
PTERODACTYL = [pygame.image.load(os.path.join("Things/Pterodactyl", "BirdOne.png")), pygame.image.load(os.path.join("Things/Pterodactyl", "BirdTwo.png"))]

#All images below relate to the Sprite (Like different costumes for the sprite)
SPRITE_RUNNING = [pygame.image.load(os.path.join("Things/Sprite", "RunOne-Sprite.png")), pygame.image.load(os.path.join("Things/Sprite", "RunTwo-Sprite.png"))]
SPRITE_JUMPING = pygame.image.load(os.path.join("Things/Sprite", "Jump-Sprite.png"))
SPRITE_DUCKING = [pygame.image.load(os.path.join("Things/Sprite", "DuckOne-Sprite.png")), pygame.image.load(os.path.join("Things/Sprite", "DuckTwo-Sprite.png"))]

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
            obstacles.pop()

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

def main():
    global map_speed, xgroundposition, ygroundposition, points, obstacles
    game = True
    xgroundposition = 0
    ygroundposition = 375
    clock = pygame.time.Clock()
    player = Sprite()
    map_speed = 14
    points = 0
    font = pygame.font.SysFont("Arial", 30)
    obstacles = []
    death_amount = 0

    def score():
        global points, map_speed
        points += 1
        if points % 100 == 0:
            map_speed += 1
        text = font.render("Points: " + str(points), True , (0,0,139))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        GAME_DISPLAY.blit(text, textRect)

    def ground():
        global xgroundposition, ygroundposition
        image_width = GROUND.get_width()
        GAME_DISPLAY.blit(GROUND, (xgroundposition, ygroundposition))
        GAME_DISPLAY.blit(GROUND, (image_width + xgroundposition, ygroundposition))
        if xgroundposition <= -image_width:
            GAME_DISPLAY.blit(GROUND, (image_width + xgroundposition, ygroundposition))
            xgroundposition = 0
        xgroundposition -= map_speed

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

        GAME_DISPLAY.fill((173,216,230))
        input = pygame.key.get_pressed()

        player.draw(GAME_DISPLAY)
        player.update(input)

        for obstacle in obstacles:
            obstacle.draw(GAME_DISPLAY)
            obstacle.update()
            if player.sprite_hitbox.colliderect(obstacle.rect):
                death_amount += 1
                frontpage(death_amount)
        
        if len(obstacles) == 0:
            if random.randint(0, 3) == 0:
                obstacles.append(SmallCacti(SMALL_CACTI))
            elif random.randint(0, 3) == 1:
                obstacles.append(Pterodactyl(PTERODACTYL))
            elif random.randint(0, 3) == 2:
                obstacles.append(Pterodactyl2(PTERODACTYL))
            elif random.randint(0, 3) == 3:
                obstacles.append(SmallCacti(SMALL_CACTI))
                       
        ground()

        score()

        clock.tick(50)
        pygame.display.update()

def compare(points, high_scr):
    if points > high_scr:
        return points
    else:
        return high_scr

def high_score(points):
    d = shelve.open('highscore.txt')     
    high_scr = d['score']
    d['score'] = compare(points, high_scr) 
    if points > high_scr:
        high_scr = points
    return high_scr

def frontpage(death_amount):
    global points
    game = True
    while game:
        font = pygame.font.SysFont("Arial", 30)
        GAME_DISPLAY.fill((255,215,0))
        if death_amount == 0:
            text = font.render("Press a Key to Start", True, (65,105,225))
        elif death_amount > 0:
            score = font.render("High Score: " + str(high_score(points)), True, (65,105,225))
            scoreRect = score.get_rect()
            scoreRect.center = (WIDTH_OF_SCREEN // 2, HEIGHT_OF_SCREEN // 2 + 100)
            GAME_DISPLAY.blit(score, scoreRect)
            score = font.render("Score: " + str(points), True, (65,105,225))
            scoreRect = score.get_rect()
            scoreRect.center = (WIDTH_OF_SCREEN // 2, HEIGHT_OF_SCREEN // 2 + 50)
            GAME_DISPLAY.blit(score, scoreRect)
            text = font.render("Press a Key to Restart", True, (65,105,225))
        textRect = text.get_rect()
        textRect.center = (WIDTH_OF_SCREEN // 2, HEIGHT_OF_SCREEN // 2)
        GAME_DISPLAY.blit(text, textRect)
        pygame.display.update()
        for instance in pygame.event.get():
            if instance.type == pygame.KEYDOWN:
                main()
            if instance.type == pygame.QUIT:
                game = False
                pygame.quit()
                quit()

frontpage(death_amount = 0)