import pygame
import sys
from pygame.locals import *
import random


class Bird():
     def __init__(self, pos_x, pos_y, speed):  #初始化
          self.images = [bird_0_image, bird_1_image, bird_2_image]
          self.order = 0  #应该放第几张图片
          self.number = 3   #做一个动画一共需要3张图
          self.image = self.images[self.order]
          self.rect = self.image.get_rect()  #取出一个代表图片的矩形
          self.rect.x = pos_x  #矩形左上角的坐标
          self.rect.y = pos_y
          #小鸟图片并非充满整个rect，做碰撞检测需要小鸟的精确位置，记做self.base
          self.base = pygame.Rect(self.rect.x + 6, self.rect.y + 13, 34, 24)
          self.speed_y = speed
          self.crash = 0  #坠落情况
          self.score = 0  #分数
          self.direct = 1  #用于开始界面，小鸟上下浮动的动画，判断小鸟飞动方向
     def draw(self, screen):  #画在屏幕上
          screen.blit(self.image, (self.rect.x, self.rect.y))
     def flap(self):  #扇翅膀动画
          if self.order >= self.number - 1:
              self.order = -1
          self.order += 1
          self.image = self.images[self.order]
     def move_y(self):  #小鸟动作规律以及积分情况
          coin_sound = pygame.mixer.Sound("coin_sound.wav")
          self.rect.y += self.speed_y
          self.speed_y += gravity
          self.base = pygame.Rect(self.rect.x + 6, self.rect.y + 13, 34, 24)
          if self.rect.x == pipe_1.rect_up.x or self.rect.x == pipe_2.rect_up.x + 1:
               coin_sound.play()
               self.score = max(pipe_1.order, pipe_2.order) - 1
               
     def up_and_down(self, pos_y):  #开始界面，小鸟上下浮动的动画
          if self.rect.y <= pos_y:
               self.direct = 1
               self.rect.y += self.direct
          elif self.rect.y >= pos_y + 5 :
               self.direct = -1
               self.rect.y += self.direct
          else:
               self.rect.y += self.direct
     def soar(self, speed):  #点击小鸟飞起
          self.speed_y = speed
     def drop(self):  #小鸟坠落
          self.rect.y += self.speed_y
          self.speed_y += gravity
     def die(self):  #小鸟死亡
          self.rect.y = 365
          self.image = self.images[2]
          
          
###柱子1###
class Pipe_1():
     def __init__(self):  #初始化
          self.images = [pipe_up_image, pipe_down_image]
          self.rand= random.randrange(50, 270, 20)
          self.rect_up = self.images[0].get_rect()  #上部分柱子
          self.rect_down = self.images[1].get_rect()  #下部分柱子
          self.order = 1  #柱子编号
          self.rect_up.x = 1.5 * screen_width  #位置
          self.rect_down.x = 1.5 * screen_width
          self.rect_up.y = 400 - self.rand
          self.rect_down.y  = - self.rand - 20
     def draw(self, screen):  #画在屏幕上
          screen.blit(self.images[0], (self.rect_up.x, self.rect_up.y))
          screen.blit(self.images[1], (self.rect_down.x, self.rect_down.y))
     def move_x(self):  #柱子动作规律
          if self.rect_up.x > -pipe_width:
               self.rect_up.x -= pipe_speed
               self.rect_down.x -= pipe_speed
          else:
               self.reset()
     def reset(self):  #移出屏幕后重新进入屏幕
          self.rand = random.randrange(50, 270, 20)
          self.rect_up.x = screen_width
          self.rect_down.x = screen_width
          self.rect_up.y = 400 - self.rand
          self.rect_down.y  = -self.rand - 20  ##柱子是320个像素点，地面以上部分400个像素点，两柱之间距离有点近，- 20拉大20个像素的距离，可根据喜好随意设置
          self.order += 2
     def collide(self, bird_rect):  #判断与小鸟的碰撞
          if self.rect_up.colliderect(bird_rect):
               collide_pipe = 1
          elif self.rect_down.colliderect(bird_rect):
               collide_pipe= 1
          else:
               collide_pipe = 0
          return collide_pipe
     def halt(self):
          pass
     
###柱子2，与柱子1一模一样，不再注释###
class Pipe_2():
     def __init__(self):
          self.images = [pipe_up_image, pipe_down_image]
          self.rand= random.randrange(50, 270, 20)
          self.rect_up = self.images[0].get_rect()
          self.rect_down = self.images[1].get_rect()
          self.order = 0
          self.reset()
     def draw(self, screen):
          screen.blit(self.images[0], (self.rect_up.x, self.rect_up.y))
          screen.blit(self.images[1], (self.rect_down.x, self.rect_down.y))
     def move_x(self):
          if pipe_1.rect_up.x < self.rect_up.x:
               self.rect_up.x = pipe_1.rect_up.x + (screen_width + pipe_width)/2
               self.rect_down.x = pipe_1.rect_down.x + (screen_width + pipe_width)/2
          elif pipe_1.rect_up.x > self.rect_up.x and self.rect_up.x > -pipe_width:
               self.rect_up.x -= pipe_speed
               self.rect_down.x -= pipe_speed
          else:
               self.reset()
     def reset(self):
          self.rand = random.randrange(50, 270, 20)
          self.rect_up.x = pipe_1.rect_up.x + (screen_width + pipe_width)/2
          self.rect_down.x = pipe_1.rect_up.x + (screen_width + pipe_width)/2
          self.rect_up.y = 400 - self.rand
          self.rect_down.y  = - self.rand - 20
          self.order += 2
     def collide(self, bird_rect):
          if self.rect_up.colliderect(bird_rect):
               collide_pipe = 1
          elif self.rect_down.colliderect(bird_rect):
               collide_pipe= 1
          else:
                collide_pipe = 0
          return collide_pipe
     def halt(self):
          pass
               
          
          ###地面###
class Land():
     def __init__(self):  #初始化
          self.image = land_image
          self.rect = self.image.get_rect()
          self.rect.x = 0
          self.rect.y = 400
          
     def draw(self, screen):  #画在屏幕上
          screen.blit(self.image, (self.rect.x, self.rect.y))
     def move_x(self):  #地面动作规律
          if self.rect.x > -44:
               self.rect.x -= pipe_speed
          else:
               self.rect.x = 0
     def collide(self, bird_rect):  #判断与小鸟碰撞
          if self.rect.colliderect(bird_rect):
               collide_land = 1
          else:
               collide_land = 0
          return collide_land
     def halt(self):
          pass
     
###分数###
class Score():
     def __init__(self):
          self.images = [num_0_image, num_1_image, num_2_image, num_3_image,
                         num_4_image, num_5_image, num_6_image, num_7_image,
                         num_8_image, num_9_image]
          self.hun_pos_3 = 108
          self.dec_pos_3 = 132
          self.dec_pos_2 = 120
          self.uni_pos_3 = 156
          self.uni_pos_2 = 144
          self.uni_pos_1 = 132
     def draw(self, screen, score):  #画在屏幕上，为了保持分数在屏幕正中央，判断分数有几位，根据位数画图
          if score < 10:  
               screen.blit(self.images[score], (self.uni_pos_1, 0))
          if score >= 10 and score <100:
               screen.blit(self.images[score%10], (self.uni_pos_2, 0))
               screen.blit(self.images[int(score/10)], (self.dec_pos_2, 0))
          if score > 100:
               screen.blit(self.images[score%10], (self.uni_pos_3, 0))
               screen.blit(self.images[int((score%100)/10)], (self.dec_pos_3, 0))
               screen.blit(self.images[int(score/100)], (self.hun_pos_3, 0))
