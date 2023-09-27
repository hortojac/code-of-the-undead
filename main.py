import sys
import pygame
from settings import *
from map import Map
from main_menu import MainMenu

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
        # Create a Map instance
        self.map = Map()
        # probably a better way to do this but for now
        # 0 means main menu 1 means play
        self.game_state = 0

    def run_game(self):
        # Start the main loop for the game.
        while True:
            for event in pygame.event.get():
                # Check for quit events
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and (event.mod & pygame.KMOD_CTRL):
                        pygame.quit()
                        sys.exit()

            dt = self.clock.tick() / 1000.0
            # Draw the menu
            if self.game_state == 0:
                self.game_state = self.main_menu.run()
            # Draw the map
            if self.game_state == 1:
                self.map.run(dt)
            # Make the most recently drawn screen visible
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run_game()
