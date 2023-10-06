#import procon_class as goc
import pygame, sys, os,csv,time,copy,random,requests
from pygame.locals import *

#start :初期設定を行う(0:グラフィカル 1:なし)
#update:画面を更新する(0)
#get   :情報を取得する
#       turn, walls, territories, width, height, mason, structures, masons
#action:情報を送信する(第二引数に配列を用いる)
#       1 職人番号
#       2 アクション(0:滞在 1:移動 2:建築 3:解体)
#       3 方向
#send  :送信し、ゲームを進行する（中止）
#       0

def main():
    cwd=os.getcwd()+"/status"
    os.chdir(cwd)

    id=10
    server_url = "http://localhost:3000/matches/"+str(id)
    header={"procon-token": "kochi89665ca9ed3105039b52d806dab0a35e70b96906f7a7db2025da133a323"}
    

    t1=time.time()
    AI1=AI()
    AI2=AI()
    AI3=AI()
    AI4=AI()
    AI5=AI()
    AI6=AI()
    AIs=[AI1,AI2,AI3,AI4,AI5,AI6]

    #セットアップ
    for i in range(len(AIs)):
        AIs[i].mason_num=(i+1)
    
    with open("turn.dat") as file:
        turn=int(file.read())

    ctime=time.time()
    reload_time=0.1
    turn=0
    while 1:
        if time.time()-ctime > reload_time:
            ctime=time.time()
            if turn != game("get","turn"):
                turn=game("get","turn")
                
                #取る行動の選択
                actionchoice=ChoiceAction(AIs)

                #選択の送信
                for i in range(len(AIs)):
                    print([i+1]+actionchoice[i])
                    game("action", [i+1]+actionchoice[i])

    t2=time.time()
    print(t2-t1)



def game(command, value):
    if command=="get":
        with open("mason.dat") as file:
            mason=int(file.read())
        with open("size.dat") as file:
            data=file.read().split(",")
            height=int(data[0])
            width=int(data[1])
        with open("turn.dat") as file:
            turn=int(file.read())

        if value=="turn":
            with open("turn.dat") as file:
                data=file.read()
            return int(data)
        
        elif value=="walls":
            walls=[]
            with open("walls.csv") as file:
                data=list(csv.reader(file))
            for i in range(height):
                walls.append([])
                for k in range(width):
                    walls[i].append(int(data[i][k]))
            return walls
        
        elif value=="territories":
            territories=[]
            with open("territories.csv") as file:
                data=list(csv.reader(file))
            for i in range(height):
                territories.append([])
                for k in range(width):
                    territories[i].append(int(data[i][k]))
            return territories
        
        elif value=="width":
            return width
        
        elif value=="height":
            return height
        
        elif value=="mason":
            return mason
        
        elif value=="structures":
            structures=[]
            with open("structures.csv") as file:
                data=list(csv.reader(file))
            for i in range(height):
                structures.append([])
                for k in range(width):
                    structures[i].append(int(data[i][k]))
            return structures
        
        elif value=="masons":
            masons=[]
            with open("masons.csv") as file:
                data=list(csv.reader(file))
            for i in range(height):
                masons.append([])
                for k in range(width):
                    masons[i].append(int(data[i][k]))
            return masons

    if command=="send":
        a=0
    


def ChoiceAction(AIs):
    actionchoice=[]
    for i in range(len(AIs)):
        AIs[i].actionassess(game("get", "structures"), game("get", "walls"), game("get", "territories"),game("get", "masons"), game("get", "height"), game("get", "width"))
        #最も評価値の高い行動を検索
        maxvalue=0
        bestaction=0
        for k in range(len(AI.actions)):
            if AIs[i].value[k]>maxvalue:
                bestaction=k
                maxvalue=AIs[i].value[k]
        actionchoice.append(AIs[i].actions[bestaction])

    return actionchoice



