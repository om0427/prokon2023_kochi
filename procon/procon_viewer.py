#import procon_class as goc
import pygame, sys, time, os, csv, copy,requests
from pygame.locals import *
def main():
    beforetime=time.time()
    pygame.init()#pygameを初期化する
    pygame.display.set_mode((850,680),0,32)#画面の大きさを設定する
    screen=pygame.display.get_surface()#画面を取得する
    pygame.display.set_caption('procon_gameorder')

    cwd=os.getcwd()+"/status"
    os.chdir(cwd)
    with open("turn.dat") as file:
        turn=int(file.read())
    while turn!=0:
        with open("turn.dat") as file:
            turn=int(file.read())
        time.sleep(0.1)
    os.chdir("../")

    while 1:
        pygame.display.update()#画面の更新
        pygame.time.wait(15)#150fごとに画面を更新
        screen.fill((0,0,0,0))#画面の背景色

        if (time.time()-beforetime) > 1:
            Functions.reload()
            beforetime=time.time()

        match Functions.Scene:
            case 0:
                pygame.quit()
                sys.exit()
            case 1:
                Functions.font = pygame.font.SysFont("microsoftyaheiui", 0)
                Functions.Scene=2
                Functions.reload()
            case 2:
                Functions.DisplayField(screen)
                Functions.Button(screen)
            case 3:
                Functions.DisplayTerritory(screen)
                Functions.Button(screen)
            #case _:

        for event in pygame.event.get():
            if event.type==QUIT:#終了イベント
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                Functions.mousepos = event.pos
            else:
                Functions.mousepos = -1

