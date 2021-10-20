#オセロの盤面の描画
from pygame.locals import *
import pygame as pg
import sys
import othello_main as om
import othello_board as ob
import othello_ai as oa
def draw(array):
    print(array)

def window():
    pg.init()
    flag = True
    window_width = 960
    window_height = 720

    #スクリーンサイズを設定
    screen = pg.display.set_mode((window_width, window_height))	
    screen.fill((255, 255, 255), (0, 0, window_width, window_height))

    #タイトルの設定
    pg.display.set_caption("オセロ")	

    font1 = pg.font.SysFont(None, 30)
    text1 = font1.render("White:", True, (0,0,0))
    text2 = font1.render("black:", True, (0,0,0))
    screen.blit(text1, (10,10))
    screen.blit(text2, (200,10))

    screen.fill((0,255,0),(20,80, 640, 640))
    color = (0, 0, 0)
    for i in range(9):
        pg.draw.line(screen, color, (i*80+20, 80), (i*80+20, window_height))
        pg.draw.line(screen, color, (20, i*80+80), (660, i*80+80))

    #オセロボードのインスタンス
    board = ob.othello_board()
    board.return_candidate()

    text3 = font1.render(str(board.white), True, (0,0,0))
    text4 = font1.render(str(board.black), True, (0,0,0))
    screen.blit(text3, (110,10))
    screen.blit(text4, (300,10))
    
    for i in range(8):
        for j in range(8):
            if(board.board[i][j] == -1):
                pg.draw.circle(screen, (255, 255, 255), (i * 80 + 60, j * 80 + 120), 35, width = 0)
            elif(board.board[i][j] == 1):
                pg.draw.circle(screen, (0, 0, 0), (i * 80 + 60, j * 80 + 120), 35, width = 0)
            elif(board.board[i][j] == 0):
                pg.draw.circle(screen, (10, 10, 10), (j * 80 + 60, i * 80 + 120), 10, width = 0)

    while(1):
        for event in pg.event.get():	
            if event.type == pg.QUIT:		
                pg.quit()		
                sys.exit(0)	
        
            # マウスクリック時の動作
            if event.type == MOUSEBUTTONDOWN:
                #再描画
                screen.fill((255, 255, 255), (0, 0, window_width, window_height))
                screen.blit(text1, (10,10))
                screen.blit(text2, (200,10))

                screen.fill((0,255,0),(20,80, 640, 640))
                color = (0, 0, 0)
                for i in range(9):
                    pg.draw.line(screen, color, (i*80+20, 80), (i*80+20, window_height))
                    pg.draw.line(screen, color, (20, i*80+80), (660, i*80+80))

                #場所の取得
                x, y = event.pos
                x = int((x - 20) / 80)
                y = int((y - 80) / 80)
                
                #ゲームの実行
                flag = om.game(board, x, y)
                x, y = oa.ai_put(board)
                flag = om.game(board, x, y)
                print(board.board)

                #石の数の表示
                text3 = font1.render(str(board.white), True, (0,0,0))
                text4 = font1.render(str(board.black), True, (0,0,0))
                screen.blit(text3, (110,10))
                screen.blit(text4, (300,10))

                
                #円の描画
                for i in range(8):
                    for j in range(8):
                        if(board.board[i][j] == -1):
                            pg.draw.circle(screen, (255, 255, 255), (j * 80 + 60, i * 80 + 120), 40, width = 0)
                        elif(board.board[i][j] == 1):
                            pg.draw.circle(screen, (0, 0, 0), (j * 80 + 60, i * 80 + 120), 40, width = 0)
                        elif(board.board[i][j] == 0):
                            pg.draw.circle(screen, (10, 10, 10), (j * 80 + 60, i * 80 + 120), 10, width = 0)
                
                
        
        pg.display.update()
        
        

        if(not flag):
            while(1):
                for event in pg.event.get():	
                    if event.type == pg.QUIT:		
                        pg.quit()		
                        sys.exit(0)	

    print("finish")	


if __name__	== "__main__":
    window()