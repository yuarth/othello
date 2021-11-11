#自動でAI同士の対戦を進める
import othello_main as om
import othello_board as ob
import othello_ai as oa
import time
import sqlite3
import numpy as np

start = time.time()

#試合数
auto_games = 10000000000

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
        game_record = {}
        #ゲームの開始
        while flag:    
            #db記録用
            candidate_list = []
            weight_list = []
            input_data = []
            #棋譜
            

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
            game_record[str(x) + str(y)] = id
            
        print("black", board.black, "white", board.white)
        if board.black > board.white:
            winner = 1
        else:
            winner = -1
        db_update(game_record, winner)
        

    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    #db_read()
    con.close()	

def db_insert(insert_data):
    try:
        cur.execute("""
        create table IF NOT EXISTS OTHELLOBOARD (
            ID integer primary key,
            BOARDBLACK varchar(256),
            BOARDWHITE varchar(256),
            CANDIDATE LIST,
            WEIGHT LIST
            );
            """)

        cur.execute('SELECT * FROM OTHELLOBOARD WHERE BOARDBLACK = ? and BOARDWHITE = ?', (insert_data[0], insert_data[1],))
        rows = cur.fetchall()		# 検索結果をリストとして取得
        if not rows:
            cur.execute('INSERT INTO OTHELLOBOARD (BOARDBLACK, BOARDWHITE, CANDIDATE, WEIGHT) VALUES(?, ?, ?, ?)', insert_data)

        for row in cur.execute('SELECT * FROM OTHELLOBOARD WHERE BOARDBLACK = ? and BOARDWHITE = ?', (insert_data[0], insert_data[1],)):
            id = row[0]
        return id

    except sqlite3.Error as e:		# エラー処理
        print("Error occurred:", e.args[0])
    
    con.commit()					# データベース更新の確定


def db_read():
    db_path = "othellodb.db"			# データベースファイル名を指定
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)	# データベースに接続
    cur = con.cursor()	
    for row in cur.execute('SELECT * FROM OTHELLOBOARD'):
        print(row)
        #for item in row:
            #print(f'{str(type(item)):15}:{item}')
    con.close()	


def db_update(game_record, winner):
    
    count = 1
    candidate = []
    weight = []
    values = list(game_record.keys())
    keys = list(game_record.values())
    count = 1
    for i in keys:
        id = str(i)
        for row in cur.execute('SELECT * FROM OTHELLOBOARD WHERE ID = ?', (id,)):
            #print(row)
            tmp = 0
            for item in row:                    
                if(tmp == 3):
                    if(item == None):
                        tmp_dict = None
                        break
                    if len(item[0]) == 1:
                        item = ['0' + item[0]]
                    candidate = item
                if(tmp == 4):
                    weight = item
                tmp = tmp + 1
            
            else:
                tmp_dict = dict(zip(candidate, weight))
        if len(keys) - count == 0:
            break
        if tmp_dict != None:
            try:
                if count % 2 == 1:
                    tmp_dict[values[count]] = str(int(tmp_dict[values[count]]) + count * winner)
                else:
                    tmp_dict[values[count]] = str(int(tmp_dict[values[count]]) - count * winner)
                weight = list(tmp_dict.values())
            except:
                print(tmp_dict)
                print(values[count])
                print(count)
        try:
            cur.execute('UPDATE OTHELLOBOARD SET WEIGHT = ? WHERE ID = ?', (weight, id,))
        except sqlite3.Error as e:		# エラー処理
            print("Error occurred:", e.args[0])
        count = count + 1
        con.commit()

if __name__	== "__main__":
    main()
    db_read()