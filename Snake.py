
import pygame
import random
from enum import Enum
from collections import namedtuple

from regex import B
import Config
from Config import *

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    QUIT = 5
    
Point = namedtuple('Point', 'x, y')

class Food:
    def __init__(self, screen, screen_w, screen_h):
        # initialize food to a random position on the screen
        self.x = random.randint(0, (screen_w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.y = random.randint(0, (screen_h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE

        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.point = Point(self.x, self.y)
        
        if screen != None:
            self.image = pygame.image.load("image/Cookie.jpg").convert()

    def draw(self):
        if (self.screen == None):
            return

        self.screen.blit(self.image, (self.x, self.y))
        
    # move food to another position
    def move(self):
        self.x = random.randint(0, (self.screen_w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        self.y = random.randint(0, (self.screen_h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.point = Point(self.x, self.y)

class Snake:
    def __init__(self, screen, screen_w, screen_h):
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.direction = Direction.RIGHT

        if (self.screen == None):
            self.head = Point(320, 240)
        else:
            self.head = Point(self.screen_w/2, self.screen_h/2)

        self.body = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.color_index = 0
        self.color = COLORS[self.color_index]

    # move snake head if key pressed
    def move(self):
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)

        # we move snake head by adding a block in front of original head.
        self.body.insert(0, self.head)

    # draw each block of snake's body
    def draw(self):
        if (self.screen == None): 
            return
        for i, pt in enumerate(self.body):
            # snake head is always red
            if i == 0:
                pygame.draw.rect(self.screen, RED1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.screen, RED2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            # snake body's color    
            else:    
                pygame.draw.rect(self.screen, self.color[0], pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.screen, self.color[1], pygame.Rect(pt.x+4, pt.y+4, 12, 12))

    def is_out_of_bounds(self):
        return self.head.x > self.screen_w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.screen_h - BLOCK_SIZE or self.head.y < 0

    # snake collide with itself or boundary?
    def is_collision(self):
        # hits boundary
        if self.is_out_of_bounds():
            return True

        # hits itself
        if self.head in self.body[1:]:
            return True
        
        return False

    def is_collision_up(self):
        if self.is_out_of_bounds() or self.head.y < BLOCK_SIZE:
            return True
        # check if body above
        up_point = Point(self.head.x, self.head.y - BLOCK_SIZE)
        if up_point in self.body:
            return True

        return False

    def is_collision_down(self):
        if self.is_out_of_bounds() or self.head.y >= self.screen_h - BLOCK_SIZE:
            return True
        
        # check if body below
        down_point = Point(self.head.x, self.head.y + BLOCK_SIZE)
        if down_point in self.body:
            return True

        return False
    
    def is_collision_left(self):
        if self.is_out_of_bounds() or self.head.x < BLOCK_SIZE:
            return True
        
        # check if body left
        left_point = Point(self.head.x - BLOCK_SIZE, self.head.y)
        if left_point in self.body:
            return True

        return False
    
    def is_collision_right(self):
        if self.is_out_of_bounds() or self.head.x >= self.screen_w - BLOCK_SIZE:
            return True
        
        # check if body right
        right_point = Point(self.head.x + BLOCK_SIZE, self.head.y)
        if right_point in self.body:
            return True

        return False

    def change_color(self):
        if (self.color_index == 2):
            self.color_index = 0
        else:
            self.color_index += 1
        self.color = COLORS[self.color_index]

class SnakeGame:
    
    def __init__(self, w=Config.SCREEN_WIDTH, h=Config.SCREEN_HEIGHT, gui=True):
        self.gui = gui
        self.display = None
        if (self.gui):
            self.w = w
            self.h = h
            # init display
            self.display = pygame.display.set_mode((self.w, self.h))
            pygame.display.set_caption('Snake')
            
        self.clock = pygame.time.Clock()
        
        self.snake = Snake(self.display, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)

        self.score = 0

        self.food = Food(self.display, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        self.food.draw()

    def reset(self):
        self.snake = Snake(self.display, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        self.food = Food(self.display, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        self.food.draw()
        self.score = 0

    # game cycle    
    def play_step(self, movement_direction):
        # 1. collect user input and move
        if movement_direction.value == Direction.RIGHT.value and self.snake.direction.value != Direction.LEFT.value:
            self.snake.direction = Direction.RIGHT
        elif movement_direction.value == Direction.LEFT.value and self.snake.direction.value != Direction.RIGHT.value:
            self.snake.direction = Direction.LEFT
        elif movement_direction.value == Direction.UP.value and self.snake.direction.value != Direction.DOWN.value:
            self.snake.direction = Direction.UP
        elif movement_direction.value == Direction.DOWN.value and self.snake.direction.value != Direction.UP.value:
            self.snake.direction = Direction.DOWN

        if (movement_direction == Direction.QUIT):
            pygame.quit()
            exit()

        self.snake.move()

        # 2. check if game over (snake hit boundary or itself?)
        reward = 0
        game_over = False
        if self.snake.is_collision():
            game_over = True
            reward -= 10
            return reward, game_over, self.score
            
        # 3. Check if snake head is on the food
        ate_food = self.food_collision()
        if ate_food:
            reward += 10
        
        # 4. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        
        # 6. return game over and score
        return reward, game_over, self.score

    # check for collision with food
    def food_collision(self):
        pop = True
        # uses for loop because sometimes food spawns on snake body
        for block in self.snake.body:
            if block == self.food.point:
                self.score += 1
                self.food.move()

                # change snake body color (except head) after eating food
                self.snake.change_color()
                pop = False
                break
                
        # pop snake tail if snake didn't eat food in this cycle. 
        if pop:
            self.snake.body.pop()

        return not pop

    # update background image
    def update_background(self):
        if (self.display == None):
            return

        # self.display.blit(pygame.image.load('image/troll1.jpg'), (0,0))
        # make black background
        self.display.fill(BLACK)

    # call each sprite's draw method
    # comment self.update_background and uncomment self.display.fill(black) for black background
    def _update_ui(self):
        if (self.display == None):
            return

        self.update_background()
        
        self.snake.draw()

        self.food.draw()
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

def wait_for_key():
    while True:
        event = pygame.event.poll()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYUP:
                return
            else:
                continue

def get_arrow_keys_direction(game):
    current_direction = game.snake.direction
    event = pygame.event.poll()

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT and current_direction != Direction.RIGHT:
            return Direction.LEFT
        elif event.key == pygame.K_RIGHT and current_direction != Direction.LEFT:
            return Direction.RIGHT
        elif event.key == pygame.K_UP and current_direction != Direction.DOWN:
            return Direction.UP
        elif event.key == pygame.K_DOWN and current_direction != Direction.UP:
            return Direction.DOWN

    if event.type == pygame.QUIT:
        return Direction.QUIT
    
    return current_direction

if __name__ == '__main__':
    from AgentAI import Agent

    game = SnakeGame(gui=Config.DISPLAY_GUI, w=Config.SCREEN_WIDTH, h=Config.SCREEN_HEIGHT)
    agent = Agent(game)

    if Config.GAME_MODE == Player.HUMAN:
        wait_for_key()
    
        # game loop
        while True:
            movement_input = get_arrow_keys_direction(game)
            _, game_over, score = game.play_step(movement_input)
            
            if game_over == True:
                break
            
        print('Final Score', score)

        wait_for_key()
    elif Config.GAME_MODE == Player.AI_TRAIN:
        # train ai
        agent.train()
        pass
    elif Config.GAME_MODE == Player.AI_DEMO:
        # demo ai
        agent.demo()
        pass
        
    pygame.quit()