import pygame
import sys
from game import Game
from settings import WIDTH, HEIGHT, FPS

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Miner")
    clock = pygame.time.Clock()

    game = Game(window)

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