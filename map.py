import pygame

class Map:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.grid_size = 64 # Size of each tile in the tile map
        self.rows = 5  # Number of rows in the tile map
        self.columns = 5  # Number of columns in the tile map

    def calculate_offset(self):
        # Calculate the offset of the tile map in the x and y direction
        self.offset_x = (self.settings.screen_width - self.grid_size * self.columns) // 2
        self.offset_y = (self.settings.screen_height - self.grid_size * self.rows) // 2

    def draw(self):
        self.calculate_offset()
        # Draw the tile map
        for row in range(self.rows):
            for col in range(self.columns):
                x = self.offset_x + col * self.grid_size
                y = self.offset_y + row * self.grid_size
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.grid_size, self.grid_size), 1)


