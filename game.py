import pygame
from enums import GameState, Colour
from player import Player
from asteroid import Asteroid
from settings import WIDTH, HEIGHT, GAME_WIDTH, GAME_HEIGHT, ASTEROID_COUNT, ASTEROID_WIN_COUNT, TIME_LIMIT
from utils import display_main_menu, display_pause_menu, display_end_screen
from network import Network
import random
import sys

class Game:
    def __init__(self, window, debug=False):
        self.window = window
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.large_font = pygame.font.SysFont(None, 72)
        self.camera_offset = pygame.Vector2(0, 0)
        self.background = self.create_background()
        self.game_state = GameState.MAIN_MENU
        self.network = None
        self.player_id = None
        self.debug = debug
        self.reset_game()

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
            # if self.debug:
                # print(f"Created asteroid at position {asteroid.pos}")
            self.all_sprites.add(asteroid)
            self.asteroid_group.add(asteroid)
        if self.debug:
            print(f"Game reset. Created {ASTEROID_COUNT} new asteroids")
        # print(self.all_sprites)
        # print(self.asteroid_group)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.game_state == GameState.MAIN_MENU:
                if event.key == pygame.K_1:
                    self.reset_game()  # Reset the game when starting a new game
                    self.game_state = GameState.PLAYING
                elif event.key == pygame.K_2:
                    self.start_multiplayer()
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

    def start_multiplayer(self):
        try:
            self.network = Network()
            self.player_id = self.network.receive()
            if self.debug:
                print(f"Player ID: {self.player_id}")
            initial_game_state = self.network.receive()
            if self.debug:
                print(f"Initial game state: {initial_game_state}")
            self.update_multiplayer(initial_game_state)
            self.game_state = GameState.PLAYING
        except Exception as e:
            print(f"Unable to connect to server: {e}")
            self.game_state = GameState.MAIN_MENU

    def update(self, dt):
        if self.game_state == GameState.PLAYING:
            self.update_playing(dt)
        elif self.game_state == GameState.PAUSED:
            pass
        elif self.game_state in [GameState.WON, GameState.GAME_OVER]:
            pass

    def update_playing(self, dt):
        if self.network:
            self.network.send({'type': 'move', 'pos': self.player.pos})
            game_state = self.network.receive()
            self.update_multiplayer(game_state)
        else:
            self.all_sprites.update(self.camera_offset)
            hits = pygame.sprite.spritecollide(self.player, self.asteroid_group, True)
            if hits:
                self.score += len(hits)
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            if self.score >= ASTEROID_WIN_COUNT:
                self.game_state = GameState.WON
            elif elapsed_time >= TIME_LIMIT:
                self.game_state = GameState.GAME_OVER

    def update_multiplayer(self, game_state):
        if self.debug:
            print("Updating multiplayer game state")
            print(f"Received game state: {game_state}")
        self.all_sprites.empty()
        self.asteroid_group.empty()
        for player_id, player_data in game_state['players'].items():
            if self.debug:
                print(f"Adding player {player_id} at position {player_data['pos']}")
            player = Player.deserialize(player_data)
            self.all_sprites.add(player)
            if player_id == self.player_id:
                self.player = player
        for asteroid_data in game_state['asteroids']:
            if self.debug:
                print(f"Adding asteroid at position {asteroid_data['pos']} with angle {asteroid_data['angle']}")
            asteroid = Asteroid.deserialize(asteroid_data)
            self.asteroid_group.add(asteroid)
            self.all_sprites.add(asteroid)

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