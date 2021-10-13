#オセロの盤面の描画
from pygame.locals import *
import pygame as pg
import sys

def draw(array, player):
    array = array * player
    print(array)

def window():
    pg.init()

    window_width = 960
    window_height = 720

    #スクリーンサイズを設定
    screen = pg.display.set_mode((window_width, window_height))	
    screen.fill((255, 255, 255), (0, 0, window_width, window_height))

    #タイトルの設定
    pg.display.set_caption("オセロ")	

            


    font1 = pg.font.SysFont(None, 30)
    text1 = font1.render("White", True, (0,0,0))
    text2 = font1.render("black", True, (0,0,0))
    screen.blit(text1, (10,10))
    screen.blit(text2, (200,10))

    screen.fill((0,255,0),(20,80, 640, 640))
    color = (0, 0, 0)
    for i in range(9):
        pg.draw.line(screen, color, (i*80+20, 80), (i*80+20, window_height))
        pg.draw.line(screen, color, (20, i*80+80), (660, i*80+80))

    while(1):
        for event in pg.event.get():	
            if event.type == pg.QUIT:		
                pg.quit()		
                sys.exit(0)	
        
            # マウスクリック時の動作
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
            
                x = int((x - 20) / 80)
                y = int((y - 80) / 80)
                print("mouse clicked -> (" + str(x) + ", " + str(y) + ")")

        pg.display.update()		

if __name__	== "__main__":
    window()