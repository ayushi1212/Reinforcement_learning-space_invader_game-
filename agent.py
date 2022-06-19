import torch
import random
from collections import deque
from space_game_AI import SpaceGame, Direction, Point
import numpy as np
from model import Space_Net, Trainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_game=0
        self.epsilon=0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY) #popleft(),if limit exceeds maxlen
        self.model=Space_Net(23,256,3,2)
        self.trainer= Trainer(self.model,lr=LR, gamma=self.gamma)

    def get_state(self,game):
       player = game.player
       player_l = game.player
       player_r = Point(player.x + 65, player.y)
       player_u = Point(player.x, player.y-65)
       player_d = Point(player.x, player.y+65)
       player_c = Point(player.x+30,player.y-30)

       arrow = game.arrow
       arrow_l = game.arrow
       arrow_r = Point(arrow.x + 30, arrow.y)
       arrow_u = Point(arrow.x, arrow.y-30)
       arrow_d = Point(arrow.x, arrow.y+30)
       arrow_c = Point(arrow.x+15,arrow.y-15)

       enemy1 = game.enemy1
       enemy1_l = game.enemy1
       enemy1_r = Point(enemy1.x + 30, enemy1.y)
       enemy1_u = Point(enemy1.x, enemy1.y-30)
       enemy1_d = Point(enemy1.x, enemy1.y+30)
       enemy1_c = Point(enemy1.x+15,enemy1.y-15)

       enemy2 = game.enemy2
       enemy2_l = game.enemy2
       enemy2_r = Point(enemy2.x + 30, enemy2.y)
       enemy2_u = Point(enemy2.x, enemy2.y-30)
       enemy2_d = Point(enemy2.x, enemy2.y+30)
       enemy2_c = Point(enemy2.x+15,enemy2.y-15)

       enemy3 = game.enemy3
       enemy3_l = game.enemy3
       enemy3_r = Point(enemy3.x + 30, enemy3.y)
       enemy3_u = Point(enemy3.x, enemy3.y-30)
       enemy3_d = Point(enemy3.x, enemy3.y+30)
       enemy3_c = Point(enemy3.x+15,enemy3.y-15)

       enemy4 = game.enemy4
       enemy4_l = game.enemy4
       enemy4_r = Point(enemy4.x + 30, enemy4.y)
       enemy4_u = Point(enemy4.x, enemy4.y-30)
       enemy4_d = Point(enemy4.x, enemy4.y+30)
       enemy4_c = Point(enemy4.x+15,enemy4.y-15)

       enemy5 = game.enemy5
       enemy5_l = game.enemy5
       enemy5_r = Point(enemy5.x + 30, enemy5.y)
       enemy5_u = Point(enemy5.x, enemy5.y-30)
       enemy5_d = Point(enemy5.x, enemy5.y+30)
       enemy5_c = Point(enemy5.x+15,enemy5.y-15)

       enemy6 = game.enemy6
       enemy6_l = game.enemy6
       enemy6_r = Point(enemy6.x + 30, enemy6.y)
       enemy6_u = Point(enemy6.x, enemy6.y-30)
       enemy6_d = Point(enemy6.x, enemy6.y+30)
       enemy6_c = Point(enemy6.x+15,enemy6.y-15)

       dir_l = game.direction == Direction.LEFT
       dir_r = game.direction == Direction.RIGHT
       dir_n = game.direction == Direction.NOTHING

       action_shoot = True
       action_dont_shoot = False

       state = [

           #direction danger
           ##enemy1
           (dir_n and player.y-enemy1.y<20) or
           (dir_n and player_c.y - enemy1.y < 20) or
           (dir_n and player_l.y - enemy1.y < 20) or
           (dir_n and player_r.y - enemy1.y < 20) or
           (dir_n and player_u.y - enemy1.y < 20) or
           (dir_n and player_d.y - enemy1.y < 20) or
           (dir_n and player.y - enemy1_l.y < 20) or
           (dir_n and player.y - enemy1_u.y < 20) or
           (dir_n and player.y - enemy1_r.y < 20) or
           (dir_n and player.y - enemy1_c.y < 20) or
           (dir_n and player.y - enemy1_d.y < 20) or
           (dir_l and player.y - enemy1.y < 20) or
           (dir_l and player_c.y - enemy1.y < 20) or
           (dir_l and player_l.y - enemy1.y < 20) or
           (dir_l and player_r.y - enemy1.y < 20) or
           (dir_l and player_u.y - enemy1.y < 20) or
           (dir_l and player_d.y - enemy1.y < 20) or
           (dir_l and player.y - enemy1_l.y < 20) or
           (dir_l and player.y - enemy1_u.y < 20) or
           (dir_l and player.y - enemy1_r.y < 20) or
           (dir_l and player.y - enemy1_c.y < 20) or
           (dir_l and player.y - enemy1_d.y < 20) or
           (dir_r and player.y - enemy1.y < 20) or
           (dir_r and player_c.y - enemy1.y < 20) or
           (dir_r and player_l.y - enemy1.y < 20) or
           (dir_r and player_r.y - enemy1.y < 20) or
           (dir_r and player_u.y - enemy1.y < 20) or
           (dir_r and player_d.y - enemy1.y < 20) or
           (dir_r and player.y - enemy1_l.y < 20) or
           (dir_r and player.y - enemy1_u.y < 20) or
           (dir_r and player.y - enemy1_r.y < 20) or
           (dir_r and player.y - enemy1_c.y < 20) or
           (dir_r and player.y - enemy1_d.y < 20),


           # danger from
           # enemy2
           (dir_n and player.y - enemy2.y < 20) or
           (dir_n and player_c.y - enemy2.y < 20) or
           (dir_n and player_l.y - enemy2.y < 20) or
           (dir_n and player_r.y - enemy2.y < 20) or
           (dir_n and player_u.y - enemy2.y < 20) or
           (dir_n and player_d.y - enemy2.y < 20) or
           (dir_n and player.y - enemy2_l.y < 20) or
           (dir_n and player.y - enemy2_u.y < 20) or
           (dir_n and player.y - enemy2_r.y < 20) or
           (dir_n and player.y - enemy2_c.y < 20) or
           (dir_n and player.y - enemy2_d.y < 20) or
           (dir_l and player.y - enemy2.y < 20) or
           (dir_l and player_c.y - enemy2.y < 20) or
           (dir_l and player_l.y - enemy2.y < 20) or
           (dir_l and player_r.y - enemy2.y < 20) or
           (dir_l and player_u.y - enemy2.y < 20) or
           (dir_l and player_d.y - enemy2.y < 20) or
           (dir_l and player.y - enemy2_l.y < 20) or
           (dir_l and player.y - enemy2_u.y < 20) or
           (dir_l and player.y - enemy2_r.y < 20) or
           (dir_l and player.y - enemy2_c.y < 20) or
           (dir_l and player.y - enemy2_d.y < 20) or
           (dir_r and player.y - enemy2.y < 20) or
           (dir_r and player_c.y - enemy2.y < 20) or
           (dir_r and player_l.y - enemy2.y < 20) or
           (dir_r and player_r.y - enemy2.y < 20) or
           (dir_r and player_u.y - enemy2.y < 20) or
           (dir_r and player_d.y - enemy2.y < 20) or
           (dir_r and player.y - enemy2_l.y < 20) or
           (dir_r and player.y - enemy2_u.y < 20) or
           (dir_r and player.y - enemy2_r.y < 20) or
           (dir_r and player.y - enemy2_c.y < 20) or
           (dir_r and player.y - enemy2_d.y < 20),


           # danger from enemy3
           (dir_n and player.y - enemy3.y < 20) or
           (dir_n and player_c.y - enemy3.y < 20) or
           (dir_n and player_l.y - enemy3.y < 20) or
           (dir_n and player_r.y - enemy3.y < 20) or
           (dir_n and player_u.y - enemy3.y < 20) or
           (dir_n and player_d.y - enemy3.y < 20) or
           (dir_n and player.y - enemy3_l.y < 20) or
           (dir_n and player.y - enemy3_u.y < 20) or
           (dir_n and player.y - enemy3_r.y < 20) or
           (dir_n and player.y - enemy3_c.y < 20) or
           (dir_n and player.y - enemy3_d.y < 20) or
           (dir_l and player.y - enemy3 .y < 20) or
           (dir_l and player_c.y - enemy3.y < 20) or
           (dir_l and player_l.y - enemy3.y < 20) or
           (dir_l and player_r.y - enemy3.y < 20) or
           (dir_l and player_u.y - enemy3.y < 20) or
           (dir_l and player_d.y - enemy3.y < 20) or
           (dir_l and player.y - enemy3_l.y < 20) or
           (dir_l and player.y - enemy3_u.y < 20) or
           (dir_l and player.y - enemy3_r.y < 20) or
           (dir_l and player.y - enemy3_c.y < 20) or
           (dir_l and player.y - enemy3_d.y < 20) or
           (dir_r and player.y - enemy3.y < 20) or
           (dir_r and player_c.y - enemy3.y < 20) or
           (dir_r and player_l.y - enemy3.y < 20) or
           (dir_r and player_r.y - enemy3.y < 20) or
           (dir_r and player_u.y - enemy3.y < 20) or
           (dir_r and player_d.y - enemy3.y < 20) or
           (dir_r and player.y - enemy3_l.y < 20) or
           (dir_r and player.y - enemy3_u.y < 20) or
           (dir_r and player.y - enemy3_r.y < 20) or
           (dir_r and player.y - enemy3_c.y < 20) or
           (dir_r and player.y - enemy3_d.y < 20),


           # danger from enemy4
           (dir_n and player.y - enemy4.y < 20) or
           (dir_n and player_c.y - enemy4.y < 20) or
           (dir_n and player_l.y - enemy4.y < 20) or
           (dir_n and player_r.y - enemy4.y < 20) or
           (dir_n and player_u.y - enemy4.y < 20) or
           (dir_n and player_d.y - enemy4.y < 20) or
           (dir_n and player.y - enemy4_l.y < 20) or
           (dir_n and player.y - enemy4_u.y < 20) or
           (dir_n and player.y - enemy4_r.y < 20) or
           (dir_n and player.y - enemy4_c.y < 20) or
           (dir_n and player.y - enemy4_d.y < 20) or
           (dir_l and player.y - enemy4.y < 20) or
           (dir_l and player_c.y - enemy4.y < 20) or
           (dir_l and player_l.y - enemy4.y < 20) or
           (dir_l and player_r.y - enemy4.y < 20) or
           (dir_l and player_u.y - enemy4.y < 20) or
           (dir_l and player_d.y - enemy4.y < 20) or
           (dir_l and player.y - enemy4_l.y < 20) or
           (dir_l and player.y - enemy4_u.y < 20) or
           (dir_l and player.y - enemy4_r.y < 20) or
           (dir_l and player.y - enemy4_c.y < 20) or
           (dir_l and player.y - enemy4_d.y < 20) or
           (dir_r and player.y - enemy4.y < 20) or
           (dir_r and player_c.y - enemy4.y < 20) or
           (dir_r and player_l.y - enemy4.y < 20) or
           (dir_r and player_r.y - enemy4.y < 20) or
           (dir_r and player_u.y - enemy4.y < 20) or
           (dir_r and player_d.y - enemy4.y < 20) or
           (dir_r and player.y - enemy4_l.y < 20) or
           (dir_r and player.y - enemy4_u.y < 20) or
           (dir_r and player.y - enemy4_r.y < 20) or
           (dir_r and player.y - enemy4_c.y < 20) or
           (dir_r and player.y - enemy4_d.y < 20),


           # danger from enemy5
           (dir_n and player.y - enemy5.y < 20) or
           (dir_n and player_c.y - enemy5.y < 20) or
           (dir_n and player_l.y - enemy5.y < 20) or
           (dir_n and player_r.y - enemy5.y < 20) or
           (dir_n and player_u.y - enemy5.y < 20) or
           (dir_n and player_d.y - enemy5.y < 20) or
           (dir_n and player.y - enemy5_l.y < 20) or
           (dir_n and player.y - enemy5_u.y < 20) or
           (dir_n and player.y - enemy5_r.y < 20) or
           (dir_n and player.y - enemy5_c.y < 20) or
           (dir_n and player.y - enemy5_d.y < 20) or
           (dir_l and player.y - enemy5.y < 20) or
           (dir_l and player_c.y - enemy5.y < 20) or
           (dir_l and player_l.y - enemy5.y < 20) or
           (dir_l and player_r.y - enemy5.y < 20) or
           (dir_l and player_u.y - enemy5.y < 20) or
           (dir_l and player_d.y - enemy5.y < 20) or
           (dir_l and player.y - enemy5_l.y < 20) or
           (dir_l and player.y - enemy5_u.y < 20) or
           (dir_l and player.y - enemy5_r.y < 20) or
           (dir_l and player.y - enemy5_c.y < 20) or
           (dir_l and player.y - enemy5_d.y < 20) or
           (dir_r and player.y - enemy5.y < 20) or
           (dir_r and player_c.y - enemy5.y < 20) or
           (dir_r and player_l.y - enemy5.y < 20) or
           (dir_r and player_r.y - enemy5.y < 20) or
           (dir_r and player_u.y - enemy5.y < 20) or
           (dir_r and player_d.y - enemy5.y < 20) or
           (dir_r and player.y - enemy5_l.y < 20) or
           (dir_r and player.y - enemy5_u.y < 20) or
           (dir_r and player.y - enemy5_r.y < 20) or
           (dir_r and player.y - enemy5_c.y < 20) or
           (dir_r and player.y - enemy5_d.y < 20),


           # danger from enemy6
           (dir_n and player.y - enemy6.y < 20) or
           (dir_n and player_c.y - enemy6.y < 20) or
           (dir_n and player_l.y - enemy6.y < 20) or
           (dir_n and player_r.y - enemy6.y < 20) or
           (dir_n and player_u.y - enemy6.y < 20) or
           (dir_n and player_d.y - enemy6.y < 20) or
           (dir_n and player.y - enemy6_l.y < 20) or
           (dir_n and player.y - enemy6_u.y < 20) or
           (dir_n and player.y - enemy6_r.y < 20) or
           (dir_n and player.y - enemy6_c.y < 20) or
           (dir_n and player.y - enemy6_d.y < 20) or
           (dir_l and player.y - enemy6.y < 20) or
           (dir_l and player_c.y - enemy6.y < 20) or
           (dir_l and player_l.y - enemy6.y < 20) or
           (dir_l and player_r.y - enemy6.y < 20) or
           (dir_l and player_u.y - enemy6.y < 20) or
           (dir_l and player_d.y - enemy6.y < 20) or
           (dir_l and player.y - enemy6_l.y < 20) or
           (dir_l and player.y - enemy6_u.y < 20) or
           (dir_l and player.y - enemy6_r.y < 20) or
           (dir_l and player.y - enemy6_c.y < 20) or
           (dir_l and player.y - enemy6_d.y < 20) or
           (dir_r and player.y - enemy6.y < 20) or
           (dir_r and player_c.y - enemy6.y < 20) or
           (dir_r and player_l.y - enemy6.y < 20) or
           (dir_r and player_r.y - enemy6.y < 20) or
           (dir_r and player_u.y - enemy6.y < 20) or
           (dir_r and player_d.y - enemy6.y < 20) or
           (dir_r and player.y - enemy6_l.y < 20) or
           (dir_r and player.y - enemy6_u.y < 20) or
           (dir_r and player.y - enemy6_r.y < 20) or
           (dir_r and player.y - enemy6_c.y < 20) or
           (dir_r and player.y - enemy6_d.y < 20),

           ##danger action from enemy

           #enemy1
           (action_shoot and player.y - enemy1.y < 20) or
           (action_shoot and player_l.y - enemy1.y < 20) or
           (action_shoot and player_u.y - enemy1.y < 20) or
           (action_shoot and player_c.y - enemy1.y < 20) or
           (action_shoot and player_r.y - enemy1.y < 20) or
           (action_shoot and player_d.y - enemy1.y < 20) or
           (action_shoot and player.y - enemy1_l.y < 20) or
           (action_shoot and player.y - enemy1_u.y < 20) or
           (action_shoot and player.y - enemy1_r.y < 20) or
           (action_shoot and player.y - enemy1_c.y < 20) or
           (action_shoot and player.y - enemy1_d.y < 20) or
           (action_dont_shoot and player.y - enemy1.y < 20) or
           (action_dont_shoot and player.y - enemy1.y < 20) or
           (action_dont_shoot and player_l.y - enemy1.y < 20) or
           (action_dont_shoot and player_u.y - enemy1.y < 20) or
           (action_dont_shoot and player_c.y - enemy1.y < 20) or
           (action_dont_shoot and player_r.y - enemy1.y < 20) or
           (action_dont_shoot and player_d.y - enemy1.y < 20) or
           (action_dont_shoot and player.y - enemy1_l.y < 20) or
           (action_dont_shoot and player.y - enemy1_u.y < 20) or
           (action_dont_shoot and player.y - enemy1_r.y < 20) or
           (action_dont_shoot and player.y - enemy1_c.y < 20) or
           (action_dont_shoot and player.y - enemy1_d.y < 20),

           #enemy2
           (action_shoot and player.y - enemy2.y < 20) or
           (action_shoot and player_l.y - enemy2.y < 20) or
           (action_shoot and player_u.y - enemy2.y < 20) or
           (action_shoot and player_c.y - enemy2.y < 20) or
           (action_shoot and player_r.y - enemy2.y < 20) or
           (action_shoot and player_d.y - enemy2.y < 20) or
           (action_shoot and player.y - enemy2_l.y < 20) or
           (action_shoot and player.y - enemy2_u.y < 20) or
           (action_shoot and player.y - enemy2_r.y < 20) or
           (action_shoot and player.y - enemy2_c.y < 20) or
           (action_shoot and player.y - enemy2_d.y < 20) or
           (action_dont_shoot and player.y - enemy2.y < 20) or
           (action_dont_shoot and player_l.y - enemy2.y < 20) or
           (action_dont_shoot and player_u.y - enemy2.y < 20) or
           (action_dont_shoot and player_c.y - enemy2.y < 20) or
           (action_dont_shoot and player_r.y - enemy2.y < 20) or
           (action_dont_shoot and player_d.y - enemy2.y < 20) or
           (action_dont_shoot and player.y - enemy2_l.y < 20) or
           (action_dont_shoot and player.y - enemy2_u.y < 20) or
           (action_dont_shoot and player.y - enemy2_r.y < 20) or
           (action_dont_shoot and player.y - enemy2_c.y < 20) or
           (action_dont_shoot and player.y - enemy2_d.y < 20),

           #enemy3
           (action_shoot and player.y - enemy3.y < 20) or
           (action_shoot and player_l.y - enemy3.y < 20) or
           (action_shoot and player_u.y - enemy3.y < 20) or
           (action_shoot and player_c.y - enemy3.y < 20) or
           (action_shoot and player_r.y - enemy3.y < 20) or
           (action_shoot and player_d.y - enemy3.y < 20) or
           (action_shoot and player.y - enemy3_l.y < 20) or
           (action_shoot and player.y - enemy3_u.y < 20) or
           (action_shoot and player.y - enemy3_r.y < 20) or
           (action_shoot and player.y - enemy3_c.y < 20) or
           (action_shoot and player.y - enemy3_d.y < 20) or
           (action_dont_shoot and player.y - enemy3.y < 20) or
           (action_dont_shoot and player_l.y - enemy3.y < 20) or
           (action_dont_shoot and player_u.y - enemy3.y < 20) or
           (action_dont_shoot and player_c.y - enemy3.y < 20) or
           (action_dont_shoot and player_r.y - enemy3.y < 20) or
           (action_dont_shoot and player_d.y - enemy3.y < 20) or
           (action_dont_shoot and player.y - enemy3_l.y < 20) or
           (action_dont_shoot and player.y - enemy3_u.y < 20) or
           (action_dont_shoot and player.y - enemy3_r.y < 20) or
           (action_dont_shoot and player.y - enemy3_c.y < 20) or
           (action_dont_shoot and player.y - enemy3_d.y < 20),

           #enemy4
           (action_shoot and player.y - enemy4.y < 20) or
           (action_shoot and player_l.y - enemy4.y < 20) or
           (action_shoot and player_u.y - enemy4.y < 20) or
           (action_shoot and player_c.y - enemy4.y < 20) or
           (action_shoot and player_r.y - enemy4.y < 20) or
           (action_shoot and player_d.y - enemy4.y < 20) or
           (action_shoot and player.y - enemy4_l.y < 20) or
           (action_shoot and player.y - enemy4_u.y < 20) or
           (action_shoot and player.y - enemy4_r.y < 20) or
           (action_shoot and player.y - enemy4_c.y < 20) or
           (action_shoot and player.y - enemy4_d.y < 20) or
           (action_dont_shoot and player.y - enemy4.y < 20) or
           (action_dont_shoot and player_l.y - enemy4.y < 20) or
           (action_dont_shoot and player_u.y - enemy4.y < 20) or
           (action_dont_shoot and player_c.y - enemy4.y < 20) or
           (action_dont_shoot and player_r.y - enemy4.y < 20) or
           (action_dont_shoot and player_d.y - enemy4.y < 20) or
           (action_dont_shoot and player.y - enemy4_l.y < 20) or
           (action_dont_shoot and player.y - enemy4_u.y < 20) or
           (action_dont_shoot and player.y - enemy4_r.y < 20) or
           (action_dont_shoot and player.y - enemy4_c.y < 20) or
           (action_dont_shoot and player.y - enemy4_d.y < 20),

           #enemy5
           (action_shoot and player.y - enemy5.y < 20) or
           (action_shoot and player_l.y - enemy5.y < 20) or
           (action_shoot and player_u.y - enemy5.y < 20) or
           (action_shoot and player_c.y - enemy5.y < 20) or
           (action_shoot and player_r.y - enemy5.y < 20) or
           (action_shoot and player_d.y - enemy5.y < 20) or
           (action_shoot and player.y - enemy5_l.y < 20) or
           (action_shoot and player.y - enemy5_u.y < 20) or
           (action_shoot and player.y - enemy5_r.y < 20) or
           (action_shoot and player.y - enemy5_c.y < 20) or
           (action_shoot and player.y - enemy5_d.y < 20) or
           (action_dont_shoot and player.y - enemy5.y < 20) or
           (action_dont_shoot and player_l.y - enemy5.y < 20) or
           (action_dont_shoot and player_u.y - enemy5.y < 20) or
           (action_dont_shoot and player_c.y - enemy5.y < 20) or
           (action_dont_shoot and player_r.y - enemy5.y < 20) or
           (action_dont_shoot and player_d.y - enemy5.y < 20) or
           (action_dont_shoot and player.y - enemy5_l.y < 20) or
           (action_dont_shoot and player.y - enemy5_u.y < 20) or
           (action_dont_shoot and player.y - enemy5_r.y < 20) or
           (action_dont_shoot and player.y - enemy5_c.y < 20) or
           (action_dont_shoot and player.y - enemy5_d.y < 20),

           # enemy6
           (action_shoot and player.y - enemy6.y < 20) or
           (action_shoot and player_l.y - enemy6.y < 20) or
           (action_shoot and player_u.y - enemy6.y < 20) or
           (action_shoot and player_c.y - enemy6.y < 20) or
           (action_shoot and player_r.y - enemy6.y < 20) or
           (action_shoot and player_d.y - enemy6.y < 20) or
           (action_shoot and player.y - enemy6_l.y < 20) or
           (action_shoot and player.y - enemy6_u.y < 20) or
           (action_shoot and player.y - enemy6_r.y < 20) or
           (action_shoot and player.y - enemy6_c.y < 20) or
           (action_shoot and player.y - enemy6_d.y < 20) or
           (action_dont_shoot and player.y - enemy6.y < 20) or
           (action_dont_shoot and player_l.y - enemy6.y < 20) or
           (action_dont_shoot and player_u.y - enemy6.y < 20) or
           (action_dont_shoot and player_c.y - enemy6.y < 20) or
           (action_dont_shoot and player_r.y - enemy6.y < 20) or
           (action_dont_shoot and player_d.y - enemy6.y < 20) or
           (action_dont_shoot and player.y - enemy6_l.y < 20) or
           (action_dont_shoot and player.y - enemy6_u.y < 20) or
           (action_dont_shoot and player.y - enemy6_r.y < 20) or
           (action_dont_shoot and player.y - enemy6_c.y < 20) or
           (action_dont_shoot and player.y - enemy6_d.y < 20),

           #Move direction
           dir_l,
           dir_r,
           dir_n,

           #action stae
           action_shoot,
           action_dont_shoot,

           ##enemy_arrow_collision_points

           ##enemy 1
           (arrow_c.x==enemy1.x and arrow_c.y==enemy1.y) or
           (arrow_l.x == enemy1.x and arrow_l.y == enemy1_l.y) or
           (arrow_r.x == enemy1.x and arrow_r.y == enemy1_l.y) or
           (arrow_u.x == enemy1.x and arrow_u.y == enemy1_l.y) or
           (arrow_d.x == enemy1.x and arrow_d.y == enemy1_l.y) or
           (arrow_c.x == enemy1.x and arrow_c.y == enemy1_c.y) or
           (arrow_l.x == enemy1.x and arrow_l.y == enemy1_c.y) or
           (arrow_r.x == enemy1.x and arrow_r.y == enemy1_c.y) or
           (arrow_u.x == enemy1.x and arrow_u.y == enemy1_c.y) or
           (arrow_d.x == enemy1.x and arrow_d.y == enemy1_c.y) or
           (arrow_c.x == enemy1.x and arrow_c.y == enemy1_r.y) or
           (arrow_l.x == enemy1.x and arrow_l.y == enemy1_r.y) or
           (arrow_r.x == enemy1.x and arrow_r.y == enemy1_r.y) or
           (arrow_u.x == enemy1.x and arrow_u.y == enemy1_r.y) or
           (arrow_d.x == enemy1.x and arrow_d.y == enemy1_r.y) or
           (arrow_c.x == enemy1.x and arrow_c.y == enemy1_u.y) or
           (arrow_l.x == enemy1.x and arrow_l.y == enemy1_u.y) or
           (arrow_r.x == enemy1.x and arrow_r.y == enemy1_u.y) or
           (arrow_u.x == enemy1.x and arrow_u.y == enemy1_u.y) or
           (arrow_d.x == enemy1.x and arrow_d.y == enemy1_u.y) or
           (arrow_c.x == enemy1.x and arrow_c.y == enemy1_d.y) or
           (arrow_l.x == enemy1.x and arrow_l.y == enemy1_d.y) or
           (arrow_r.x == enemy1.x and arrow_r.y == enemy1_d.y) or
           (arrow_u.x == enemy1.x and arrow_u.y == enemy1_d.y) or
           (arrow_d.x == enemy1.x and arrow_d.y == enemy1_d.y),

           ##enemy2
           (arrow_c.x == enemy2.x and arrow_c.y == enemy2.y) or
           (arrow_l.x == enemy2.x and arrow_l.y == enemy2_l.y) or
           (arrow_r.x == enemy2.x and arrow_r.y == enemy2_l.y) or
           (arrow_u.x == enemy2.x and arrow_u.y == enemy2_l.y) or
           (arrow_d.x == enemy2.x and arrow_d.y == enemy2_l.y) or
           (arrow_c.x == enemy2.x and arrow_c.y == enemy2_c.y) or
           (arrow_l.x == enemy2.x and arrow_l.y == enemy2_c.y) or
           (arrow_r.x == enemy2.x and arrow_r.y == enemy2_c.y) or
           (arrow_u.x == enemy2.x and arrow_u.y == enemy2_c.y) or
           (arrow_d.x == enemy2.x and arrow_d.y == enemy2_c.y) or
           (arrow_c.x == enemy2.x and arrow_c.y == enemy2_r.y) or
           (arrow_l.x == enemy2.x and arrow_l.y == enemy2_r.y) or
           (arrow_r.x == enemy2.x and arrow_r.y == enemy2_r.y) or
           (arrow_u.x == enemy2.x and arrow_u.y == enemy2_r.y) or
           (arrow_d.x == enemy2.x and arrow_d.y == enemy2_r.y) or
           (arrow_c.x == enemy2.x and arrow_c.y == enemy2_u.y) or
           (arrow_l.x == enemy2.x and arrow_l.y == enemy2_u.y) or
           (arrow_r.x == enemy2.x and arrow_r.y == enemy2_u.y) or
           (arrow_u.x == enemy2.x and arrow_u.y == enemy2_u.y) or
           (arrow_d.x == enemy2.x and arrow_d.y == enemy2_u.y) or
           (arrow_c.x == enemy2.x and arrow_c.y == enemy2_d.y) or
           (arrow_l.x == enemy2.x and arrow_l.y == enemy2_d.y) or
           (arrow_r.x == enemy2.x and arrow_r.y == enemy2_d.y) or
           (arrow_u.x == enemy2.x and arrow_u.y == enemy2_d.y) or
           (arrow_d.x == enemy2.x and arrow_d.y == enemy2_d.y),

           #enemy3
           (arrow_c.x == enemy3.x and arrow_c.y == enemy3.y) or
           (arrow_l.x == enemy3.x and arrow_l.y == enemy3_l.y) or
           (arrow_r.x == enemy3.x and arrow_r.y == enemy3_l.y) or
           (arrow_u.x == enemy3.x and arrow_u.y == enemy3_l.y) or
           (arrow_d.x == enemy3.x and arrow_d.y == enemy3_l.y) or
           (arrow_c.x == enemy3.x and arrow_c.y == enemy3_c.y) or
           (arrow_l.x == enemy3.x and arrow_l.y == enemy3_c.y) or
           (arrow_r.x == enemy3.x and arrow_r.y == enemy3_c.y) or
           (arrow_u.x == enemy3.x and arrow_u.y == enemy3_c.y) or
           (arrow_d.x == enemy3.x and arrow_d.y == enemy3_c.y) or
           (arrow_c.x == enemy3.x and arrow_c.y == enemy3_r.y) or
           (arrow_l.x == enemy3.x and arrow_l.y == enemy3_r.y) or
           (arrow_r.x == enemy3.x and arrow_r.y == enemy3_r.y) or
           (arrow_u.x == enemy3.x and arrow_u.y == enemy3_r.y) or
           (arrow_d.x == enemy3.x and arrow_d.y == enemy3_r.y) or
           (arrow_c.x == enemy3.x and arrow_c.y == enemy3_u.y) or
           (arrow_l.x == enemy3.x and arrow_l.y == enemy3_u.y) or
           (arrow_r.x == enemy3.x and arrow_r.y == enemy3_u.y) or
           (arrow_u.x == enemy3.x and arrow_u.y == enemy3_u.y) or
           (arrow_d.x == enemy3.x and arrow_d.y == enemy3_u.y) or
           (arrow_c.x == enemy3.x and arrow_c.y == enemy3_d.y) or
           (arrow_l.x == enemy3.x and arrow_l.y == enemy3_d.y) or
           (arrow_r.x == enemy3.x and arrow_r.y == enemy3_d.y) or
           (arrow_u.x == enemy3.x and arrow_u.y == enemy3_d.y) or
           (arrow_d.x == enemy3.x and arrow_d.y == enemy3_d.y),

           #enemy4
           (arrow_c.x == enemy4.x and arrow_c.y == enemy4.y) or
           (arrow_l.x == enemy4.x and arrow_l.y == enemy4_l.y) or
           (arrow_r.x == enemy4.x and arrow_r.y == enemy4_l.y) or
           (arrow_u.x == enemy4.x and arrow_u.y == enemy4_l.y) or
           (arrow_d.x == enemy4.x and arrow_d.y == enemy4_l.y) or
           (arrow_c.x == enemy4.x and arrow_c.y == enemy4_c.y) or
           (arrow_l.x == enemy4.x and arrow_l.y == enemy4_c.y) or
           (arrow_r.x == enemy4.x and arrow_r.y == enemy4_c.y) or
           (arrow_u.x == enemy4.x and arrow_u.y == enemy4_c.y) or
           (arrow_d.x == enemy4.x and arrow_d.y == enemy4_c.y) or
           (arrow_c.x == enemy4.x and arrow_c.y == enemy4_r.y) or
           (arrow_l.x == enemy4.x and arrow_l.y == enemy4_r.y) or
           (arrow_r.x == enemy4.x and arrow_r.y == enemy4_r.y) or
           (arrow_u.x == enemy4.x and arrow_u.y == enemy4_r.y) or
           (arrow_d.x == enemy4.x and arrow_d.y == enemy4_r.y) or
           (arrow_c.x == enemy4.x and arrow_c.y == enemy4_u.y) or
           (arrow_l.x == enemy4.x and arrow_l.y == enemy4_u.y) or
           (arrow_r.x == enemy4.x and arrow_r.y == enemy4_u.y) or
           (arrow_u.x == enemy4.x and arrow_u.y == enemy4_u.y) or
           (arrow_d.x == enemy4.x and arrow_d.y == enemy4_u.y) or
           (arrow_c.x == enemy4.x and arrow_c.y == enemy4_d.y) or
           (arrow_l.x == enemy4.x and arrow_l.y == enemy4_d.y) or
           (arrow_r.x == enemy4.x and arrow_r.y == enemy4_d.y) or
           (arrow_u.x == enemy4.x and arrow_u.y == enemy4_d.y) or
           (arrow_d.x == enemy4.x and arrow_d.y == enemy4_d.y),

           ##enemy 5
           (arrow_c.x == enemy5.x and arrow_c.y == enemy5_l.y) or
           (arrow_l.x == enemy5.x and arrow_l.y == enemy5_l.y) or
           (arrow_r.x == enemy5.x and arrow_r.y == enemy5_l.y) or
           (arrow_u.x == enemy5.x and arrow_u.y == enemy5_l.y) or
           (arrow_d.x == enemy5.x and arrow_d.y == enemy5_l.y) or
           (arrow_c.x == enemy5.x and arrow_c.y == enemy5_c.y) or
           (arrow_l.x == enemy5.x and arrow_l.y == enemy5_c.y) or
           (arrow_r.x == enemy5.x and arrow_r.y == enemy5_c.y) or
           (arrow_u.x == enemy5.x and arrow_u.y == enemy5_c.y) or
           (arrow_d.x == enemy5.x and arrow_d.y == enemy5_c.y) or
           (arrow_c.x == enemy5.x and arrow_c.y == enemy5_r.y) or
           (arrow_l.x == enemy5.x and arrow_l.y == enemy5_r.y) or
           (arrow_r.x == enemy5.x and arrow_r.y == enemy5_r.y) or
           (arrow_u.x == enemy5.x and arrow_u.y == enemy5_r.y) or
           (arrow_d.x == enemy5.x and arrow_d.y == enemy5_r.y) or
           (arrow_c.x == enemy5.x and arrow_c.y == enemy5_u.y) or
           (arrow_l.x == enemy5.x and arrow_l.y == enemy5_u.y) or
           (arrow_r.x == enemy5.x and arrow_r.y == enemy5_u.y) or
           (arrow_u.x == enemy5.x and arrow_u.y == enemy5_u.y) or
           (arrow_d.x == enemy5.x and arrow_d.y == enemy5_u.y) or
           (arrow_c.x == enemy5.x and arrow_c.y == enemy5_d.y) or
           (arrow_l.x == enemy5.x and arrow_l.y == enemy5_d.y) or
           (arrow_r.x == enemy5.x and arrow_r.y == enemy5_d.y) or
           (arrow_u.x == enemy5.x and arrow_u.y == enemy5_d.y) or
           (arrow_d.x == enemy5.x and arrow_d.y == enemy5_d.y),

           ##enemy 6
           (arrow_c.x == enemy6.x and arrow_c.y == enemy6_l.y) or
           (arrow_l.x == enemy6.x and arrow_l.y == enemy6_l.y) or
           (arrow_r.x == enemy6.x and arrow_r.y == enemy6_l.y) or
           (arrow_u.x == enemy6.x and arrow_u.y == enemy6_l.y) or
           (arrow_d.x == enemy6.x and arrow_d.y == enemy6_l.y) or
           (arrow_c.x == enemy6.x and arrow_c.y == enemy6_c.y) or
           (arrow_l.x == enemy6.x and arrow_l.y == enemy6_c.y) or
           (arrow_r.x == enemy6.x and arrow_r.y == enemy6_c.y) or
           (arrow_u.x == enemy6.x and arrow_u.y == enemy6_c.y) or
           (arrow_d.x == enemy6.x and arrow_d.y == enemy6_c.y) or
           (arrow_c.x == enemy6.x and arrow_c.y == enemy6_r.y) or
           (arrow_l.x == enemy6.x and arrow_l.y == enemy6_r.y) or
           (arrow_r.x == enemy6.x and arrow_r.y == enemy6_r.y) or
           (arrow_u.x == enemy6.x and arrow_u.y == enemy6_r.y) or
           (arrow_d.x == enemy6.x and arrow_d.y == enemy6_r.y) or
           (arrow_c.x == enemy6.x and arrow_c.y == enemy6_u.y) or
           (arrow_l.x == enemy6.x and arrow_l.y == enemy6_u.y) or
           (arrow_r.x == enemy6.x and arrow_r.y == enemy6_u.y) or
           (arrow_u.x == enemy6.x and arrow_u.y == enemy6_u.y) or
           (arrow_d.x == enemy6.x and arrow_d.y == enemy6_u.y) or
           (arrow_c.x == enemy6.x and arrow_c.y == enemy6_d.y) or
           (arrow_l.x == enemy6.x and arrow_l.y == enemy6_d.y) or
           (arrow_r.x == enemy6.x and arrow_r.y == enemy6_d.y) or
           (arrow_u.x == enemy6.x and arrow_u.y == enemy6_d.y) or
           (arrow_d.x == enemy6.x and arrow_d.y == enemy6_d.y),
           ]

       return np.array(state,dtype=int)


    def remember(self,state,direction,action,reward,new_state,done):
        self.memory.append((state,direction,action,reward,new_state,done)) ##popleft if exceeds maxlen


    def train_long_memory(self):
        if len(self.memory)>BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
            print('1k', len(self.memory))
            states,directions,actions,rewards,new_states,dones=zip(*mini_sample)
            self.trainer.train_step(states, directions,actions, rewards, new_states, dones)
        else:
            print('1k>or<', len(self.memory))
            mini_sample = self.memory
            states,directions,actions,rewards,new_states,dones=zip(*mini_sample)
            self.trainer.train_step(states, directions, actions, rewards, new_states, dones)

    def train_short_memory(self,state,direction,action,reward,new_state,done):
        self.trainer.train_step(state,direction,action,reward,new_state,done )

    def get_direction_action(self,state):
        self.epsilon = 80 - self.n_game
        final_direction_move = [0,0,0]
        final_action_move = [0,0]
        if random.randint(0,200)<self.epsilon:
            move1 = random.randint(0,2)
            move2 = random.randint(0,1)
            final_direction_move[move1]=1
            final_action_move[move2]=1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            dir, act = self.model(state0)
            move1 = torch.argmax(dir).item()
            move2 = torch.argmax(act)
            final_direction_move[move1]=1
            final_action_move[move2]=1

        return final_direction_move,final_action_move


def train():
    plot_scores=[]
    plot_mean_scores=[]
    total_score=0
    record=0
    agent=Agent()
    game=SpaceGame()

    while True:
        #get old state
        state_old = agent.get_state(game)

        #get move
        final_dir_move, final_ac_move = agent.get_direction_action(state_old)

        #perform move and get new state
        done, reward, score = game.playstep(final_dir_move,final_ac_move)

        #state_new
        state_new = agent.get_state(game)

        #train short memory
        agent.train_short_memory(state_old,final_dir_move,final_ac_move,reward,state_new,done)

        agent.remember(state_old,final_dir_move,final_ac_move,reward,state_new,done)

        if done:
            game.reset()
            agent.n_game += 1
            agent.train_long_memory()

            if score>record:
                record=score
                agent.model.save()

            print('Game',agent.n_game,'Score',score,'Reward',reward)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score/agent.n_game
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()