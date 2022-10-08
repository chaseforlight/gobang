import pygame
from game_value import GameValue

class ChessBoard:
    def __init__(self):
        pass
    def display_chessboard(self):
        #画横线
        for top in range(30,900,60):
            pygame.draw.line(GameValue.window,'black',(30,top),(870,top))
        #画竖线
        for left in range(30,900,60):
            pygame.draw.line(GameValue.window,'black',(left,30),(left,870))
