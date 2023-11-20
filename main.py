"""
Description: This script contains the main game loop and is the entry point for the game.
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
import sys
from settings import *
from map import Map
from Menus.main_menu import MainMenu
from Menus.settings_menu import SettingsMenu
from Menus.credits_menu import CreditsMenu
from Menus.game_saves_menu import GameSavesMenu

class Game:
    # Overall class to manage game assets and behavior.
    def __init__(self):
        # Initialize the game, and create resources.
        pygame.init()
        # Create a icon instance
        self.programIcon = pygame.image.load('assets/icon.png')
        # Set the program icon
        pygame.display.set_icon(self.programIcon)
        # Set the screen size to the monitor's size
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Set the game title
        pygame.display.set_caption("Code of the Undead")
        # Create a Clock instance
        self.clock = pygame.time.Clock()
        # Create a Main Menu instance
        self.main_menu = MainMenu()
        # Create a Settings Menu instance
        self.settings_menu = SettingsMenu()
        # Create a Credits Menu instance
        self.credits_menu = CreditsMenu()
        # Create a Game Saves Menu instance
        self.game_saves_menu = GameSavesMenu()
        # Set the game state to the main menu
        self.game_state = "Main Menu"
        # Set the save name to an empty string
        self.save_name = ""
        # Boolean to check if the map has been loaded
        self.map_has_been_loaded = False

    def handle_events(self):
        for event in pygame.event.get():
            # Check for quit events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and (event.mod & pygame.KMOD_CTRL):
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = "Pause Menu"

    def draw_main_menu(self):
        # Draw the menu
        self.game_state = self.main_menu.run()
    
    def draw_settings_menu(self):
        # Draw the settings menu
        self.game_state = self.settings_menu.run(self.game_state)

    def draw_credits_menu(self):
        # Draw the credits menu
        self.game_state = self.credits_menu.run()

    def draw_game_saves_menu(self):
        # Draw the game saves menu
        self.game_state, self.save_name = self.game_saves_menu.run()

    def draw_map(self, dt):
        # Draw the map
        self.map.run(dt)
  
    def draw_pause_menu(self):
        # Draw the pause menu
        self.game_state = self.settings_menu.run(self.game_state)

    def quit_game(self):
        self.map.write_game_save(self.save_name)
        del self.map
        self.map_has_been_loaded = False
        self.game_saves_menu.parse_game_save_date(self.save_name)
        self.draw_game_saves_menu()

    def run_game(self):
        # Start the main loop for the game.
        while True:
            self.handle_events()

            dt = self.clock.tick() / 1000.0

            if self.game_state == "Main Menu":
                self.draw_main_menu()
            elif self.game_state == "Settings":
                self.draw_settings_menu()
            elif self.game_state == "Credits":
                self.draw_credits_menu()
            elif self.game_state == "Game Saves Menu":
                self.draw_game_saves_menu()
            elif self.game_state == "Play":
                if self.map_has_been_loaded == False:
                    self.map = Map(self.save_name)
                    self.map_has_been_loaded = True
                self.draw_map(dt)
            elif self.game_state == "Pause Menu":
                self.draw_pause_menu()
            elif self.game_state == "Quit":
                self.quit_game()

            # Make the most recently drawn screen visible
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run_game()
