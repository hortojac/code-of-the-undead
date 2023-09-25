import pygame
from settings import *

class MainMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.origin = (0,0)
        self.background = pygame.image.load("./assets/badmenu.png")
        self.play_button = pygame.image.load("./assets/badplaybutton.png")
        self.play_button_width = self.play_button.get_width()
        self.play_button_height = self.play_button.get_height()
        self.play_button_pos = (SCREEN_WIDTH/2 - (self.play_button_width/2), SCREEN_HEIGHT/2 - (self.play_button_height/2))

    def run(self):
        self.display_surface.blit(self.background, self.origin)
        self.display_surface.blit(self.play_button, self.play_button_pos)
        pygame.event.get()
        mouse_state = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if ((mouse_pos[0] > self.play_button_pos[0]) and (mouse_pos[0] < (self.play_button_pos[0] + self.play_button_width))) and \
        ((mouse_pos[1] > self.play_button_pos[1]) and (mouse_pos[1] < (self.play_button_pos[1] + self.play_button_height))) and \
        mouse_state[0] == True:
            return 1
        else:
            return 0
