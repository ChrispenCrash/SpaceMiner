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

# Create a background surface for stars
background = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
background.fill(Colour.DARK_GREY)
for (x, y) in stars:
    pygame.draw.rect(background, Colour.WHITE, (x, y, 2, 2))

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
game_state = GameState.MAIN_MENU  # Start with the main menu

def reset_game():
    global score, start_time, game_state, all_sprites, asteroid_group, player
    score = 0
    start_time = pygame.time.get_ticks()
    game_state = GameState.PLAYING
    all_sprites.empty()
    asteroid_group.empty()
    player = Player()
    all_sprites.add(player)
    for _ in range(ASTEROID_COUNT):
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroid_group.add(asteroid)

def display_main_menu():
    window.fill(Colour.BLACK)
    title_text = large_font.render("Space Miner", True, Colour.WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    window.blit(title_text, title_rect)

    single_player_text = font.render("1. Single Player", True, Colour.WHITE)
    single_player_rect = single_player_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    window.blit(single_player_text, single_player_rect)

    multiplayer_text = font.render("2. Multiplayer", True, Colour.WHITE)
    multiplayer_rect = multiplayer_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    window.blit(multiplayer_text, multiplayer_rect)

    options_text = font.render("3. Options", True, Colour.WHITE)
    options_rect = options_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    window.blit(options_text, options_rect)

    exit_text = font.render("4. Exit", True, Colour.WHITE)
    exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    window.blit(exit_text, exit_rect)

    pygame.display.flip()

def display_pause_menu():
    window.fill(Colour.BLACK)
    pause_text = large_font.render("Paused", True, Colour.WHITE)
    pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    window.blit(pause_text, pause_rect)

    resume_text = font.render("Press P to resume", True, Colour.WHITE)
    resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    window.blit(resume_text, resume_rect)

    reset_text = font.render("Press R to reset", True, Colour.WHITE)
    reset_rect = reset_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    window.blit(reset_text, reset_rect)

    main_menu_text = font.render("Press M for Main Menu", True, Colour.WHITE)
    main_menu_rect = main_menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    window.blit(main_menu_text, main_menu_rect)

    quit_text = font.render("Press ESC to quit", True, Colour.WHITE)
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    window.blit(quit_text, quit_rect)

    pygame.display.flip()

# Game Loop
running = True
while running:
    dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_remaining = max(0, TIME_LIMIT - elapsed_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == GameState.MAIN_MENU:
                if event.key == pygame.K_1:
                    game_state = GameState.PLAYING
                elif event.key == pygame.K_2:
                    print("Multiplayer mode not implemented yet.")
                elif event.key == pygame.K_3:
                    print("Options menu not implemented yet.")
                elif event.key == pygame.K_4:
                    running = False
            elif game_state == GameState.PLAYING:
                if event.key == pygame.K_p:
                    game_state = GameState.PAUSED
            elif game_state == GameState.PAUSED:
                if event.key == pygame.K_p:
                    game_state = GameState.PLAYING
                elif event.key == pygame.K_m:
                    game_state = GameState.MAIN_MENU
                elif event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif game_state in [GameState.WON, GameState.GAME_OVER]:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_m:
                    game_state = GameState.MAIN_MENU
                elif event.key == pygame.K_ESCAPE:
                    running = False

    if game_state == GameState.MAIN_MENU:
        display_main_menu()
    elif game_state == GameState.PLAYING:
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
        window.blit(background, -camera_offset)

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

    elif game_state == GameState.PAUSED:
        display_pause_menu()

    else:
        # Draw Background Stars
        window.blit(background, -camera_offset)

        # Display victory or game over screen
        if game_state == GameState.WON:
            message_text = large_font.render("You won!", True, Colour.GREEN)
        else:
            message_text = large_font.render("Game over!", True, Colour.RED)

        message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(message_text, message_rect)

        # Optionally, you can add instructions to quit or restart
        # instruction_text = font.render("Press R to restart, M for main menu, or ESC to quit", True, Colour.WHITE)
        # instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        # window.blit(instruction_text, instruction_rect)
        reset_text = font.render("Press R to restart", True, Colour.WHITE)
        reset_rect = reset_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        window.blit(reset_text, reset_rect)

        main_menu_text = font.render("Press M for Main Menu", True, Colour.WHITE)
        main_menu_rect = main_menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        window.blit(main_menu_text, main_menu_rect)

        quit_text = font.render("Press ESC to quit", True, Colour.WHITE)
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        window.blit(quit_text, quit_rect)

        # Check for exit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        elif keys[pygame.K_r]:
            reset_game()
        elif keys[pygame.K_m]:
            game_state = GameState.MAIN_MENU

    pygame.display.flip()

pygame.quit()
sys.exit()