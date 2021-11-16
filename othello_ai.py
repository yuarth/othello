#AIの打ち筋
from math import inf
import random
import numpy as np
import othello_board as ob
import othello_main as om
import time

#評価関数

def ai_random(board):
    index = np.where(board.return_candidate() == 1)
    x_candidate_list, y_candidate_list = index
    i = random.randrange(len(x_candidate_list))
    x = x_candidate_list[i]
    y = y_candidate_list[i]
    return int(x), int(y)

def ai_put(board):
    index = np.where(board.return_candidate() == 1)
    x_candidate_list, y_candidate_list = index

    #alpha-beta法で得られた一番評価値が高いものを選択
    depth = 4
    if(board.turn >= 60 - depth):
        depth = 60 - board.turn


    predict_board = ob.othello_board()
    index = 0
    for i in range(len(x_candidate_list)):
    #for i in range(2):
        #盤面の複製
        predict_board.board = board.board
        predict_board.player_board = board.player_board
        predict_board.opponent_board = board.opponent_board
        predict_board.legal_board = board.legal_board
        
        om.game(predict_board, int(x_candidate_list[i]), int(y_candidate_list[i]))
        tmp = alphabeta(-100, 100, depth, predict_board)
        print("#########")
        print("tmp", tmp, i)
        print("#########")
        if i == 0:
            max = tmp
        if tmp > max:
            index = i

    x = x_candidate_list[index]
    y = y_candidate_list[index]
    return int(x), int(y)

#盤面評価
def ai_evaluate(board):
    predict_board = ob.othello_board()
    predict_board.board = board.board
    predict_board.player_board = board.player_board
    predict_board.opponent_board = board.opponent_board
    predict_board.legal_board = board.legal_board
    predict_board.player = board.player

    score = 0
    c = predict_board.return_candidate()
    column_list, row_list = np.where(c > 0)
    
    if(len(column_list) == 0):
            return 100 * predict_board.player
    
    #おける場所の数
    score = score + len(column_list)
    #評価値が高いおける場所
    index = 0
    max = predict_board.evaluate_board[row_list[0]][column_list[0]]
    for i in range(1, len(column_list)):  
        tmp = predict_board.evaluate_board[row_list[i]][column_list[i]]
        if tmp > max:
            max = tmp
            index = i
    score = score + max

    #盤面の石の数の差
    predict_board.count_stone()
    score = score + (predict_board.black - predict_board.white) * 10 * predict_board.player


    return score

#alpha-beta法
def alphabeta(board, alpha=inf, beta=-inf, depth=5):
    predict_board = ob.othello_board()
    
    #depth = even:相手番, odd:自番
    if depth == 0:
        e = ai_evaluate(board)
        print("evaluate:", e, "player:",predict_board.player, "depth",depth)
        return e
    c = board.return_candidate()
    column_list, row_list = np.where(c > 0)
    
    #最大値(自番)
    if board.player == 1:
        max = -inf
        if(len(column_list) == 0):
            return 100
        for i in range(len(column_list)):
            predict_board.board = board.board
            predict_board.player_board = board.player_board
            predict_board.opponent_board = board.opponent_board
            predict_board.legal_board = board.legal_board
            predict_board.player = board.player
            om.game(predict_board, int(column_list[i]), int(row_list[i]))
            tmp = alphabeta(predict_board, alpha, beta, depth-1)
            #print("alpha", tmp, "player:",predict_board.player, "depth",depth)
            print("alpha",alpha, "beta", beta)
            if tmp >= max:
                max = tmp
                alpha = max
            if alpha <= beta:
                print("break")
                break
        return alpha
    #最小値(相手番)
    else:
        min = inf
        if(len(column_list) == 0):
            return -100
        for i in range(len(column_list)):
            predict_board.board = board.board
            predict_board.player_board = board.player_board
            predict_board.opponent_board = board.opponent_board
            predict_board.legal_board = board.legal_board
            predict_board.player = board.player
            om.game(predict_board, int(column_list[i]), int(row_list[i]))
            tmp = alphabeta(predict_board, alpha, beta, depth-1)
            print("beta",beta, "alpha", alpha)
            #print("beta", tmp, "player:",predict_board.player, "depth",depth)
            if tmp <= min:
                min = tmp
                beta = min
            if alpha <= beta:
                print("break")
                break
        return beta


if __name__	== "__main__":
    board = ob.othello_board()
    score = alphabeta(board)
    print("score", score)
    #print(ai_put(board))