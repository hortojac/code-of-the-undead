import pygame
from pygame import gfxdraw

class Character:
    def __init__(self, screen):
        self.screen = screen
        self.color = (255, 0, 0)  # Red color for the circle
        self.radius = 25  # Radius of the circle
        self.x = self.screen.get_width() // 2  # Initial x-coordinate in the middle
        self.y = self.screen.get_height() // 2  # Initial y-coordinate in the middle

    def draw(self):
        # pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius, 1)
        gfxdraw.aacircle(self.screen, self.x, self.y, self.radius, self.color)
        gfxdraw.filled_circle(self.screen, self.x, self.y, self.radius, self.color)

