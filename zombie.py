"""
Description: This script contains the Zombie class, which is used to create enemies.
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

class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos, group, character, npc, display_surface):
        super().__init__(group)

        self.camera_group = group # Store a reference to the camera group
        self.display_surface = display_surface # Store a reference to the display surface
        self.character = character  # Store a reference to the character
        self.npc = npc # Store a reference to the npc

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
        # Imports zombie animations from sprite sheets
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

    def follow_human(self):
        self.direction = pygame.math.Vector2(0,0)
        # Calculate the distance to the character and to the npc
        distance_to_character = (self.character.pos - self.pos).length()
        distance_to_npc = (self.npc.pos - self.pos).length()
        # Compare the distances
        if distance_to_character < distance_to_npc:
            target_pos = self.character.pos
        else:
            target_pos = self.npc.pos
        # Calculate the distance to the target
        distance_to_target = (target_pos - self.pos).length()
        # Only follow if within 256 units
        if distance_to_target <= 256:
            self.direction_to_human = target_pos - self.pos
            # Set the direction vector and status based on character movement
            if not self.death_bool: # Ensure the zombie sprite doesn't flip if it's in its death state
                if self.direction_to_human.x < 0:
                    self.direction.x = -1
                    self.status = 'left'
                elif self.direction_to_human.x > 0:
                    self.direction.x = 1
                    self.status = 'right'
                if self.direction_to_human.y < 0:
                    self.direction.y = -1
                    if self.direction.x == 0:
                        self.status = 'up'
                elif self.direction_to_human.y > 0:
                    self.direction.y = 1
                    if self.direction.x == 0:
                        self.status = 'down'

    def is_alive(self):
        return not self.death_bool

    def kill_zombie(self, damage):
        self.health -= damage # Reduce the health of the zombie
        if self.health <= 0:
            self.death_bool = True
            self.direction.magnitude() == 0 # Stop moving
            timer_thread = threading.Thread(target=self.delayed_kill) # Create a thread to kill the zombie after 5 seconds
            timer_thread.start() # Start the thread

    def delayed_kill(self):
        time.sleep(5) # Wait 5 seconds
        self.kill() # Kill the zombie

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

    def draw_health_bar(self):
        camera_offset = self.camera_group.offset # Get the camera offset
        self.health_bar_width = 32 # Width of the health bar
        self.health_bar_height = 5 # Height of the health bar
        self.health_bar_x = self.pos.x - camera_offset.x - 16 # X-coordinate of the top-left corner of the health bar
        self.health_bar_y = self.pos.y - camera_offset.y - 48 # Y-coordinate of the top-left corner of the health bar

        # Calculate the current health bar width based on the current health value
        self.current_health_width = (self.health / 10) * self.health_bar_width

        # Draw the background of the health bar (gray), accounting for Health text size (20) and padding (10)
        pygame.draw.rect(self.display_surface, (128, 128, 128), (self.health_bar_x, (self.health_bar_y + 30), self.health_bar_width, self.health_bar_height))

        # Draw the current health bar (red), accounting for Health text size (20) and padding (10)
        pygame.draw.rect(self.display_surface, (255, 0, 0), (self.health_bar_x, (self.health_bar_y + 30), self.current_health_width, self.health_bar_height))

    def update(self, dt):
        self.is_alive() # Check if the zombie is alive
        self.follow_human() # Update direction and speed to follow the character
        if not self.death_bool:
            self.move(dt) # Only move if not in the death state
        self.get_status() # Update the status (animation)
        self.animate(dt) # Update the animation
        self.draw_health_bar() # Draw the health bar

