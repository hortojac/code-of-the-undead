"""
Description: This script contains the Map class which is responsible for drawing the tile map and all sprites.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: September 19, 2023
Date Modified: October 09, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
from typing import List, Optional
import pygame
import math
import openai
import os
from pygame.rect import Rect
from pygame.surface import Surface
from settings import *
from character import Character
from zombie import Zombie
from npc import NPC 
from sprites import Generic

openai_api_key = os.environ.get('OPENAI_API_KEY')

class Map:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()

        self.font = pygame.font.Font(None, 32)
        self.input_text = ""
        self.output_text = ""
        self.input_rect = pygame.Rect(50, 400, 200, 100)
        self.output_rect = pygame.Rect(50, 510, 200, 100)
        self.cursor_visible = True
        self.cursor_time = pygame.time.get_ticks()
        self.text_box_active = False

        self.setup()

    def setup(self):
        Generic(pos=(0, 0), surf=pygame.image.load(
            './assets/Test_map/map.png').convert_alpha(), groups=self.all_sprites, z=LAYERS['background'])
        self.character = Character(((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)), self.all_sprites)
        self.zombie = Zombie((0,0), self.all_sprites)
        self.npc = NPC(((SCREEN_WIDTH // 2 + 100), (SCREEN_HEIGHT // 2 + 200)), self.all_sprites)

    def run(self, dt):
        # Fill the display surface with a background color (white)
        self.display_surface.fill('white')

        if self.character.rect.colliderect(self.zombie.rect) : # If the enemy and player collide
            self.character.health_bool = False
            self.zombie.attack_bool = True
            self.zombie.kill_zombie(1)
        else:
            self.character.health_bool = True
            self.zombie.attack_bool = False

        if self.character.delete_enemy: # TODO : Remove this, just for testing purposes
            self.zombie.pos = pygame.math.Vector2(0,0)

        for bullet in self.character.bullets:
            bullet.draw()
            if bullet.rect.colliderect(self.zombie.rect):
                self.zombie.kill_zombie(1)
                print("collide")

        # Draw all sprites on top of the grid
        self.all_sprites.custom_draw(self.character) # Draw character on top of map
        self.character.draw_stamina_bar(self.display_surface, dt) # Draw stamina bar
        self.character.draw_health_bar(self.display_surface, dt) # Draw health bar
        self.zombie.character_input(self.character.pos) # Send character position to zombie
        self.all_sprites.update(dt) # update all sprites

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