class Functions:
    Scene=1#シーン
    mousepos=-1#マウス位置

    side=1

    width=25
    height=25
    mason=6
    masons=[]
    structures=[]
    territories=[]
    walls=[]

    turn=0
    
    #ボタンの選択
    allow_side=0
    mason_choice=0
    action_choice=0
    dir_choice=0

    #データの再読み込み
    def reload():
        files=["masons.csv","structures.csv","territories.csv","walls.csv"]
        cwd=os.getcwd()
        os.chdir(cwd+"/status")

        with open("mason.dat") as file:
            Functions.mason=int(file.read())
        with open("size.dat") as file:
            data=file.read().split(",")
            Functions.height=int(data[0])
            Functions.width=int(data[1])
        with open("turn.dat") as file:
            Functions.turn=int(file.read())

        Functions.masons=[]
        with open(files[0]) as file:
            data=list(csv.reader(file))
        for i in range(Functions.height):
            Functions.masons.append([])
            for k in range(Functions.width):
                Functions.masons[i].append(int(data[i][k]))
        
        Functions.structures=[]
        with open(files[1]) as file:
            data=list(csv.reader(file))
        for i in range(Functions.height):
            Functions.structures.append([])
            for k in range(Functions.width):
                Functions.structures[i].append(int(data[i][k]))

        Functions.territories=[]
        with open(files[2]) as file:
            data=list(csv.reader(file))
        for i in range(Functions.height):
            Functions.territories.append([])
            for k in range(Functions.width):
                Functions.territories[i].append(int(data[i][k]))
        Functions.old_territory=copy.deepcopy(Functions.territories)

        Functions.walls=[]
        with open(files[3]) as file:
            data=list(csv.reader(file))
        for i in range(Functions.height):
            Functions.walls.append([])
            for k in range(Functions.width):
                Functions.walls[i].append(int(data[i][k]))


        os.chdir("../")

    
    #フィールドの描画
    def DisplayField(screen):
        for i in range(Functions.height):
            for k in range(Functions.width):
                #構造物の描画
                match Functions.structures[i][k]:
                    case 0:
                        pygame.draw.rect(screen, (255,255,255,0), Rect(11+25*k,11+25*i,23,23))
                    case 1:
                        pygame.draw.rect(screen, (157,204,224,0), Rect(11+25*k,11+25*i,23,23))
                    case 2:
                        pygame.draw.rect(screen, (116,80,48,0), Rect(11+25*k,11+25*i,23,23))
                #城壁の描画
                match Functions.walls[i][k]:
                    case 1:
                        pygame.draw.rect(screen, (234,145,152,0), Rect(15+25*k,15+25*i,15,15))
                    case 2:
                        pygame.draw.rect(screen, (9,194,137,0), Rect(15+25*k,15+25*i,15,15))
                #職人の描画
                if Functions.masons[i][k]>0:
                    pygame.draw.circle(screen, (255,0,0), (22.5+25.0*float(k),22.5+25.0*float(i)), 10)
                    text = Functions.font.render(str(Functions.masons[i][k]), True, (0,255,255))
                    screen.blit(text, (17.5+25.0*float(k),10+25.0*float(i)))
                elif Functions.masons[i][k]<0:
                    pygame.draw.circle(screen, (0,255,0), (22.5+25.0*float(k),22.5+25.0*float(i)), 10)
                    text = Functions.font.render(str(-Functions.masons[i][k]), True, (255,0,255))
                    screen.blit(text, (17.5+25.0*float(k),10+25.0*float(i)))


    #ボタン
    def Button(screen):
        #モード選択の表示
        pygame.draw.rect(screen, (255,255,255,0), Rect(670,25,135,25))
        Functions.font = pygame.font.SysFont("microsoftyaheiui", 13)
        text = Functions.font.render("フィールド描画モード", True, (0,0,0))
        screen.blit(text, (672,27))
        pygame.draw.rect(screen, (255,255,255,0), Rect(670,60,135,25))
        text = Functions.font.render("陣地描画モード", True, (0,0,0))
        screen.blit(text, (672,62))
        #進行中のサイドを表示
        if Functions.turn%2==Functions.side:
            pygame.draw.rect(screen, (255,0,0,0), Rect(670,100,45,45))
            pygame.draw.rect(screen, (0,126,0,0), Rect(765,105,35,35))
        else:
            pygame.draw.rect(screen, (126,0,0,0), Rect(675,105,35,35))
            pygame.draw.rect(screen, (0,255,0,0), Rect(760,100,45,45))
        #動かす職人を選択
        Functions.font = pygame.font.SysFont("microsoftyaheiui", 17)
        text=Functions.font.render("動かす職人", True, (255,255,255))
        screen.blit(text, (672,150))
        mposition=[[670,180],[720,180],[770,180],[670,230],[720,230],[770,230]]
        for i in range(Functions.mason):
            if i+1==Functions.mason_choice:
                pygame.draw.rect(screen, (255,255,0,0), Rect(mposition[i][0],mposition[i][1],40,40))  
            else:
                pygame.draw.rect(screen, (255,255,255,0), Rect(mposition[i][0],mposition[i][1],40,40))        
            text=Functions.font.render(str(i+1), True, (0,0,0))
            screen.blit(text, (mposition[i][0]+15,mposition[i][1]+10))
        #職人の行動を選択
        text=Functions.font.render("アクション", True, (255,255,255))
        screen.blit(text, (672,280))
        action_text=["滞在","移動","建築","解体"]
        aposition=[[670,310],[720,310],[670,360],[720,360]]
        for i in range(4):
            if i+1==Functions.action_choice:
                pygame.draw.rect(screen, (255,255,0,0), Rect(aposition[i][0],aposition[i][1],40,40))   
            else:
                pygame.draw.rect(screen, (255,255,255,0), Rect(aposition[i][0],aposition[i][1],40,40))        
            text=Functions.font.render(action_text[i], True, (0,0,0))
            screen.blit(text, (aposition[i][0]+2,aposition[i][1]+8))
        #行動の方向を選択
        text=Functions.font.render("方向", True, (255,255,255))
        screen.blit(text, (672,410))
        dir_num=[1,2,3,8,0,4,7,6,5]
        dposition=[[670,440],[720,440],[770,440],[670,490],[720,490],[770,490],[670,540],[720,540],[770,540]]
        for i in range(9):
            if dir_num[i]==Functions.dir_choice-1:
                pygame.draw.rect(screen, (255,255,0,0), Rect(dposition[i][0],dposition[i][1],40,40))  
            else:
                pygame.draw.rect(screen, (255,255,255,0), Rect(dposition[i][0],dposition[i][1],40,40))        
            text=Functions.font.render(str(dir_num[i]), True, (0,0,0))
            screen.blit(text, (dposition[i][0]+5,dposition[i][1]+10))
        #決定・実行ボタン
        pygame.draw.rect(screen, (125,125,255,0), Rect(670,600,60,30))
        text=Functions.font.render("決定", True, (0,0,0))
        screen.blit(text, (672,602))
        pygame.draw.rect(screen, (125,125,255,0), Rect(740,600,60,30))
        text=Functions.font.render("送信", True, (0,0,0))
        screen.blit(text, (742,602))

        #左クリック時の処理
        if Functions.mousepos!=-1:
            #表示モード変更
            if 670<=Functions.mousepos[0]<=670+135 and 25<=Functions.mousepos[1]<=25+25:
                Functions.Scene=2
            elif 670<=Functions.mousepos[0]<=670+135 and 60<=Functions.mousepos[1]<=60+25:
                Functions.Scene=3
            #職人選択
            for i in range(Functions.mason):
                if mposition[i][0]<=Functions.mousepos[0]<=mposition[i][0]+40 and mposition[i][1]<=Functions.mousepos[1]<=mposition[i][1]+40:
                    Functions.mason_choice=i+1
            #行動選択
            for i in range(4):
                if aposition[i][0]<=Functions.mousepos[0]<=aposition[i][0]+40 and aposition[i][1]<=Functions.mousepos[1]<=aposition[i][1]+40:
                    Functions.action_choice=i+1
            #方向選択
            for i in range(9):
                if dposition[i][0]<=Functions.mousepos[0]<=dposition[i][0]+40 and dposition[i][1]<=Functions.mousepos[1]<=dposition[i][1]+40:
                    Functions.dir_choice=dir_num[i]+1
            #決定
            if 670<=Functions.mousepos[0]<=730 and 600<=Functions.mousepos[1]<=630:
                if Functions.mason_choice!=0 and Functions.action_choice!=0 and Functions.dir_choice!=0:
                    Functions.actions[Functions.mason_choice-1]=[Functions.action_choice-1,Functions.dir_choice-1]
            #送信
            if 740<=Functions.mousepos[0]<=800 and 600<=Functions.mousepos[1]<=630:
                Functions.FieldAction()
                pygame.time.wait(300)


    #陣地の描画
    def DisplayTerritory(screen):
        for i in range(Functions.height):
            for k in range(Functions.width):
                match Functions.territories[i][k]:
                    case 0:
                        pygame.draw.rect(screen, (255,255,255,0), Rect(10+25*k,11+25*i,25,25))
                    case 1:
                        pygame.draw.rect(screen, (255,0,0,0), Rect(10+25*k,11+25*i,25,25))
                    case 2:
                        pygame.draw.rect(screen, (0,255,0,0), Rect(10+25*k,11+25*i,25,25))
                    case 3:
                        pygame.draw.rect(screen, (255,255,0,0), Rect(10+25*k,11+25*i,25,25))



if __name__=='__main__':
    main()
