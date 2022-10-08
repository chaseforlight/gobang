import sys
import pygame
from time import sleep
from game_value import GameValue
from chessboard import ChessBoard
from intersection import *
from chess_piece import *
from pen import Pen
from boardevaluate import *

class MainGame:
    def __init__(self):
        pass
    def start_game(self):
        pygame.init()
        self.init_game()
        inittuple6()
        while True:
            sleep(0.02)
            self.get_events()

            if GameValue.game_over:
                self.blit_game_over_text()

            pygame.display.update()

    def init_game(self):
        self.init_window()
        #GameValue.window.fill((1,77,103))
        self.set_background()
        self.blit_chessboard()
        create_intersections()
    
    def restart_game(self):
        GameValue.intersection_list = []
        GameValue.last_piece = 'white'
        GameValue.chessboard_map = [[0 for i in range(16)] for j in range(16)]
        GameValue.game_over = 0
        GameValue.chess_piece_count = 0
        self.init_game()

        
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end_game()  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.end_game()
                elif event.key == pygame.K_p:
                    self.restart_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and GameValue.game_over == 0:
                mouse_pos = pygame.mouse.get_pos()
                x = (mouse_pos[0] + 45) // 60
                y = (mouse_pos[1] + 45) // 60
                for intersection in GameValue.intersection_list:
                    if intersection.rect.collidepoint(mouse_pos) and GameValue.chessboard_map[x][y] == 0:
                        #if GameValue.last_piece == 'white':
                            bc = ChessPiece('black',intersection.rect.center)
                            bc.display_chess_piece() #该行实现点击鼠标后立刻显示黑棋，而不是等到AI算完后再一起显示
                            GameValue.chess_piece_count += 1
                            pygame.display.update()
                            # GameValue.black_chess_piece_list.append(bc)
                            GameValue.last_piece = 'black'
                            GameValue.chessboard_map[x][y] = 1

                            if self.check_game_over(1,x,y):
                                GameValue.game_over = 1
                                break
                            if self.check_draw():
                                GameValue.game_over = 3

                            value,point = analyse(GameValue.chessboard_map,1,float('-inf'),float('inf'))
                            print(value,point)
                            GameValue.AI_pos[0] = point[0] * 60 - 30
                            GameValue.AI_pos[1] = point[1] * 60 - 30
                        #else:
                            #wc = ChessPiece('white',intersection.rect.center)
                            sleep(1)
                            wc = ChessPiece('white',GameValue.AI_pos)
                            wc.display_chess_piece()
                            GameValue.chess_piece_count += 1
                            # GameValue.white_chess_piece_list.append(wc)
                            GameValue.last_piece = 'white'
                            GameValue.chessboard_map[point[0]][point[1]] = 2

                            if self.check_game_over(2,point[0],point[1]):
                                GameValue.game_over = 2
                            if self.check_draw():
                                GameValue.game_over = 3

                        #inittuple6()
                        #print(evaluate(GameValue.chessboard_map))
                        
    def init_window(self):
        GameValue.window = pygame.display.set_mode((GameValue.screen_width,GameValue.screen_height))
        pygame.display.set_caption("五子棋")

    def end_game(self):
        pygame.quit()
        sys.exit()

    def set_background(self):
        background = pygame.image.load('gobang/images/back.png')
        bg_rect = background.get_rect()
        bg_rect.topleft = (0,0)
        GameValue.window.blit(background,bg_rect)

    def blit_chessboard(self):
        cb = ChessBoard()
        cb.display_chessboard()

    def check_game_over(self,piece_type,centerx,centery): #1 表示黑棋，2 表示白棋
        max_same_pieces = 1
        #检查左右方向
        x = centerx + 1
        while(x <= 15 and GameValue.chessboard_map[x][centery] == piece_type):
            max_same_pieces += 1
            x += 1
        x = centerx - 1
        while(x >= 1 and GameValue.chessboard_map[x][centery] == piece_type):
            max_same_pieces += 1
            x -= 1

        if max_same_pieces >= 5:
            return True

        max_same_pieces = 1
        #检查上下方向
        y = centery + 1
        while(y <= 15 and GameValue.chessboard_map[centerx][y] == piece_type):
            max_same_pieces += 1
            y += 1
        y = centery - 1
        while(y >= 1 and GameValue.chessboard_map[centerx][y] == piece_type):
            max_same_pieces += 1
            y -= 1

        if max_same_pieces >= 5:
            return True

        max_same_pieces = 1
        #检查左上-右下方向
        x , y = centerx - 1,centery - 1
        while(x >= 1 and y >= 1 and GameValue.chessboard_map[x][y] == piece_type):
            max_same_pieces += 1
            x -= 1
            y -= 1
        x , y = centerx + 1,centery + 1
        while(x <= 15 and y <= 15 and GameValue.chessboard_map[x][y] == piece_type):
            max_same_pieces += 1
            x += 1
            y += 1

        if max_same_pieces >= 5:
            return True

        max_same_pieces = 1
        #检查左下-右上方向
        x , y = centerx - 1,centery + 1
        while(x >= 1 and y <= 15 and GameValue.chessboard_map[x][y] == piece_type):
            max_same_pieces += 1
            x -= 1
            y += 1
        x , y = centerx + 1,centery - 1
        while(x <= 15 and y >= 1 and GameValue.chessboard_map[x][y] == piece_type):
            max_same_pieces += 1
            x += 1
            y -= 1

        if max_same_pieces >= 5:
            return True

        return False

    def check_draw(self):
        return GameValue.chess_piece_count == 225
        
    def blit_game_over_text(self):
        p = Pen(GameValue.game_over)
        p.display_text()

if __name__ == '__main__':
    mg = MainGame()
    mg.start_game()
