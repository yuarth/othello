import othello_board as ob
import othello_ai as oa
import othello_draw as od
import numpy as np

def main():
    #初期盤面
    board1 = ob.othello_board()
    turn = 0

    while(turn < 60):
        #石の置く場所
        print("x")
        x = int(input())
        while(x < 0 | x > 7):
            print("again")
            x = int(input())

        print("y")
        y = int(input())
        while(y < 0 | y > 7):
            print("again")
            y = int(input())

        put = board1.coordinate_to_bit(x,y)
        #石を置く
        if ((board1.board_check() & put) == put):
            board1.reverse_stone(put)
            print("ok")
            
        else:
            print("ng")

        board1.bit_to_board()

        #盤面の描画
        od.draw(board1.board, board1.player)

        #手番交代
        board1.player = board1.player * -1
        tmp = board1.player_board
        board1.player_board = board1.opponent_board
        board1.opponent_board = tmp
        turn = turn + 1

#pygame用
def game(board, x, y):
    #石を置く
    put = board.coordinate_to_bit(x, y)
    if not ((board.board_check() & put) == put):
        #print("ng")    
        return True
    else:
        #print("ok")
        board.reverse_stone(put)
        board.bit_to_board()
        board.turn = board.turn + 1
        #手番交代
        tmp = board.player_board
        board.player_board = board.opponent_board
        board.opponent_board = tmp
        board.player = board.player * -1
        #カウント
        board.count_stone()
        board.board_check()
        if(board.is_pass()):
            print("pass")
            tmp = board.player_board
            board.player_board = board.opponent_board
            board.opponent_board = tmp
            board.player = board.player * -1
            board.board_check()
            if(board.is_pass()):
                #print("game end")
                return False
        return True
    

if __name__	== "__main__":
    main()