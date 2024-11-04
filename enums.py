from enum import Enum

class GameState(Enum):
    PLAYING = 1
    WON = 2
    GAME_OVER = 3

class Colour(tuple, Enum):
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    ORANGE = (255, 165, 0)
    GREY = (128, 128, 128)
    DARK_GREY = (15, 15, 15)