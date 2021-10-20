import numpy as np
from numpy.lib.function_base import blackman


#０：候補、１：黒、−１：白、nan：なし
class othello_board:
    board = np.zeros((8,8))
    player_board = 0x0000_0008_1000_0000
    opponent_board = 0x0000_0010_0800_0000
    legal_board = 0x0000_0000_0000_0000
    player = 1
    black = 2
    white = 2
    turn = 0
    evaluate_board = np.zeros((8, 8))

    def __init__(self):    
        self.board[:,:] = np.nan
        self.player_board = 0x0000_0008_1000_0000
        self.opponent_board = 0x0000_0010_0800_0000
        self.legal_board = 0x0000_0000_0000_0000
        self.bit_to_board()
        self.player = 1
        self.black = 2
        self.white = 2
        self.turn = 0
        self.evaluate_board = [
            [15, 0, 10, 0, 0, 10, 0, 15],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [10, 0, 10, 0, 0, 10, 0, 10],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [10, 0, 10, 0, 0, 10, 0, 10],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [15, 0, 10, 0, 0, 10, 0, 15]
        ]

    def bit_to_board(self):
        tmp = 0x8000_0000_0000_0000
        for i in range(8):
            for j in range(8):
                if (tmp & self.player_board) > 0:
                    self.board[i][j] = self.player
                elif (tmp & self.opponent_board) > 0:
                    self.board[i][j] = self.player * -1
                tmp = tmp >> 1


    def reverse_stone(self, put):
        reverse_board = 0x0000_0000_0000_0000

        for i in range(8):
            rev = 0x0000_0000_0000_0000
            
            mask = self.transfer(put, i)

            while ((mask != 0) and ((mask & self.opponent_board) != 0)):
                rev |= mask
                mask = self.transfer(mask, i)

            if (mask & self.player_board) != 0 :
                reverse_board |= rev

        self.player_board ^= put | reverse_board
        self.opponent_board ^= reverse_board

    def transfer(self, put, k):
        #上
        if k == 0:
            return (put << 8) & 0xffffffffffffff00
        #右上
        elif k == 1:
            return (put << 7) & 0x7f7f7f7f7f7f7f00
        #右
        elif k == 2:
            return (put >> 1) & 0x7f7f7f7f7f7f7f7f
        #右下
        elif k == 3:
            return (put >> 9) & 0x007f7f7f7f7f7f7f
        #下
        elif k == 4:
            return (put >> 8) & 0x00ffffffffffffff
        #左下
        elif k == 5:
            return (put >> 7) & 0x00fefefefefefefe
        #左
        elif k == 6:
            return (put << 1) & 0xfefefefefefefefe
        #左上
        elif k == 7:
            return (put << 9) & 0xfefefefefefefe00
        else:
            return 0

    def count_stone(self):
        self.black = np.count_nonzero(self.board == 1)
        self.white = np.count_nonzero(self.board == -1)

    def board_check(self):
        #条件の調査

        horizontal_watch_board = self.opponent_board & 0x7e7e_7e7e_7e7e_7e7e
        vertical_watch_board = self.opponent_board & 0x00FF_FFFF_FFFF_FF00
        allside_watch_board = self.opponent_board & 0x007e_7e7e_7e7e_7e00

        blank_board = ~(self.player_board | self.opponent_board)
   
        #左
        tmp = horizontal_watch_board & (self.player_board << 1) 
        
        for i in range(5):
            tmp |= horizontal_watch_board & (tmp << 1)
            
        self.legal_board = blank_board & (tmp << 1)

        #右
        tmp = horizontal_watch_board & (self.player_board >> 1) 
        for i in range(5):
            tmp |= horizontal_watch_board & (tmp >> 1)

        self.legal_board |= blank_board & (tmp >> 1)

        #上
        tmp = vertical_watch_board & (self.player_board << 8)
        for i in range(5):
            tmp |= vertical_watch_board & (tmp << 8)

        self.legal_board |= blank_board & (tmp << 8)

        #下
        tmp = vertical_watch_board & (self.player_board >> 8)
        for i in range(5):
            tmp |= vertical_watch_board & (tmp >> 8)

        self.legal_board |= blank_board & (tmp >> 8)

        #左上
        tmp = allside_watch_board & (self.player_board << 9)
        for i in range(5):
            tmp |= allside_watch_board & (tmp << 9)

        self.legal_board |= blank_board & (tmp << 9)

        #右下
        tmp = allside_watch_board & (self.player_board >> 9)
        for i in range(5):
            tmp |= allside_watch_board & (tmp >> 9)

        self.legal_board |= blank_board & (tmp >> 9)        

        #右上
        tmp = allside_watch_board & (self.player_board << 7)
        for i in range(5):
            tmp |= allside_watch_board & (tmp << 7)

        self.legal_board |= blank_board & (tmp << 7)

        #左下
        tmp = allside_watch_board & (self.player_board >> 7)
        for i in range(5):
            tmp |= allside_watch_board & (tmp >> 7)

        self.legal_board |= blank_board & (tmp >> 7)  

        self.board = np.where(self.board == 0, np.nan, self.board)
        tmp = 0x8000_0000_0000_0000
        for i in range(8):
            for j in range(8):
                if (tmp & self.legal_board) > 0:
                    self.board[i][j] = 0
                tmp = tmp >> 1  

        return self.legal_board

    def coordinate_to_bit(self, x, y):
        put = 0x8000_0000_0000_0000
        put = put >> x
        put = put >> (y * 8)
        return put

    def return_candidate(self):
        l = self.board_check()
        tmp = 0x8000_0000_0000_0000
        a = np.zeros((8,8))
        for i in range(8):
            for j in range(8):
                if (tmp & l) > 0:
                    a[j][i] = 1
                tmp = tmp >> 1
        return a


    def is_pass(self):
        return (self.legal_board == 0x0000_0000_0000_0000)

    


def testprint(bit):
        #おける場所の表示
        tmp = 0x8000_0000_0000_0000
        tmp_array = np.zeros((8,8))
        for i in range(8):
            for j in range(8):
                if (tmp & bit) > 0:
                    tmp_array[i][j] = 1
                
                tmp = tmp >> 1
        print(tmp_array)