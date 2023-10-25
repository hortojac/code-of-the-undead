"""
Description: This script contains the NPC class for the game which is used to create NPCs.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: October 08, 2023
Date Modified: October 25, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
import threading
import time
from settings import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, group, character):
        super().__init__(group)

        self.character = character  # Store a reference to the character

        # Call the import_assets method to import all the animations
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # Set the image and rect attributes for the npc
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['npc']

        # Movement of the npc
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 0 # Initialize speed to 0
        self.walking_speed = 100  # Waling speed
        self.sprinting_speed = 200  # Sprinting speed

        # Stamina variables
        self.max_stamina = 100  # Initial maximum stamina value
        self.stamina = self.max_stamina  # Current stamina value
        self.stamina_regen_rate = 10  # Stamina regeneration rate per second
        self.stamina_degen_rate = 20  # Stamina degeneration rate per second

        # Health variables
        self.death_bool = False # Boolean to check if character is dead or not
        self.health_bool = True # Boolean to check if character is losing health or not
        self.max_health = 100  # Initial maximum health value
        self.health = self.max_health  # Current health value
        self.health_regen_rate = 1  # Health regeneration rate per second
        self.health_degen_rate = 25  # Health degeneration rate per second

        self.max_distance = 32 # Maximum distance from the character

    def import_assets(self):
        # Imports npc animations from sprite sheets
        self.animations = {
            'up': [], 'down': [], 'right': [], 'left': [],
            'up_idle': [], 'down_idle': [], 'right_idle': [], 'left_idle': [],
            'up_death': [], 'down_death': [], 'right_death': [], 'left_death': []
        }
        
        # Define sprite sheet configurations
        sprite_sheets = {
            './assets/textures/npc/npc_walk.png': {
                'rows': 4, 'cols': 4, 'animations': ['down', 'up', 'right', 'left']
            },
            './assets/textures/npc/npc_idle.png': {
                'rows': 4, 'cols': 2, 'animations': ['down_idle', 'up_idle', 'right_idle', 'left_idle']
            },
            './assets/textures/npc/npc_death.png': {
                'rows': 4, 'cols': 4, 'animations': ['down_death', 'up_death', 'right_death', 'left_death']
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
        if self.speed == self.walking_speed:
            self.frame_index += 4 * dt
        elif self.speed == self.sprinting_speed:
            self.frame_index += 8 * dt
        if self.death_bool: 
            if self.frame_index >= len(self.animations[self.status]) - 1: 
                self.frame_index = len(self.animations[self.status]) - 1 # Stop at the last frame
        else:
            if self.frame_index >= len(self.animations[self.status]):
                self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def follow_character(self):
        # Get the direction vector to the character
        self.direction_to_character = self.character.pos - self.pos
        # Calculate the distance to the character
        distance_to_character = self.direction_to_character.length()
        # Reset the direction vector
        self.direction = pygame.math.Vector2(0,0)
        # If the distance exceeds the max distance, set the direction vector
        if distance_to_character > self.max_distance:
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

            self.speed = self.walking_speed  # Set the speed to walking speed
        else:
            self.speed = 0  # Stop moving if within the max distance

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        if self.death_bool:
            self.status = self.status.split('_')[0] + '_death'

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

    def delayed_kill(self):
            time.sleep(5) # Wait 5 seconds
            self.kill() # Kill the npc

    def check_health(self, dt):
        if self.health_bool: # If health_bool is true, regenerate health
            self.health += self.health_regen_rate * dt * 1.25 # Regenerate health
            if self.health >= self.max_health: # If health is greater than or equal to max health, set health to max health
                self.health = self.max_health # Set health to max health
        else: 
            self.health -= self.health_degen_rate * dt * 1.25 # Degenerate health
            if self.health <= 0: # If health is less than or equal to 0, set health to 0
                self.death_bool = True
                self.direction.magnitude() == 0 # Stop moving
                timer_thread = threading.Thread(target=self.delayed_kill) # Create a thread to kill the npc after 5 seconds
                timer_thread.start() # Start the thread

    def update(self, dt):
        self.follow_character()  # Update direction and speed to follow the character
        self.move(dt)  # Move the NPC
        self.get_status()  # Update the status (animation)
        self.animate(dt)  # Animate the NPC
        self.check_health(dt)
