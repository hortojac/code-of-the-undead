import sys
import pygame

from settings import Settings
from character import Character
from map import Map

class Game:
    # Overall class to manage game assets and behavior.
    def __init__(self):
        # Initialize the game, and create resources.
        pygame.init()
        self.settings = Settings()
        # Set the screen size to the monitor's size
        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Code of the Undead")
        # Create a Clock instance
        self.clock = pygame.time.Clock()
        # Create a Map instance
        self.map = Map(self.settings, self.screen)
        # Create a Character instance
        self.character = Character(self.screen)

    def run_game(self):
        # Start the main loop for the game.
        while True:
            self._check_events()
            self._update_character_position()
            self._update_screen()

            # Control the frame rate
            self.clock.tick(self.settings.FPS)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and (event.mod & pygame.KMOD_CTRL):
                    pygame.quit()
                    sys.exit()

    def _update_character_position(self):
        # Check for keys that are continuously pressed
        keys = pygame.key.get_pressed()
        if keys[self.settings.key_up]:
            self.character.y -= self.settings.walk_speed
            if keys[self.settings.key_sprint]:
                self.character.y -= self.settings.sprint_speed
        if keys[self.settings.key_down]:
            self.character.y += self.settings.walk_speed
            if keys[self.settings.key_sprint]:
                self.character.y += self.settings.sprint_speed
        if keys[self.settings.key_left]:
            self.character.x -= self.settings.walk_speed
            if keys[self.settings.key_sprint]:
                self.character.x -= self.settings.sprint_speed
        if keys[self.settings.key_right]:
            self.character.x += self.settings.walk_speed
            if keys[self.settings.key_sprint]:
                self.character.x += self.settings.sprint_speed

    def _update_screen(self):
        # Set the screen background color
        self.screen.fill(self.settings.bg_color)
        # Draw the map
        self.map.draw()
        # Draw the character with the camera offsets
        self.character.draw()
        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run_game()

