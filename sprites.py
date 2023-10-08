"""
Description: This script contains the Generic class, which is used to create generic sprites.
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

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['background']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
