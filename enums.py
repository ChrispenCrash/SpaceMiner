from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    WON = auto()
    GAME_OVER = auto()
    PAUSED = auto()

class GameScreen(Enum):
    SPLASH = auto()
    MAIN_MENU = auto()
    SINGLE_PLAYER = auto()
    MULTI_PLAYER = auto()
    SETTINGS = auto()

class Colour(tuple, Enum):
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    ORANGE = (255, 165, 0)
    GREY = (128, 128, 128)
    DARK_GREY = (15, 15, 15)