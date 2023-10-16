"""
Description: This script contains the Zombie class, which is used to create enemies.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: October 08, 2023
Date Modified: October 13, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
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
        self.direction = pygame.math.Vector2(0,0) # Initialize the direction vector
        self.pos = pygame.math.Vector2(self.rect.center) # Initialize the position vector
        self.speed = 10  # Speed of the zombie

        # Zombie stats
        self.health = 10 # Health of the zombie

        # Booleans to determine the status of the zombie
        self.attack_bool = False # Boolean to determine if the zombie is attacking
        self.death_bool = False # Boolean to determine if the zombie is dead  

    def import_assets(self):
        # Imports zombie animations from sprite sheets.
        self.animations = {
            'up': [], 'down': [], 'right': [], 'left': [],
            'up_idle': [], 'down_idle': [], 'right_idle': [], 'left_idle': [],
            'up_attack': [], 'down_attack': [], 'right_attack': [], 'left_attack': [],
            'up_death': [], 'down_death': [], 'right_death': [], 'left_death': []
        }
        
        # Define sprite sheet configurations
        sprite_sheets = {
            './assets/textures/zombie/zombie_walk.png': {
                'rows': 4, 'cols': 10, 'animations': ['down', 'up', 'right', 'left']
            },
            './assets/textures/zombie/zombie_idle.png': {
                'rows': 4, 'cols': 5, 'animations': ['down_idle', 'up_idle', 'right_idle', 'left_idle']
            },
            './assets/textures/zombie/zombie_attack.png': {
                'rows': 4, 'cols': 8, 'animations': ['down_attack', 'up_attack', 'right_attack', 'left_attack']
            },
            './assets/textures/zombie/zombie_death.png': {
                'rows': 4, 'cols': 7, 'animations': ['down_death', 'up_death', 'right_death', 'left_death']
            }
        }
        
        for path, config in sprite_sheets.items():
            sprite_sheet = pygame.image.load(path).convert_alpha()
            sprite_width = sprite_sheet.get_width() // config['cols']
            sprite_height = sprite_sheet.get_height() // config['rows']
            
            # Ensure the number of animations matches the number of rows
            if len(config['animations']) != config['rows']:
                raise ValueError(f"Number of animations for {path} does not match the number of rows.")
            
            for row in range(config['rows']):
                for col in range(config['cols']):
                    x = col * sprite_width
                    y = row * sprite_height
                    sprite = sprite_sheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))
                    self.animations[config['animations'][row]].append(sprite)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.death_bool: 
            if self.frame_index >= len(self.animations[self.status]) - 1: 
                self.frame_index = len(self.animations[self.status]) - 1 # Stop at the last frame
        else:
            if self.frame_index >= len(self.animations[self.status]):
                self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def character_input(self, character_pos):
        self.direction = pygame.math.Vector2(0,0)
        # Get the direction vector to the character
        self.direction_to_character = character_pos - self.pos
        # Set the direction vector and status based on character movement
        if not self.death_bool: # Ensure the zombie sprite doesn't flip if it's in its death state
            if self.direction_to_character.x < 0:
                self.direction.x = -1
                self.status = 'left'
            elif self.direction_to_character.x > 0:
                self.direction.x = 1
                self.status = 'right'
            if self.direction_to_character.y < 0:
                self.direction.y = -1
                if self.direction.x == 0:
                    self.status = 'up'
            elif self.direction_to_character.y > 0:
                self.direction.y = 1
                if self.direction.x == 0:
                    self.status = 'down'

    def kill_zombie(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.death_bool = True
            self.direction.magnitude() == 0
            self.direction_to_character == 0
            # TODO: Add self.kill()? 

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        if self.attack_bool:
            self.status = self.status.split('_')[0] + '_attack'
        if self.death_bool:
            self.status = self.status.split('_')[0] + '_death'

    def move(self, dt):
        # Normalize the direction vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = round(self.pos.x) # Round the value before updating

        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = round(self.pos.y) # Round the value before updating

    def update(self, dt):
        if not self.death_bool:
            self.move(dt) # Only move if not in the death state
        self.get_status()
        self.animate(dt)
        

