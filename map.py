import pygame

class Map:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen

    def draw(self):
        grid_size = 64
        for x in range(0, self.settings.screen_width, grid_size):
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.settings.screen_height))
        for y in range(0, self.settings.screen_height, grid_size):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.settings.screen_width, y))
