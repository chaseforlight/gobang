import pygame
from game_value import GameValue

class ChessPiece:
    def __init__(self,color,center):
        self.images = {
            'white' : pygame.image.load('images/white_chesspiece.png'),
            'black' : pygame.image.load('images/black_chesspiece.png'),
        }
        self.color = color
        self.image = self.images[self.color]
        self.rect = self.image.get_rect()
        self.rect.center = center

    def display_chess_piece(self):
        self.image = self.images[self.color]
        GameValue.window.blit(self.image,self.rect)

