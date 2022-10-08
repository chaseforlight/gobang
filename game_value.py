class GameValue:
    window = None
    screen_width = 900
    screen_height = 900
    intersection_list = []
    # white_chess_piece_list = []
    # black_chess_piece_list = []
    last_piece = 'white'
    chess_piece_count = 0 #以便判断是否和棋
    chessboard_map = [[0 for i in range(16)] for j in range(16)]
    #行指标从1 到 15，列指标从1 到 15
    # 0 表示没有棋子，1 表示有黑棋， 2 表示有白棋 

    game_over = 0 #0 即没有结束，1 为黑棋赢，2 为白棋赢

    AI_pos = [0,0]
