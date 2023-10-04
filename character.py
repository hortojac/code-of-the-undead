"""
Description: This script contains the Character class, which is used to create the playable character.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: September 19, 2023
Date Modified: October 04, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
from settings import *
from support import *

class Character(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # Call the import_assets method to import all the animations
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # Set the image and rect attributes for the character
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # Movement of the character
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

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'right': [], 'left': [
        ], 'up_idle': [], 'down_idle': [], 'right_idle': [], 'left_idle': []}
        # Import all the animations
        for animation in self.animations.keys():
            full_path = "./assets/textures/character/" + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self, dt):
        # Check for keys that are continuously pressed
        keys = pygame.key.get_pressed()
        # Initialize direction vector
        self.direction = pygame.math.Vector2(0, 0)
        # Check for sprinting (SHIFT key)
        sprinting = keys[KEY_SPRINT]
        # Set the direction vector and status based on the keys pressed
        if keys[KEY_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[KEY_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        if keys[KEY_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[KEY_DOWN]:
            self.direction.y = 1
            self.status = 'down'

        # Adjust speed based on sprinting state
        if sprinting:
            self.speed = self.sprinting_speed # Set speed to sprinting speed
            self.stamina -= self.stamina_degen_rate * dt * 1.25 # Reduce stamina
            if self.stamina <= 0: # Make sure stamina doesn't go below 0
                self.stamina = 0 # Set stamina to 0 when it goes below 0
                self.speed = self.walking_speed # Set speed to walking speed
        else:
            self.speed = self.walking_speed # Set speed to walking speed
            self.stamina += self.stamina_regen_rate * dt * 1.25 # Increase stamina
            if self.stamina >= self.max_stamina: # Make sure stamina doesn't exceed the maximum value
                self.stamina = self.max_stamina # Set stamina to the maximum value

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def move(self, dt):
        # Normalize the direction vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def draw_stamina_bar(self, display_surface):
        self.stamina_bar_width = OVERLAY_POSITIONS['Stamina']['size'][0]  # Width of the stamina bar
        self.stamina_bar_height = OVERLAY_POSITIONS['Stamina']['size'][1]  # Height of the stamina bar
        self.stamina_bar_x = OVERLAY_POSITIONS['Stamina']['position'][0]  # X-coordinate of the top-left corner of the stamina bar
        self.stamina_bar_y = OVERLAY_POSITIONS['Stamina']['position'][1]  # Y-coordinate of the top-left corner of the stamina bar

        # Calculate the current stamina bar width based on the current stamina value
        self.current_stamina_width = (self.stamina / self.max_stamina) * self.stamina_bar_width

        font = pygame.font.SysFont('Arial', 20) # Font for the stamina text
        text_surface = font.render('Stamina:', True, (0, 0, 0)) # Create the stamina text surface
        display_surface.blit(text_surface, (self.stamina_bar_x, self.stamina_bar_y)) # Draws text above the stamina bar

        # Draw the background of the stamina bar (gray), accounting for Stamina text size (20) and padding (10)
        pygame.draw.rect(display_surface, (128, 128, 128), (self.stamina_bar_x, (self.stamina_bar_y + 30), self.stamina_bar_width, self.stamina_bar_height))
        
        # Draw the current stamina bar (green), accounting for Stamina text size (20) and padding (10)
        pygame.draw.rect(display_surface, (0, 255, 0), (self.stamina_bar_x, (self.stamina_bar_y + 30), self.current_stamina_width, self.stamina_bar_height)) 

    def update(self, dt):
        self.input(dt)
        self.get_status()
        self.move(dt)
        self.animate(dt)
