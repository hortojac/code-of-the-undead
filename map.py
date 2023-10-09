"""
Description: This script contains the Map class which is responsible for drawing the tile map and all sprites.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: September 19, 2023
Date Modified: October 08, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
from typing import List, Optional
import pygame

from pygame.rect import Rect
from pygame.surface import Surface
from settings import *
from character import Character
from enemy import Enemy
from sprites import Generic

class Map:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.setup()

    def setup(self):
        Generic(pos=(0, 0), surf=pygame.image.load(
            './assets/Test_map/map.png').convert_alpha(), groups=self.all_sprites, z=LAYERS['background'])
        self.character = Character((640, 360), self.all_sprites)
        self.enemy_one = Enemy((0,0))

    def run(self, dt):
        # Fill the display surface with a background color (white)
        self.display_surface.fill('white')

        if self.character.rect.colliderect(self.enemy_one.rect) : # If the enemy and player collide
            self.character.health_bool = False
        else:
            self.character.health_bool = True

        # Draw all sprites on top of the grid
        self.all_sprites.custom_draw(self.character) # Draw character on top of map
        self.enemy_one.draw() # Draw enemy
        self.character.draw_stamina_bar(self.display_surface, dt) # Draw stamina bar
        self.character.draw_health_bar(self.display_surface, dt) # Draw health bar
        self.all_sprites.update(dt) # update all sprites
        self.enemy_one.update(self.character.pos, dt)  # update enemyone

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w 
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, character):
        self.center_target_camera(character) # Center camera on player

        # Active elements
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft - self.offset
                    self.display_surface.blit(sprite.image, offset_pos)
