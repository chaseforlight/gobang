import pygame
from game_value import GameValue

class Pen:
    def __init__(self,win_side): #1 为黑棋赢，2 为白棋赢
        self.texts = ['','黑棋获胜!','白棋获胜!','和 棋！']

        self.font_name = '方正舒体'
        self.font = pygame.font.SysFont(self.font_name,50)
        self.win_side = win_side
        self.msg = self.texts[self.win_side]
        self.text = self.font.render(self.msg,True,'red')
        self.rect = self.text.get_rect()
        self.rect.center = (450,450)

    def display_text(self):
        GameValue.window.blit(self.text,self.rect)
