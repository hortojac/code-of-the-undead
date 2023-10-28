"""
Description: This script contains the Projectile class which is responsible for creating and updating the bullet sprites.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: September 28, 2023
Date Modified: October 28, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
import math
from settings import *

class Projectile(pygame.sprite.Sprite): # FIXME: Add bullet sprites to this classes using the above method.
    def __init__(self, pos, velocity, group):
        super().__init__(group)
        self.velocity = velocity # Velocity of the bullet
        image = pygame.image.load("assets/textures/character/bulletone.png")# Loads image for bullet
        rotate_angle = math.atan(self.velocity.y/self.velocity.x) * 180 / math.pi - 90 # Calculates angle to rotate bullet by (in degrees)
        self.image = pygame.transform.rotate(image, rotate_angle) # Sets sprite image to rotated bullet
        self.rect = self.image.get_rect(center=pos) # Set the rect attribute of the bullet
        self.pos = pygame.math.Vector2(pos) # Set the pos attribute of the bullet
        self.z = LAYERS['bullet'] # Set the z attribute of the bullet

    def update(self, dt):
        self.pos += self.velocity * dt # Update the position of the bullet
        self.rect.center = self.pos # Update the rect attribute of the bullet
        if not MAP_BOUNDARY.colliderect(self.rect):  # Check against the map boundary instead of screen rect
            self.kill() # Kill the bullet if it is outside the map boundary