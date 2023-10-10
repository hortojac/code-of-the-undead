"""
Description: This script contains the Zombie class, which is used to create enemies.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: October 08, 2023
Date Modified: October 09, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
import sys
from settings import *
from support import *

class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # Call the import_assets method to import all the animations
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # Set the image and rect attributes for the zombie
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['zombie']

        # Movement of the zombie
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 25  # Speed of the zombie

        self.health = 10 # Health of the zombie

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'right': [], 'left': [
        ], 'up_idle': [], 'down_idle': [], 'right_idle': [], 'left_idle': []}
        # Import all the animations
        for animation in self.animations.keys():
            full_path = "./assets/textures/zombie/" + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def character_input(self, character_pos):
        # Initialize direction vector
        self.direction = pygame.math.Vector2(0, 0)
        # Get the direction vector to the character
        direction_to_character = character_pos - self.pos
        # Set the direction vector and status based on character movement
        if direction_to_character.x < 0:
            self.direction.x = -1
            self.status = 'left'
        elif direction_to_character.x > 0:
            self.direction.x = 1
            self.status = 'right'
        if direction_to_character.y < 0:
            self.direction.y = -1
            if self.direction.x == 0:
                self.status = 'up'
        elif direction_to_character.y > 0:
            self.direction.y = 1
            if self.direction.x == 0:
                self.status = 'down'

    def hurt(self, damage):
        self.health -= damage
        if self.health <= 0:
            pygame.quit() #TODO : Need to add death animation and remove sprite from group
            sys.exit()
        
    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def move(self, dt):
        # Normalize the direction vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = round(self.pos.x)  # Round the value before updating

        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = round(self.pos.y)  # Round the value before updating
 
    def update(self, dt):
        self.move(dt)
        self.get_status()
        self.animate(dt)
