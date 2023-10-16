"""
Description: This script contains the Character class, which is used to create the playable character.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: September 19, 2023
Date Modified: October 13, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
import sys
import math
from settings import *

class Character(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.font = pygame.font.SysFont('Arial', 20) # Font for the stamina and health text

        # Call the import_assets method to import all the animations
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # Set the image and rect attributes for the character
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['player']

        # Movement of the character
        self.direction = pygame.math.Vector2() # Initialize the direction vector
        self.pos = pygame.math.Vector2(self.rect.center) # Initialize the position vector
        self.speed = 0  # Initialize speed to 0
        self.walking_speed = 100  # Waling speed
        self.sprinting_speed = 200  # Sprinting speed

        # Stamina variables
        self.sprinting_bool = False # Boolean to check if character is sprinting or not
        self.max_stamina = 100  # Initial maximum stamina value
        self.stamina = self.max_stamina  # Current stamina value
        self.stamina_regen_rate = 10  # Stamina regeneration rate per second
        self.stamina_degen_rate = 20  # Stamina degeneration rate per second

        # Health variables
        self.health_bool = True # Boolean to check if character is losing health or not
        self.max_health = 100  # Initial maximum health value
        self.health = self.max_health  # Current health value
        self.health_regen_rate = 1  # Health regeneration rate per second
        self.health_degen_rate = 10  # Health degeneration rate per second

        self.talking_with_npc = False # Boolean to check if character is talking with an NPC or not
        self.equip_weapon = False # Boolean to check if character has equiped pistol or not
        self.delete_enemy = False # TODO : Remove this, just for testing purposes

        # List to hold character's bullets
        self.bullets = []

    def import_assets(self):
        # Imports character animations from sprite sheets.
        self.animations = {
            'up': [], 'down': [], 'right': [], 'left': [],
            'up_idle': [], 'down_idle': [], 'right_idle': [], 'left_idle': [],
            'up_shoot': [], 'down_shoot': [], 'right_shoot': [], 'left_shoot': []
        }
        
        # Define sprite sheet configurations
        sprite_sheets = {
            './assets/textures/character/character_walk.png': {
                'rows': 4, 'cols': 4, 'animations': ['down', 'up', 'right', 'left']
            },
            './assets/textures/character/character_idle.png': {
                'rows': 4, 'cols': 2, 'animations': ['down_idle', 'up_idle', 'right_idle', 'left_idle']
            },
            './assets/textures/character/character_shoot.png': {
                'rows': 4, 'cols': 4, 'animations': ['down_shoot', 'up_shoot', 'right_shoot', 'left_shoot']
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
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        self.direction = pygame.math.Vector2(0,0)
        # Check for keys that are continuously pressed
        keys = pygame.key.get_pressed()
        # Check for sprinting (SHIFT key)
        self.sprinting = keys[KEY_SPRINT]
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
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: # Detects key inputs
                mousex, mousey = pygame.mouse.get_pos()
                self.shoot(mousex, mousey)

        self.toggle_enemy = keys[pygame.K_z] # TODO : Remove this, just for testing purposes
        if self.toggle_enemy:
            self.delete_enemy = True

        self.toggle_weapon = keys[KEY_WEAPON]
        if self.toggle_weapon:
            self.equip_weapon = True

        # Adjust speed based on sprinting state
        if self.sprinting:
            self.speed = self.sprinting_speed # Set speed to sprinting speed if sprinting
            self.sprinting_bool = True # Set sprinting boolean to true if sprinting
            if self.stamina == 0:
                self.speed = self.walking_speed # Set speed to walking speed if stamina is 0 (out of stamina)
        else:
            self.speed = self.walking_speed # Set speed to walking speed if not sprinting
            self.sprinting_bool = False # Set sprinting boolean to false if not sprinting

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        if self.equip_weapon:
            self.status = self.status.split('_')[0] + '_shoot'

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

    def draw_stamina_bar(self, display_surface, dt):
        if self.sprinting_bool: # If sprinting, degenerate stamina
            if self.direction.magnitude() > 0: # If moving, degenerate stamina
                self.stamina -= self.stamina_degen_rate * dt * 1.25 # Degenerate stamina
                if self.stamina <= 0: # If stamina is less than or equal to 0, set stamina to 0
                    self.stamina = 0 # Set stamina to 0
            elif self.direction.magnitude() == 0 and self.stamina < self.max_stamina: # Check if not moving and stamina is less than max stamina
                self.stamina += self.stamina_regen_rate * dt * 1.25 # Regenerate stamina
                if self.stamina >= self.max_stamina: # If stamina is greater than or equal to max stamina, set stamina to max stamina
                    self.stamina = self.max_stamina # Set stamina to max stamina
        else:
            self.stamina += self.stamina_regen_rate * dt * 1.25 # Regenerate stamina
            if self.stamina >= self.max_stamina: # If stamina is greater than or equal to max stamina, set stamina to max stamina
                self.stamina = self.max_stamina # Set stamina to max stamina

        self.stamina_bar_width = OVERLAY_POSITIONS['Stamina']['size'][0]  # Width of the stamina bar
        self.stamina_bar_height = OVERLAY_POSITIONS['Stamina']['size'][1]  # Height of the stamina bar
        self.stamina_bar_x = OVERLAY_POSITIONS['Stamina']['position'][0]  # X-coordinate of the top-left corner of the stamina bar
        self.stamina_bar_y = OVERLAY_POSITIONS['Stamina']['position'][1]  # Y-coordinate of the top-left corner of the stamina bar

        # Calculate the current stamina bar width based on the current stamina value
        self.current_stamina_width = (self.stamina / self.max_stamina) * self.stamina_bar_width
        text_surface = self.font.render('Stamina:', True, (0, 0, 0)) # Create the stamina text surface
        display_surface.blit(text_surface, (self.stamina_bar_x, self.stamina_bar_y)) # Draws text above the stamina bar

        # Draw the background of the stamina bar (gray), accounting for Stamina text size (20) and padding (10)
        pygame.draw.rect(display_surface, (128, 128, 128), (self.stamina_bar_x, (
            self.stamina_bar_y + 30), self.stamina_bar_width, self.stamina_bar_height))

        # Draw the current stamina bar (green), accounting for Stamina text size (20) and padding (10)
        pygame.draw.rect(display_surface, (0, 255, 0), (self.stamina_bar_x, (self.stamina_bar_y + 30), self.current_stamina_width, self.stamina_bar_height))
    
    def draw_health_bar(self, display_surface, dt):
        if self.health_bool: # If health_bool is true, regenerate health
            self.health += self.health_regen_rate * dt * 1.25 # Regenerate health
            if self.health >= self.max_health: # If health is greater than or equal to max health, set health to max health
                self.health = self.max_health # Set health to max health
        else: 
            self.health -= self.health_degen_rate * dt * 1.25 # Degenerate health
            if self.health <= 0: # If health is less than or equal to 0, set health to 0
                # TODO Add in character death animation and game over screen
                pygame.quit() # Close game
                sys.exit()
                # self.health = 0 # Set health to 0

        self.health_bar_width = OVERLAY_POSITIONS['Health']['size'][0] # Width of the health bar
        self.health_bar_height = OVERLAY_POSITIONS['Health']['size'][1] # Height of the health bar
        self.health_bar_x = OVERLAY_POSITIONS['Health']['position'][0] # X-coordinate of the top-left corner of the health bar
        self.health_bar_y = OVERLAY_POSITIONS['Health']['position'][1] # Y-coordinate of the top-left corner of the health bar

        # Calculate the current health bar width based on the current health value
        self.current_health_width = (self.health / self.max_health) * self.health_bar_width
        text_surface = self.font.render('Health:', True, (0, 0, 0))
        display_surface.blit(text_surface, (self.health_bar_x, self.health_bar_y))

        # Draw the background of the health bar (gray), accounting for Health text size (20) and padding (10)
        pygame.draw.rect(display_surface, (128, 128, 128), (self.health_bar_x, (self.health_bar_y + 30), self.health_bar_width, self.health_bar_height))

        # Draw the current health bar (red), accounting for Health text size (20) and padding (10)
        pygame.draw.rect(display_surface, (255, 0, 0), (self.health_bar_x, (self.health_bar_y + 30), self.current_health_width, self.health_bar_height))

    # Shoot function
    def shoot(self, mousex, mousey, speed = 5):
        distance_x = mousex - self.pos.x
        distance_y = mousey - self.pos.y
        shoot_angle = math.atan2(distance_y, distance_x)
        self.bullets.append(Projectile(self.pos.x, self.pos.y, 6, (0,0,0), math.cos(shoot_angle), math.sin(shoot_angle)))  

    def update(self, dt):
        self.input()
        self.move(dt)
        self.get_status()
        self.animate(dt)
        
        # Loop that iterates through all bullets
        for bullet in self.bullets:
            if bullet.x < 9000 and bullet.x > 0 and bullet.y < 9000 and bullet.y > 0:
                bullet.x += bullet.xvel  # Moves the bullet by its x velocity
                bullet.y += bullet.yvel  # Moves the bullet by its y velocity
            else:
                self.bullets.pop(self.bullets.index(bullet))  # This will remove the bullet if it is off screen

# Projectile class
class Projectile(object):
    def __init__(self,x,y,radius,color,xangle, yangle):
        # Sets position, appearance, and trajectory of projectile
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.image = pygame.image.load("./assets/textures/character/bulletone.png")  # Load image
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Make a rect that matches image
        self.xfacing = xangle
        self.yfacing = yangle
        self.z = LAYERS['bullet']  # Set layer

        # Sets velocity of projectile. Current speed is 8; Hope to add modifiable speed per weapon
        speed = 10
        self.xvel = speed * xangle
        self.yvel = speed * yangle

    # Draw function called by map to draw circle on screen
    def draw(self):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        surface = pygame.display.get_surface()  # Get the surface
        pygame.draw.circle(surface, self.color, (self.x,self.y), self.radius)
        surface.blit(self.image, self.rect.topleft)  # Print the image using top-left as reference
        