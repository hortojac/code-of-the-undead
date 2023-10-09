"""
Description: This script contains the Enemy class, which is used to create enemies.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: October 08, 2023
Date Modified: October 08, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
import sys
from settings import *

class Enemy:
    # Initialize
    def __init__(self, pos):
        self.image = pygame.image.load("./assets/textures/zombie_test.png")  # Load image
        self.health = 10  # Set enemy health
        self.rect = self.image.get_rect(center=pos)  # Make a rect that matches image
        self.pos = pygame.math.Vector2(self.rect.center)  # Set position
        self.z = LAYERS['enemy']  # Set layer
        self.speed = 50  # Movement speed

    def update(self, player_pos, dt):
        # Calculate direction vector towards player
        direction = pygame.math.Vector2(player_pos) - self.pos
        if direction.length() > 0:  # Avoid division by zero
            direction.normalize_ip()  # Normalize the vector (length of 1)
            self.pos += direction * self.speed * dt  # Move towards player
            self.rect.center = self.pos  # Update rect position

        if self.health <= 0:  # If enemy has no health
            pygame.quit()  # Close game
            sys.exit()  # End game

    def hurt(self, damage):
        self.health -= damage

    def draw(self):
        surface = pygame.display.get_surface()  # Get the surface
        surface.blit(self.image, self.rect.topleft)  # Print the image using top-left as reference
