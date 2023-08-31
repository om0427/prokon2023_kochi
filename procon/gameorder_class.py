import pygame,sys,csv,os,copy
from pygame.locals import *
class Functions:
    Scene=1#シーン
    mousepos=-1#マウス位置

    width=25
    height=25
    mason=4
    masons=[]
    structures=[]
    territories=[]
    walls=[]

    turn=0

    #ターン進行のための情報
    pre_side=1#先行のサイド　1:自分　-1:相手
    current_side=pre_side#現在のサイド
    old_territory=[]#一ターン前の領地情報
    actions=[]#職人の行動 行動タイプ、方向

    #ボタンの選択
    allow_side=0
    mason_choice=0
    action_choice=0
    dir_choice=0

    coef_rampart=10
    coef_territory=30
    coef_castle=100
    myScore=0
    enemyScore=0



    #---以降、主関数---#

    #値の初期化
    def init():
        #変数
        Functions.Scene=2
        for i in range(Functions.mason):
            Functions.actions.append([0,0])

        #---以降、ファイルインポート---#

        files=["masons.csv","structures.csv","territories.csv","walls.csv"]
        cwd=os.getcwd()
        os.chdir(cwd+"/data")

        with open(files[0]) as file:
            data=list(csv.reader(file))
        for i in range(Functions.height):
            Functions.masons.append([])
            for k in range(Functions.width):
                Functions.masons[i].append(int(data[i][k]))

        with open(files[1]) as file:
            data=list(csv.reader(file))
        for i in range(Functions.height):
            Functions.structures.append([])
            for k in range(Functions.width):
                Functions.structures[i].append(int(data[i][k]))

        with open(files[2]) as file:
            data=list(csv.reader(file))
        for i in range(Functions.height):
            Functions.territories.append([])
            for k in range(Functions.width):
                Functions.territories[i].append(int(data[i][k]))
        Functions.old_territory=copy.deepcopy(Functions.territories)

        with open(files[3]) as file:
            data=list(csv.reader(file))
        for i in range(Functions.height):
            Functions.walls.append([])
            for k in range(Functions.width):
                Functions.walls[i].append(int(data[i][k]))

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
        if Functions.current_side==1:
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
    
    #情報の表示
    def Information(screen):
        text = Functions.font.render("ターン: "+str(Functions.turn), True, (255,255,255))
        screen.blit(text, (10,650))
        text = Functions.font.render("行動...", True, (255,255,255))
        screen.blit(text, (100,650))
        textpos=[[150,650],[240,650],[330,650],[420,650],[510,650],[600,650]]
        let1=["滞在","移動","建築","解体"]
        let2=["・","↖","↑","↗","→","↘","↓","↙","←"]
        for i in range(Functions.mason):
            text = Functions.font.render(str(Functions.pre_side*(i+1))+": "+let1[Functions.actions[i][0]]+" "+let2[Functions.actions[i][1]], True, (255,255,255))
            screen.blit(text, (textpos[i][0],textpos[i][1]))
        text = Functions.font.render("スコア: "+str(Functions.myScore)+", "+str(Functions.enemyScore), True, (255,255,255))
        screen.blit(text, (700,650))

    #陣地の調査
    def SerchTerritory():
        #   serchrampart 
        #   0:平地         
        #   1:未探査の城壁 
        #   2:探査中の城壁
        #   3:未探査の城壁周辺地
        #   4:探査中の城壁周辺地
        #   5:個別探査対象の地
        #   6:陣地

        #データ成形#
        serchrampart1=copy.deepcopy(Functions.walls)
        serchrampart2=copy.deepcopy(Functions.walls)
        #[[0 for k in range(Functions.width)] for i in range(Functions.height)]
        serchrampart1=[[0 if k==2 else k for k in serchrampart1[i]] for i in range(Functions.height)]
        serchrampart2=[[0 if k==1 else k for k in serchrampart2[i]] for i in range(Functions.height)]
        serchrampart2=[[1 if k==2 else k for k in serchrampart2[i]] for i in range(Functions.height)]

        Functions.eachcul(serchrampart1)
        Functions.eachcul(serchrampart2)

        for i in range(Functions.height):
            for k in range(Functions.width):
                if serchrampart1[i][k]==6 and serchrampart2[i][k]==6:
                    Functions.territories[i][k]=3
                elif serchrampart1[i][k]==6:
                    Functions.territories[i][k]=1
                elif serchrampart2[i][k]==6:
                    Functions.territories[i][k]=2
                else:
                    Functions.territories[i][k]=0
        
        territory1=copy.deepcopy(Functions.territories)
        territory2=copy.deepcopy(Functions.territories)
        old_territory1=copy.deepcopy(Functions.old_territory)
        old_territory2=copy.deepcopy(Functions.old_territory)

        territory1=[[0 if k==2 else k for k in territory1[i]] for i in range(Functions.height)]
        territory2=[[0 if k==1 else k for k in territory2[i]] for i in range(Functions.height)]
        territory2=[[1 if k==2 else k for k in territory2[i]] for i in range(Functions.height)]
        old_territory1=[[0 if k==2 else k for k in old_territory1[i]] for i in range(Functions.height)]
        old_territory2=[[0 if k==1 else k for k in old_territory2[i]] for i in range(Functions.height)]
        old_territory2=[[1 if k==2 else k for k in old_territory2[i]] for i in range(Functions.height)]

        for i in range(Functions.height):
            for k in range(Functions.width):
                if territory1[i][k]==0 and old_territory1[i][k]==1:
                    territory1[i][k]=2
                if territory2[i][k]==0 and old_territory2[i][k]==1:
                    territory2[i][k]=2

        Functions.opentrty(territory1,2)
        Functions.opentrty(territory2,1)

        for i in range(Functions.height):
            for k in range(Functions.width):
                if territory1[i][k]==1 and territory2[i][k]==1:
                    Functions.territories[i][k]=3
                elif territory1[i][k]==1:
                    Functions.territories[i][k]=1
                elif territory2[i][k]==1:
                    Functions.territories[i][k]=2
                else:
                    Functions.territories[i][k]=0

    #アクションの実行
    def FieldAction():
        Functions.old_territory=copy.deepcopy(Functions.territories)

        Functions.delete()
        Functions.build()
        Functions.move()
        
        Functions.SerchTerritory()
        Functions.Score()
        Functions.turn=Functions.turn+1
        Functions.current_side=-Functions.current_side
        for i in range(Functions.mason):
            Functions.actions[i]=[0,0]

    #職人の移動
    def move():
        #職人が移動する位置配列の初期化
        currentpos=[]
        movepos=[]
        for i in range(Functions.mason):
            movepos.append([-1,-1])
            currentpos.append([-1,-1])
        old_masons=copy.deepcopy(Functions.masons)
        #職人が移動する位置を調べる
        for j in range(Functions.mason):
            cposx=-1
            cposy=-1
            if Functions.actions[j][0]==1:
                for i in range(Functions.height):
                    for k in range(Functions.width):
                        if Functions.masons[i][k]==Functions.current_side*(j+1):
                            cposx=k
                            cposy=i
            currentpos[j][1]=cposx
            currentpos[j][0]=cposy
            posx=[cposx, cposx-1,  cposx , cposx+1, cposx+1, cposx+1,  cposx , cposx-1, cposx-1]
            posy=[cposy, cposy-1, cposy-1, cposy-1,  cposy , cposy+1, cposy+1, cposy+1,  cposy ]

            if 0<=posx[Functions.actions[j][1]]<=Functions.width-1 and 0<=posy[Functions.actions[j][1]]<=Functions.height-1:
                movepos[j][1]=posx[Functions.actions[j][1]]
                movepos[j][0]=posy[Functions.actions[j][1]]
        #職人を移動させる
        for i in range(Functions.mason):
            if Functions.actions[i][0]==1:
                #移動できるか判別する
                movable=True
                #池や相手チームの城壁には移動できない
                if Functions.structures[movepos[i][0]][movepos[i][1]]==1:
                    movable=False
                elif Functions.current_side==-1 and Functions.walls[movepos[i][0]][movepos[i][1]]==1 or Functions.current_side==1 and Functions.walls[movepos[i][0]][movepos[i][1]]==2:
                    movable=False
                #同じ領域に複数の職人が入ることはできない
                elif Functions.masons[movepos[i][0]][movepos[i][1]]!=0:
                    movable=False
                #前のターンにいたところに入ることはできない
                elif old_masons[movepos[i][0]][movepos[i][1]]!=0:
                    movable=False
                #同時に複数の職人が同じ領域に移動を指定していた場合はその全ての職人が移動できない
                for k in range(Functions.mason):
                    if i!=k and movepos[i][0]==movepos[k][0] and movepos[i][1]==movepos[k][1]:
                        movable=False
                
                if movable:
                    Functions.masons[currentpos[i][0]][currentpos[i][1]]=0
                    Functions.masons[movepos[i][0]][movepos[i][1]]=Functions.current_side*(i+1)

    #城壁の建設
    def build():
        for j in range(Functions.mason):
            if Functions.actions[j][0]==2:
                for i in range(Functions.height):
                    for k in range(Functions.width):
                        if Functions.masons[i][k]==Functions.current_side*(j+1):
                            posx=[-1, -1,  k , -1, k+1, -1,  k , -1, k-1]
                            posy=[-1, -1, i-1, -1,  i , -1, i+1, -1,  i ]
                            if posx[Functions.actions[j][1]]==-1:
                                break
                            elif 0<=posx[Functions.actions[j][1]]<=Functions.height-1 and 0<=posy[Functions.actions[j][1]]<=Functions.width-1:
                                #建設できるかどうかを検査する
                                buildable=True
                                #城、相手の城壁、相手の職人の位置には建設できない
                                x=posx[Functions.actions[j][1]]
                                y=posy[Functions.actions[j][1]]
                                if Functions.structures[y][x]==2:
                                    buildable=False
                                elif Functions.walls[y][x]== 1 and Functions.current_side==-1 or Functions.walls[y][x]== 2 and Functions.current_side==1:
                                    buildable=False
                                elif Functions.masons[y][x]<0 and Functions.current_side>0 or Functions.masons[y][x]>0 and Functions.current_side<0:
                                    buildable=False
                                #建設
                                if buildable:
                                    if Functions.current_side==1:
                                        Functions.walls[y][x]=1
                                        if Functions.old_territory[y][x]==1:
                                            Functions.old_territory[y][x]=0
                                            Functions.territories[y][x]=0
                                        elif Functions.old_territory[y][x]==3:
                                            Functions.old_territory[y][x]=2
                                            Functions.territories[y][x]=2
                                    else:
                                        Functions.walls[y][x]=2
                                        if Functions.old_territory[y][x]==2:
                                            Functions.old_territory[y][x]=0
                                            Functions.territories[y][x]=0
                                        elif Functions.old_territory[y][x]==3:
                                            Functions.old_territory[y][x]=1
                                            Functions.territories[y][x]=1

    #城壁の解体
    def delete():
        for j in range(Functions.mason):
            if Functions.actions[j][0]==3:
                cposx=-1
                cposy=-1
                for i in range(Functions.height):
                    for k in range(Functions.width):
                        if Functions.masons[i][k]==Functions.current_side*(j+1):
                            cposx=k
                            cposy=i
                posx=[-1, -1,  cposx , -1, cposx+1, -1,  cposx , -1, cposx-1]
                posy=[-1, -1, cposy-1, -1,  cposy , -1, cposy+1, -1,  cposy ]

                if 0<=posx[Functions.actions[j][1]]<=Functions.width-1 and 0<=posy[Functions.actions[j][1]]<=Functions.height-1:
                    Functions.walls[posy[Functions.actions[j][1]]][posx[Functions.actions[j][1]]]=0

    #スコアを計算する
    def Score():
        #城壁の個数を計算する
        rampartnum1=0
        rampartnum2=0
        for i in range(Functions.height):
            for k in range(Functions.width):
                if Functions.walls[i][k]==1:
                    rampartnum1=rampartnum1+1
                elif Functions.walls[i][k]==2:
                    rampartnum2=rampartnum2+1
        #陣地の個数を計算する
        territorynum1=0
        territorynum2=0
        for i in range(Functions.height):
            for k in range(Functions.width):
                if Functions.territories[i][k]==1 or Functions.territories[i][k]==3:
                    territorynum1=territorynum1+1
                elif Functions.territories[i][k]==2 or Functions.territories[i][k]==3:
                    territorynum2=territorynum2+1
        #陣地内の城の個数を計算する
        castlenum1=0
        castlenum2=0
        for i in range(Functions.height):
            for k in range(Functions.width):
                if Functions.structures[i][k]==2:
                    if Functions.territories[i][k]==1 or Functions.territories[i][k]==3:
                        castlenum1=castlenum1+1
                    elif Functions.territories[i][k]==2 or Functions.territories[i][k]==3:
                        castlenum2=castlenum2+1
        #個数をもとにスコアを計算する
        Functions.myScore=rampartnum1*Functions.coef_rampart+territorynum1*Functions.coef_territory+castlenum1*Functions.coef_castle
        Functions.enemyScore=rampartnum2*Functions.coef_rampart+territorynum2*Functions.coef_territory+castlenum2*Functions.coef_castle


    #---以降、副関数---#

    #敵味方それぞれの陣地の調査
    def eachcul(serchrampart):
        while Functions.serchlist(serchrampart,1):
            #城壁周辺地に印をつける
            for i in range(Functions.height):
                for k in range(Functions.width):
                    if serchrampart[i][k]==1:
                        serchrampart[i][k]=2
                        Functions.sercharoundrampart(i,k,serchrampart)
                        break
                    else:
                        continue
                    break

        #隣接する城壁周辺地をまとめて0にそって伸ばし、縁に当たる場合は全て0にする
        areas=[]
        while Functions.serchlist(serchrampart,3): 
            for i in range(Functions.height):
                for k in range(Functions.width):
                    if serchrampart[i][k]==3:
                        serchrampart[i][k]=4
                        Functions.sercharoundarea(i,k,serchrampart)
                        Functions.serchedge(serchrampart)
                        break
                    else:
                        continue
                    break

    #指定した位置の周囲の城壁を探査中にする
    def sercharoundrampart(i,k,serchrampart):
        exist=[]#周囲に存在する未探査城壁

        posx=[i-1, i-1, i-1,  i , i+1, i+1, i+1,  i ]
        posy=[k-1,  k , k+1, k+1, k+1,  k , k-1, k-1]
        for j in range(8):
            if 0<=posx[j]<=Functions.height-1 and 0<=posy[j]<=Functions.width-1:
                if serchrampart[posx[j]][posy[j]]==1:
                    exist.append(j)
                elif serchrampart[posx[j]][posy[j]]==0:
                    serchrampart[posx[j]][posy[j]]=3

        if(len(exist)==0):
            return 0
        else:
            for j in range(len(exist)):
                serchrampart[posx[exist[j]]][posy[exist[j]]]=2
                Functions.sercharoundrampart(posx[exist[j]],posy[exist[j]],serchrampart)

    #指定した位置の周囲の土地を探査中にする
    def sercharoundarea(i,k,serchrampart):
        exist=[]#周囲に存在する未探査地

        posx=[i-1,  i , i+1,  i ]
        posy=[ k , k+1,  k , k-1]
        for j in range(4):
            if 0<=posx[j]<=Functions.height-1 and 0<=posy[j]<=Functions.width-1:
                if serchrampart[posx[j]][posy[j]]==3:
                    exist.append(j)
        
        if(len(exist)==0):
            return 0
        else:
            for j in range(len(exist)):
                serchrampart[posx[exist[j]]][posy[exist[j]]]=4
                Functions.sercharoundarea(posx[exist[j]],posy[exist[j]],serchrampart)

    #二次元配列に目的の値があるか判別する
    def serchlist(list,value):
        is_dearea=False
        for i in list:
            if value in i:
                is_dearea=True
                break
        return is_dearea

    #周囲の土地が城壁に囲まれているか調べ、囲まれていなければ0にする
    def serchedge(serchrampart):
        is_edge=False
        while Functions.serchlist(serchrampart,4) and not is_edge:
            for i in range(Functions.height):
                for k in range(Functions.width):
                    if serchrampart[i][k]==4:
                        serchrampart[i][k]=5
                        posx=[i-1,  i , i+1,  i ]
                        posy=[ k , k+1,  k , k-1]
                        for j in range(4):
                            if 0<=posx[j]<=Functions.height-1 and 0<=posy[j]<=Functions.width-1:
                                if serchrampart[posx[j]][posy[j]]==0:
                                    serchrampart[posx[j]][posy[j]]=4
                            else:
                                is_edge=True
                                break
        
        if is_edge:
            for i in range(Functions.height):
                for k in range(Functions.width):
                    if serchrampart[i][k]==4 or serchrampart[i][k]==5:
                        serchrampart[i][k]=0
        else:
            for i in range(Functions.height):
                for k in range(Functions.width):
                    if serchrampart[i][k]==5:
                        serchrampart[i][k]=6

    #開放された領地に対する処理
    def opentrty(territory,otherside):
        while Functions.serchlist(territory,2):
            for i in range(Functions.height):
                for k in range(Functions.width):
                    if territory[i][k]==2:
                        xpos=k
                        ypos=i
                        break
                    else:
                        continue
                    break
            Functions.opentrtyaround(ypos,xpos,territory)
            is_open=False
            for i in range(Functions.height):
                for k in range(Functions.width):
                    if territory[i][k]==3:
                        if Functions.walls[i][k]==otherside:
                            is_open=True
                        if Functions.territories[i][k]==otherside or Functions.territories[i][k]==3:
                            is_open=True
            if is_open:
                for i in range(Functions.height):
                    for k in range(Functions.width):
                        if territory[i][k]==3:
                            territory[i][k]=0

        for i in range(Functions.height):
            for k in range(Functions.width):
                if territory[i][k]==3:
                    territory[i][k]=1

    #開放された領地に対する処理
    def opentrtyaround(i,k,territory):
        exist=[]#周囲に存在する未探査城壁

        posy=[i-1,  i , i+1,  i ]
        posx=[ k , k+1,  k , k-1]
        for j in range(4):
            if 0<=posx[j]<=Functions.height-1 and 0<=posy[j]<=Functions.width-1:
                if territory[posy[j]][posx[j]]==2:
                    exist.append(j)

        if(len(exist)==0):
            return 0
        else:
            for j in range(len(exist)):
                territory[posy[exist[j]]][posx[exist[j]]]=3
                Functions.opentrtyaround(posy[exist[j]],posx[exist[j]],territory)

