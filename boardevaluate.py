'''
    实现棋局评估、落子模拟并返回最佳落子位置
'''


import pygame
from game_value import GameValue
import copy

# 大写均表示白棋（AI）行为对应的分数，小写均表示黑棋（玩家）行为对应的分数

WU = 1  # 1000000
HUOSI = 2  # 50000
CHONGSI = 3  # 400
HUOSAN = 4  # 400
MIANSAN = 5  # 20
HUOER = 6  # 20
MIANER = 7  # 1
HUOYI = 8  # 1

wu = 9  # -10000000
huosi = 10  # -100000
chongsi = 11  # -100000
huosan = 12  # -8000
miansan = 13  # -50
huoer = 14  # -50
mianer = 15  # -3
huoyi = 16  # -3

weights = [0, 1000000, 50000, 400, 400, 20, 20, 1, 1, -
           10000000, -100000, -100000, -8000, -50, -50, -3, -3]

# 0无子，1黑子，2白子，3边界
tuple6type = [[[[[[0, 0, 0, 0] for a in range(4)] for b in range(
    4)] for c in range(4)] for d in range(4)] for e in range(4)]


#pos_score = [[(10*(8 - max(abs(x - 8), abs(y - 8)))) for x in range(16)] for y in range(16)]


def inittuple6():
    # 白连5,ai赢
    tuple6type[2][2][2][2][2][2] = WU
    tuple6type[2][2][2][2][2][0] = WU
    tuple6type[0][2][2][2][2][2] = WU
    tuple6type[2][2][2][2][2][1] = WU
    tuple6type[1][2][2][2][2][2] = WU
    tuple6type[3][2][2][2][2][2] = WU  # 边界考虑
    tuple6type[2][2][2][2][2][3] = WU
    # 黑连5,ai输
    tuple6type[1][1][1][1][1][1] = wu
    tuple6type[1][1][1][1][1][0] = wu
    tuple6type[0][1][1][1][1][1] = wu
    tuple6type[1][1][1][1][1][2] = wu
    tuple6type[2][1][1][1][1][1] = wu
    tuple6type[3][1][1][1][1][1] = wu
    tuple6type[1][1][1][1][1][3] = wu
    # 白活4
    tuple6type[0][2][2][2][2][0] = HUOSI
    # 黑活4
    tuple6type[0][1][1][1][1][0] = huosi
    # 白活3
    tuple6type[0][2][2][2][0][0] = HUOSAN
    tuple6type[0][0][2][2][2][0] = HUOSAN
    tuple6type[0][2][0][2][2][0] = HUOSAN
    tuple6type[0][2][2][0][2][0] = HUOSAN
    # 黑活3
    tuple6type[0][1][1][1][0][0] = huosan
    tuple6type[0][0][1][1][1][0] = huosan
    tuple6type[0][1][0][1][1][0] = huosan
    tuple6type[0][1][1][0][1][0] = huosan
    # 白活2
    tuple6type[0][2][2][0][0][0] = HUOER
    tuple6type[0][2][0][2][0][0] = HUOER
    tuple6type[0][2][0][0][2][0] = HUOER
    tuple6type[0][0][2][2][0][0] = HUOER
    tuple6type[0][0][2][0][2][0] = HUOER
    tuple6type[0][0][0][2][2][0] = HUOER
    # 黑活2
    tuple6type[0][1][1][0][0][0] = huoer
    tuple6type[0][1][0][1][0][0] = huoer
    tuple6type[0][1][0][0][1][0] = huoer
    tuple6type[0][0][1][1][0][0] = huoer
    tuple6type[0][0][1][0][1][0] = huoer
    tuple6type[0][0][0][1][1][0] = huoer
    # 白活1
    tuple6type[0][2][0][0][0][0] = HUOYI
    tuple6type[0][0][2][0][0][0] = HUOYI
    tuple6type[0][0][0][2][0][0] = HUOYI
    tuple6type[0][0][0][0][2][0] = HUOYI
    # 黑活1
    tuple6type[0][1][0][0][0][0] = huoyi
    tuple6type[0][0][1][0][0][0] = huoyi
    tuple6type[0][0][0][1][0][0] = huoyi
    tuple6type[0][0][0][0][1][0] = huoyi

    x = 0
    y = 0
    ix = 0
    iy = 0  # x:左5中黑个数,y:左5中白个数,ix:右5中黑个数,iy:右5中白个数
    for p1 in range(4):
        for p2 in range(3):
            for p3 in range(3):
                for p4 in range(3):
                    for p5 in range(3):
                        for p6 in range(4):
                            x = y = ix = iy = 0

                            if(p1 == 1):
                                x += 1
                            elif(p1 == 2):
                                y += 1

                            if(p2 == 1):
                                x += 1
                                ix += 1
                            elif(p2 == 2):
                                y += 1
                                iy += 1

                            if(p3 == 1):
                                x += 1
                                ix += 1
                            elif(p3 == 2):
                                y += 1
                                iy += 1

                            if(p4 == 1):
                                x += 1
                                ix += 1
                            elif(p4 == 2):
                                y += 1
                                iy += 1

                            if(p5 == 1):
                                x += 1
                                ix += 1
                            elif(p5 == 2):
                                y += 1
                                iy += 1

                            if(p6 == 1):
                                ix += 1
                            elif(p6 == 2):
                                iy += 1

                            if(p1 == 3 or p6 == 3):  # 有边界
                                if(p1 == 3 and p6 != 3):  # 左边界
                                    # 白冲4
                                    if(ix == 0 and iy == 4):  # 若右边有空位是活4也没关系，因为活4权重远大于冲4，再加上冲4权重变化可以不计
                                        if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                            tuple6type[p1][p2][p3][p4][p5][p6] = CHONGSI

                                    # 黑冲4
                                    if(ix == 4 and iy == 0):
                                        if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                            tuple6type[p1][p2][p3][p4][p5][p6] = chongsi

                                    # 白眠3
                                    if(ix == 0 and iy == 3):
                                        if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                            tuple6type[p1][p2][p3][p4][p5][p6] = MIANSAN

                                    # 黑眠3
                                    if(ix == 3 and iy == 0):
                                        if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                            tuple6type[p1][p2][p3][p4][p5][p6] = miansan

                                    # 白眠2
                                    if(ix == 0 and iy == 2):
                                        if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                            tuple6type[p1][p2][p3][p4][p5][p6] = MIANER

                                    # 黑眠2
                                    if(ix == 2 and iy == 0):
                                        if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                            tuple6type[p1][p2][p3][p4][p5][p6] = mianer

                                elif(p6 == 3 and p1 != 3):  # 右边界
                                    # 白冲4
                                    if(x == 0 and y == 4):
                                        if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                            tuple6type[p1][p2][p3][p4][p5][p6] = CHONGSI

                                    # 黑冲4
                                    if(x == 4 and y == 0):
                                        if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                            tuple6type[p1][p2][p3][p4][p5][p6] = chongsi

                                    # 黑眠3
                                    if(x == 3 and y == 0):
                                        if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                            tuple6type[p1][p2][p3][p4][p5][p6] = miansan

                                    # 白眠3
                                    if(x == 0 and y == 3):
                                        if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                            tuple6type[p1][p2][p3][p4][p5][p6] = MIANSAN

                                    # 黑眠2
                                    if(x == 2 and y == 0):
                                        if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                            tuple6type[p1][p2][p3][p4][p5][p6] = mianer

                                    # 白眠2
                                    if(x == 0 and y == 2):
                                        if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                            tuple6type[p1][p2][p3][p4][p5][p6] = MIANER

                            else:  # 无边界
                                # 白冲4
                                if((x == 0 and y == 4) or (ix == 0 and iy == 4)):
                                    if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                        tuple6type[p1][p2][p3][p4][p5][p6] = CHONGSI

                                # 黑冲4
                                if((x == 4 and y == 0) or (ix == 4 and iy == 0)):
                                    if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                        tuple6type[p1][p2][p3][p4][p5][p6] = chongsi

                                # 白眠3
                                if((x == 0 and y == 3) or (ix == 0 and iy == 3)):
                                    if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                        tuple6type[p1][p2][p3][p4][p5][p6] = MIANSAN

                                # 黑眠3
                                if((x == 3 and y == 0) or (ix == 3 and iy == 0)):
                                    if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                        tuple6type[p1][p2][p3][p4][p5][p6] = miansan

                                # 白眠2
                                if((x == 0 and y == 2) or (ix == 0 and iy == 2)):
                                    if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                        tuple6type[p1][p2][p3][p4][p5][p6] = MIANER

                                # 黑眠2
                                if((x == 2 and y == 0) or (ix == 2 and iy == 0)):
                                    if(tuple6type[p1][p2][p3][p4][p5][p6] == 0):
                                        tuple6type[p1][p2][p3][p4][p5][p6] = mianer


