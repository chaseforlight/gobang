import pygame
from game_value import GameValue

class Menu:
    def __init__(self):
        self.background = pygame.image.load('images/back.png')
        self.msg = '五    子    棋'
        self.font_name = '华文行楷'
        self.font = pygame.font.SysFont(self.font_name,150)
        self.text = self.font.render(self.msg,True,'yellow')
        self.rect = self.text.get_rect()
        self.rect.center = (450,200)

    def show_buttons(self):
        b1 = Button('p v p',(450,600))
        b2 = Button('p v e',(450,700))
        b3 = Button('e v e',(450,800))
        GameValue.button_list = [b1,b2,b3]
        b1.show_button()
        b2.show_button()
        b3.show_button()

    def show_menu(self):
        GameValue.window = pygame.display.set_mode((GameValue.screen_width,GameValue.screen_height))
        pygame.display.set_caption("五子棋")
        GameValue.window.blit(self.background,(0,0))
        GameValue.window.blit(self.text,self.rect)
        self.show_buttons()

class Button:
    def __init__(self,msg,center):
        self.font_name = 'microsofttaile'
        self.font = pygame.font.SysFont(self.font_name,50)
        self.text = self.font.render(msg,True,'blue')
        self.rect = self.text.get_rect()
        self.rect.center = center

    def show_button(self):
        GameValue.window.blit(self.text,self.rect)

    def check_click(self,mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False
