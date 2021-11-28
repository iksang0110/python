import random
from time import sleep

import pygame
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640

BLACK = (0,0,0)
WHITE = (225,225,225)
YELLOW = (250,250,50)
RED = (250, 50, 50)

FPS = 60

class Fighter(pygame.sprite.Sprite):
    def __ini__(self):
        super(Fighter,self).__init__()
        self.image = pygame.image.load('fighter.png')
        self.rect =self.image.get.rect()
        self.rect.x = int(WINDOW_WIDTH / 2)
        self.rect.y = WINDOW_HEIGHT - self.rect.height
        self.dx = 0
        self.dy = 0
    
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
            self.rect.x -= self.dx

        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite


class Missile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Missile, self).__init__()
        self.image = pygame.image.load('missile.png')
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound('missile.wav')

    def launch(self):
        self.sound.play()

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0:
            self.kill()


    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite


class Rock(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Rock, self).__init__()
        rock_images = ('rock01.png','rock02.png','rock03.png','rock04.png','rock05.png','rock06.png','rock07.png','rock08.png','rock09.png','rock10.png',)
        self.image = pygame.image.load(random.choice(rock_images))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
    
    def update(self):
        self.rect.y += self.speed

    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            return True


def draw_text(text, font, surface, x,y,main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)


def occur_explosion(surface,x,y):
    explosion_image = pygame.image.load('explosion.png')
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image,explosion_rect)

    explosion_sounds = ('explosion01.wav','explosion02.wav','explosion03.wav',)
    explosion_sound =  pygame.mixer.Sound(random.choice(explosion_sounds))
    explosion_sounds.play()


def game_loop():
    default_font = pygame.font.Font('NanumGothic.ttf', 28)
    background_image = pygame.image.load('background.png')
    gameover_sound = pygame.mixer.Sound('gameover.wav')
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1)
    fps_clock = pygame.itme.Clock()

    fighter = Fighter()
    missile = pygame.sprite.Group()
    rocks = pygame.sprite.Group()

    occur_prob = 40
    shot_count = 0
    count_missed = 0

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if __name__ == '__main__':
                    if event.key == pygame.K_LEFT:
                        fighter.dx -= 5
                    elif event.key == pygame.K_RIGHT:
                        fighter.dx += 5
                    elif event.key == pygame.K_UP:
                        fighter.dy -= 5
                    elif event.key == pygame.K_DOWN:
                        fighter.dy += 5
                    elif event.key == pygame.K_SPACE:
                        missile = Missile(fighter.rect.centerx, fighter.rect.y, 10)
                        missile.launch()
                        missile.add(missile)