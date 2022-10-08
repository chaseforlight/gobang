import pygame
from game_value import *

class RedSpot:
    def __init__(self,center):
        self.image = pygame.image.load('images/redspot.png')
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.live = True
    def display_redspot(self):
        GameValue.window.blit(self.image,self.rect)
