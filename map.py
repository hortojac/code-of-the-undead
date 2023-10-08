"""
Description: This script contains the Map class which is responsible for drawing the tile map and all sprites.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: September 19, 2023
Date Modified: October 04, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
from typing import List, Optional
import pygame
import sys

from pygame.rect import Rect
from pygame.surface import Surface
from settings import *
from character import Character
from sprites import Generic


class Map:
    def __init__(self):
        '''self.grid_size = 32  # Size of each tile in the tile map
        self.rows = 15  # Number of rows in the tile map
        self.columns = 15  # Number of columns in the tile map'''
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        '''self.base_tile_sheet = pygame.image.load(
            "./assets/tile_floor_updated.png")  # Load the base tile sheet image
        self.tile_size = (32, 32)  # Size of each tile in the sheet'''
        # Create a 2D array to represent the tile map
        # self.tile_map = self.create_tile_map()
        self.setup()

    def setup(self):
        Generic(pos=(0, 0), surf=pygame.image.load(
            './assets/Test_map/map.png').convert_alpha(), groups=self.all_sprites, z=LAYERS['background'])
        self.character = Character(
            ((640, 360)), self.all_sprites)

    '''def calculate_offset(self):
        # Calculate the offset of the tile map in the x and y direction
        self.offset_x = (SCREEN_WIDTH - self.grid_size * self.columns) // 2
        self.offset_y = (SCREEN_HEIGHT - self.grid_size * self.rows) // 2'''

    '''def create_tile_map(self):
        # Create a 2D array to represent the tile map (initialize with the base tile)
        tile_map = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        return tile_map'''

    def run(self, dt):
        # self.calculate_offset()
        # Fill the display surface with a background color (white)
        self.display_surface.fill('white')

        # Draw the tiles based on the tile map
        '''for row in range(self.rows):
            for col in range(self.columns):
                x = self.offset_x + col * self.grid_size
                y = self.offset_y + row * self.grid_size
                tile_image = self.base_tile_sheet.subsurface(
                    pygame.Rect(0, 0, self.tile_size[0], self.tile_size[1]))

        # Draw the base tile on the display surface
        self.display_surface.blit(tile_image, (x, y))

        # Draw a test rectangle
        self.test_rect = pygame.Rect(
            (SCREEN_WIDTH // 1.2), (SCREEN_HEIGHT // 2), 32, 32)
        pygame.draw.rect(self.display_surface, (255, 0, 0), self.test_rect)

        if self.character.rect.colliderect(self.test_rect):
            self.character.health -= 20 * dt * 1.25
        if self.character.health <= 0:
            self.character.health = 0
            pygame.quit()
            sys.exit()

        else:
            self.character.health += 10 * dt * 1.25
            if self.character.health >= self.character.max_health:
                self.character.health = self.character.max_health'''

        # Draw a test rectangle
        self.test_rect = pygame.Rect((SCREEN_WIDTH // 1.2), (SCREEN_HEIGHT // 2), 32, 32)
        pygame.draw.rect(self.display_surface, (255, 0, 0), self.test_rect)

        if self.character.rect.colliderect(self.test_rect):
            self.character.health -= 20  * dt * 1.25
            if self.character.health <= 0:
                self.character.health = 0
                pygame.quit()
                sys.exit()
        else:
            self.character.health += 10 * dt * 1.25
            if self.character.health >= self.character.max_health:
                self.character.health = self.character.max_health

        # Draw all sprites on top of the grid

       # self.all_sprites.draw(self.display_surface)
        self.all_sprites.custom_draw(self.character)
        self.character.draw_stamina_bar(self.display_surface)
        self.character.draw_health_bar(self.display_surface)
        self.all_sprites.update(dt)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, character):

        self.center_target_camera(character)

        # active elements
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft - self.offset
                    self.display_surface.blit(sprite.image, offset_pos)


'''class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, character):
        self.offset.x = character.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = character.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, sprite.rect)'''
