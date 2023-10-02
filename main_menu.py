import sys
import pygame
from settings import *

class MainMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()#get the surface to draw
        self.origin = (0,0)#define the origin

        self.title = pygame.image.load("./assets/main_menu/goodtitle.png")#load the png of the title of the game
        self.title_width = self.title.get_width()#get width of title png
        self.title_height = self.title.get_height()#get height of title png
        self.title_pos = (SCREEN_WIDTH/2 - (self.title_width/2), 25)#define the position of the title png

        self.exit_button = pygame.image.load("./assets/main_menu/exitbutton.png")#load exit button png
        self.highlighted_exit = pygame.image.load("./assets/main_menu/exitbutton_highlighted.png")#load highlighted exit button
        self.exit_button_width = self.exit_button.get_width()#get width of the exit png
        self.exit_button_height = self.exit_button.get_height()#get height of the exit png
        self.exit_button_pos = (SCREEN_WIDTH/2 - (self.exit_button_width/2), SCREEN_HEIGHT - (25 + self.exit_button_height))#define position of exit button (25 pix up and in middle)

        self.play_button = pygame.image.load("./assets/main_menu/play_button.png")#load the play button png
        self.highlighted_play = pygame.image.load("./assets/main_menu/play_button_highlighted.png")#load highlihgted play button
        self.play_button_width = self.play_button.get_width()#get the width of the play button
        self.play_button_height = self.play_button.get_height()#get the height of the play button
        self.play_button_pos = (SCREEN_WIDTH/2 - (self.play_button_width/2), self.exit_button_pos[1] - (10 + self.play_button_height))#define position of play button (10 above exit)

        self.settings_button = pygame.image.load("./assets/main_menu/settingsbutton.png")#load the settings button png
        self.highlighted_settings = pygame.image.load("./assets/main_menu/settingsbutton_highlighted.png")#load highlihgted settings button
        self.settings_button_width = self.settings_button.get_width()#get width of settings button
        self.settings_button_height = self.settings_button.get_height()#get height of settings button
        self.settings_button_pos = ((self.play_button_pos[0] - (10 + self.settings_button_width)), (self.play_button_pos[1] + self.play_button_height + 5 - (self.settings_button_height/2)))#define position of settings button

        self.credits_button = pygame.image.load("./assets/main_menu/creditsbutton.png")#load the credits button png
        self.highlighted_credits = pygame.image.load("./assets/main_menu/creditsbutton_highlighted.png")#load highlighted credits button
        self.credits_button_width = self.credits_button.get_width()#get width of credits button
        self.credits_button_height = self.credits_button.get_height()#get height of credits button
        self.credits_button_pos = ((self.play_button_pos[0] + self.play_button_width + 10), (self.settings_button_pos[1]))#define position of credits button

        self.code_bi = pygame.image.load("./assets/main_menu/bi_for_code.png")#load the png of word code in binary
        self.code_bi_width = self.code_bi.get_width()#get width of code binary
        self.code_bi_x = 0#x position of code binary png
        self.code_bi_y = (SCREEN_HEIGHT/6) - 40#y position of code binary png
        self.code_bi_2 = pygame.image.load("./assets/main_menu/bi_for_code.png")#load the 2nd png of word code in binary
        self.code_bi_2_width = self.code_bi_width#sets width to the same as the first
        self.code_bi_2_x = 0 + self.code_bi_width#sets the image location to the end of the first code bi
        self.code_bi_2_y = self.code_bi_y#sets to the same y position as the first one

        self.of_bi = pygame.image.load("./assets/main_menu/of_bi.png")#load the png of word of in binary
        self.of_bi_width = self.of_bi.get_width()#gets width of of_bi binary
        self.of_bi_x = 0#x position of binary png
        self.of_bi_y = 2*(SCREEN_HEIGHT/6) - 40#y position of of_binary png
        self.of_bi_2 = pygame.image.load("./assets/main_menu/of_bi.png")#load the png of word of in binary
        self.of_bi_2_width = self.of_bi_width#gets width of of_bi binary
        self.of_bi_2_x = self.of_bi_x - self.of_bi_2_width#x position of binary png
        self.of_bi_2_y = self.of_bi_y#y position of of_binary png

        self.the_bi = pygame.image.load("./assets/main_menu/the_bi.png")#load the png of word the in binary
        self.the_bi_width = self.the_bi.get_width()#gets width of the_bi binary
        self.the_bi_x = 0#x position of the binary png
        self.the_bi_y = 3*(SCREEN_HEIGHT/6) - 40#y position of the_binary png
        self.the_bi_2 = pygame.image.load("./assets/main_menu/the_bi.png")#load the png of word the in binary
        self.the_bi_2_width = self.the_bi_width#gets width of the_bi binary
        self.the_bi_2_x = 0 + self.the_bi_width#x position of the binary png
        self.the_bi_2_y = self.the_bi_y#y position of the_binary png

        self.undead_bi = pygame.image.load("./assets/main_menu/Undead_bi.png")#load the png of word undead in binary
        self.undead_bi_width = self.undead_bi.get_width()#gets width of undead_bi binary
        self.undead_bi_x = 0#x position of undead binary png
        self.undead_bi_y = 4*(SCREEN_HEIGHT/6) - 40#y position of undead_binary png
        self.undead_bi_2 = pygame.image.load("./assets/main_menu/undead_bi.png")#load the png of word undead in binary
        self.undead_bi_2_width = self.undead_bi_width#gets width of undead_bi binary
        self.undead_bi_2_x = 0 + self.undead_bi_width#x position of undead binary png
        self.undead_bi_2_y = self.undead_bi_y#y position of undead_binary png

        self.initials_bi = pygame.image.load("./assets/main_menu/GSNJE_bi.png")#load the png of word undead in binary
        self.initials_bi_width = self.initials_bi.get_width()#gets width of undead_bi binary
        self.initials_bi_x = 0#x position of undead binary png
        self.initials_bi_y = 5*(SCREEN_HEIGHT/6) - 40#y position of undead_binary png
        self.initials_bi_2 = pygame.image.load("./assets/main_menu/GSNJE_bi.png")#load the png of word undead in binary
        self.initials_bi_2_width = self.initials_bi_width#gets width of undead_bi binary
        self.initials_bi_2_x = self.initials_bi_x - self.initials_bi_2_width#x position of undead binary png
        self.initials_bi_2_y = self.initials_bi_y#y position of undead_binary png

    #This function is called over and over in main when game_state is 0 (main menu)
    def run(self):
        self.display_surface.fill((10, 10, 10))#fills the screen with dark grey
        self.display_surface.blit(self.code_bi, (self.code_bi_x, self.code_bi_y))#draw binary code
        self.display_surface.blit(self.code_bi_2, (self.code_bi_2_x, self.code_bi_2_y))#draw 2nd binary code
        if self.code_bi_2_x == 0:#if the 2nd png of the bi image has reached the left side of the screen
            self.code_bi_x = 0 + self.code_bi_2_width#it puts the first image of binary on the end of thet 2nd
        else:
            self.code_bi_x -= 1#scroll the binary code png
        if self.code_bi_x == 0:#if the first png of the bi image is on the left side of the screen
            self.code_bi_2_x = 0 + self.code_bi_width#it puts the second image of binary on the end of the first
        else:
            self.code_bi_2_x -= 1#scroll 2nd binary code png

        self.display_surface.blit(self.of_bi, (self.of_bi_x, self.of_bi_y))#draw binary of
        self.display_surface.blit(self.of_bi_2, (self.of_bi_2_x, self.of_bi_2_y))#draw 2nd binary of
        if self.of_bi_2_x  == 0:#if the 2nd png of the bi image has reached the right side of the screen
            self.of_bi_x = 0 - self.of_bi_width#it puts the first image of binary with its right end on the 0th pixel
        else:
            self.of_bi_x += 0.25#scroll the binary of png
        if self.of_bi_x == 0:#if the first png of the bi image is on the right side of the screen
            self.of_bi_2_x = 0 - self.of_bi_2_width#it puts the second image of binary with its right end on the 0th pixel
        else:
            self.of_bi_2_x += 0.25#scroll 2nd binary of png

        self.display_surface.blit(self.the_bi, (self.the_bi_x, self.the_bi_y))#draw binary the
        self.display_surface.blit(self.the_bi_2, (self.the_bi_2_x, self.the_bi_2_y))#draw 2nd binary the
        if self.the_bi_2_x == 0:#if the 2nd png of the bi image has reached the left side of the screen
            self.the_bi_x = 0 + self.the_bi_2_width#it puts the first image of binary on the end of thet 2nd
        else:
            self.the_bi_x -= 0.5#scroll the binary the png
        if self.the_bi_x == 0:#if the first png of the bi image is on the left side of the screen
            self.the_bi_2_x = 0 + self.the_bi_width#it puts the second image of binary on the end of the first
        else:
            self.the_bi_2_x -= 0.5#scroll 2nd binary the png

        self.display_surface.blit(self.undead_bi, (self.undead_bi_x, self.undead_bi_y))#draw binary the
        self.display_surface.blit(self.undead_bi_2, (self.undead_bi_2_x, self.undead_bi_2_y))#draw 2nd binary the
        if self.undead_bi_2_x == 0:#if the 2nd png of the bi image has reached the left side of the screen
            self.undead_bi_x = 0 + self.undead_bi_2_width#it puts the first image of binary on the end of thet 2nd
        else:
            self.undead_bi_x -= 2#scroll the binary the png
        if self.undead_bi_x == 0:#if the first png of the bi image is on the left side of the screen
            self.undead_bi_2_x = 0 + self.undead_bi_width#it puts the second image of binary on the end of the first
        else:
            self.undead_bi_2_x -= 2#scroll 2nd binary the png

        self.display_surface.blit(self.initials_bi, (self.initials_bi_x, self.initials_bi_y))#draw binary the
        self.display_surface.blit(self.initials_bi_2, (self.initials_bi_2_x, self.initials_bi_2_y))#draw 2nd binary the
        if self.initials_bi_2_x == 0:#if the 2nd png of the bi image has reached the right side of the screen
            self.initials_bi_x = 0 - self.initials_bi_width#it puts the first image of binary with its right end on the 0th pixel
        else:
            self.initials_bi_x += 1#scroll the binary the png
        if self.initials_bi_x == 0:#if the first png of the bi image is on the right side of the screen
            self.initials_bi_2_x = 0 - self.initials_bi_2_width#it puts the second image of binary with its right end on the 0th pixel
        else:
            self.initials_bi_2_x += 1#scroll 2nd binary the png
        self.display_surface.blit(self.title, self.title_pos)#draws the title
        self.display_surface.blit(self.exit_button, self.exit_button_pos)#draws the exit button
        self.display_surface.blit(self.play_button, self.play_button_pos)#draws the play button
        self.display_surface.blit(self.settings_button, self.settings_button_pos)#draws the settings button
        self.display_surface.blit(self.credits_button, self.credits_button_pos)#draw the credits button

        for event in pygame.event.get():#loops through game events
            if event.type == pygame.QUIT:#if it is a quit event it quits the game and exits it
                 pygame.quit()
                 sys.exit()
        pygame.event.get()#gets game event
        mouse_state = pygame.mouse.get_pressed()#gets which mouse buttons are currently pressed and which are not
        mouse_pos = pygame.mouse.get_pos()#gets the position of the mouse

        #check position of mouse and if mouse is clicked to see if and what button is pressed
        if ((mouse_pos[0] > self.play_button_pos[0]) and (mouse_pos[0] < (self.play_button_pos[0] + self.play_button_width))) and \
        ((mouse_pos[1] > self.play_button_pos[1]) and (mouse_pos[1] < (self.play_button_pos[1] + self.play_button_height))):
            self.display_surface.blit(self.highlighted_play, self.play_button_pos)#draws highlighted button over normal button if mouse is in its position
            if mouse_state[0] == True:#if left mouse button is clicked
                return 1 #returns 1 which is the game_state of "playing"
        #check position of mouse
        if ((mouse_pos[0] > self.settings_button_pos[0]) and (mouse_pos[0] < (self.settings_button_pos[0] + self.settings_button_width))) and \
        ((mouse_pos[1] > self.settings_button_pos[1]) and (mouse_pos[1] < (self.settings_button_pos[1] + self.settings_button_height))):
            self.display_surface.blit(self.highlighted_settings, self.settings_button_pos)#draws highlighted button over normal button if mouse is in its position
        #checks position of mouse
        if ((mouse_pos[0] > self.credits_button_pos[0]) and (mouse_pos[0] < (self.credits_button_pos[0] + self.credits_button_width))) and \
        ((mouse_pos[1] > self.credits_button_pos[1]) and (mouse_pos[1] < (self.credits_button_pos[1] + self.credits_button_height))):
            self.display_surface.blit(self.highlighted_credits, self.credits_button_pos)#draws highlighted button over normal button if mouse is in its position
        #checks position of mouse and if the left button is clicked
        if ((mouse_pos[0] > self.exit_button_pos[0]) and (mouse_pos[0] < (self.exit_button_pos[0] + self.exit_button_width))) and \
        ((mouse_pos[1] > self.exit_button_pos[1]) and (mouse_pos[1] < (self.exit_button_pos[1] + self.exit_button_height))):
            self.display_surface.blit(self.highlighted_exit, self.exit_button_pos)#draws highlighted button over normal button if mouse is in its position
            if mouse_state[0] == True:#if left button is clicked it quits and exits the game
                pygame.quit()
                sys.exit()
            else:
                return 0#if the button is not clicked it returns 0 -- the main menu game_state
        else:
            return 0 #returns 0 game_state of main menu -- runs if no button is clicked
