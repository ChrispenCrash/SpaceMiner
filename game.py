import pygame
from enums import GameState, Colour
from player import Player
from asteroid import Asteroid
from settings import WIDTH, HEIGHT, GAME_WIDTH, GAME_HEIGHT, ASTEROID_COUNT, ASTEROID_WIN_COUNT, TIME_LIMIT
from utils import display_main_menu, display_pause_menu, display_end_screen
import random
import sys

class Game:
    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.large_font = pygame.font.SysFont(None, 72)
        self.camera_offset = pygame.Vector2(0, 0)
        self.background = self.create_background()
        self.reset_game()
        self.game_state = GameState.MAIN_MENU

    def create_background(self):
        STAR_DENSITY = 0.0002
        STAR_COUNT = int(GAME_WIDTH * GAME_HEIGHT * STAR_DENSITY)
        stars = [(random.randint(0, GAME_WIDTH), random.randint(0, GAME_HEIGHT)) for _ in range(STAR_COUNT)]
        background = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        background.fill(Colour.DARK_GREY)
        for (x, y) in stars:
            pygame.draw.rect(background, Colour.WHITE, (x, y, 2, 2))
        return background

    def reset_game(self):
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.all_sprites = pygame.sprite.Group()
        self.asteroid_group = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        for _ in range(ASTEROID_COUNT):
            asteroid = Asteroid()
            self.all_sprites.add(asteroid)
            self.asteroid_group.add(asteroid)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.game_state == GameState.MAIN_MENU:
                if event.key == pygame.K_1:
                    self.game_state = GameState.PLAYING
                elif event.key == pygame.K_2:
                    print("Multiplayer mode not implemented yet.")
                elif event.key == pygame.K_3:
                    print("Options menu not implemented yet.")
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()
            elif self.game_state == GameState.PLAYING:
                if event.key == pygame.K_p:
                    self.game_state = GameState.PAUSED
            elif self.game_state == GameState.PAUSED:
                if event.key == pygame.K_p:
                    self.game_state = GameState.PLAYING
                elif event.key == pygame.K_m:
                    self.game_state = GameState.MAIN_MENU
                elif event.key == pygame.K_r:
                    self.reset_game()
                    self.game_state = GameState.PLAYING
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif self.game_state in [GameState.WON, GameState.GAME_OVER]:
                if event.key == pygame.K_r:
                    self.reset_game()
                    self.game_state = GameState.PLAYING
                elif event.key == pygame.K_m:
                    self.game_state = GameState.MAIN_MENU
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def update(self, dt):
        if self.game_state == GameState.PLAYING:
            self.update_playing(dt)
        elif self.game_state == GameState.PAUSED:
            pass
        elif self.game_state in [GameState.WON, GameState.GAME_OVER]:
            pass

    def update_playing(self, dt):
        self.all_sprites.update(self.camera_offset)
        hits = pygame.sprite.spritecollide(self.player, self.asteroid_group, True)
        if hits:
            self.score += len(hits)
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        if self.score >= ASTEROID_WIN_COUNT:
            self.game_state = GameState.WON
        elif elapsed_time >= TIME_LIMIT:
            self.game_state = GameState.GAME_OVER

    def draw(self):
        if self.game_state == GameState.MAIN_MENU:
            display_main_menu(self.window, self.large_font, self.font, self.background, self.camera_offset)
        elif self.game_state == GameState.PLAYING:
            self.draw_playing()
        elif self.game_state == GameState.PAUSED:
            display_pause_menu(self.window, self.large_font, self.font, self.background, self.camera_offset)
        else:
            display_end_screen(self.window, self.large_font, self.font, self.game_state, self.background, self.camera_offset)

    def draw_playing(self):
        self.window.blit(self.background, -self.camera_offset)
        for sprite in self.all_sprites:
            sprite.draw(self.window, self.camera_offset)
        score_text = self.font.render(f"Score: {self.score}", True, Colour.WHITE)
        self.window.blit(score_text, (10, 10))
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        time_remaining = max(0, TIME_LIMIT - elapsed_time)
        minutes = int(time_remaining) // 60
        seconds = int(time_remaining) % 60
        timer_text = self.font.render(f"Time: {minutes}:{seconds:02}", True, Colour.WHITE)
        self.window.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))