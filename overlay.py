import pygame
from settings import *


class Overlay:
    def __init__(self, character):

        # set up
        self.display_surface = pygame.display.get_surface()
        self.character = character

        # imports
        overlay_path = "./assets/textures/overlay/"
