import pygame
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        mouse_motion = pygame.mouse.get_pos()
        self.image = pygame.image.load('data/resources/graphics/sprites/player/player.png').convert_alpha()
        self.rect = self.image.get_rect(center=(mouse_motion[0], 700))

    def update(self):
        self.rect.x = pygame.mouse.get_pos()[0] - 37

    def create_bullet(self):
        shoot_sound = pygame.mixer.Sound('data/resources/audio/shoot.mp3')
        shoot_sound.set_volume(0.02)
        shoot_sound.play()
        return Bullet(pygame.mouse.get_pos()[0], self.rect.y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('data/resources/graphics/sprites/player/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= 10
        if self.rect.y <= -100:
            self.kill()

        # bullet collision
        if pygame.sprite.spritecollide(self, enemy_group, True):
            explosion_sound = pygame.mixer.Sound('data/resources/audio/medium-explosion.mp3')
            explosion_sound.set_volume(0.02)
            explosion_sound.play()
            self.kill()
            explosion_group.add(Explosion(self.rect.centerx, self.rect.centery))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speeds = [5, 7, 9]
        self.speed = randint(0, 2)
        if self.speed == 0:
            self.image = pygame.image.load('data/resources/graphics/sprites/enemy/enemy1.png').convert_alpha()
        if self.speed == 1:
            self.image = pygame.image.load('data/resources/graphics/sprites/enemy/enemy2.png').convert_alpha()
        if self.speed == 2:
            self.image = pygame.image.load('data/resources/graphics/sprites/enemy/enemy3.png').convert_alpha()

        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect(midbottom=(randint(40, 440), randint(-900, -200)))

    def update(self):
        self.rect.y += self.speeds[self.speed]
        if self.rect.y > 900:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []

        for ex in range(1, 8):
            image = pygame.image.load(f'data/resources/graphics/sprites/explosion/explosion{ex}.png')
            image = pygame.transform.scale2x(image)
            self.images.append(image)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = 0

    def update(self):
        explosion_speed = 3
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
explosion_group = pygame.sprite.GroupSingle()
