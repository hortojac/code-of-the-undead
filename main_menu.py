import sys
import pygame
from settings import *

class MainMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()#get the surface to draw
        self.origin = (0,0)#define the origin

        self.title = pygame.image.load("./assets/goodtitle.png")#load the png of the title of the game
        self.title_width = self.title.get_width()#get width of title png
        self.title_height = self.title.get_height()#get height of title png
        self.title_pos = (SCREEN_WIDTH/2 - (self.title_width/2), 25)#define the position of the title png

        self.exit_button = pygame.image.load("./assets/exitbutton.png")#load exit button png
        self.exit_button_width = self.exit_button.get_width()#get width of the exit png
        self.exit_button_height = self.exit_button.get_height()#get height of the exit png
        self.exit_button_pos = (SCREEN_WIDTH/2 - (self.exit_button_width/2), SCREEN_HEIGHT - (25 + self.exit_button_height))#define position of exit button (25 pix up and in middle)

        self.play_button = pygame.image.load("./assets/play_button.png")#load the play button png
        self.play_button_width = self.play_button.get_width()#get the width of the play button
        self.play_button_height = self.play_button.get_height()#get the height of the play button
        self.play_button_pos = (SCREEN_WIDTH/2 - (self.play_button_width/2), self.exit_button_pos[1] - (10 + self.play_button_height))#define position of play button (10 above exit)

        self.settings_button = pygame.image.load("./assets/settingsbutton.png")#load the settings button png
        self.settings_button_width = self.settings_button.get_width()#get width of settings button
        self.settings_button_height = self.settings_button.get_height()#get height of settings button
        self.settings_button_pos = ((self.play_button_pos[0] - (10 + self.settings_button_width)), (self.play_button_pos[1] + self.play_button_height + 5 - (self.settings_button_height/2)))#define position of settings button

        self.credits_button = pygame.image.load("./assets/creditsbutton.png")#load the credits button png
        self.credits_button_width = self.credits_button.get_width()#get width of credits button
        self.credits_button_height = self.credits_button.get_height()#get height of credits button
        self.credits_button_pos = ((self.play_button_pos[0] + self.play_button_width + 10), (self.settings_button_pos[1]))#define position of credits button

        self.code_bi = pygame.image.load("./assets/bi_for_code.png")#load the png of word code in binary
        self.code_bi_width = self.code_bi.get_width()#get width of code binary
        self.code_bi_x = 0#x position of code binary png
        self.code_bi_y = 10#y position of code binary png
        self.code_bi_2 = pygame.image.load("./assets/bi_for_code.png")#load the 2nd png of word code in binary
        self.code_bi_2_width = self.code_bi_width#sets width to the same as the first
        self.code_bi_2_x = 0 + self.code_bi_width#sets the image location to the end of the first code bi
        self.code_bi_2_y = self.code_bi_y#sets to the same y position as the first one

    #This function is called over and over in main when game_state is 0 (main menu)
    def run(self):
        self.display_surface.fill((10, 10, 10))#fills the screen with dark grey
        self.display_surface.blit(self.code_bi, (self.code_bi_x, self.code_bi_y))#draw binary code
        self.display_surface.blit(self.code_bi_2, (self.code_bi_2_x, self.code_bi_2_y))#draw 2nd binary code
        if self.code_bi_2_x == 0:
            self.code_bi_x = 0 + self.code_bi_2_width
        else:
            self.code_bi_x -= 1#scroll the binary code png
        if self.code_bi_x == 0:
            self.code_bi_2_x = 0 + self.code_bi_width
        else:
            self.code_bi_2_x -= 1#scroll 2nd binary code png
        self.display_surface.blit(self.title, self.title_pos)#draws the title
        self.display_surface.blit(self.exit_button, self.exit_button_pos)#draws the exit button
        self.display_surface.blit(self.play_button, self.play_button_pos)#draws the play button
        self.display_surface.blit(self.settings_button, self.settings_button_pos)#draws the settings button
        self.display_surface.blit(self.credits_button, self.credits_button_pos)#draw the credits button

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
        pygame.event.get()
        mouse_state = pygame.mouse.get_pressed()#gets which mouse buttons are currently pressed and which are not
        mouse_pos = pygame.mouse.get_pos()#gets the position of the mouse

        #check position of mouse and if mouse is clicked to see if and what button is pressed
        if ((mouse_pos[0] > self.play_button_pos[0]) and (mouse_pos[0] < (self.play_button_pos[0] + self.play_button_width))) and \
        ((mouse_pos[1] > self.play_button_pos[1]) and (mouse_pos[1] < (self.play_button_pos[1] + self.play_button_height))) and \
        mouse_state[0] == True:
            return 1 #returns 1 which is the game_state of "playing"
        if ((mouse_pos[0] > self.exit_button_pos[0]) and (mouse_pos[0] < (self.exit_button_pos[0] + self.exit_button_width))) and \
        ((mouse_pos[1] > self.exit_button_pos[1]) and (mouse_pos[1] < (self.exit_button_pos[1] + self.exit_button_height))) and \
        mouse_state[0] == True:
            pygame.quit()
            sys.exit()
        else:
            return 0 #returns 0 game_state of main menu -- runs if no button is clicked
