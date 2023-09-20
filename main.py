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

        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Code of the Undead")

        # Create a Clock instance
        self.clock = pygame.time.Clock()

        self.character = Character(self.screen)

        self.map = Map(self.settings, self.screen)

    def run_game(self):
        # Start the main loop for the game.
        while True:
            self._check_events()
            self._update_screen()

            # Control the frame rate
            self.clock.tick(self.settings.FPS)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # Check for keys that are continuously pressed
        keys = pygame.key.get_pressed()
        if keys[self.settings.key_up]:
            self.character.y -= self.settings.move_speed
            if keys[self.settings.key_sprint]:
                self.character.y -= self.settings.sprint_speed
        if keys[self.settings.key_down]:
            self.character.y += self.settings.move_speed
            if keys[self.settings.key_sprint]:
                self.character.y += self.settings.sprint_speed
        if keys[self.settings.key_left]:
            self.character.x -= self.settings.move_speed
            if keys[self.settings.key_sprint]:
                self.character.x -= self.settings.sprint_speed
        if keys[self.settings.key_right]:
            self.character.x += self.settings.move_speed
            if keys[self.settings.key_sprint]:
                self.character.x += self.settings.sprint_speed

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        self.map.draw()

        self.character.draw()

        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run_game()
