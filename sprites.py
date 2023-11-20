"""
Description: This script contains the Generic class, which is used to create generic sprites.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: October 08, 2023
Date Modified: October 08, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

import pygame
import threading
import time
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['background']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


class AttackSprite(pygame.sprite.Sprite):
    def __init__(self, pos, group, z=LAYERS['foreground']):
        super().__init__(group)
        self.pos = pygame.math.Vector2(pos)
        self.camera_group = group
        self.image = pygame.image.load(
            "assets/textures/character/bulletone.png")
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        self.lifetime = .1  # Lifetime in milliseconds

    def update(self, dt):
        self.pos
        self.rect.center = self.pos
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
