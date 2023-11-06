"""
Description: This script contains the settings for the game.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: September 19, 2023
Date Modified: October 08, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
from pygame.math import Vector2

# Set the screen width and height to the monitor's size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TITLE_SIZE = 64

# Font path
PIXEL_FONT_PATH = "./Game_Font/PressStart2P-Regular.ttf"

# Overlay size and position
OVERLAY_POSITIONS = {
    'Ranged_Weapon': {
        'position': (40, SCREEN_HEIGHT - 15),  # (x, y)
        'size': (0, 0)  # (width, height)
    },
    'Melee_Weapon': {
        'position': (70, SCREEN_HEIGHT - 5),  # (x, y)
        'size': (0, 0)  # (width, height)
    },
    'Stamina': {
        'position': (10, 10),  # (x, y)
        'size': (200, 20)  # (width, height)
    },
    'Health': {
        'position': (10, 70), # (x, y)
        'size': (200, 20)  # (width, height)
    },
}

# Define deafult key bindings
KEY_UP = pygame.K_w  # Move up
KEY_DOWN = pygame.K_s  # Move down
KEY_LEFT = pygame.K_a  # Move left
KEY_RIGHT = pygame.K_d  # Move right

KEY_SPRINT = pygame.K_LSHIFT  # Sprint

KEY_WEAPON = pygame.K_e # Equip weapon
KEY_SWAP = pygame.K_q # Switch weapons
KEY_SHOOT = 1 # Shoot weapon

# Define Layers for the game
LAYERS = {
    'background': 0,
    'player': 1,
    'bullet' : 1,
    'zombie': 1,
    'npc': 1,
    'foreground': 2,
    'overlay': 3,
    'rain': 4,
}

MAP_BOUNDARY = pygame.Rect(0, 0, 1387, 872) # HACK: Hard-coded map boundary
