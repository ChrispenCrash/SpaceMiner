import pygame
import random
import math
import sys

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

# Set up the display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blob Collect Game")
clock = pygame.time.Clock()

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, PLAYER_COLOR, (10, 10), 10)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(0, -1)  # Facing upwards
        self.angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += PLAYER_ROTATE_SPEED
        if keys[pygame.K_RIGHT]:
            self.angle -= PLAYER_ROTATE_SPEED

        # Update direction based on angle
        self.direction = pygame.math.Vector2(0, -1).rotate(self.angle)
        self.pos += self.direction * PLAYER_SPEED
        self.rect.center = self.pos

        # Keep the player within the game area
        self.pos.x = max(10, min(WIDTH - 10, self.pos.x))
        self.pos.y = max(10, min(HEIGHT - 10, self.pos.y))

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

# Game Loop
running = True
while running:
    dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.spritecollide(player, food_group, True)
    if hits:
        score += len(hits)
        print(f"Score: {score}")

    # Check for win or time up
    if score >= FOOD_COUNT:
        print("You collected all the food blobs! You win!")
        running = False
    elif elapsed_time >= TIME_LIMIT:
        print("Time's up! Game over!")
        running = False

    # Draw
    window.fill(BLACK)
    all_sprites.draw(window)
    pygame.display.flip()

pygame.quit()
sys.exit()