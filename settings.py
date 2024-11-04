WIDTH, HEIGHT = 600, 600
GAME_SIZE_MULTIPLIER = 4
FPS = 60
PLAYER_SPEED = 5
PLAYER_ROTATE_SPEED = 5
ASTEROID_DENSITY = 0.00001
ASTEROID_WIN_COUNT = 20
TIME_LIMIT = 30  # in seconds

# Game space dimensions
GAME_WIDTH, GAME_HEIGHT = WIDTH * GAME_SIZE_MULTIPLIER, HEIGHT * GAME_SIZE_MULTIPLIER
ASTEROID_COUNT = int(GAME_WIDTH * GAME_HEIGHT * ASTEROID_DENSITY)
