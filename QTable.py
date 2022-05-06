import numpy as np

from Config import *

class QTable():
    def __init__(self, state_size, actions):
        self.tableShape = (pow(2, state_size), actions)
        self.table = np.zeros(self.tableShape)

    def updateTable(self, state, action, Q_new):
        index = self._getIndex(state, action)
        self.table[index] = Q_new

    def getQVal(self, state, action):
        index = self._getIndex(state, action)
        return self.table[index]

    def _getIndex(self, state, action):
        state_index = 0
        power = 1
        for idx in range(11):
            state_index += power * state[10-idx]
            power = power * 2

        if np.array_equal(action, [1, 0, 0]): # straight
            action_index = 0
        elif np.array_equal(action, [0, 1, 0]): # right turn
            action_index = 1
        else: # left turn
            action_index = 2

        index = (state_index, action_index)
        return index

class QTrainer:
    def __init__(self, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.table = QTable(11,3)   # hard coded for our snake model

    def train_step(self, state, action, reward, next_state, done):
        Q_old = self.table.getQVal(state,action)
        if done:
            Q_new = Q_old + self.lr * (reward - Q_old)
        else:
            possibleActions = [[1,0,0], [0,1,0], [0,0,1]]
            possibleQs = [0,0,0]
            for choice in range(3):
                possibleQs[choice] = (self.table.getQVal(next_state, possibleActions[choice]))
            Q_new = Q_old + self.lr * (reward + self.gamma * max(possibleQs) - Q_old)
            self.table.updateTable(state, action, Q_new)

    def get_action(self, state):
        possibleActions = [[1,0,0], [0,1,0], [0,0,1]]
        possibleQs = [0,0,0]
        for choice in range(3):
            possibleQs[choice] = (self.table.getQVal(state, possibleActions[choice]))
        action = possibleActions[np.argmax(possibleQs)]
        return action