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
