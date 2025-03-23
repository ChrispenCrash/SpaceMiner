import pygame
import random
from settings import GAME_WIDTH, GAME_HEIGHT, ASTEROID_HEIGHT, ASTEROID_WIDTH

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.Vector2(random.randint(10, GAME_WIDTH - 10), random.randint(10, GAME_HEIGHT - 10))
        self.angle = random.choice([0, 90, 180, 270])

        if pygame.display.get_init():
            asteroid_image = pygame.image.load("assets/asteroid.png").convert_alpha()
            self.image = pygame.transform.scale(asteroid_image, (ASTEROID_HEIGHT, ASTEROID_WIDTH))
            self.image = pygame.transform.rotate(self.image, self.angle)
        else:
            # Fill a white square if pygame is not initialized
            self.image = pygame.Surface((ASTEROID_HEIGHT, ASTEROID_WIDTH))
            self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

    def draw(self, surface, camera_offset):
        if self.image:
            draw_position = self.rect.topleft - camera_offset
            surface.blit(self.image, draw_position)

    def serialize(self):
        return {'pos': (self.pos.x, self.pos.y), 'angle': self.angle}

    @staticmethod
    def deserialize(data):
        asteroid = Asteroid()
        asteroid.pos = pygame.Vector2(data['pos'])
        asteroid.angle = data['angle']
        if pygame.display.get_init():
            asteroid_image = pygame.image.load("assets/asteroid.png").convert_alpha()
            asteroid.image = pygame.transform.scale(asteroid_image, (ASTEROID_HEIGHT, ASTEROID_WIDTH))
            asteroid.image = pygame.transform.rotate(asteroid.image, asteroid.angle)
        else:
            asteroid.image = pygame.Surface((ASTEROID_HEIGHT, ASTEROID_WIDTH))
            asteroid.image.fill((255, 255, 255))
        asteroid.rect = asteroid.image.get_rect(center=(asteroid.pos.x, asteroid.pos.y))
        return asteroid