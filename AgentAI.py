
from typing import final
from Snake import Direction
from Utils import plot
import numpy as np
import torch
import random
from collections import deque
from Model import Linear_QNet, QTrainer
from Config import *

class Agent:
    def __init__(self, game):
        self.game = game
        
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(12, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def train(self):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        while True:
            # get old state
            state_old = self.get_state()

            # get move
            final_move = self.get_action(state_old)

            # perform move and get new state
            reward, done, score = self.game.play_step(final_move)
            state_new = self.get_state()

            # train short memory
            self.train_short_memory(state_old, final_move.value, reward, state_new, done)

            # remember
            self.remember(state_old, final_move.value, reward, state_new, done)

            if done:
                # train long memory, plot result
                self.game.reset()
                self.n_games += 1
                self.train_long_memory()

                if score > record:
                    record = score
                    self.model.save()

                print('Game', self.n_games, 'Score', score, 'Record:', record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / self.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)

    def play(self):
        while True:
            movement_input = Direction.RIGHT
            game_over, score = self.game.play_step(movement_input)

    def get_state(self):
        # 1. collision up
        # 2. collision down
        # 3. collision left
        # 4. collision right
        # 5. movement up
        # 6. movement down
        # 7. movement left
        # 8. movement right
        # 9. food left
        # 10. food right
        # 11. food up
        # 12. food down
        # in future, can add map data or snake travel history

        state = [
            self.game.snake.is_collision_up(),
            self.game.snake.is_collision_down(),
            self.game.snake.is_collision_left(),
            self.game.snake.is_collision_right(),
            self.game.snake.direction.value == Direction.UP.value,
            self.game.snake.direction.value == Direction.DOWN.value,
            self.game.snake.direction.value == Direction.LEFT.value,
            self.game.snake.direction.value == Direction.RIGHT.value,
            self.game.food.x < self.game.snake.head.x,
            self.game.food.x > self.game.snake.head.x,
            self.game.food.y < self.game.snake.head.y,
            self.game.food.y > self.game.snake.head.y
        ]
        
        return np.array(state, dtype=int)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        if random.randint(0, 100) < self.epsilon:
            move = random.randint(0, 3)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()

        final_move = None
        if move == 0:
            final_move = Direction.UP
        elif move == 1:
            final_move = Direction.DOWN
        elif move == 2:
            final_move = Direction.LEFT
        elif move == 3:
            final_move = Direction.RIGHT

        return final_move

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached
