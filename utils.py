import pygame
from enums import Colour, GameState
from settings import WIDTH, HEIGHT

def display_main_menu(window, large_font, font, background, camera_offset):
    window.blit(background, -camera_offset)
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

def display_pause_menu(window, large_font, font, background, camera_offset):
    window.blit(background, -camera_offset)
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

def display_end_screen(window, large_font, font, game_state, background, camera_offset):
    window.blit(background, -camera_offset)
    if game_state == GameState.WON:
        message_text = large_font.render("You won!", True, Colour.GREEN)
    else:
        message_text = large_font.render("Game over!", True, Colour.RED)

    message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(message_text, message_rect)

    reset_text = font.render("Press R to restart", True, Colour.WHITE)
    reset_rect = reset_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    window.blit(reset_text, reset_rect)

    main_menu_text = font.render("Press M for Main Menu", True, Colour.WHITE)
    main_menu_rect = main_menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    window.blit(main_menu_text, main_menu_rect)

    quit_text = font.render("Press ESC to quit", True, Colour.WHITE)
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
    window.blit(quit_text, quit_rect)

    pygame.display.flip()