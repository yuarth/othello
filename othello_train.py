#自動でAI同士の対戦を進める
import othello_main as om
import othello_board as ob
import othello_ai as oa
import time

start = time.time()

#試合数
auto_games = 1

for i in range(auto_games):
    board = ob.othello_board()
    flag = True
    while flag:    
        #置く位置の取得
        #x, y = oa.ai_random(board)
        x, y = oa.ai_put(board)
        print(board.turn)
        flag = om.game(board, x, y)
    #結果の保存

    print("black", board.black, "white", board.white)

elapsed_time = time.time() - start
print("elapsed_time:{0}".format(elapsed_time) + "[sec]")