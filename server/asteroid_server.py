import random
from server_settings import GAME_WIDTH, GAME_HEIGHT

class Asteroid:
    def __init__(self):
        self.pos = (random.randint(10, GAME_WIDTH - 10), random.randint(10, GAME_HEIGHT - 10))
        self.angle = random.choice([0, 90, 180, 270])

    def serialize(self):
        return {'pos': self.pos, 'angle': self.angle}

    @staticmethod
    def deserialize(data):
        asteroid = Asteroid()
        asteroid.pos = data['pos']
        asteroid.angle = data['angle']
        return asteroid