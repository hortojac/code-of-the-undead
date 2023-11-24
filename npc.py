"""
Description: This script contains the NPC class for the game which is used to create NPCs.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: October 08, 2023
Date Modified: November 19, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
import threading
import time
import openai
import os
import concurrent.futures
from dotenv import load_dotenv
from settings import *
from projectile import Projectile

# Load the OpenAI API key from the .env file
load_dotenv()
# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.camera_group = group

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
        self.sprinting_bool = False # Boolean to check if npc is sprinting or not
        self.max_stamina = 100  # Initial maximum stamina value
        self.stamina = self.max_stamina  # Current stamina value
        self.stamina_regen_rate = 10  # Stamina regeneration rate per second
        self.stamina_degen_rate = 20  # Stamina degeneration rate per second

        # Health variables
        self.death_bool = False # Boolean to check if npc is dead or not
        self.health_bool = True # Boolean to check if npc is losing health or not
        self.max_health = 100  # Initial maximum health value
        self.health = self.max_health  # Current health value
        self.health_regen_rate = 1  # Health regeneration rate per second
        self.health_degen_rate = 25  # Health degeneration rate per second

        self.equip_weapon = False # Boolean to check if npc has equiped pistol or not
        self.is_shooting = False # Boolean to check if npc is shooting or not

        self.max_distance = 32  # Maximum distance to the character

        self.game_state = {}  # Dictionary to hold the game state information
        self.nearby_zombies = []  # List to hold the positions of nearby zombies

        self.agent = GameAgent(self)  # Pass the NPC instance to GameAgent

    def import_assets(self):
        # Imports npc animations from sprite sheets
        self.animations = {
            'up': [], 'down': [], 'right': [], 'left': [],
            'up_idle': [], 'down_idle': [], 'right_idle': [], 'left_idle': [],
            'up_shoot': [], 'down_shoot': [], 'right_shoot': [], 'left_shoot': [],
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
            './assets/textures/npc/npc_shoot.png': {
                'rows': 4, 'cols': 4, 'animations': ['down_shoot', 'up_shoot', 'right_shoot', 'left_shoot']
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

    def move_towards_character(self, dt):
        direction = self.character.pos - self.pos
        distance_to_character = direction.length()

        if not self.death_bool: # If npc is dead, stop moving
            if not self.is_shooting:  # Only follow character if not currently shooting
                if distance_to_character > self.max_distance:
                    self.direction = direction.normalize()  # Normalize the direction
                    self.speed = self.sprinting_speed if self.sprinting_bool and self.stamina > 0 else self.walking_speed
                    
                    # Set status based on direction
                    if abs(self.direction.x) > abs(self.direction.y):
                        self.status = 'right' if self.direction.x > 0 else 'left'
                    else:
                        self.status = 'down' if self.direction.y > 0 else 'up'
                    
                    # Apply movement
                    self.pos += self.direction * self.speed * dt
                    self.rect.center = round(self.pos.x), round(self.pos.y)
                else:
                    self.speed = 0  # Stop moving if within the max distance
            else:
                self.speed = 0  # Stop moving if shooting

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        if self.equip_weapon:
            self.status = self.status.split('_')[0] + '_shoot'
        if self.death_bool:
            self.status = self.status.split('_')[0] + '_death'

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

    def check_stamina(self, dt):
        if self.sprinting_bool: # If sprinting, degenerate stamina
            if self.direction.magnitude() > 0: # If moving, degenerate stamina
                self.stamina -= self.stamina_degen_rate * dt * 1.25 # Degenerate stamina
                if self.stamina <= 0: # If stamina is less than or equal to 0, set stamina to 0
                    self.stamina = 0 # Set stamina to 0
                    self.speed = self.walking_speed # Set speed to walking speed if stamina is 0 (out of stamina)
            elif self.direction.magnitude() == 0 and self.stamina < self.max_stamina: # Check if not moving and stamina is less than max stamina
                self.stamina += self.stamina_regen_rate * dt * 1.25 # Regenerate stamina
                if self.stamina >= self.max_stamina: # If stamina is greater than or equal to max stamina, set stamina to max stamina
                    self.stamina = self.max_stamina # Set stamina to max stamina
        else:
            self.stamina += self.stamina_regen_rate * dt * 1.25 # Regenerate stamina
            if self.stamina >= self.max_stamina: # If stamina is greater than or equal to max stamina, set stamina to max stamina
                self.stamina = self.max_stamina # Set stamina to max stamina

    def is_alive(self):
        return not self.death_bool

    def shoot(self, target_x, target_y): #FIXME: Shooting a bullet doesn't get drawn on the screen right now
        print("NPC is shooting")
        print(target_x, target_y)
        # Get the direction vector from NPC's position to target's position
        direction = pygame.math.Vector2(target_x, target_y) - self.pos
        # Normalize the direction vector to get a unit vector
        normalized_direction = direction.normalize()
        # Multiply the normalized direction by the bullet's speed to get the bullet's velocity
        bullet_velocity = normalized_direction * 500  # Assuming the bullet speed is 500
        Projectile(self.pos, bullet_velocity, self.groups()[0])  # Create a bullet
        self.is_shooting = False # Set is_shooting to false after shooting
        self.equip_weapon = False # Set equip_weapon to false after shooting

    def get_nearby_zombies(self, zombies, max_distance=128):
        for zombie in zombies:
            distance = self.pos.distance_to(zombie.pos)
            if distance <= max_distance:
                self.nearby_zombies.append(zombie.pos)

    def update_game_state(self, character, zombies):
        self.character = character
        self.get_nearby_zombies(zombies) # Get the positions of nearby zombies
        # Collect game state information
        self.game_state = {
            'npc_health': self.health,
            'npc_stamina': self.stamina,
            'npc_position': self.pos,
            'character_position': self.character.pos,
            'character_health': self.character.health,
            'zombie_positions': self.nearby_zombies
        }

    def execute_actions(self, actions, dt): #FIXME: Shooting is buggy right now
        # Execute the actions returned by the GameAgent
        for action in actions:
            if action['type'] == 'move':
                # Move to the character's position
                self.move_towards_character(dt)
            elif action['type'] == 'shoot':
                self.equip_weapon = True # Equip weapon
                self.is_shooting = True # Set is_shooting to true
                # Shoot the zombie at its position
                zombie_position = self.nearby_zombies[0]
                target_x, target_y = zombie_position.x, zombie_position.y
                self.shoot(target_x, target_y)
                self.equip_weapon = True # Equip weapon
                self.is_shooting = True # Set is_shooting to true

    def update(self, dt):
        self.is_alive() # Check if npc is alive
        self.get_status()  # Update the status (animation)
        self.animate(dt)  # Animate the NPC
        self.check_health(dt) # Check health
        self.check_stamina(dt) # Check stamina
        
        # Check if the OpenAI API should be called
        if self.agent.should_call_openai_api():
            actions = self.agent.act()  # Get actions from the GameAgent
            self.execute_actions(actions, dt)  # Execute the actions
        else:
            self.move_towards_character(dt)  # Move towards the character

class GameAgent:
    def __init__(self, npc):
        self.npc = npc
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.previous_zombie_positions = []

    def should_call_openai_api(self):
        if self.npc.game_state['zombie_positions'] == None:
            return False
        else:
            # Check if this is the first call or if there's a new zombie in range
            if len(self.npc.game_state['zombie_positions']) != len(self.previous_zombie_positions):
                self.previous_zombie_positions = self.npc.game_state['zombie_positions']
                return True

    def act(self):
        # Convert current_game_state to a string or other format suitable for your language model
        formatted_state = self.format_game_state()
        # Submit the OpenAI API call to the executor
        future = self.executor.submit(self.get_language_model_response, formatted_state)
        # Do other work here, and then wait for the API call to complete if necessary
        response = future.result()
        # Parse the response to get the actions for the NPC
        actions = self.parse_response(response)
        return actions

    def format_game_state(self):
        # Convert current_game_state to a format suitable for your language model
        formatted_state = f"""
        NPC Health: {self.npc.game_state['npc_health']}
        NPC Stamina: {self.npc.game_state['npc_stamina']}
        NPC Position: {self.npc.game_state['npc_position']}
        Character Health: {self.npc.game_state['character_health']}
        Character Position: {self.npc.game_state['character_position']}
        Zombie Positions: {self.npc.game_state['zombie_positions']}
        """
        return formatted_state

    def get_language_model_response(self, formatted_state):
        # Send formatted_state to your language model and return the response
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a npc in a zombie apocalypse. Using the Game state information provided. Do you move to the character or do you shoot the zombie? Reply with 'move' or 'shoot'"},
                    {"role": "user", "content": formatted_state},
                ],
                max_tokens=50
            )
            print(response)
            return response.choices[0].message['content'] if response.choices else ""
        except openai.error.OpenAIError as e:
            print(f"An error occurred: {e}")
            return ""

    def parse_response(self, response):
        actions = []
        if "move" in response:
            actions.append({'type': 'move', 'target': 'character'})
        elif "shoot" in response:
            actions.append({'type': 'shoot', 'target': 'zombie'})
        return actions
