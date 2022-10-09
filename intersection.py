'''
    处理棋盘横竖线之间的交叉点，实现点击落子效果
'''

import pygame
from game_value import GameValue

class Intersection:
    def __init__(self,center):
        self.image = pygame.image.load('images/black_chesspiece.png')
        self.rect = self.image.get_rect()
        self.rect.center = center

def create_intersections():
    for top in range(30,900,60):
        for left in range(30,900,60):
            point = Intersection((left,top))
            GameValue.intersection_list.append(point)
