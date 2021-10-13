import othello_board as ob
import othello_ai as oa
import othello_draw as od
import numpy as np
#初期盤面
board1 = ob.othello_board()

player = 1
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

    #石を置く
    if board1.board_check(x, y):
        board1.reverse_stone(x, y)
        print("ok")
        
    else:
        print("ng")

    board1.bit_to_array()

    #盤面の描画
    od.draw(board1.board, player)

    #手番交代
    player = player * -1
    tmp = board1.player_board
    board1.player_board = board1.opponent_board
    board1.opponent_board = tmp
    turn = turn + 1