inittuple6()

def evaluate(board):
    '''棋局评估'''
    A = [[0 for i in range(17)] for j in range(17)]
    for i in range(17):
        A[i][0] = 3
        A[i][16] = 3
        A[0][i] = 3
        A[16][i] = 3

    for i in range(1, 16):
        for j in range(1, 16):
            A[i][j] = board[i][j]

    stats = [0 for i in range(17)]  # 存储各状态数量

    for i in range(1, 16):
        for j in range(12):
            type = tuple6type[A[i][j]][A[i][j+1]][A[i]
                                                  [j+2]][A[i][j+3]][A[i][j+4]][A[i][j+5]]
            stats[type] += 1

    for j in range(1, 16):
        for i in range(12):
            type = tuple6type[A[i][j]][A[i+1][j]][A[i+2]
                                                  [j]][A[i+3][j]][A[i+4][j]][A[i+5][j]]
            stats[type] += 1

    for i in range(12):
        for j in range(12):
            type = tuple6type[A[i][j]][A[i+1][j+1]][A[i+2]
                                                    [j+2]][A[i+3][j+3]][A[i+4][j+4]][A[i+5][j+5]]
            stats[type] += 1

    for i in range(12):
        for j in range(5, 17):
            type = tuple6type[A[i][j]][A[i+1][j-1]][A[i+2]
                                                    [j-2]][A[i+3][j-3]][A[i+4][j-4]][A[i+5][j-5]]
            stats[type] += 1

    score = 0
    for i in range(1, 17):
        score += stats[i] * weights[i]
    return score

