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
FOOD_COUNT = 10
TIME_LIMIT = 30  # in seconds

class Colour(tuple, Enum):
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

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

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image_orig, Colour.GREEN, (10, 10), 10)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.angle = random.uniform(0, 360)
        radians = math.radians(self.angle)
        self.direction = pygame.math.Vector2(math.cos(radians), math.sin(radians))
        
        # List to store tail positions
        self.tail_positions = []
        self.max_tail_length = 13  # Adjust for desired tail length

    def update(self):
        # Update position and rotation as before
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROTATE_SPEED
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROTATE_SPEED

        self.angle %= 360
        radians = math.radians(self.angle)
        self.direction = pygame.math.Vector2(math.cos(radians), math.sin(radians))
        self.pos += self.direction * PLAYER_SPEED

        # Boundary checks
        if self.pos.x <= 10:
            self.pos.x = 10
            self.direction.x *= -1
            self.angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
        elif self.pos.x >= WIDTH - 10:
            self.pos.x = WIDTH - 10
            self.direction.x *= -1
            self.angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
        if self.pos.y <= 10:
            self.pos.y = 10
            self.direction.y *= -1
            self.angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
        elif self.pos.y >= HEIGHT - 10:
            self.pos.y = HEIGHT - 10
            self.direction.y *= -1
            self.angle = math.degrees(math.atan2(self.direction.y, self.direction.x))

        # Rotate the image
        self.image = pygame.transform.rotate(self.image_orig, -self.angle)
        self.rect = self.image.get_rect(center=self.pos)

        # Add current position to tail positions
        self.tail_positions.append(self.pos.copy())
        if len(self.tail_positions) > self.max_tail_length:
            self.tail_positions.pop(0)  # Limit the tail length

    def draw(self, surface):
        # Define the tail size and fading effect
        max_radius = 10  # Largest radius, closest to the player
        min_radius = 2   # Smallest radius, farthest from the player
        
        tail_length = len(self.tail_positions)
        
        for i, pos in enumerate(self.tail_positions):
            # Set radius and alpha for the fading and tapering effect
            # Both radius and alpha decrease further from the player
            radius = int(min_radius + (max_radius - min_radius) * (i / tail_length))
            alpha = int(255 * (i / tail_length))  # More transparent for smaller, far segments
            color = (*Colour.GREEN, alpha)
            
            # Draw each segment with its computed size and alpha
            tail_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(tail_surf, color, (radius, radius), radius)
            surface.blit(tail_surf, pos - pygame.math.Vector2(radius, radius))  # Center the tail segment

        # Draw the player itself
        surface.blit(self.image, self.rect)

# Update the main loop to call player.draw() instead of relying on the default all_sprites.draw(window)

# Food Class
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, Colour.RED, (7, 7), 7)
        self.rect = self.image.get_rect(center=(random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10)))

# Sprite Groups
all_sprites = pygame.sprite.Group()
food_group = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Spawn initial food blobs
for _ in range(FOOD_COUNT):
    food = Food()
    all_sprites.add(food)
    food_group.add(food)

# Game Variables
score = 0
start_time = pygame.time.get_ticks()
game_state = GameState.PLAYING  # Using Enum instead of string

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
        hits = pygame.sprite.spritecollide(player, food_group, True)
        if hits:
            score += len(hits)

        # Check for win or time up
        if score >= FOOD_COUNT:
            game_state = GameState.WON
        elif elapsed_time >= TIME_LIMIT:
            game_state = GameState.GAME_OVER

        # Draw
        window.fill(Colour.BLACK)

        # all_sprites.draw(window)
        # Draw all elements
        window.fill(Colour.BLACK)
        for sprite in all_sprites:
            if isinstance(sprite, Player):
                sprite.draw(window)  # Custom draw method for player with tail
            else:
                window.blit(sprite.image, sprite.rect)


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