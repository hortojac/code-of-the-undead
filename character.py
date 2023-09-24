import pygame

from settings import *
from support import import_folder

class Character(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.import_assets()

        self.image = pygame.Surface((32, 64))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=pos)

        # Movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def import_assets(self):
        self.animations = {}

        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        # Check for keys that are continuously pressed
        keys = pygame.key.get_pressed()
        
        # Initialize direction vector
        self.direction = pygame.math.Vector2(0, 0)

        if keys[KEY_LEFT]:
            if keys[KEY_SPRINT]:
                self.direction.x = -2
            else:
                self.direction.x = -1
        elif keys[KEY_RIGHT]:
            if keys[KEY_SPRINT]:
                self.direction.x = 2
            else:
                self.direction.x = 1

        if keys[KEY_UP]:
            if keys[KEY_SPRINT]:
                self.direction.y = -2
            else:
                self.direction.y = -1
        elif keys[KEY_DOWN]:
            if keys[KEY_SPRINT]:
                self.direction.y = 2
            else:
                self.direction.y = 1

    def move(self, dt):
        # Normalize the direction vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.move(dt)