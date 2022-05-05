from random import random
from Model import Linear_QNet, QTrainer
import torch

LR = 0.001
gamma = 0.9 # discount rate

model = Linear_QNet(12, 256, 4)
trainer = QTrainer(model, lr=LR, gamma=gamma)

def train_short_memory(state, action, reward, next_state, done):
    trainer.train_step(state, action, reward, next_state, done)

# state_old_1 = [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0]
# state_new_1 = [1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0]
# state_old_1 = torch.tensor(state_old_1, dtype=torch.float)
# state_new_1 = torch.tensor(state_new_1, dtype=torch.float)

state_old_2 = [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0]
state_old_2 = torch.tensor(state_old_2, dtype=torch.float)

state_new_2_u = [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0]
state_new_2_d = [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0]
state_new_2_l = [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0]
state_new_2_r = [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0]

reward_1 = 0
reward_2 = -10

for i in range(0, 100):
    prediction = model(state_old_2)
    move = torch.argmax(prediction).item()
    print(prediction)
    print(move)

    out_state = None

    if move == 0:
        out_state = state_new_2_u
        reward_2 = 0
    elif move == 1:
        out_state = state_new_2_d
        reward_2 = 0
    elif move == 2:
        out_state = state_new_2_l
        reward_2 = -10
    elif move == 3:
        out_state = state_new_2_r
        reward_2 = -10

    # 50% of time choose random move
    if random() > 0.5:
        move = int(random() * 4)

    state_new_2 = torch.tensor(out_state, dtype=torch.float)
    train_short_memory(state_old_2, 3, reward_2, state_new_2, False)