minnum = float('-inf') #初始 alpha 值
maxnum = float('inf') #初始 beta 值
def analyse(board,depth,alpha,beta,maxdepth = 4):
    '''利用极大极小搜索与alpha-beta剪枝实现给定深度的搜索，返回最佳评估值和最佳落点'''
    best_point = [0,0]
    if depth > maxdepth:
        return evaluate(board),best_point
    curvalue = 0
    possible_points = seek_points(board,depth)
    for p in possible_points:
        copy_board = copy.deepcopy(board)
        if depth % 2 != 0:
            copy_board[p[0]][p[1]] = 2
            curvalue,t = analyse(copy_board,depth+1,alpha,beta,maxdepth)
            copy_board[p[0]][p[1]] = 0
            if curvalue > alpha:
                alpha = curvalue
                best_point = [p[0],p[1]]
            if alpha >= beta:
                return alpha,best_point
        else:
            copy_board[p[0]][p[1]] = 1
            curvalue,t = analyse(copy_board,depth+1,alpha,beta,maxdepth)
            copy_board[p[0]][p[1]] = 0
            if curvalue < beta:
                beta = curvalue
                best_point = [p[0],p[1]]
            if alpha >= beta:
                return beta,best_point
    if depth % 2 != 0:
        return alpha,best_point
    else:
        return beta,best_point
    
def seek_points(board,depth):
    '''
        利用局部搜索和静态评价启发，将每一次搜索的点的个数缩小为10，以减少搜索时间
        返回一个有10个点的列表，每个点为一列表，格式为 [x,y]

        在此函数中，应特别注意depth的影响，做好分类讨论
    '''
    copyboard = copy.deepcopy(board) #对于多维列表，需使用此方式深拷贝，否则会无意修改原列表的值
    points = [] #存储预估10个最佳落点
    is_possible = [[0 for i in range(16)] for j in range(16)] #存储可能可以落子的位置，1 表示有可能落子

    #根据深度初始化worth列表
    if depth % 2 != 0:
        worth = [[minnum for i in range(16)] for j in range(16)]
    else:
        worth = [[maxnum for i in range(16)] for j in range(16)]

    #以每个有子点为中心，上下、左右、左斜、右斜四个方向各延申三格，设为可能落子点
    for i in range(1,16):
        for j in range(1,16):
            if board[i][j] != 0:
                for k in range(-3,4):
                    if 0 < i+k < 16:
                        is_possible[i+k][j] = 1
                    if 0 < j+k < 16:
                        is_possible[i][j+k] = 1
                    if 0 < i+k < 16 and 0 < j+k < 16:
                        is_possible[i+k][j+k] = 1
                    if 0 < i+k < 16 and 0 < j-k < 16:
                        is_possible[i+k][j-k] = 1

    #用棋局评估函数评估每个可能落子点，并将结果存储在worth中。
    #由于在设置可能落子点时未考虑该点是否已存在棋子，故此处应添加 board[i][j] == 0 的判断
    for i in range(1,16):
        for j in range(1,16):
            if board[i][j] == 0 and is_possible[i][j] == 1:
                if depth % 2 != 0:
                    copyboard[i][j] = 2
                    worth[i][j] = evaluate(copyboard)
                else:
                    copyboard[i][j] = 1
                    worth[i][j] = evaluate(copyboard)
                copyboard[i][j] = 0

    #根据depth选取worth中评估值最高或最低的10个点，并按从优到劣的顺序填充入points列表，以实现更快剪枝
    if depth % 2 != 0:
        for k in range(10):
            w = minnum
            best_point = [0,0]
            for i in range(1,16):
                for j in range(1,16):
                    if worth[i][j] > w:
                        w = worth[i][j]
                        best_point = [i,j]

            points.append(best_point)
            worth[best_point[0]][best_point[1]] = minnum

    else:
        for k in range(10):
            w = maxnum
            best_point = [0,0]
            for i in range(1,16):
                for j in range(1,16):
                    if worth[i][j] < w:
                        w = worth[i][j]
                        best_point = [i,j]

            points.append(best_point)
            worth[best_point[0]][best_point[1]] = maxnum

    return points

#测试用代码
# board = [[0 for i in range(16)] for j in range(16)]
# board[8][8] = 1
#print(seek_points(board,1))
# value,point = analyse(board,1,minnum,maxnum)
# print(value,point)

#该文件参考自 https://blog.csdn.net/livingsu/article/details/104539741
#            https://blog.csdn.net/livingsu/article/details/104544562