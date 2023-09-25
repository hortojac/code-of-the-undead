import pygame

class MainMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.origin = (0,0)
        self.background = pygame.image.load("./assets/badmenu.png")

    def run(self):
        self.display_surface.blit(self.background, self.origin)