import sys
import pygame
import random
from time import sleep
from game_value import GameValue
from chessboard import ChessBoard
from intersection import *
from chess_piece import *
from pen import Pen
from boardevaluate import *
from menu import *
from redspot import *

inittuple6()

class MainGame:
    def __init__(self):
        pass
    def start_game(self):
        pygame.init()
        m = Menu()
        if GameValue.game_start == 0:
            while GameValue.game_start == 0:
                m.show_menu()
                self.get_events()
                pygame.display.update()
        self.init_game()
        if GameValue.game_mode == 3:
            self.init_ai_vs_ai()
        while True:
            sleep(0.02)
            self.get_events()
            self.blit_chess_pieces()#红点一经创建便无法删除，所以只能通过每次画棋子来覆盖掉原来的红点
            self.blit_redspot()
            if GameValue.game_over:
                self.blit_game_over_text()
            else:
                if GameValue.game_mode == 3:
                    self.ai_vs_ai()

            pygame.display.update()

    def init_game(self):
        self.init_window()
        #GameValue.window.fill((1,77,103))
        self.set_background()
        self.blit_chessboard()
        create_intersections()
    
    def restart_game(self): #在当前模式下重新开始游戏
        GameValue.intersection_list = []
        GameValue.chess_piece_list = []
        GameValue.last_piece = 'white'
        GameValue.chess_piece_count = 0
        GameValue.chessboard_map = [[0 for i in range(16)] for j in range(16)]
        GameValue.game_over = 0
        GameValue.last_point = [-5,-5]
        self.init_game()

    def go_back_to_menu(self):#返回主菜单
        GameValue.intersection_list = []
        GameValue.chess_piece_list = []
        GameValue.last_piece = 'white'
        GameValue.chess_piece_count = 0
        GameValue.chessboard_map = [[0 for i in range(16)] for j in range(16)]
        GameValue.game_over = 0
        GameValue.game_start = 0
        GameValue.last_point = [-5,-5]
        m = Menu()
        if GameValue.game_start == 0:
            while GameValue.game_start == 0:
                m.show_menu()
                self.get_events()
                pygame.display.update()
        self.init_game()
        if GameValue.game_mode == 3:
            self.init_ai_vs_ai()


        
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end_game()  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.end_game()
                elif event.key == pygame.K_r:
                    self.restart_game()
                elif event.key == pygame.K_p:
                    self.go_back_to_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN and GameValue.game_over == 0:
                if GameValue.game_start == 0:
                    for i in range(len(GameValue.button_list)):
                        mouse_pos = pygame.mouse.get_pos()
                        if GameValue.button_list[i].check_click(mouse_pos):
                            GameValue.game_start = 1
                            GameValue.game_mode = i + 1


                if GameValue.game_mode == 1:
                    self.pvp()
                elif GameValue.game_mode == 2:
                    self.pve()

                        
    def init_window(self):
        GameValue.window = pygame.display.set_mode((GameValue.screen_width,GameValue.screen_height))
        pygame.display.set_caption("五子棋")

    def end_game(self):
        pygame.quit()
        sys.exit()

    def set_background(self):
        background = pygame.image.load('images/back.png')
        bg_rect = background.get_rect()
        bg_rect.topleft = (0,0)
        GameValue.window.blit(background,bg_rect)

    def blit_chessboard(self):
        cb = ChessBoard()
        cb.display_chessboard()

    def blit_chess_pieces(self):
        for cp in GameValue.chess_piece_list:
            cp.display_chess_piece()

    def blit_redspot(self): #追踪最后一次下棋位置
        rs = RedSpot(GameValue.last_point)
        rs.display_redspot()
        

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

    def check_draw(self): #检查是否和棋
        return GameValue.chess_piece_count == 225
        
    def blit_game_over_text(self):
        p = Pen(GameValue.game_over)
        p.display_text()


    def init_ai_vs_ai(self): #随机设置黑棋第一点和白棋第一点，以便使 ai vs ai 的棋局富于变化性
        x1 = random.randint(1,15)
        y1 = random.randint(1,15)
        x2 = random.randint(1,15)
        y2 = random.randint(1,15)
        GameValue.chessboard_map[x1][y1] = 1
        GameValue.chessboard_map[x2][y2] = 2
        ChessPiece('black',(x1*60-30,y1*60-30)).display_chess_piece()
        ChessPiece('white',(x2*60-30,y2*60-30)).display_chess_piece()
        GameValue.chess_piece_count = 2

    def ai_vs_ai(self):
        minnum = float('-inf')
        maxnum = float('inf')
        value1,point1 = analyse(GameValue.chessboard_map,1,minnum,maxnum,2)
        GameValue.AI1_pos[0] = point1[0] * 60 - 30
        GameValue.AI1_pos[1] = point1[1] * 60 - 30
        GameValue.last_point = GameValue.AI1_pos
        bc = ChessPiece('black',GameValue.AI1_pos)
        bc.display_chess_piece()
        GameValue.chess_piece_list.append(bc)
        GameValue.chess_piece_count += 1
        pygame.display.update()
        GameValue.last_piece = 'black'
        GameValue.chessboard_map[point1[0]][point1[1]] = 1
        if self.check_game_over(1,point1[0],point1[1]):
            GameValue.game_over = 1
            return
        if self.check_draw():
            GameValue.game_over = 3
            return

        value2,point2 = analyse(GameValue.chessboard_map,1,minnum,maxnum,4)
        GameValue.AI2_pos[0] = point2[0] * 60 - 30
        GameValue.AI2_pos[1] = point2[1] * 60 - 30
        GameValue.last_point = GameValue.AI2_pos
        wc = ChessPiece('white',GameValue.AI2_pos)
        wc.display_chess_piece()
        GameValue.chess_piece_list.append(wc)
        GameValue.chess_piece_count += 1
        pygame.display.update()
        GameValue.last_piece = 'white'
        GameValue.chessboard_map[point2[0]][point2[1]] = 2
        if self.check_game_over(2,point2[0],point2[1]):
            GameValue.game_over = 2
        if self.check_draw():
            GameValue.game_over = 3

        sleep(1)

    def pvp(self): #模式一 ： 玩家对玩家
        mouse_pos = pygame.mouse.get_pos()
        x = (mouse_pos[0] + 45) // 60
        y = (mouse_pos[1] + 45) // 60
        for intersection in GameValue.intersection_list:
            if intersection.rect.collidepoint(mouse_pos) and GameValue.chessboard_map[x][y] == 0:
                if GameValue.last_piece == 'white':
                    bc = ChessPiece('black',intersection.rect.center)
                    bc.display_chess_piece() #该行实现点击鼠标后立刻显示黑棋，而不是等到AI算完后再一起显示
                    GameValue.chess_piece_list.append(bc)
                    GameValue.last_point[0] = intersection.rect.center[0]
                    GameValue.last_point[1] = intersection.rect.center[1]
                    GameValue.chess_piece_count += 1
                    pygame.display.update()
                    GameValue.last_piece = 'black'
                    GameValue.chessboard_map[x][y] = 1

                    if self.check_game_over(1,x,y):
                        GameValue.game_over = 1
                        break
                    if self.check_draw():
                        GameValue.game_over = 3

                else:
                    wc = ChessPiece('white',intersection.rect.center)
                    wc.display_chess_piece()
                    GameValue.chess_piece_list.append(wc)
                    GameValue.last_point[0] = intersection.rect.center[0]
                    GameValue.last_point[1] = intersection.rect.center[1]
                    GameValue.chess_piece_count += 1
                    GameValue.last_piece = 'white'
                    GameValue.chessboard_map[x][y] = 2

                    if self.check_game_over(2,x,y):
                        GameValue.game_over = 2
                    if self.check_draw():
                        GameValue.game_over = 3

    def pve(self): #模式二 ：玩家对电脑
        mouse_pos = pygame.mouse.get_pos()
        x = (mouse_pos[0] + 45) // 60
        y = (mouse_pos[1] + 45) // 60
        for intersection in GameValue.intersection_list:
            if intersection.rect.collidepoint(mouse_pos) and GameValue.chessboard_map[x][y] == 0:
                bc = ChessPiece('black',intersection.rect.center)
                bc.display_chess_piece() #该行实现点击鼠标后立刻显示黑棋，而不是等到AI算完后再一起显示
                GameValue.chess_piece_count += 1
                pygame.display.update()
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

                sleep(1)
                wc = ChessPiece('white',GameValue.AI_pos)
                wc.display_chess_piece()
                GameValue.chess_piece_list.append(wc)
                GameValue.last_point = GameValue.AI_pos
                GameValue.chess_piece_count += 1
                GameValue.last_piece = 'white'
                GameValue.chessboard_map[point[0]][point[1]] = 2

                if self.check_game_over(2,point[0],point[1]):
                    GameValue.game_over = 2
                if self.check_draw():
                    GameValue.game_over = 3

    def eve(self):
        pass
        

if __name__ == '__main__':
    mg = MainGame()
    mg.start_game()
