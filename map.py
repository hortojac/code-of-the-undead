import pygame
from settings import *
from character import Character

class Map:
    def __init__(self):
        self.grid_size = 64 # Size of each tile in the tile map
        self.rows = 5  # Number of rows in the tile map
        self.columns = 5  # Number of columns in the tile map
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.setup()

    def setup(self):
        self.character = Character((640, 360), self.all_sprites)

    def calculate_offset(self):
        # Calculate the offset of the tile map in the x and y direction
        self.offset_x = (SCREEN_WIDTH - self.grid_size * self.columns) // 2
        self.offset_y = (SCREEN_HEIGHT - self.grid_size * self.rows) // 2

    def run(self, dt):
        self.calculate_offset()
        self.display_surface.fill((255, 255, 255))
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
        