class AI:
    masonpos=[-1,-1]#この職人の座標
    mason_num=1

    buildrampartnum=7
    rampartsize=3

    diferdecay=0.9#距離によって評価値がどの程度減衰するか

    #移動するときの評価係数
    neartocastle=1#城への近さ係数
    neartofriend=1#味方の職人との近さ係数
    #neartofront=1#盤面中心との近さ係数
    neartoenemy=1#敵の職人との近さ係数
    neartorampartable=1#城郭にすべき地点との近さ
    #neartomyrampart=1#自身の城郭への近さ
    #neartoenmrampart=1#相手の城郭への近さ

    #建築するときの評価関数
    isrampartable=1#その場所を城郭にすべきか
    #isnearrampart=1#その場所が城郭の外側に接しているか
    #isenemyterritory=1#その場所が敵領地か

    #解体するときの評価関数
    #isnearrampart=1#その城壁が城郭か
    isstructure=1#敵の城壁があるか

    
    #合法手のリストを求める
    def LegalMove(self, height, width, mason, walls, masons, structures):
        LMlist=[]
        if mason>0:
            othersidewall=2
        else:
            othersidewall=1
        for i in range(height):
            for k in range(width):
                if masons[i][k]==mason:
                    posx=[k-1,  k , k+1, k+1, k+1,  k , k-1, k-1]
                    posy=[i-1, i-1, i-1,  i , i+1, i+1, i+1,  i ]
                    for j in range(8):
                        if 0<=posy[j]<=height-1 and 0<=posx[j]<=width-1:
                            if walls[posy[j]][posx[j]]!=othersidewall and masons[posy[j]][posx[j]]==0 and structures[posy[j]][posx[j]]!=1:
                                LMlist.append([1,j+1])
                    posx=[ k , k+1,  k , k-1]
                    posy=[i-1,  i , i+1,  i ]
                    translatenum=[2,4,6,8]
                    for j in range(4):
                        if 0<=posy[j]<=height-1 and 0<=posx[j]<=width-1:
                            if walls[posy[j]][posx[j]]==0 and structures[posy[j]][posx[j]]!=2:
                                if (mason<0 and masons[posy[j]][posx[j]]<=0) or (mason>0 and masons[posy[j]][posx[j]]>=0):
                                    LMlist.append([2,translatenum[j]])
                            if walls[posy[j]][posx[j]]==othersidewall:
                                LMlist.append([3,translatenum[j]])

        return LMlist


    actionablepos=[]#建築、解体できる位置には1が入る
    #建築できる場所を求める
    def actionable(self,structures, height, width, pos):
        AI.actionablepos=[]
        for i in range(height):
            AI.actionablepos.append([])
            for k in range(width):
                AI.actionablepos[i].append(0)
        
        def actionablemarking(structures, height,width,pos):
            aposx=[pos[1]-1,  pos[1] , pos[1]+1, pos[1]+1, pos[1]+1,  pos[1] , pos[1]-1, pos[1]-1]
            aposy=[pos[0]-1, pos[0]-1, pos[0]-1,  pos[0] , pos[0]+1, pos[0]+1, pos[0]+1,  pos[0] ]
            for i in range(8):
                if 0<=aposx[i]<=width-1 and 0<=aposy[i]<=height-1:
                    if structures[aposy[i]][aposx[i]]!=1 and AI.actionablepos[aposy[i]][aposx[i]]!=1:
                        AI.actionablepos[aposy[i]][aposx[i]]=1
                        actionablemarking(structures,height,width,[aposx[i], aposy[i]])
        
        actionablemarking(structures, height, width, pos)

        for i in range(height):
            for k in range(width):
                if AI.actionablepos[i][k]==0:
                    aposx=[ k , k+1,  k , k-1]
                    aposy=[i-1,  i , i+1,  i ]
                    for j in range(4):
                        if 0<=aposx[j]<=width-1 and 0<=aposy[j]<=height-1:
                            if AI.actionablepos[aposy[j]][aposx[j]]==1:
                                AI.actionablepos[i][k]=2
                                break
        
        for i in range(height):
            for k in range(width):
                if AI.actionablepos[i][k]==2:
                    AI.actionablepos[i][k]=1
                if structures[i][k]==2:
                    AI.actionablepos[i][k]=0


    #現地点から目的地までの経路を探索する
    def RouteSerch(self,structures, height, width, currentpos, destination):
        oldL=[[[currentpos[0],currentpos[1]]]]#経路上の座標が並べられた配列の集合配列
        newL=[]
        mark=[]

        for i in range(height):
            mark.append([])
            for k in range(width):
                mark[i].append(0)
        mark[currentpos[1]][currentpos[0]]=1

        for time in range(10):
            for pos in oldL:
                nextposx=[pos[-1][0]-1,  pos[-1][0] , pos[-1][0]+1, pos[-1][0]+1, pos[-1][0]+1,  pos[-1][0] , pos[-1][0]-1, pos[-1][0]-1]
                nextposy=[pos[-1][1]-1, pos[-1][1]-1, pos[-1][1]-1,  pos[-1][1] , pos[-1][1]+1, pos[-1][1]+1 , pos[-1][1]+1, pos[-1][1] ]

                for i in range(8):
                    if 0<=nextposx[i]<=width-1 and 0<=nextposy[i]<=height-1:
                        if structures[nextposy[i]][nextposx[i]]!=1 and mark[nextposy[i]][nextposx[i]]==0:
                            newL.append(pos+[[nextposx[i],nextposy[i]]])
                            mark[nextposy[i]][nextposx[i]]=1
                            if destination in pos+[[nextposx[i],nextposy[i]]]:
                                return newL[-1]
            oldL=copy.deepcopy(newL)
            newL=[]

        return -1


    #城郭となる城壁を置くべき位置を求める
    def buildrampart(self, height, width, castlepos, size):
        mark=[]
        for i in range(height):
            mark.append([])
            for k in range(width):
                mark[i].append(0)
        
        oldsearchpos=[castlepos]
        newsearchpos=[]
        mark[castlepos[1]][castlepos[0]]=1
        for i in range(size):
            for pos in oldsearchpos:
                aroundposx=[ pos[0] , pos[0]+1,  pos[0] , pos[0]-1]
                aroundposy=[pos[1]-1,  pos[1] , pos[1]+1,  pos[1] ]

                for k in range(4):
                    if 0<=aroundposx[k]<=width-1 and 0<=aroundposy[k]<=height-1:
                        if mark[aroundposy[k]][aroundposx[k]]==0:
                            if AI.actionablepos[aroundposy[k]][aroundposx[k]]==1:
                                if i<size-1:
                                    mark[aroundposy[k]][aroundposx[k]]=2
                                    newsearchpos.append([aroundposx[k],aroundposy[k]])
                                else:
                                    mark[aroundposy[k]][aroundposx[k]]=3
                            elif mark[pos[1]][pos[0]]==1:
                                if i<size-1:
                                    mark[aroundposy[k]][aroundposx[k]]=1
                                    newsearchpos.append([aroundposx[k],aroundposy[k]])
                                else:
                                    return -1
                            elif mark[pos[1]][pos[0]]==2:
                                mark[aroundposy[k]][aroundposx[k]]=3
                    
                    elif mark[pos[1]][pos[0]]==2:
                        mark[pos[1]][pos[0]]=3
                    else:
                        return -1
            

            oldsearchpos=copy.deepcopy(newsearchpos)
            newsearchpos=[]

        for i in range(height):
            for k in range(width):
                if mark[i][k]==3:
                    mark[i][k]=1
                else:
                    mark[i][k]=0
        
        return mark                  

    buildmark=[]#城郭にすべき位置
    #建築できる場所、一つの城についての城郭にすべき場所の情報から、建築すべき場所を求める
    #size:城郭の半径 pos:職人の位置 choicenum:囲う城の個数
    def buildplan(self, structures, height, width, size, pos, choicenum):
        AI.actionable(self,structures, height, width, pos)#建築できる場所を求める

        castle=[]#全ての城の位置
        for i in range(height):
            for k in range(width):
                if structures[i][k]==2:
                    castle.append([k,i])
        castle=random.sample(castle,choicenum)#ランダムに選んだ城の位置

        mark=[]#建築すべき場所に1をおいた二次元配列
        for i in range(height):
            mark.append([])
            for k in range(width):
                mark[i].append(0)
        for castlepos in castle:
            assen=AI.buildrampart(self, height, width, castlepos, size)
            if assen!=-1:
                for i in range(height):
                    for k in range(width):
                        if assen[i][k]==1:
                            mark[i][k]=1
        
        return mark

    actions=[]#合法行動のリスト
    value=[]#各行動の評価
    #行動評価
    def actionassess(self, structures, walls, territories, masons, width, height):
        AI.actions=AI.LegalMove(self,height, width, AI.mason_num, walls, masons, structures)

        for i in range(height):
            for k in range(width):
                if masons[i][k]==AI.mason_num:
                    AI.masonpos=[k,i]

        AI.value=[]
        for i in AI.actions:
            AI.value.append(0)

        AI.buildmark=AI.buildplan(self,structures, height, width, AI.rampartsize, AI.masonpos, AI.buildrampartnum)

        buildpos=[]#城郭にすべき位置に建築できる位置
        for i in range(height):
            for k in range(width):
                if AI.mason_num>0:
                    mynum=1
                else:
                    mynum=2
                if AI.buildmark[i][k]==1 and walls[i][k]!=mynum:
                    direx=[ k , k+1,  k , k-1]
                    direy=[i-1,  i , i+1,  i ]
                    for d in range(4):
                        if 0<=direx[d]<=width-1 and 0<=direy[d]<=height-1:
                            if AI.actionablepos[direy[d]][direx[d]]==1 and structures[i][k]!=1:
                                buildpos.append([direx[d],direy[d]])

        castles=[]#城の位置
        mymasons=[]#味方の職人の位置
        enmasons=[]#敵の職人の位置
        for i in range(height):
            for k in range(width):
                if structures[i][k]==2:
                    castles.append([k,i])
                if masons[i][k]*AI.mason_num>0 and masons[i][k]!=AI.mason_num:
                    mymasons.append([k,i])
                elif masons[i][k]*AI.mason_num<0:
                    enmasons.append([k,i])

        #城の近さ評価値を求める
        distances=AI.moveassess(self, structures, height, width,castles)
        for i in range(len(AI.actions)):
            if distances[i]!=0:
                value=AI.neartocastle
                for k in range(distances[i]):
                    value=value*AI.diferdecay
                AI.value[i] +=value
        
        #味方の職人との近さ評価値を求める
        distances=AI.moveassess(self, structures, height, width, mymasons)
        for i in range(len(AI.actions)):
            if distances[i]!=0:
                value=AI.neartofriend
                for k in range(distances[i]):
                    value=value*AI.diferdecay
                AI.value[i] +=value

        #敵の職人との近さ評価値を求める
        distances=AI.moveassess(self, structures, height, width, enmasons)
        for i in range(len(AI.actions)):
            if distances[i]!=0:
                value=AI.neartoenemy
                for k in range(distances[i]):
                    value=value*AI.diferdecay
                AI.value[i] +=value

        #城郭にすべき位置に建築できる位置との近さ評価値を求める
        distances=AI.moveassess(self, structures, height, width, buildpos)
        for i in range(len(AI.actions)):
            if distances[i]!=0:
                value=AI.neartorampartable
                for k in range(distances[i]):
                    value=value*AI.diferdecay
                AI.value[i] +=value

        #城郭にすべき位置に建築する評価値を求める
        direx=[ AI.masonpos[0] , AI.masonpos[0]+1,  AI.masonpos[0] , AI.masonpos[0]-1]
        direy=[AI.masonpos[1]-1,  AI.masonpos[1] , AI.masonpos[1]+1,  AI.masonpos[1] ]
        direnum=[2,4,6,8]
        if AI.mason_num>0:
            mynum=1
        else:
            mynum=2
        for d in range(4):
            if AI.buildmark[direy[d]][direx[d]]==1:
                for i in range(len(AI.actions)):
                    if AI.actions[i][0]==1 and AI.actions[i][1]==direnum[d]:
                        AI.value[i]+=AI.isrampartable

        for i in range(len(AI.actions)):
            if AI.actions[i][0]==0:
                AI.value[i]+=AI.isstructure


    #移動行動の評価
    def moveassess(self, structures, height, width, distinations):
        directionx=[-1,0,1,1,1,0,-1,-1]
        directiony=[-1,-1,-1,0,1,1,1,0]

        distance=[]
        for i in AI.actions:
            distance.append(0)

        list=[]
        for d in distinations:
            r=AI.RouteSerch(self,structures, height, width, AI.masonpos, d)
            if r!=-1:
                list.append(r)
        
        #各方向の最も近い距離を求める
        for data in list:
            if len(data)>1:
                for i in range(8):
                    if data[1][0]-data[0][0]==directionx[i] and data[1][1]-data[0][1]==directiony[i]:
                        for k in range(len(AI.actions)):
                            if AI.actions[k][0]==1 and AI.actions[k][1]==i+1:
                                if distance[k]==0 or distance[k]>len(data)-1:
                                    distance[k]=len(data)-1
        
        return distance


        #for data in list:
        #    print(data)
    
        

if __name__=='__main__':
    main()
