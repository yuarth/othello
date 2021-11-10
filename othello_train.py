#自動でAI同士の対戦を進める
import othello_main as om
import othello_board as ob
import othello_ai as oa
import time
import sqlite3
import numpy as np

start = time.time()

#試合数
auto_games = 1

#db接続
sqlite3.register_adapter(list, lambda l: ';'.join([str(i) for i in l]))
sqlite3.register_converter('LIST', lambda s: [item.decode('utf-8')  for item in s.split(bytes(b';'))])
db_path = "othellodb.db"			# データベースファイル名を指定
con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)	# データベースに接続
cur = con.cursor()	

def main():
    for i in range(auto_games):
        board = ob.othello_board()
        flag = True

        #ゲームの開始
        while flag:    
            #db記録用
            candidate_list = []
            weight_list = []
            input_data = []
            #棋譜
            game_record = {}

            #置く位置の取得
            if board.player == 1:
                x, y = oa.ai_random(board)
            else:
                #x, y = oa.ai_put(board)
                x, y = oa.ai_random(board)

            print(board.turn)
            flag = om.game(board, x, y)
            if(board.player == 1):
                input_data.append(str(board.player_board))
                input_data.append(str(board.opponent_board))
            else:
                input_data.append(str(board.opponent_board))
                input_data.append(str(board.player_board))
                
            c_x, c_y = np.where(board.return_candidate())
            for i in range(len(c_x)):
                tmp_candidate = str(c_x[i]) + str(c_y[i])
                candidate_list.append(tmp_candidate)
            weight_list = [0 for i in range(len(candidate_list))]
            
        
            #結果の保存
            input_data.append(candidate_list)
            input_data.append(weight_list)

            id = db_insert(input_data)
            game_record[id] = str(x) + str(y)

        db_update(game_record)
        print("black", board.black, "white", board.white)

    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    #db_read()
    con.close()	

def db_insert(insert_data):
    try:
        cur.execute("""
        create table IF NOT EXISTS OTHELLOBOARD (
            ID integer primary key autoincrement,
            BOARDBLACK varchar(256),
            BOARDWHITE varchar(256),
            CANDIDATE LIST,
            WEIGHT LIST
            );
            """)

        cur.execute('SELECT * FROM OTHELLOBOARD WHERE BOARDBLACK = ? and BOARDWHITE = ?', (insert_data[0], insert_data[1]))
        rows = cur.fetchall()		# 検索結果をリストとして取得
        if not rows:				# リストが空のとき
            cur.execute('INSERT INTO OTHELLOBOARD (BOARDBLACK, BOARDWHITE, CANDIDATE, WEIGHT) VALUES(?, ?, ?, ?)', insert_data)

        cur.execute('SELECT * FROM OTHELLOBOARD WHERE BOARDBLACK = ? and BOARDWHITE = ?', (insert_data[0], insert_data[1]))
        rows = cur.fetchall()
        return rows[0]

    except sqlite3.Error as e:		# エラー処理
        print("Error occurred:", e.args[0])
    
    con.commit()					# データベース更新の確定


def db_read():
    for row in cur.execute('SELECT * FROM OTHELLOBOARD'):
        print(row)
        for item in row:
            print(f'{str(type(item)):15}:{item}')



def db_update(game_record):
    for key, value in game_record:
        cur.execute('SELECT * FROM OTHELLOBOARD WHERE ID = ?', )
        rows = cur.fetchall()		# 検索結果をリストとして取得
        candidate = rows[3]
        weight = rows[4]
        tmp_dict = dict(zip(candidate, weight))

        try:
            cur.execute('UPDATE OTHELLOBOARD SET WEIGHT = ? WHERE ID = ?', (weight, id))
        except sqlite3.Error as e:		# エラー処理
            print("Error occurred:", e.args[0])


if __name__	== "__main__":
    main()
    