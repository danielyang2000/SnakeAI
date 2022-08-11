# SP2022 Data Science Lab Final Project

# SnakeAI 
#### Ammar Fatehi, Lauren Head, Allen Jiang, Johanna McCormack, Eralp Orkun, Daniel Yang

## INTRODUCTION
The video game Snake has been around for decades, giving people plenty of time to hone their skills. As the soceity focuses more and more on artificial intelligence, our teams wonders if any human player can be surpassed by Artifical Intelligence. Many data scientists have experimented with AI video game players, and our main goal is to create an AI model that learns to play Snake better than any human being could. 

We explored this with a method of reinforcement learning, called Deep Q Learning, to train a Neural Network to select optimal moves for Snake. This will require a baseline Snake environment (`Snake.py`), an Agent (`AgentAI.py`), AKA our AI “player”, and an underlying neural net model (`Model.py`) for the training.

## INSTALL
Please install the modules listed in `requirements.txt` with the following command:
```python
pip install -r requirements.txt
```
## RUN
To manually play the snake game:
```python
python snake_game_human.py
```

Using AI to play the snake game (currently doesn't train):
```python
python Snake.py
```
#### please note that c in `config.py` cannot be capitalized on GitHub, so please manually capitalize 'c' after cloning this repo
