import pygame
import random

from settings import GAME_WIDTH, GAME_HEIGHT

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        asteroid_image = pygame.image.load("assets/asteroid.png").convert_alpha()
        self.image = pygame.transform.scale(asteroid_image, (7, 7))
        rotation_angle = random.choice([0, 90, 180, 270])
        self.image = pygame.transform.rotate(asteroid_image, rotation_angle)
        
        # Set the position of the asteroid
        self.rect = self.image.get_rect(center=(random.randint(10, GAME_WIDTH - 10), random.randint(10, GAME_HEIGHT - 10)))

    def draw(self, surface, camera_offset):
        surface.blit(self.image, self.rect.topleft - camera_offset)