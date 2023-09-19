import sys
import pygame

from settings import Settings
from character import Character

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
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

        # Check for keys that are continously pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.character.y -= 2
        if keys[pygame.K_s]:
            self.character.y += 2
        if keys[pygame.K_a]:
            self.character.x -= 2
        if keys[pygame.K_d]:
            self.character.x += 2

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.character.draw()
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run_game()
