"""
Description: This script contains the GameSavesMenu class which is responsible for drawing the saves menu and handling user input.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: November 11, 2023
Date Modified: November 11, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
import json
import os
from settings import *

class GameSavesMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface() # Get the surface to draw
        self.origin = (0,0) # Define the origin

        self.game_save_directory = "./Game_Saves" # Define the game save directory
        self.game_saves = [] # List of game saves
        self.game_saves_dates = [] # List of game save dates
        self.save_buttons = [] # List of save buttons
        self.highlighted_save_buttons = [] # List of highlighted save buttons

        # Fonts for display
        self.title_font = pygame.font.Font(PIXEL_FONT_PATH, 64)
        self.text_font = pygame.font.Font(PIXEL_FONT_PATH, 16)

        self.mainmenu_button = pygame.image.load("./assets/main_menu/mainmenu_button.png") # Load exit button png
        self.highlighted_mainmenu = pygame.image.load("./assets/main_menu/mainmenu_button_highlighted.png") # Load highlighted exit button
        self.mainmenu_button_width = self.mainmenu_button.get_width() # Get width of the exit png
        self.mainmenu_button_height = self.mainmenu_button.get_height() # Get height of the exit png
        self.mainmenu_button_pos = (SCREEN_WIDTH/2 - (self.mainmenu_button_width/2), SCREEN_HEIGHT - (25 + self.mainmenu_button_height)) # Define position of exit button (25 pix up and in middle)

        self.createsave_button = pygame.image.load("./assets/main_menu/createsave_button.png") # Load the create save button png
        self.highlighted_createsave = pygame.image.load("./assets/main_menu/createsave_button_highlighted.png") # Load highlihgted create save button
        self.createsave_button_width = self.createsave_button.get_width() # Get the width of the create save button
        self.createsave_button_height = self.createsave_button.get_height() # Get the height of the create save button
        self.createsave_button_pos = (SCREEN_WIDTH/2 - (self.createsave_button_width/2), self.mainmenu_button_pos[1] - (10 + self.createsave_button_height)) # Define the position of the create save button

        for i in range(1, 6):
            save_button = pygame.image.load(f"./assets/main_menu/save{i}_button.png")
            highlighted_save_button = pygame.image.load(f"./assets/main_menu/save{i}_button_highlighted.png")
            self.save_buttons.append(save_button)
            self.highlighted_save_buttons.append(highlighted_save_button)

        self.load_game_saves() # Load the game saves

    def load_game_saves(self):
        # Load existing game saves from the Game_Save directory
        for i in range(1, 6):
            save_path = os.path.join(self.game_save_directory, f"GameSave{i}.json")
            if os.path.exists(save_path):
                self.game_saves.append(f"GameSave{i}")
                self.parse_game_save_date(f"GameSave{i}")

    def parse_game_save_date(self, save_name):
        save_path = f"./Game_Saves/{save_name}.json"

        # Load the JSON data from the file
        with open(save_path, 'r') as json_file:
            save_data = json.load(json_file)

        if 'saveDate' in save_data:
            save_date = save_data['saveDate']
            
            # Extract date and time components
            year = save_date.get('year', 'YYYY')
            month = save_date.get('month', 'MM')
            day = save_date.get('day', 'DD')
            hour = save_date.get('hour', 'HH')
            minute = save_date.get('minute', 'MM')

            # Format date and time as "MM/DD/YYYY - HOUR:MINUTE"
            formatted_date_time = f"{month}/{day}/{year} - {hour}:{minute}"
            # Add the formatted date and time to the list of game save dates
            self.game_saves_dates.append(formatted_date_time)

    def create_new_game_save(self):
        if len(self.game_saves) < 5:
            # Increment the save file number
            new_save_number = len(self.game_saves) + 1
            new_save_name = f"GameSave{new_save_number}"
            save_path = os.path.join(self.game_save_directory, f"{new_save_name}.json")
            game_save = {}
            with open(save_path, "w") as file:
                json.dump(game_save, file)
            self.game_saves.append(new_save_name)
            return new_save_name
        else:
            return None  # Return None if the maximum number of saves has been reached

    # This function is called over and over in main when game_state is "Settings"
    def run(self):
        self.display_surface.fill((10, 10, 10))  # Fills the screen with dark grey

        # Display title
        title = self.title_font.render("Game Saves", True, (0, 224, 11))
        self.display_surface.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, 25))

        pygame.event.get() # Gets game event
        mouse_state = pygame.mouse.get_pressed() # Gets which mouse buttons are currently pressed and which are not
        mouse_pos = pygame.mouse.get_pos() # Gets the position of the mouse

        # Display the main menu button
        self.display_surface.blit(self.mainmenu_button, self.mainmenu_button_pos)
        # Display the create save button
        self.display_surface.blit(self.createsave_button, self.createsave_button_pos)

        # Display save buttons for each existing save
        for i, save in enumerate(self.game_saves):
            # Extract the save number from the save name (e.g., "GameSave1" -> 1)
            save_number = int(save.replace("GameSave", "")) - 1

            date_and_time = self.text_font.render("Date and Time Saved:", True, (255, 255, 255))

            # Calculate the position for each save button
            save_button_x = self.save_buttons[save_number].get_width() + 72
            save_button_y = 25 + 64 + 25 + i * (self.save_buttons[save_number].get_height() + 10)
            save_button_pos = (save_button_x, save_button_y)

            # Display the save button
            self.display_surface.blit(self.save_buttons[save_number], save_button_pos)
            self.display_surface.blit(date_and_time, (save_button_pos[0] + 320, save_button_pos[1] + 15))
            self.display_surface.blit(self.text_font.render(self.game_saves_dates[i], True, (255, 255, 255)), (save_button_pos[0] + 320, save_button_pos[1] + 36))

            # Check if the mouse is over the button and if it's clicked
            if ((mouse_pos[0] > save_button_pos[0]) and (mouse_pos[0] < (save_button_pos[0] + self.save_buttons[save_number].get_width()))) and \
            ((mouse_pos[1] > save_button_pos[1]) and (mouse_pos[1] < (save_button_pos[1] + self.save_buttons[save_number].get_height()))):
                self.display_surface.blit(self.highlighted_save_buttons[save_number], save_button_pos)
                if mouse_state[0] == True:  # If left mouse button is clicked
                    pygame.time.wait(500)
                    return "Play", save

        # Checks position of mouse and if the left button is clicked
        if ((mouse_pos[0] > self.mainmenu_button_pos[0]) and (mouse_pos[0] < (self.mainmenu_button_pos[0] + self.mainmenu_button_width))) and \
        ((mouse_pos[1] > self.mainmenu_button_pos[1]) and (mouse_pos[1] < (self.mainmenu_button_pos[1] + self.mainmenu_button_height))):
            self.display_surface.blit(self.highlighted_mainmenu, self.mainmenu_button_pos) # Draws highlighted button over normal button if mouse is in its position
            if mouse_state[0] == True:  # If left button is clicked
                pygame.time.wait(500)
                return "Main Menu", "" # Returns Main Menu which is the game_state of "main menu"

        # Check position of mouse and if mouse is clicked to see if and what button is pressed
        if ((mouse_pos[0] > self.createsave_button_pos[0]) and (mouse_pos[0] < (self.createsave_button_pos[0] + self.createsave_button_width))) and \
        ((mouse_pos[1] > self.createsave_button_pos[1]) and (mouse_pos[1] < (self.createsave_button_pos[1] + self.createsave_button_height))):
            self.display_surface.blit(self.highlighted_createsave, self.createsave_button_pos) # draws highlighted button over normal button if mouse is in its position
            if mouse_state[0] == True: # If left mouse button is clicked
                pygame.time.wait(500)
                save_name = self.create_new_game_save() # Create a new game save
                if save_name != None:
                    return "Play", save_name # Return the game state and the name of the new game save
                else:
                    print("Maximum number of saves reached")
                    return "Game Saves Menu", ""
            else:
                return "Game Saves Menu", "" # Return the game state and an empty string
        else:
            return "Game Saves Menu", ""