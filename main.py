import pygame
import os
import sys
import argparse
from game import Game
from settings import WIDTH, HEIGHT, FPS

# doesn't work
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

def main():
    parser = argparse.ArgumentParser(description="Space Miner Game")
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Miner")
    clock = pygame.time.Clock()

    game = Game(window, debug=args.debug)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        game.update(dt)
        game.draw()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()