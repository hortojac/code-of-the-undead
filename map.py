"""
Description: This script contains the Map class which is responsible for drawing the tile map and all sprites.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: September 19, 2023
Date Modified: October 25, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
from typing import List, Optional
import pygame
import json
import datetime
from pygame.rect import Rect
from pygame.surface import Surface
from settings import *
from character import Character
from zombie import Zombie
from npc import NPC 
from sprites import Generic
from projectile import Projectile

class Map():
    def __init__(self, save_name):
        self.save_name = save_name
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()

        self.font = pygame.font.Font(None, 32)
        self.input_text = ""
        self.output_text = ""
        self.input_rect = pygame.Rect(50, 400, 200, 100)
        self.output_rect = pygame.Rect(50, 510, 200, 100)
        self.cursor_visible = True
        self.cursor_time = pygame.time.get_ticks()
        self.text_box_active = False

        self.walls = []#list to hold walls
        self.zombies = []  # List to hold all zombies

        self.setup()
        self.load_game_save(self.save_name)

    def setup(self):
        background = pygame.image.load('./assets/Test_map/eaton_g_outline.png').convert_alpha()
        Generic(pos=(0, 0), surf=background, groups=self.all_sprites, z=LAYERS['background'])
        
        ###Create the Collisions for the map - will want to move this to the corresponding map level
        for x in range(0, 1200):#loop through every pixel of outline
            for y in range(0, 800):
                color = background.get_at((x, y))#gets the color of the current pixel
                if (color[0] == 0 and color[1] == 0 and color [2] == 0):#if the pixel is black
                    self.walls.append(pygame.Rect(x, y, 1, 1))#add a rect for that pixel in the walls list

        self.character = Character(((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)), self.all_sprites, self.walls)
        self.npc = NPC(((SCREEN_WIDTH // 2 + 100), (SCREEN_HEIGHT // 2 + 200)), self.all_sprites)
        for i in range(2):
            zombie_position = (i * 500, 0)
            zombie = Zombie(zombie_position, self.all_sprites, self.character, self.npc, self.display_surface)
            self.zombies.append(zombie)

    def load_game_save(self, save_name):
        save_path = f"./Game_Saves/{save_name}.json"

        # Load the JSON data from the file
        with open(save_path, 'r') as json_file:
            save_data = json.load(json_file)

        # Check if the loaded data is for the character
        if 'character' in save_data:
            character_data = save_data['character']
            if 'pos' in character_data:
                # Set the character's position based on the loaded data
                self.character.pos.x = character_data['pos']['x']
                self.character.pos.y = character_data['pos']['y']
            if 'health' in character_data:
                # Set the character's health based on the loaded data
                self.character.health = character_data['health']
            if 'stamina' in character_data:
                # Set the character's stamina based on the loaded data
                self.character.stamina = character_data['stamina']

        # Check if the loaded data is for the NPC
        if 'npc' in save_data:
            npc_data = save_data['npc']
            if 'pos' in npc_data:
                # Set the npc's position based on the loaded data
                self.npc.pos.x = npc_data['pos']['x']
                self.npc.pos.y = npc_data['pos']['y']
            if 'health' in npc_data:
                # Set the npc's health based on the loaded data
                self.npc.health = npc_data['health']
            if 'stamina' in npc_data:
                # Set the npc's stamina based on the loaded data
                self.npc.stamina = npc_data['stamina']

        # Check if the loaded data is for zombies
        if 'zombies' in save_data:
            zombie_data_list = save_data['zombies']
            for i, zombie_data in enumerate(zombie_data_list):
                if i < len(self.zombies):
                    zombie = self.zombies[i]
                    if 'pos' in zombie_data:
                        # Set the zombie's position based on the loaded data
                        zombie.pos.x = zombie_data['pos']['x']
                        zombie.pos.y = zombie_data['pos']['y']
                    if 'health' in zombie_data:
                        # Set the zombie's health based on the loaded data
                        zombie.health = zombie_data['health']

    def write_game_save(self, save_name):
        save_path = f"./Game_Saves/{save_name}.json"

        # Create a dictionary to store the save data
        save_data = {}

        # Add the date to the save data
        save_data['saveDate'] = {
            "year": datetime.datetime.now().year,
            "month": datetime.datetime.now().month,
            "day": datetime.datetime.now().day,
            "hour": datetime.datetime.now().hour,
            "minute": datetime.datetime.now().minute
        }

        # Add the character's data to the save data
        save_data['character'] = {
            'pos': {
                'x': self.character.pos.x,
                'y': self.character.pos.y
            },
            'health': self.character.health,
            'stamina': self.character.stamina
        }

        # Add the NPC's data to the save data
        save_data['npc'] = {
            'pos': {
                'x': self.npc.pos.x,
                'y': self.npc.pos.y
            },
            'health': self.npc.health,
            'stamina': self.npc.stamina
        }

        # Create a list to store zombie data
        zombie_data_list = []
        for zombie in self.zombies:
            zombie_data = {
                'pos': {
                    'x': zombie.pos.x,
                    'y': zombie.pos.y
                },
                'health': zombie.health,
            }
            zombie_data_list.append(zombie_data)

        # Add the zombie data list to the save data
        save_data['zombies'] = zombie_data_list

        # Save the JSON data to the file
        with open(save_path, 'w') as json_file:
            json.dump(save_data, json_file, indent=4)
    
    def run(self, dt):
        # Fill the display surface with a background color (white)
        self.display_surface.fill('white')
        # Check collision between character and each living zombie
        collision_with_character = any(zombie.is_alive() and self.character.rect.colliderect(zombie.rect) for zombie in self.zombies)
        self.character.health_bool = not collision_with_character
        # Check collision between npc and each living zombie
        collision_with_npc = any(zombie.is_alive() and self.npc.rect.colliderect(zombie.rect) for zombie in self.zombies)
        self.npc.health_bool = not collision_with_npc
        # Check if living zombies are attacking the character or NPC
        for zombie in self.zombies:
            if zombie.is_alive():
                zombie.attack_bool = self.character.rect.colliderect(zombie.rect) or self.npc.rect.colliderect(zombie.rect)

        # Check collision between bullet and each zombie
        for bullet in self.all_sprites.sprites():
            if isinstance(bullet, Projectile):
                for zombie in self.zombies:
                    if zombie.is_alive() and zombie.rect.colliderect(bullet.rect):
                        zombie.kill_zombie(2)
                        bullet.kill()

        # Draw all sprites on top of the grid
        self.all_sprites.custom_draw(self.character) # Draw character on top of map
        self.character.draw_stamina_bar(self.display_surface, dt) # Draw stamina bar
        self.character.draw_health_bar(self.display_surface, dt) # Draw health bar
        self.npc.update_game_state(self.character, self.zombies) # update game state for NPC
        self.all_sprites.update(dt) # update all sprites
        
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w 
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, character):
        self.center_target_camera(character) # Center camera on player

        # Active elements
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft - self.offset
                    self.display_surface.blit(sprite.image, offset_pos)

