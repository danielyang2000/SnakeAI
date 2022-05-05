
from typing import final

from regex import D
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
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

        # self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = torch.device("cpu")
        self.model.to(self.device)

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

        collision_front = None
        collision_left = None
        collision_right = None

        food_left = None
        food_right = None
        food_forward = None
        food_behind = None

        if self.game.snake.direction.value == Direction.UP.value:
            collision_front = self.game.snake.is_collision_up()
            collision_left = self.game.snake.is_collision_left()
            collision_right = self.game.snake.is_collision_right()

            food_left = self.game.food.x <= self.game.snake.head.x
            food_right = self.game.food.x > self.game.snake.head.x
            food_forward = self.game.food.y <= self.game.snake.head.y
            food_behind = self.game.food.y > self.game.snake.head.y
        elif self.game.snake.direction.value == Direction.DOWN.value:
            collision_front = self.game.snake.is_collision_down()
            collision_left = self.game.snake.is_collision_right()
            collision_right = self.game.snake.is_collision_left()

            food_left = self.game.food.x > self.game.snake.head.x
            food_right = self.game.food.x <= self.game.snake.head.x
            food_forward = self.game.food.y > self.game.snake.head.y
            food_behind = self.game.food.y <= self.game.snake.head.y
        elif self.game.snake.direction.value == Direction.LEFT.value:
            collision_front = self.game.snake.is_collision_left()
            collision_left = self.game.snake.is_collision_down()
            collision_right = self.game.snake.is_collision_up()

            food_left = self.game.food.y > self.game.snake.head.y
            food_right = self.game.food.y <= self.game.snake.head.y
            food_forward = self.game.food.x <= self.game.snake.head.x
            food_behind = self.game.food.x > self.game.snake.head.x
        elif self.game.snake.direction.value == Direction.RIGHT.value:
            collision_front = self.game.snake.is_collision_right()
            collision_left = self.game.snake.is_collision_up()
            collision_right = self.game.snake.is_collision_down()

            food_left = self.game.food.y <= self.game.snake.head.y
            food_right = self.game.food.y > self.game.snake.head.y
            food_forward = self.game.food.x > self.game.snake.head.x
            food_behind = self.game.food.x <= self.game.snake.head.x

        state = [
            collision_front,
            collision_left,
            collision_right,
            self.game.snake.direction.value == Direction.UP.value,
            self.game.snake.direction.value == Direction.DOWN.value,
            self.game.snake.direction.value == Direction.LEFT.value,
            self.game.snake.direction.value == Direction.RIGHT.value,

            # Food location 
            self.game.food.x < self.game.snake.head.x,  # food left
            self.game.food.x > self.game.snake.head.x,  # food right
            self.game.food.y < self.game.snake.head.y,  # food up
            self.game.food.y > self.game.snake.head.y  # food down
        ]
        
        return np.array(state, dtype=int)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        if random.randint(0, 200) < self.epsilon:
            snake_direction = self.game.snake.direction
            move = -1
            while move == -1:
                move = random.randint(0, 3)
                if snake_direction.value == Direction.UP.value and move == Direction.DOWN.value or \
                    snake_direction.value == Direction.DOWN.value and move == Direction.UP.value or \
                    snake_direction.value == Direction.LEFT.value and move == Direction.RIGHT.value or \
                    snake_direction.value == Direction.RIGHT.value and move == Direction.LEFT.value:
                    move = -1

        else:
            state0 = torch.tensor(state, dtype=torch.float, device=self.device)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()

            if self.game.snake.direction.value == Direction.UP.value:
                if move == 0:
                    move = Direction.UP.value
                elif move == 1:
                    move = Direction.LEFT.value
                elif move == 2:
                    move = Direction.RIGHT.value
            elif self.game.snake.direction.value == Direction.DOWN.value:
                if move == 0:
                    move = Direction.DOWN.value
                elif move == 1:
                    move = Direction.RIGHT.value
                elif move == 2:
                    move = Direction.LEFT.value
            elif self.game.snake.direction.value == Direction.LEFT.value:
                if move == 0:
                    move = Direction.LEFT.value
                elif move == 1:
                    move = Direction.DOWN.value
                elif move == 2:
                    move = Direction.UP.value
            elif self.game.snake.direction.value == Direction.RIGHT.value:
                if move == 0:
                    move = Direction.RIGHT.value
                elif move == 1:
                    move = Direction.UP.value
                elif move == 2:
                    move = Direction.DOWN.value

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
