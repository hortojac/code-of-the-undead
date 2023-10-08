import pygame
import sys

class Enemy:
    # Initialize
    def __init__(self, pos):
        self.image = pygame.image.load("./assets/textures/zombie_test.png") # Load image
        self.health = 10 # Set enemy health
        self.rect = self.image.get_rect(center=pos) # Make a rect that matches image
        self.pos = pygame.math.Vector2(self.rect.center)  # Set posiiton
    def update(self, player_pos):    
        player_vec = pygame.math.Vector2(player_pos) # Convert player position to a vector    
        direction = player_vec - self.pos # Calculate the direction vector from enemy to player   
        direction.normalize_ip() # Normalize the direction vector to get a unit vector  
        self.pos += direction * 0.1 # Move the enemy towards the player by a certain speed (e.g., 0.5)
        self.rect.center = self.pos # Update the rect position
        if self.health <= 0:  # Check enemy health
            pygame.quit()
            sys.exit()

    def draw(self):
        surface = pygame.display.get_surface() # Get the surface
        surface.blit(self.image, (self.pos.x, self.pos.y)) # Print the image