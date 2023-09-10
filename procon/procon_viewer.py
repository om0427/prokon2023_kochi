import procon_class as goc
import pygame, sys, time
from pygame.locals import *
def main():
    beforetime=time.time()
    pygame.init()#pygameを初期化する
    pygame.display.set_mode((850,680),0,32)#画面の大きさを設定する
    screen=pygame.display.get_surface()#画面を取得する
    pygame.display.set_caption('procon_gameorder')
    while 1:
        pygame.display.update()#画面の更新
        #pygame.time.wait(15)#150fごとに画面を更新
        screen.fill((0,0,0,0))#画面の背景色

        if (time.time()-beforetime) > 1:
            goc.Functions.reload()
            beforetime=time.time()

        match goc.Functions.Scene:
            case 0:
                pygame.quit()
                sys.exit()
            case 1:
                goc.Functions.font = pygame.font.SysFont("microsoftyaheiui", 0)
                goc.Functions.init()
            case 2:
                goc.Functions.DisplayField(screen)
                goc.Functions.Button(screen)
                goc.Functions.Information(screen)
            case 3:
                goc.Functions.DisplayTerritory(screen)
                goc.Functions.Button(screen)
                goc.Functions.Information(screen)
            #case _:

        for event in pygame.event.get():
            if event.type==QUIT:#終了イベント
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                goc.Functions.mousepos = event.pos
            else:
                goc.Functions.mousepos = -1

if __name__=='__main__':
    main()
