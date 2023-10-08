"""
Description: This script contains the Overlay class, which is used to create the overlays.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: October 08, 2023
Date Modified: October 08, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

import pygame
from settings import *

class Overlay:
    def __init__(self, character):

        # set up
        self.display_surface = pygame.display.get_surface()
        self.character = character

        # imports
        overlay_path = "./assets/textures/overlay/"
