import pygame
from enum import Enum
from collections import namedtuple
from pygame import mixer

pygame.init()
mixer.init()

class Direction(Enum):
    RIGHT=1
    LEFT=2
    NOTHING=3

background = pygame.image.load('space_bg.png')
spaceship = pygame.image.load('spaceship.png') #64*64
enemy = pygame.image.load('alien.png') #32*32
bullet = pygame.image.load('arrow-up.png') #32*32
font = pygame.font.Font('C:\\Users\\Administrator\\Downloads\\arial\\arial.ttf',25)
WHITE = (255,255,255)
BLOCK_SIZE = 20

mixer.music.load("Pubg Bullet Sound Message.mp3")
mixer.music.set_volume(0.7)
mixer.music.play()

Point = namedtuple('Point','x,y')

class SpaceGame:

  def __init__(self,w=800,h=450):
      self.w=w
      self.h=h
      #init display
      self.display = pygame.display.set_mode((self.w,self.h))
      pygame.display.set_caption('Space Game')
      self.player = Point(350,380)
      self.arrow = Point(365,355)
      self.enemy1 = Point(0,0)
      self.enemy2 = Point(160,0)
      self.enemy3 = Point(320,0)
      self.enemy4 = Point(480,0)
      self.enemy5 = Point(640,0)
      self.action = False
      self.direction = Direction.NOTHING
      self.clock = pygame.time.Clock()
      self.count=0
      self.score = 0


  def playstep(self):
      #collect user input
      for event in pygame.event.get():
          if event.type==pygame.QUIT:
              pygame.quit()
              quit()
          if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_LEFT:
                self.direction = Direction.LEFT
             elif event.key == pygame.K_RIGHT:
                self.direction = Direction.RIGHT
             elif event.key == pygame.K_SPACE:
                self.action = True

          if event.type == pygame.KEYUP:
             if event.key == pygame.K_LEFT:
                self.direction = Direction.NOTHING
             elif event.key == pygame.K_RIGHT:
                self.direction = Direction.NOTHING
             elif event.key == pygame.K_SPACE:
                self.action = True

      self.move(self.direction,self.action)

      if self.arrow.y < 10:
          self.action=False

      game_over = False
      if self.is_collison() or self.count>2:
          game_over = True
          return game_over,self.score

      if self.is_enemy_collison():
          self.score += 1
          mixer.music.unpause()

      else:
          mixer.music.pause()

      self.update_ui()
      self.clock.tick(10)

      return game_over,self.score

  def is_enemy_collison(self):

      enemy1 = [(-10,self.enemy1.y),(-5,self.enemy1.y),(0,self.enemy1.y),(5,self.enemy1.y),
                (10,self.enemy1.y),(15,self.enemy1.y),(20,self.enemy1.y),(25,self.enemy1.y),(30,self.enemy1.y),
                (35,self.enemy1.y),(40,self.enemy1.y)]
      enemy2 = [(150,self.enemy2.y),(155,self.enemy2.y),(160,self.enemy2.y),(165,self.enemy2.y),
                (170,self.enemy2.y),(175,self.enemy2.y),(180,self.enemy2.y)]
      enemy3 = [(310,self.enemy3.y),(315,self.enemy3.y),(320,self.enemy3.y),(325,self.enemy3.y),
                (330,self.enemy3.y),(345,self.enemy3.y),(350,self.enemy3.y)]
      enemy4 = [(470,self.enemy4.y),(475,self.enemy4.y),(480,self.enemy4.y),(485,self.enemy4.y),
                (490,self.enemy4.y),(495,self.enemy4.y),(500,self.enemy4.y)]
      enemy5 = [(630,self.enemy5.y),(635,self.enemy5.y),(640,self.enemy5.y),(645,self.enemy5.y),
                (650,self.enemy5.y),(655,self.enemy5.y),(660,self.enemy5.y)]
      x = self.arrow.x
      y = self.arrow.y

      arrow = [(x-10,y),(x-5,y),(x,y-10),(x,y-5),(x,y),(x-5,y),(x+10,y),(x,y+5),(x,y+10),
               (x-15,y),(x-20,y),(x+20,y),(x+25,y),(x,y-15),(x,y+15),(x,y+20),(x,y-20),(x,y-25),(x,y+25),
               (x-35,y),(x-25,y),(x-30,y),(x+25,y),(x+30,y),(x+35,y),(x,y-25),(x,y-30),(x,y-35),(x,y+25),
               (x,y+30),(x,y+35),
               (x-40,y),(x-45,y),(x-50,y),(x+40,y),(x+45,y),(x+50,y),(x,y-40),(x,y+45),(x,y+50),
               (x,y+40),(x,y-45),(x,y-50)]

      x1 = self.enemy1.x
      y1 = self.enemy1.y
      x2 = self.enemy2.x
      y2 = self.enemy2.y
      x3 = self.enemy3.x
      y3 = self.enemy3.y
      x4 = self.enemy4.x
      y4 = self.enemy4.y
      x5 = self.enemy5.x
      y5 = self.enemy5.y

      check1 = any(i in arrow for i in enemy1)
      check2 = any(i in arrow for i in enemy2)
      check3 = any(i in arrow for i in enemy3)
      check4 = any(i in arrow for i in enemy4)
      check5 = any(i in arrow for i in enemy5)


      if check1 is True:
          y1 = 0
          self.enemy1 = Point(x1, y1)
          return True

      elif check2 is True:
          y2 = 0
          self.enemy2 = Point(x2, y2)
          return True

      elif check3 is True:
         y3 = 0
         self.enemy3 = Point(x3, y3)
         return True

      elif check4 is True:
           y4 = 0
           self.enemy4 = Point(x4, y4)
           return True

      elif check5 is True:
           y5 = 0
           self.enemy5 = Point(x5, y5)
           return True

      else :
          return False



  def is_collison(self):

      if self.enemy1.y == self.player.y and self.enemy1.x == self.player.x :
         return True

      enemy2 = [(150,self.enemy2.y),(155,self.enemy2.y),(160,self.enemy2.y),(165,self.enemy2.y),
                (170,self.enemy2.y),(175,self.enemy2.y),(180,self.enemy2.y)]
      if self.player in enemy2:
          return True

      enemy3 = [(310,self.enemy3.y),(315,self.enemy3.y),(320,self.enemy3.y),(325,self.enemy3.y),
                (330,self.enemy3.y),(345,self.enemy3.y),(350,self.enemy3.y)]
      if self.player in enemy3 :
         return True

      enemy4 = [(470,self.enemy4.y),(475,self.enemy4.y),(480,self.enemy4.y),(485,self.enemy4.y),
                (490,self.enemy4.y),(495,self.enemy4.y),(500,self.enemy4.y)]
      if self.player in enemy4 :
         return True

      enemy5 = [(630,self.enemy5.y),(635,self.enemy5.y),(640,self.enemy5.y),(645,self.enemy5.y),
                (650,self.enemy5.y),(655,self.enemy5.y),(660,self.enemy5.y)]
      if self.player in enemy5:
         return True


  def move(self,direction,action):
      x=self.player.x
      y=self.player.y
      x_ar = self.arrow.x
      y_ar = self.arrow.y
      x1 = self.enemy1.x
      y1 = self.enemy1.y
      x2 = self.enemy2.x
      y2 = self.enemy2.y
      x3 = self.enemy3.x
      y3 = self.enemy3.y
      x4 = self.enemy4.x
      y4 = self.enemy4.y
      x5 = self.enemy5.x
      y5 = self.enemy5.y

      if direction==Direction.RIGHT:
          x += BLOCK_SIZE
          x_ar += BLOCK_SIZE
      elif direction==Direction.LEFT:
          x -= BLOCK_SIZE
          x_ar -= BLOCK_SIZE
      elif direction==Direction.NOTHING:
          x = self.player.x
          y = self.player.y

      if y1 > 375 :
          self.count += 1
          y1 = 0
          y2 = 0
          y3 = 0
          y4 = 0
          y5 = 0

      else:

          y1 += BLOCK_SIZE
          y2 += BLOCK_SIZE
          y3 += BLOCK_SIZE
          y4 += BLOCK_SIZE
          y5 += BLOCK_SIZE

      if action==True:

          y_ar -= BLOCK_SIZE

          if y_ar == y1:
              y1 = 0
              y_ar = y - 25
          elif y_ar == y2:
              y2 = 0
              y_ar = y - 25
          elif y_ar == y3:
              y3 = 0
              y_ar = y - 25
          elif y_ar == y4:
              y4 = 0
              y_ar = y - 25
          elif y_ar == y5:
              y5 = 0
              y_ar = y - 25

      else :

          y_ar = y-25


      if x < 0:
          x = 0
          x_ar = x + 15

      if x > 735:
          x = 735
          x_ar = x + 15


      self.player = Point(x,y)
      self.arrow = Point(x_ar,y_ar)
      self.enemy1 = Point(x1, y1)
      self.enemy2 = Point(x2, y2)
      self.enemy3 = Point(x3, y3)
      self.enemy4 = Point(x4, y4)
      self.enemy5 = Point(x5, y5)


  def update_ui(self):
     self.display.fill((0,0,0))
     self.display.blit(background,(0,0))
     self.display.blit(spaceship, (self.player))
     self.display.blit(bullet,(self.arrow))
     text = font.render("Score " + str(self.score), True, WHITE)
     self.display.blit(text, (0, 420))
     self.display.blit(enemy, (self.enemy1))
     self.display.blit(enemy, (self.enemy2))
     self.display.blit(enemy, (self.enemy3))
     self.display.blit(enemy, (self.enemy4))
     self.display.blit(enemy, (self.enemy5))
     pygame.display.flip()


if __name__=='__main__':
   game=SpaceGame()

   ##game loop
   while True:

       game_over, score = game.playstep()
       if game_over == True:
           break

   print('Final Score',score)