import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import random
import sys
from enums import GameState, Colour

from player import Player
from asteroid import Asteroid

from settings import WIDTH, HEIGHT, GAME_WIDTH, GAME_HEIGHT, FPS
from settings import ASTEROID_COUNT, ASTEROID_WIN_COUNT, TIME_LIMIT

# Initialize Pygame
pygame.init()

# Add a camera offset
camera_offset = pygame.Vector2(0, 0)

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
        # all_sprites.update()
        for sprite in all_sprites:
            if isinstance(sprite, Player):
                sprite.update(camera_offset)
            else:
                sprite.update()

        # Check for collisions
        hits = pygame.sprite.spritecollide(player, asteroid_group, True)
        if hits:
            score += len(hits)

        # Check for win or time up
        if score >= ASTEROID_WIN_COUNT:
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
                sprite.draw(window, camera_offset)  # Custom draw method for player with tail
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