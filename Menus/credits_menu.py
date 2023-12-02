"""
Description: This script contains the CreditsMenu class which is responsible for drawing the credits page and handling user input.
Author: Seth Daniels, Nico Gatapia, Jacob Horton, Elijah Toliver, Gilbert Vandegrift
Date Created: September 30, 2023
Date Modified: October 30, 2023
Version: Development
Python Version: 3.11.5
Dependencies: pygame
License: MIT License
"""

# Imports
import pygame
from settings import *

class CreditsMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface() # Get the surface to draw
        self.origin = (0,0) # Define the origin

        # Fonts for display
        self.title_font = pygame.font.Font(PIXEL_FONT_PATH, 64)
        self.sub_title_font = pygame.font.Font(PIXEL_FONT_PATH, 32)
        self.author_font = pygame.font.Font(PIXEL_FONT_PATH, 24)

        self.authors = ["Seth Daniels", "Nico Gatapia", "Jacob Horton", "Elijah Toliver", "Gilbert Vandegrift"]
        self.assets = ["Apocalypse Asset Pack", "- cuddleebug", "Reborn - Main Menu Music", "- ErikMMusic"]
        self.consultants = ["Evan M. Powell - GTA"]

        self.mainmenu_button = pygame.image.load("./assets/main_menu/mainmenu_button.png") # Load exit button png
        self.highlighted_mainmenu = pygame.image.load("./assets/main_menu/mainmenu_button_highlighted.png") # Load highlighted exit button
        self.mainmenu_button_width = self.mainmenu_button.get_width() # Get width of the exit png
        self.mainmenu_button_height = self.mainmenu_button.get_height() # Get height of the exit png
        self.mainmenu_button_pos = (SCREEN_WIDTH/2 - (self.mainmenu_button_width/2), SCREEN_HEIGHT - (25 + self.mainmenu_button_height)) # Define position of exit button (25 pix up and in middle)

    # This function is called over and over in main when game_state is "Settings"
    def run(self):
        self.display_surface.fill((10, 10, 10))  # Fills the screen with dark grey

        # Display title
        title = self.title_font.render("CREDITS", True, (0, 224, 11))
        self.display_surface.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, 25))

        # Underline the sub title's font
        self.sub_title_font.set_underline(True)

        # Display subtitle "Game Developers"
        sub_title_authors = self.sub_title_font.render("Game Developers", True, (255, 255, 255))
        self.display_surface.blit(sub_title_authors, (SCREEN_WIDTH/4 - sub_title_authors.get_width()/2, 25 + title.get_height() + 50)) 

        # Calculate the total height of all authors
        total_authors_height = 0
        for author in self.authors:
            total_authors_height += self.author_font.render(author, True, (255, 255, 255)).get_height() + 10
        
        # Enumerate through the authors and display them to the screen
        y_offset_authors = 25 + title.get_height() + 50 + sub_title_authors.get_height() + 10
        for author in self.authors:
            author_text = self.author_font.render(author, True, (255, 255, 255))
            self.display_surface.blit(author_text, (SCREEN_WIDTH/4 - author_text.get_width()/2, y_offset_authors))
            y_offset_authors += author_text.get_height() + 10

        # Display subtitle "Assets"
        sub_title_assets = self.sub_title_font.render("Assets", True, (255, 255, 255))
        self.display_surface.blit(sub_title_assets, (SCREEN_WIDTH/4*3 - sub_title_assets.get_width()/2, 25 + title.get_height() + 50))

        # Enumerate through the asset credits and display them to the screen
        y_offset_assets = 25 + title.get_height() + 50 + sub_title_assets.get_height() + 10
        for asset in self.assets:
            asset_text = self.author_font.render(asset, True, (255, 255, 255))
            self.display_surface.blit(asset_text, (SCREEN_WIDTH/4*3 - asset_text.get_width()/2, y_offset_assets))
            y_offset_assets += asset_text.get_height() + 10

        # Display subtitle "Game Consultants"
        y_offset_consultants = total_authors_height + 25 + title.get_height() + 50 + sub_title_authors.get_height() + 50
        sub_title_consultants = self.sub_title_font.render("Game Consultants", True, (255, 255, 255))
        self.display_surface.blit(sub_title_consultants, (SCREEN_WIDTH/2 - sub_title_consultants.get_width()/2, y_offset_consultants))

        # Enumerate through the game consultants and display them to the screen
        y_offset_consultant = y_offset_consultants + sub_title_consultants.get_height() + 10
        for consultant in self.consultants:
            consultant_text = self.author_font.render(consultant, True, (255, 255, 255))
            self.display_surface.blit(consultant_text, (SCREEN_WIDTH/2 - consultant_text.get_width()/2, y_offset_consultant))
            y_offset_consultant += consultant_text.get_height() + 10

        pygame.event.get() # Gets game event
        mouse_state = pygame.mouse.get_pressed() # Gets which mouse buttons are currently pressed and which are not
        mouse_pos = pygame.mouse.get_pos() # Gets the position of the mouse

        # Display the exit button
        self.display_surface.blit(self.mainmenu_button, self.mainmenu_button_pos)

        # Checks position of mouse and if the left button is clicked
        if ((mouse_pos[0] > self.mainmenu_button_pos[0]) and (mouse_pos[0] < (self.mainmenu_button_pos[0] + self.mainmenu_button_width))) and \
        ((mouse_pos[1] > self.mainmenu_button_pos[1]) and (mouse_pos[1] < (self.mainmenu_button_pos[1] + self.mainmenu_button_height))):
            self.display_surface.blit(self.highlighted_mainmenu, self.mainmenu_button_pos) # Draws highlighted button over normal button if mouse is in its position
            if mouse_state[0] == True:  # If left button is clicked
                pygame.time.wait(500)
                return "Main Menu"  # Go back to the main menu
            else:
                return "Credits"  # If the button is not clicked it returns Credits -- the credits game_state
        else:
            return "Credits" # Returns Credits game_state -- runs if no button is clicked