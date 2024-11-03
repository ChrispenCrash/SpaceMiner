import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import random
import math
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 600
FPS = 60
PLAYER_SPEED = 5
PLAYER_ROTATE_SPEED = 5
ASTEROID_COUNT = 10
TIME_LIMIT = 30  # in seconds

# Define the larger game space dimensions
GAME_WIDTH, GAME_HEIGHT = WIDTH * 2, HEIGHT * 2  # Twice the size of the window

# Add a camera offset
camera_offset = pygame.Vector2(0, 0)

class Colour(tuple, Enum):
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    ORANGE = (255, 165, 0)
    GREY = (128, 128, 128)
    DARK_GREY = (15, 15, 15)

# Define GameState Enum
class GameState(Enum):
    PLAYING = 1
    WON = 2
    GAME_OVER = 3

# Set up the display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Miner")
clock = pygame.time.Clock()

# Font for score and timer
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)


# Define star density (stars per 10,000 pixels, adjust as needed)
STAR_DENSITY = 0.0002  # 0.02 stars per 100 pixels would roughly give 120 stars on a 600x600 window
STAR_COUNT = int(GAME_WIDTH * GAME_HEIGHT * STAR_DENSITY)

# Generate scaled star positions
stars = [(random.randint(0, GAME_WIDTH), random.randint(0, GAME_HEIGHT)) for _ in range(STAR_COUNT)]

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load the pixel art rocket image
        self.image_orig = pygame.image.load("assets/player_rocket.png").convert_alpha()
        self.image_orig = pygame.transform.scale(self.image_orig, (40, 40))  # Adjust dimensions as needed


        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.pos = pygame.math.Vector2(GAME_WIDTH // 2, GAME_HEIGHT // 2)  # Start in the center of the game space
        self.angle = random.uniform(0, 360)
        radians = math.radians(self.angle)
        self.direction = pygame.math.Vector2(math.cos(radians), math.sin(radians))
        
        # List to store tail positions
        self.tail_positions = []
        self.max_tail_length = 13  # Adjust for desired tail length

    def update(self):
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


    def draw(self, surface):
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


# Update the main loop to call player.draw() instead of relying on the default all_sprites.draw(window)

# Asteroid Class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        asteroid_image = pygame.image.load("assets/asteroid.png").convert_alpha()
        self.image = pygame.transform.scale(asteroid_image, (7, 7))
        rotation_angle = random.choice([0, 90, 180, 270])
        self.image = pygame.transform.rotate(asteroid_image, rotation_angle)
        
        # Set the position of the asteroid
        self.rect = self.image.get_rect(center=(random.randint(10, GAME_WIDTH - 10), random.randint(10, GAME_HEIGHT - 10)))


# Sprite Groups
all_sprites = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Spawn initial asteroids
for _ in range(ASTEROID_COUNT):
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroid_group.add(asteroid)

# Game Variables
score = 0
start_time = pygame.time.get_ticks()
game_state = GameState.PLAYING

# Game Loop
running = True
while running:
    dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_remaining = max(0, TIME_LIMIT - elapsed_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == GameState.PLAYING:
        # Update
        all_sprites.update()

        # Check for collisions
        hits = pygame.sprite.spritecollide(player, asteroid_group, True)
        if hits:
            score += len(hits)

        # Check for win or time up
        if score >= ASTEROID_COUNT:
            game_state = GameState.WON
        elif elapsed_time >= TIME_LIMIT:
            game_state = GameState.GAME_OVER

        # Draw Background Stars
        window.fill(Colour.DARK_GREY)
        for (x, y) in stars:
            star_x = x - camera_offset.x
            star_y = y - camera_offset.y
            pygame.draw.rect(window, Colour.WHITE, (star_x, star_y, 2, 2))

        # Draw all elements
        for sprite in all_sprites:
            if isinstance(sprite, Player):
                sprite.draw(window)  # Custom draw method for player with tail
            else:
                window.blit(sprite.image, sprite.rect.topleft - camera_offset)

        # Render score
        score_text = font.render(f"Score: {score}", True, Colour.WHITE)
        window.blit(score_text, (10, 10))

        # Render timer
        minutes = int(time_remaining) // 60
        seconds = int(time_remaining) % 60
        timer_text = font.render(f"Time: {minutes}:{seconds:02}", True, Colour.WHITE)
        window.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))

    else:
        # Display victory or game over screen
        window.fill(Colour.BLACK)
        if game_state == GameState.WON:
            message_text = large_font.render("You won!", True, Colour.GREEN)
        else:
            message_text = large_font.render("Game over!", True, Colour.RED)

        message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(message_text, message_rect)

        # Optionally, you can add instructions to quit or restart
        instruction_text = font.render("Press ESC to quit", True, Colour.WHITE)
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        window.blit(instruction_text, instruction_rect)

        # Check for exit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()