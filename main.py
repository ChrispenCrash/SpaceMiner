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
TIME_LIMIT = 120  # in seconds

# Colors
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
VICTORY_COLOR = (0, 255, 0)
GAME_OVER_COLOR = (255, 0, 0)

# Set up the display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blob Collect Game")
clock = pygame.time.Clock()

# Font for score and timer
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

# Define GameState Enum
class GameState(Enum):
    PLAYING = 1
    WON = 2
    GAME_OVER = 3

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image_orig, PLAYER_COLOR, (10, 10), 10)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.pos = pygame.math.Vector2(self.rect.center)
        # Start with a random angle
        self.angle = random.uniform(0, 360)
        # Direction vector based on the angle
        radians = math.radians(self.angle)
        self.direction = pygame.math.Vector2(math.cos(radians), math.sin(radians))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROTATE_SPEED
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROTATE_SPEED

        # Keep angle within [0, 360)
        self.angle %= 360

        # Update direction vector based on angle
        radians = math.radians(self.angle)
        self.direction = pygame.math.Vector2(math.cos(radians), math.sin(radians))

        # Update position
        self.pos += self.direction * PLAYER_SPEED

        # Check for collisions with walls and bounce
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

# Food Class
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, FOOD_COLOR, (7, 7), 7)
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
        window.fill(BLACK)
        all_sprites.draw(window)

        # Render score
        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        window.blit(score_text, (10, 10))

        # Render timer
        minutes = int(time_remaining) // 60
        seconds = int(time_remaining) % 60
        timer_text = font.render(f"Time: {minutes}:{seconds:02}", True, TEXT_COLOR)
        window.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))

    else:
        # Display victory or game over screen
        window.fill(BLACK)
        if game_state == GameState.WON:
            message_text = large_font.render("You won!", True, VICTORY_COLOR)
        else:
            message_text = large_font.render("Game over!", True, GAME_OVER_COLOR)

        message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(message_text, message_rect)

        # Optionally, you can add instructions to quit or restart
        instruction_text = font.render("Press ESC to quit", True, TEXT_COLOR)
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        window.blit(instruction_text, instruction_rect)

        # Check for exit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()