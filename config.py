
from enum import Enum

class Player(Enum):
    HUMAN = 1
    AI_TRAIN = 2
    AI_DEMO = 3

MAP_WIDTH = 4
MAP_HEIGHT = 4
BLOCK_SIZE = 20
SCREEN_WIDTH = MAP_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * BLOCK_SIZE

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

# controls speed of the game. Higher number means higher speed
SPEED = 1000

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001