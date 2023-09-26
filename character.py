import pygame

from settings import *
from support import *


class Character(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # Set the image and rect attributes for the character
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # Movement of the character
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 0 # Initialize speed to 0
        self.walking_speed = 100  # Waling speed
        self.sprinting_speed = 200  # Sprinting speed

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'right': [], 'left': [
        ], 'up_idle': [], 'down_idle': [], 'right_idle': [], 'left_idle': []}
        # Import all the animations
        for animation in self.animations.keys():
            full_path = "./assets/textures/character/" + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        # Check for keys that are continuously pressed
        keys = pygame.key.get_pressed()
        # Initialize direction vector
        self.direction = pygame.math.Vector2(0, 0)
        # Check for sprinting (SHIFT key)
        sprinting = keys[KEY_SPRINT]
        # Set the direction vector and status based on the keys pressed
        if keys[KEY_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[KEY_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        if keys[KEY_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[KEY_DOWN]:
            self.direction.y = 1
            self.status = 'down'

        # Adjust speed based on sprinting state
        if sprinting:
            self.speed = self.sprinting_speed
        else:
            self.speed = self.walking_speed

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

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
        self.get_status()
        self.move(dt)
        self.animate(dt)
