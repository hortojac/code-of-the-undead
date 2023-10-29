"""
Description: This script contains the SettingsMenu class which is responsible for drawing the settings menu and handling user input.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: September 28, 2023
Date Modified: October 28, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
import sys
import inspect
from settings import *

class SettingsMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface() # Get the surface to draw
        self.origin = (0,0) # Define the origin

        # Fonts for display
        self.title_font = pygame.font.SysFont('Arial', 96)
        self.sub_title_font = pygame.font.SysFont('Arial', 48)
        self.keybind_font = pygame.font.SysFont('Arial', 32)

        # Gather keybinds from settings in the order they are defined
        self.keybinds = []
        settings_source = inspect.getsourcelines(sys.modules['settings'])[0]
        for line in settings_source:
            if line.strip().startswith("KEY_"):
                attr = line.split('=')[0].strip()
                key_name = attr.split("KEY_")[1].replace("_", " ")  # Make key names more readable
                pygame_key = getattr(sys.modules['settings'], attr)

                if pygame_key == 1:  # This is our special value for the mouse click
                    key_representation = "LEFT CLICK"
                else:
                    key_representation = pygame.key.name(pygame_key).upper()

                self.keybinds.append((key_name, key_representation))

        # Calculate the maximum length of key names for alignment
        self.max_key_name_length = max([len(k[0]) for k in self.keybinds])

        self.exit_button = pygame.image.load("./assets/main_menu/mainmenu_button.png") # Load exit button png
        self.highlighted_exit = pygame.image.load("./assets/main_menu/mainmenu_button_highlighted.png") # Load highlighted exit button
        self.exit_button_width = self.exit_button.get_width() # Get width of the exit png
        self.exit_button_height = self.exit_button.get_height() # Get height of the exit png
        self.exit_button_pos = (SCREEN_WIDTH/2 - (self.exit_button_width/2), SCREEN_HEIGHT - (25 + self.exit_button_height)) # Define position of exit button (25 pix up and in middle)

    # This function is called over and over in main when game_state is "Settings"
    def run(self):
        self.display_surface.fill((10, 10, 10))  # Fills the screen with dark grey

        # Display title
        title = self.title_font.render("Settings", True, (0, 224, 11))
        self.display_surface.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, 25))

        # Display subtitle "Default Key Bindings"
        sub_title = self.sub_title_font.render("Default Key Bindings", True, (255, 255, 255))
        self.display_surface.blit(sub_title, (SCREEN_WIDTH/2 - sub_title.get_width()/2, 25 + title.get_height() + 50))

        # Adjust the y_offset to display the keybinds immediately after the subtitle
        y_offset = 25 + title.get_height() + 50 + sub_title.get_height() + 20

        # Calculate where the keybinds should be aligned on the right
        right_alignment_pos = (SCREEN_WIDTH/2 + sub_title.get_width()/2)  # Adjust this if necessary

        for keybind in self.keybinds:
            # Render the key name and the keybind separately
            key_name_text = self.keybind_font.render(keybind[0], True, (255, 255, 255))
            keybind_text = self.keybind_font.render(keybind[1], True, (255, 255, 255))
            
            # Calculate the space needed for the '-' characters
            space_for_dashes = right_alignment_pos - (SCREEN_WIDTH/2 - sub_title.get_width()/2 + key_name_text.get_width() + keybind_text.get_width())
            
            # Estimate how many '-' characters can fit in the space
            dash_width = self.keybind_font.size('-')[0]
            num_dashes = int(space_for_dashes / dash_width)
            
            dashes_text = self.keybind_font.render('-' * num_dashes, True, (255, 255, 255))
            
            # Blit the texts to the screen
            self.display_surface.blit(key_name_text, (SCREEN_WIDTH/2 - sub_title.get_width()/2, y_offset))
            self.display_surface.blit(dashes_text, (SCREEN_WIDTH/2 - sub_title.get_width()/2 + key_name_text.get_width(), y_offset))
            self.display_surface.blit(keybind_text, (right_alignment_pos - keybind_text.get_width(), y_offset))
            
            y_offset += key_name_text.get_height() + 5  # Space between keybinds

        # Display the exit button
        self.display_surface.blit(self.exit_button, self.exit_button_pos)

        pygame.event.get() # Gets game event
        mouse_state = pygame.mouse.get_pressed() # Gets which mouse buttons are currently pressed and which are not
        mouse_pos = pygame.mouse.get_pos() # Gets the position of the mouse

        # Checks position of mouse and if the left button is clicked
        if ((mouse_pos[0] > self.exit_button_pos[0]) and (mouse_pos[0] < (self.exit_button_pos[0] + self.exit_button_width))) and \
        ((mouse_pos[1] > self.exit_button_pos[1]) and (mouse_pos[1] < (self.exit_button_pos[1] + self.exit_button_height))):
            self.display_surface.blit(self.highlighted_exit, self.exit_button_pos) # Draws highlighted button over normal button if mouse is in its position
            if mouse_state[0] == True:  # If left button is clicked
                pygame.time.wait(500)
                return "Main Menu"  # Go back to the main menu
            else:
                return "Settings"  # If the button is not clicked it returns Settings -- the settings menu game_state
        else:
            return "Settings" # Returns Settings game_state -- runs if no button is clicked