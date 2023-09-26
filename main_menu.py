import pygame
from settings import *

class MainMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.origin = (0,0)
        self.background = pygame.image.load("./assets/badmenu.png")
        self.title = pygame.image.load("./assets/goodtitle.png")
        self.title_width = self.title.get_width()
        self.title_height = self.title.get_height()
        self.title_pos = (SCREEN_WIDTH/2 - (self.title_width/2), 25)
        self.play_button = pygame.image.load("./assets/badplaybutton.png")
        self.play_button_width = self.play_button.get_width()
        self.play_button_height = self.play_button.get_height()
        self.play_button_pos = (SCREEN_WIDTH/2 - (self.play_button_width/2), SCREEN_HEIGHT - (50 + self.play_button_height))

    def run(self):
        self.display_surface.fill((10, 10, 10))
        self.display_surface.blit(self.title, self.title_pos)
        self.display_surface.blit(self.play_button, self.play_button_pos)
        pygame.event.get()
        mouse_state = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        #check position of mouse and if mouse is clicked to see if and what button is pressed
        if ((mouse_pos[0] > self.play_button_pos[0]) and (mouse_pos[0] < (self.play_button_pos[0] + self.play_button_width))) and \
        ((mouse_pos[1] > self.play_button_pos[1]) and (mouse_pos[1] < (self.play_button_pos[1] + self.play_button_height))) and \
        mouse_state[0] == True:
            return 1 #returns 1 which is the game_state of "playing"
        else:
            return 0 #returns 0 game_state of main menu -- runs if no button is clicked
