
from enum import Enum

class Player(Enum):
    HUMAN = 1
    AI_TRAIN = 2
    AI_DEMO = 3

GAME_MODE = Player.HUMAN

DISPLAY_GUI = GAME_MODE == Player.HUMAN or GAME_MODE == Player.AI_DEMO

