"""
Description: This script contains the Map class which is responsible for drawing the tile map and all sprites.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: September 19, 2023
Date Modified: October 09, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
from typing import List, Optional
import pygame
import math
import openai
import os
from pygame.rect import Rect
from pygame.surface import Surface
from settings import *
from character import Character
from zombie import Zombie
from npc import NPC 
from sprites import Generic

openai_api_key = os.environ.get('OPENAI_API_KEY')

class Map:
    def __init__(self):
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

        self.setup()

    def setup(self):
        Generic(pos=(0, 0), surf=pygame.image.load(
            './assets/Test_map/map.png').convert_alpha(), groups=self.all_sprites, z=LAYERS['background'])
        self.character = Character(((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)), self.all_sprites)
        self.zombie = Zombie((0,0), self.all_sprites)
        self.npc = NPC(((SCREEN_WIDTH // 2 + 100), (SCREEN_HEIGHT // 2 + 200)), self.all_sprites)

    def run(self, dt):
        # Fill the display surface with a background color (white)
        self.display_surface.fill('white')

        if self.character.rect.colliderect(self.zombie.rect) : # If the enemy and player collide
            self.character.health_bool = False
        else:
            self.character.health_bool = True

        if self.character.delete_enemy: # TODO : Remove this, just for testing purposes
            self.zombie.pos = pygame.math.Vector2(0,0)

        for bullet in self.character.bullets:
            bullet.draw()
            if bullet.rect.colliderect(self.zombie.rect):
                self.zombie.hurt(1)
                print("collide")

        # Draw all sprites on top of the grid
        self.all_sprites.custom_draw(self.character) # Draw character on top of map
        self.character.draw_stamina_bar(self.display_surface, dt) # Draw stamina bar
        self.character.draw_health_bar(self.display_surface, dt) # Draw health bar
        self.zombie.character_input(self.character.pos)
        self.all_sprites.update(dt) # update all sprites

        # TODO : Temporary input code for talking, need to move to character class
        # This function is for handling key inputs and the text box for talking
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.text_box_active:
                    if event.key == pygame.K_ESCAPE:
                        self.text_box_active = False
                        self.character.talking_with_npc = False
                        self.input_text = ""
                        self.output_text = ""
                    elif event.key == pygame.K_RETURN:
                        self.output_text = self.get_openai_response(self.input_text)
                        self.input_text = ""     
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_F1:
                        self.input_text = "Hi, how are you?"
                    else:
                        self.input_text += event.unicode
                elif not self.text_box_active:
                    distance = math.dist(self.character.pos, self.npc.pos)
                    if distance <= 48 and event.key == pygame.K_t:
                        self.text_box_active = True
                        self.character.talking_with_npc = True
                        self.input_text = ""
                        self.output_text = ""

        if self.text_box_active:
            # Cursor blinking
            if pygame.time.get_ticks() - self.cursor_time > 500:  # blink every 500 milliseconds
                self.cursor_visible = not self.cursor_visible
                self.cursor_time = pygame.time.get_ticks()

            # INPUT TEXT
            txt_surface = self.font.render(self.input_text, True, (0,0,0))
            self.display_surface.blit(txt_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
            
            # Adjust cursor position based on the last line
            if self.cursor_visible:
                cursor_y_pos = self.input_rect.y + 5
                cursor_x_pos = self.input_rect.x + 5 + self.font.size(self.input_text)[0]
                pygame.draw.line(self.display_surface, (0,0,0), (cursor_x_pos, cursor_y_pos), (cursor_x_pos, cursor_y_pos + self.font.get_height()))
            pygame.draw.rect(self.display_surface, (0,0,0), self.input_rect, 2)
            
            # AI OUTPUT
            txt_surface_output = self.font.render(self.output_text, True, (0,0,0))
            self.display_surface.blit(txt_surface_output, (self.output_rect.x + 5, self.output_rect.y + 5))
            pygame.draw.rect(self.display_surface, (0,0,0), self.output_rect, 2)

    # Function to send a query to OpenAI and get a response
    def get_openai_response(self, query):
        response = openai.Completion.create(
            engine="davinci",
            prompt=query,
            max_tokens=10
        )
        return response.choices[0].text.strip()

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

