import pygame
import random
import math
from settings import WIDTH, HEIGHT, PLAYER_SPEED, PLAYER_HEIGHT, PLAYER_WIDTH
from settings import PLAYER_ROTATE_SPEED, GAME_WIDTH, GAME_HEIGHT
from enums import Colour

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load the pixel art rocket image
        try:
            self.image_orig = pygame.image.load("assets/player_rocket.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading player image: {e}")
            pygame.quit()
            
        self.image_orig = pygame.transform.scale(self.image_orig, (PLAYER_HEIGHT, PLAYER_WIDTH))  # Adjust dimensions as needed

        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.pos = pygame.math.Vector2(GAME_WIDTH // 2, GAME_HEIGHT // 2)  # Start in the center of the game space
        self.angle = random.uniform(0, 360)
        radians = math.radians(self.angle)
        self.direction = pygame.math.Vector2(math.cos(radians), math.sin(radians))
        
        # List to store tail positions
        self.tail_positions = []
        self.max_tail_length = 13  # Adjust for desired tail length

    def update(self, camera_offset):
        # Same movement and angle update logic as before
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROTATE_SPEED
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROTATE_SPEED

        self.angle %= 360
        radians = math.radians(self.angle)
        self.direction = pygame.math.Vector2(math.cos(radians), math.sin(radians))
        self.pos += self.direction * PLAYER_SPEED

        # Updated boundary checks for the larger game space
        if self.pos.x <= 10:
            self.pos.x = 10
            self.direction.x *= -1
            self.angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
        elif self.pos.x >= GAME_WIDTH - 10:
            self.pos.x = GAME_WIDTH - 10
            self.direction.x *= -1
            self.angle = math.degrees(math.atan2(self.direction.y, self.direction.x))

        if self.pos.y <= 10:
            self.pos.y = 10
            self.direction.y *= -1
            self.angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
        elif self.pos.y >= GAME_HEIGHT - 10:
            self.pos.y = GAME_HEIGHT - 10
            self.direction.y *= -1
            self.angle = math.degrees(math.atan2(self.direction.y, self.direction.x))

        # Rotate the image
        self.image = pygame.transform.rotate(self.image_orig, -self.angle - 90)
        self.rect = self.image.get_rect(center=self.pos)

        # Add current position to tail positions as before
        self.tail_positions.append(self.pos.copy())
        if len(self.tail_positions) > self.max_tail_length:
            self.tail_positions.pop(0)

        # Update camera offset based on player's position
        camera_offset.x = max(0, min(self.pos.x - WIDTH / 2, GAME_WIDTH - WIDTH))
        camera_offset.y = max(0, min(self.pos.y - HEIGHT / 2, GAME_HEIGHT - HEIGHT))

    def draw(self, surface, camera_offset):
        # Draw the tail relative to the camera offset
        max_radius = 7  # Largest radius for the part of the tail closest to the player
        min_radius = 2   # Smallest radius for the part of the tail farthest from the player
        
        tail_length = len(self.tail_positions)
        
        for i, pos in enumerate(self.tail_positions):
            # Set radius and alpha for the fading and tapering effect
            radius = int(min_radius + (max_radius - min_radius) * (i / tail_length))
            alpha = int(255 * (i / tail_length))  # More transparent further from the player
            color = (*Colour.ORANGE, alpha)

            # Draw each segment with computed size and transparency relative to the camera offset
            tail_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(tail_surf, color, (radius, radius), radius)
            draw_pos = pos - camera_offset  # Position adjusted by camera offset
            surface.blit(tail_surf, draw_pos - pygame.math.Vector2(radius, radius))  # Center the tail segment

        # Draw the player itself relative to the camera offset
        surface.blit(self.image, self.rect.topleft - camera_offset)

    def serialize(self):
        return {'pos': (self.pos.x, self.pos.y), 'angle': self.angle}

    @staticmethod
    def deserialize(data):
        player = Player()
        player.pos = pygame.Vector2(data['pos'])
        player.angle = data['angle']
        radians = math.radians(player.angle)
        player.direction = pygame.math.Vector2(math.cos(radians), math.sin(radians))
        player.rect = player.image.get_rect(center=player.pos)
        return player