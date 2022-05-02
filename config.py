
from enum import Enum

class Player(Enum):
    HUMAN = 1
    AI_TRAIN = 2
    AI_DEMO = 3

# GAME_MODE = Player.HUMAN
GAME_MODE = Player.AI_TRAIN
# GAME_MODE = Player.AI_DEMO

DISPLAY_GUI = GAME_MODE == Player.HUMAN or GAME_MODE == Player.AI_DEMO or GAME_MODE == Player.AI_TRAIN

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# rgb colors
WHITE = (255, 255, 255)
RED1 = (255,0,0)
RED2 = (255,100, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
YELLOW1 = (255, 255, 0)
YELLOW2 = (255, 255, 126)
GREEN1 = (0, 255, 0)
GREEN2 = (0, 255, 126)
BLACK = (0,0,0)

COLORS = [(BLUE1, BLUE2), (YELLOW1, YELLOW2), (GREEN1, GREEN2)]

BLOCK_SIZE = 20

# controls speed of the game. Higher number means higher speed
SPEED = 9999

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001