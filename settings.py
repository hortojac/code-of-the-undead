import pygame

class Settings:

    def __init__(self):
        pygame.init()  # Initialize Pygame
        info = pygame.display.Info()  # Get monitor info

        # Set the screen width and height to the monitor's size
        self.screen_width = info.current_w
        self.screen_height = info.current_h

        self.bg_color = (225, 225, 225)

        # Set the FPS
        self.FPS = 60
