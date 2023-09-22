import pygame

class Settings:
    def __init__(self):
        pygame.init()  # Initialize Pygame
        info = pygame.display.Info()  # Get monitor info

        # Set the screen width and height to the monitor's size
        self.screen_width = info.current_w
        self.screen_height = info.current_h

        self.bg_color = (225, 225, 225) # Set the background color
        
        self.FPS = 60 # Set the FPS

        self.walk_speed = 2 # Set the default movement speed
        self.sprint_speed = 4 # Set the deafult sprint speed

        # Define deafult key bindings
        self.key_up = pygame.K_w # Move up
        self.key_down = pygame.K_s # Move down
        self.key_left = pygame.K_a # Move left
        self.key_right = pygame.K_d # Move right

        self.key_sprint = pygame.K_LSHIFT # Sprint
