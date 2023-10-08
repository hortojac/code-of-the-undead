"""
Description: This script contains the Map class which is responsible for drawing the tile map and all sprites.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: September 19, 2023
Date Modified: October 06, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
from settings import *
from character import Character
from enemy import Enemy

class Map:
    def __init__(self):
        self.grid_size = 32  # Size of each tile in the tile map
        self.rows = 15  # Number of rows in the tile map
        self.columns = 15  # Number of columns in the tile map
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.base_tile_sheet = pygame.image.load("./assets/tile_floor_updated.png")  # Load the base tile sheet image
        self.tile_size = (32, 32)  # Size of each tile in the sheet
        self.tile_map = self.create_tile_map()  # Create a 2D array to represent the tile map
        self.setup()

    def setup(self):
        self.character = Character(((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)), self.all_sprites)
        self.enemy_one = Enemy((0,0))

    def calculate_offset(self):
        # Calculate the offset of the tile map in the x and y direction
        self.offset_x = (SCREEN_WIDTH - self.grid_size * self.columns) // 2
        self.offset_y = (SCREEN_HEIGHT - self.grid_size * self.rows) // 2

    def create_tile_map(self):
        # Create a 2D array to represent the tile map (initialize with the base tile)
        tile_map = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        return tile_map

    def run(self, dt):
        self.calculate_offset()
        # Fill the display surface with a background color (white)
        self.display_surface.fill((255, 255, 255))

        # Draw the tiles based on the tile map
        for row in range(self.rows):
            for col in range(self.columns):
                x = self.offset_x + col * self.grid_size
                y = self.offset_y + row * self.grid_size
                tile_image = self.base_tile_sheet.subsurface(pygame.Rect(0, 0, self.tile_size[0], self.tile_size[1]))

                # Draw the base tile on the display surface
                self.display_surface.blit(tile_image, (x, y))

        self.enemy_one.update(self.character.pos)  # update enemyone
        if self.character.rect.colliderect(self.enemy_one.rect) : # If the enemy and player collide
            self.character.health_bool = False
        else:
            self.character.health_bool = True

        self.enemy_one.draw() # Draw the enemy

        # Draw all sprites on top of the grid
        self.character.draw_stamina_bar(self.display_surface, dt)
        self.character.draw_health_bar(self.display_surface, dt)
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)


        






        

