
from Snake import Direction


class Agent:
    def __init__(self, game):
        self.game = game

    def train(self):
        while True:
            movement_input = Direction.RIGHT
            game_over, score = self.game.play_step(movement_input)

    def play(self):
        while True:
            movement_input = Direction.RIGHT
            game_over, score = self.game.play_step(movement_input)