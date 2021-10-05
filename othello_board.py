import numpy as np


#０：なし、１：黒、−１：白
class othello_board:
    board = np.zeros((8,8))

    def __init__(self):    
        self.board[:,:] = np.nan
        self.board[3, 3] = -1
        self.board[4, 4] = -1
        self.board[3, 4] = 1
        self.board[4, 3] = 1

    def put_stone(self, x, y, player):
        self.board[x, y] = player

    def revearse_stone(self):
        self.board


    def board_check(self, x, y, player):
        #条件の調査
        #すでに石が置かれていないか
        if (self.board[x, y] != -1) | (self.board[x, y] != 1):
            check1 = True
        else:
            check1 = False

        #挟める位置に置いているか
        check_x = x
        check_y = y
        upper = False
        upper_right = False
        right = False
        lower_right = False
        bellow = False
        lower_left = False
        left = False
        upper_left = False

        #上
        while(check_y > 0):
            if self.board[x, check_y - 1] == player * -1:
                upper = True

            elif (upper == True) & (self.board[x, check_y - 1] == player):
                upper_able = True
                break
            else:
                upper_able = False
                break
            check_y = check_y - 1
        #右上
        while(check_y > 0 & check_x < 7):
            if self.board[x+1, y-1] == player * -1:
                upper_right = True

            elif (upper == True) & (self.board[check_x + 1, check_y - 1] == player):
                upper_right_able = True
                break
            else:
                upper_right_able = False
                break
            check_y = check_y - 1
            check_x = check_x + 1

        #右
        if self.board[x+1, y] == player * -1:
            right = True

        #右下
        if self.board[x+1, y+1] == player * -1:
            lower_right = True

        #下
        if self.board[x, y+1] == player * -1:
            bellow = True

        #左下
        if self.board[x-1, y+1] == player * -1:
            lower_left = True

        #左
        if self.board[x-1, y] == player * -1:
            left = True

        #左上
        if self.board[x-1, y-1] == player * -1:
            upper_left = True


    
        check2 = True

        if check1 and check2:
            return True
        else:
            return False


