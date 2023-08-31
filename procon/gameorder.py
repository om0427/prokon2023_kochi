import gameorder_class as goc
import pygame, sys
from pygame.locals import *
def game(command, value):
    if command=="start" and value==0:
        
        pygame.init()#pygameを初期化する
        pygame.display.set_mode((850,680),0,32)#画面の大きさを設定する
        screen=pygame.display.get_surface()#画面を取得する
        pygame.display.set_caption('procon_gameorder')
        while 1:
            pygame.display.update()#画面の更新
            #pygame.time.wait(15)#150fごとに画面を更新
            screen.fill((0,0,0,0))#画面の背景色

            match goc.Functions.Scene:
                case 0:
                    pygame.quit()
                    sys.exit()
                case 1:
                    goc.Functions.font = pygame.font.SysFont("microsoftyaheiui", 0)
                    goc.Functions.init()
                    goc.Functions.SerchTerritory()
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

    if command=="start" and value==1:
        goc.Functions.init()
        goc.Functions.SerchTerritory()
    
    if command=="get":
        if value=="turn":
            return goc.Functions.turn
        elif value=="walls":
            return goc.Functions.walls
        elif value=="territories":
            return goc.Functions.territories
        elif value=="width":
            return goc.Functions.width
        elif value=="height":
            return goc.Functions.height
        elif value=="mason":
            return goc.Functions.mason
        elif value=="structures":
            return goc.Functions.structures
        elif value=="masons":
            return goc.Functions.masons

    if command=="action":
        goc.Functions.actions[value[0]-1]=[value[1], value[2]]
    
    if command=="send":
        goc.Functions.FieldAction()
