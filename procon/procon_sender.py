#import procon_class as goc
import os,csv,time,copy,random,requests

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

num=0

#token="kochi89665ca9ed3105039b52d806dab0a35e70b96906f7a7db2025da133a323"
token="token1"
header={"procon-token": token}

server_id_url="http://localhost:3000/matches"

response = requests.get(server_id_url, headers=header)
while response.status_code != 200:  # ステータスコード200は成功を示します
    response = requests.get(server_id_url, headers=header)
    time.sleep(0.3)

data=response.json()


if num<len(data):
    id=data["matches"][num]["id"]
    if data["matches"][num]["first"]:
        #先行:0　後攻:1
        ahrm=0
    else:
        #先行:0　後攻:1
        ahrm=1


server_url = "http://localhost:3000/matches/"+str(id)

#移動する位置(バッティング防止)
cantmoves=[]

def main():
    global cantmoves
    #先行:0　後攻:1
    global ahrm
    cwd=os.getcwd()+"/status"
    os.chdir(cwd)

    AI1=AI()
    AI1.rampartsize=3
    AI1.neartoenmrampart=0
    AI1.neartocastle=0
    AI1.neartofriend=-10
    AI2=AI()
    AI2.neartocastle=2#城への近さ係数/
    AI2.neartofriend=-21#味方の職人との近さ係数/
    AI2.neartoenemy=0#敵の職人との近さ係数/
    AI2.neartorampartable=0#城郭にすべき地点との近さ/
    AI2.neartoenmrampart=0#相手の城郭への近さ/
    AI2.neartoenemyterri=0#相手の領地への近さ/
    #建築するときの評価関数
    AI2.isrampartable=0#その場所を城郭にすべきか
    AI2.isenemyterritory=1#その場所が敵領地か
    #解体するときの評価関数
    AI2.isnearrampart=0#その城壁が城郭か
    AI2.isstructure=0#敵の城壁があるか
    AI3=AI()
    AI3.neartocastle=0
    AI3.neartofriend=-10
    AI3.rampartsize=1
    AI4=AI()
    AI4.neartocastle=-20#城への近さ係数/
    AI4.neartofriend=0#味方の職人との近さ係数/
    AI4.neartoenemy=4#敵の職人との近さ係数/
    AI4.neartorampartable=0#城郭にすべき地点との近さ/
    AI4.neartoenmrampart=2#相手の城郭への近さ/
    AI4.neartoenemyterri=2#相手の領地への近さ/
    #建築するときの評価関数
    AI4.isrampartable=10#その場所を城郭にすべきか
    AI4.isenemyterritory=1#その場所が敵領地か
    #解体するときの評価関数
    AI4.isnearrampart=10#その城壁が城郭か
    AI4.isstructure=10#敵の城壁があるか
    AI5=AI()
    AI6=AI()
    AIs_model=[AI1,AI2,AI3,AI4,AI5,AI6]
    AIs=[]


    with open("turn.dat") as file:
        turn=int(file.read())
    while turn==-1:
        with open("turn.dat") as file:
            turn=int(file.read())
        time.sleep(0.1)


    for i in range(game("get","mason")):
        AIs_model[i].Init(i+1,game("get","height"),game("get","width"),game("get","masons"))
        AIs.append(AIs_model[i])


    ctime=time.time()
    reload_time=0.1
    turn=-1

    cantmoves=[]
    for i in range(game("get","height")):
        cantmoves.append([])
        for k in range(game("get","width")):
            cantmoves[i].append(1)

    actionchoice=ChoiceAction(AIs)
    while 1:
        if time.time()-ctime > reload_time:
            ctime=time.time()
            if turn != game("get","turn"):
                turn=game("get","turn")
                if turn %2 ==ahrm:
                    #取る行動の選択
                    t1=time.time()

                    cantmoves=[]
                    for i in range(game("get","height")):
                        cantmoves.append([])
                        for k in range(game("get","width")):
                            cantmoves[i].append(1)
                    actionchoice=ChoiceAction(AIs)
                    t2=time.time()
                    #print(t2-t1)
                    #選択の送信
                    #for i in range(len(AIs)):
                    #    print(AIs[i].value)
                    #    #print(AIs[i].LegalMove(game("get", "height"), game("get", "width"),game("get","mason"), game("get", "walls"),game("get", "masons") ,game("get", "structures")))
                    
                    game("send", actionchoice)




def game(command, value):
    with open("mason.dat") as file:
#        mason=int(file.read())
        mason_data = file.read().strip()  # 改行文字を削除して読み込み
        if mason_data:
            mason = int(mason_data)
        else:
            mason = 0  # ファイルが空の場合、0 を設定
    with open("size.dat") as file:
        data = file.read().strip().split(",")
        if len(data) == 2:
            height, width = map(int, data)
        else:
            height, width = 0, 0  # ファイルが不正な形式の場合、0 で初期化
#       data=file.read().split(",")
#       height=int(data[0])
#       width=int(data[1])
    with open("turn.dat") as file:
#        turn=int(file.read())
        turn_data = file.read().strip()
    if turn_data:
        turn = int(turn_data)
    else:
        turn = 0  # ファイルが空の場合、0 で初期化
    if command=="get":
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
        actions=[]
        for i in range(mason):
            actions.append({"type":value[i][0], "dir":value[i][1]})
        #print(actions)
        #actions=[{"type":2, "dir":2},{"type":2, "dir":2}]
        data = {'turn': turn+1, "actions":actions}
        #print(data)
        response = requests.post(server_url, headers=header,json=data)
        #print(response.status_code)
    


def ChoiceAction(AIs):
    actionchoice=[]
    for i in range(len(AIs)):
        global cantmoves
        #print(cantmoves)
        AIs[i].actionassess(game("get", "structures"), game("get", "walls"), game("get", "territories"),game("get", "masons"), game("get", "height"), game("get", "width"),game("get","turn"))
        #最も評価値の高い行動を検索
        maxvalue=0
        bestaction=0
        for k in range(len(AIs[i].actions)):
            if AIs[i].value[k]>maxvalue:
                bestaction=k
                maxvalue=AIs[i].value[k]
        if len(AIs[i].actions)==0:
            actionchoice.append([0,0])
        else:
            actionchoice.append(AIs[i].actions[bestaction])

    return actionchoice




class AI:
    masonpos=[-1,-1]#この職人の座標
    mason_num=0

    buildrampartnum=1
    rampartsize=2

    diferdecay=0.9#距離によって評価値がどの程度減衰するか

    #移動するときの評価係数
    neartocastle=0.3#城への近さ係数/
    neartofriend=25#味方の職人との近さ係数/
    neartoenemy=0#敵の職人との近さ係数/
    neartorampartable=13#城郭にすべき地点との近さ/
    neartoenmrampart=0#相手の城郭への近さ/
    neartoenemyterri=5#相手の領地への近さ/

    #建築するときの評価関数
    isrampartable=12#その場所を城郭にすべきか
    isenemyterritory=0#その場所が敵領地か

    #解体するときの評価関数
    isnearrampart=20#その城壁が城郭か
    isstructure=3#敵の城壁があるか

    def Init(self,mason_num,height,width,masons):
        self.mason_num=mason_num
        for i in range(height):
            for k in range(width):
                if masons[i][k]==mason_num:
                    self.masonpos=[k,i]
    
    #合法手のリストを求める
    def LegalMove(self, height, width, mason, walls, masons, structures):
        global cantmoves
        LMlist=[]
        for i in range(height):
            for k in range(width):
                if masons[i][k]==mason:
                    posx=[k-1,  k , k+1, k+1, k+1,  k , k-1, k-1]
                    posy=[i-1, i-1, i-1,  i , i+1, i+1, i+1,  i ]
                    for j in range(8):
                        if 0<=posy[j]<=height-1 and 0<=posx[j]<=width-1:
                            if walls[posy[j]][posx[j]]!=2 and masons[posy[j]][posx[j]]==0 and structures[posy[j]][posx[j]]!=1 and cantmoves[posy[j]][posx[j]]==1:
                                LMlist.append([1,j+1])
                                cantmoves[posy[j]][posx[j]]=0

                    posx=[ k , k+1,  k , k-1]
                    posy=[i-1,  i , i+1,  i ]
                    translatenum=[2,4,6,8]
                    for j in range(4):
                        if 0<=posy[j]<=height-1 and 0<=posx[j]<=width-1:
                            if walls[posy[j]][posx[j]]==0 and structures[posy[j]][posx[j]]!=2:
                                if (mason<0 and masons[posy[j]][posx[j]]<=0) or (mason>0 and masons[posy[j]][posx[j]]>=0):
                                    LMlist.append([2,translatenum[j]])
                            if walls[posy[j]][posx[j]]==2:
                                LMlist.append([3,translatenum[j]])

        return LMlist


    actionablepos=[]#建築、解体できる位置には1が入る
    #建築できる場所を求める
    def actionable(self,structures, height, width, pos):
        self.actionablepos=[]
        for i in range(height):
            self.actionablepos.append([])
            for k in range(width):
                self.actionablepos[i].append(0)
        
        def actionablemarking(structures, height,width,pos):
            aposx=[pos[1]-1,  pos[1] , pos[1]+1, pos[1]+1, pos[1]+1,  pos[1] , pos[1]-1, pos[1]-1]
            aposy=[pos[0]-1, pos[0]-1, pos[0]-1,  pos[0] , pos[0]+1, pos[0]+1, pos[0]+1,  pos[0] ]
            for i in range(8):
                if 0<=aposx[i]<=width-1 and 0<=aposy[i]<=height-1:
                    if structures[aposy[i]][aposx[i]]!=1 and self.actionablepos[aposy[i]][aposx[i]]!=1:
                        self.actionablepos[aposy[i]][aposx[i]]=1
                        actionablemarking(structures,height,width,[aposx[i], aposy[i]])
        
        actionablemarking(structures, height, width, pos)

        for i in range(height):
            for k in range(width):
                if self.actionablepos[i][k]==0:
                    aposx=[ k , k+1,  k , k-1]
                    aposy=[i-1,  i , i+1,  i ]
                    for j in range(4):
                        if 0<=aposx[j]<=width-1 and 0<=aposy[j]<=height-1:
                            if self.actionablepos[aposy[j]][aposx[j]]==1:
                                self.actionablepos[i][k]=2
                                break
        
        for i in range(height):
            for k in range(width):
                if self.actionablepos[i][k]==2:
                    self.actionablepos[i][k]=1
                if structures[i][k]==2:
                    self.actionablepos[i][k]=0


    #現地点から目的地までの経路を探索する
    def RouteSerch(self,structures, height, width, currentpos, destination):
        oldL=[[[currentpos[0], currentpos[1]]]]#経路上の座標が並べられた配列の集合配列
        newL=[]
        mark=[]

        for i in range(height):
            mark.append([])
            for k in range(width):
                mark[i].append(0)
        mark[currentpos[1]][currentpos[0]]=1

        for time in range(20):
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
                            if self.actionablepos[aroundposy[k]][aroundposx[k]]==1:
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

    targetcastle=0
    buildmark=[]#城郭にすべき位置
    cooltime=0#次に囲う城を更新するまでの長さ
    #建築できる場所、一つの城についての城郭にすべき場所の情報から、建築すべき場所を求める
    #size:城郭の半径 pos:職人の位置 choicenum:囲う城の個数
    def buildplan(self, structures, height, width, size, pos, choicenum,walls,turn,territories):
        castle=[]#全ての城の位置
        for i in range(height):
            for k in range(width):
                if structures[i][k]==2:
                    castle.append([k,i])
        if self.cooltime<=0:
            self.actionable(structures, height, width, pos)#建築できる場所を求める
            route=[]
            routelenmin=0
            nearpoint=[]
            for i in range(len(castle)):
                route.append(self.RouteSerch(structures,height,width,self.masonpos,castle[i]))
                if route[i]!=-1 or territories[castle[i][1]][castle[i][0]]==1 or territories[castle[i][1]][castle[i][0]]==3:
                    nearpoint.append(10-len(route[i]))
                else:
                    nearpoint.append(0)
            nesnumpoint=[]
            maxnes=0
            for i in range(len(castle)):
                assen=self.buildrampart(height,width,castle[i],size)
                if assen!=-1:
                    nesnum=0
                    for i in range(height):
                        for k in range(width):
                            if assen[i][k]==1 and walls[i][k]!=1:
                                nesnum=nesnum+1
                    nesnumpoint.append(nesnum)
                    if maxnes<nesnum:
                        maxnes=nesnum
            
            for i in range(len(nesnumpoint)):
                if nesnumpoint[i]!=0:
                    nesnumpoint[i]=maxnes-nesnumpoint[i]
            maxcastle=0
            maxpoint=0
            for i in range(len(nesnumpoint)):
                if nearpoint[i]+nesnumpoint[i]>maxpoint:
                    maxpoint=nearpoint[i]+nesnumpoint[i]
                    maxcastle=i
            self.targetcastle=maxcastle
            #castle=random.sample(castle,choicenum)#ランダムに選んだ城の位置

            self.cooltime=5
        else:
            self.cooltime=self.cooltime-1
            if territories[castle[self.targetcastle][1]][castle[self.targetcastle][0]]==1 or territories[castle[self.targetcastle][1]][castle[self.targetcastle][0]]==3:
                self.cooltime=0



        mark=[]#建築すべき場所に1をおいた二次元配列
        for i in range(height):
            mark.append([])
            for k in range(width):
                mark[i].append(0)
        assen=self.buildrampart(height, width, castle[self.targetcastle], size)
        if assen!=-1:
            for i in range(height):
                for k in range(width):
                    if assen[i][k]==1:
                        mark[i][k]=1


        return mark
    


    actions=[]#合法行動のリスト
    value=[]#各行動の評価
    #行動評価
    def actionassess(self, structures, walls, territories, masons, width, height,turn):
        self.actions=self.LegalMove(height, width, self.mason_num, walls, masons, structures)

        for i in range(height):
            for k in range(width):
                if masons[i][k]==self.mason_num:
                    self.masonpos=[k,i]
        self.value=[]
        for i in self.actions:
            self.value.append(0)

        
        self.buildmark=self.buildplan(structures, height, width, self.rampartsize, self.masonpos, self.buildrampartnum,walls,turn,territories)

        buildpos=[]#城郭にすべき位置に建築できる位置
        for i in range(height):
            for k in range(width):
                if self.buildmark[i][k]==1 and walls[i][k]!=1:
                    direx=[ k , k+1,  k , k-1]
                    direy=[i-1,  i , i+1,  i ]
                    for d in range(4):
                        if 0<=direx[d]<=width-1 and 0<=direy[d]<=height-1:
                            if self.actionablepos[direy[d]][direx[d]]==1 and structures[direy[d]][direx[d]]!=1:
                                buildpos.append([direx[d],direy[d]])


        castles=[]#城の位置
        mymasons=[]#味方の職人の位置
        enmasons=[]#敵の職人の位置
        enmterri=[]#敵の領地の位置
        enmrampart=[]
        for i in range(height):
            for k in range(width):
                if structures[i][k]==2 and (territories[i][k]!=1 or territories[i][k]!=3):
                    castles.append([k,i])
                if masons[i][k]>0 and masons[i][k]!=self.mason_num:
                    mymasons.append([k,i])
                elif masons[i][k]<0:
                    enmasons.append([k,i])
                if territories[i][k]==2 or territories[i][k]==3:
                    enmterri.append([k,i])
                if walls[i][k]==2:
                    enmrampart.append([k,i])







        #評価値を求める
        #print(self.value)
        #print(self.mason_num,":",self.masonpos)
        #for data in self.buildmark:
        #    print(data)
        #print()
        #for i in range(height):
        #    for k in range(width):
        #        #if self.buildmark[i][k]==1 and walls[i][k]!=1:
        #        #    print("2",end=" ")
        #        if [k,i] in buildpos:
        #            print("1",end=" ")
        #        else:
        #            print("0",end=" ")
        #    print()
        #print()

        #城の近さ評価値を求める
        distances=self.moveassess(structures, height, width,[castles[self.targetcastle]])
        for i in range(len(self.actions)):
            if distances[i]!=0:
                value=self.neartocastle
                for k in range(distances[i]):
                    value=value*self.diferdecay
                self.value[i] +=value
        

        #味方の職人との近さ評価値を求める
        distances=self.moveassess(structures, height, width, mymasons)
        for i in range(len(self.actions)):
            if distances[i]!=0:
                value=self.neartofriend
                for k in range(distances[i]):
                    value=value*self.diferdecay
                self.value[i] +=value

        #敵の職人との近さ評価値を求める
        distances=self.moveassess(structures, height, width, enmasons)
        for i in range(len(self.actions)):
            if distances[i]!=0:
                value=self.neartoenemy
                for k in range(distances[i]):
                    value=value*self.diferdecay
                self.value[i] +=value


        #城郭にすべき位置に建築できる位置との近さ評価値を求める
        distances=self.moveassess(structures, height, width, buildpos)
        for i in range(len(self.actions)):
            if distances[i]!=0:
                value=self.neartorampartable
                for k in range(distances[i]):
                    value=value*self.diferdecay
                self.value[i] +=value

        #敵の領地との近さ評価値を求める
        distances=self.moveassess(structures,height,width,enmterri)
        for i in range(len(self.actions)):
            if distances[i]!=0:
                value=self.neartoenemyterri
                for k in range(distances[i]):
                    value=value*self.diferdecay
                self.value[i]+=value
        
        #敵の城壁との近さ評価値を求める
        distances=self.moveassess(structures,height,width,enmrampart)
        for i in range(len(self.actions)):
            if distances[i]!=0:
                value=self.neartoenmrampart
                for k in range(distances[i]):
                    value=value*self.diferdecay
                self.value[i]+=value
        

        #城郭にすべき位置に建築する評価値を求める
        direx=[ self.masonpos[0] , self.masonpos[0]+1,  self.masonpos[0] , self.masonpos[0]-1]
        direy=[self.masonpos[1]-1,  self.masonpos[1] , self.masonpos[1]+1,  self.masonpos[1] ]
        direnum=[2,4,6,8]
        for d in range(4):
            if 0<=direx[d]<=width-1 and 0<=direy[d]<=height-1:
                if self.buildmark[direy[d]][direx[d]]==1:
                    for i in range(len(self.actions)):
                        if self.actions[i][0]==2 and self.actions[i][1]==direnum[d]:
                            self.value[i]+=self.isrampartable
        
        #敵陣地に建築する評価値を求める
        direx=[ self.masonpos[0] , self.masonpos[0]+1,  self.masonpos[0] , self.masonpos[0]-1]
        direy=[self.masonpos[1]-1,  self.masonpos[1] , self.masonpos[1]+1,  self.masonpos[1] ]
        direnum=[2,4,6,8]
        for d in range(4):
            if 0<=direx[d]<=width-1 and 0<=direy[d]<=height-1:
                if territories[direy[d]][direx[d]]==2 or territories[direy[d]][direx[d]]==3:
                    for i in range(len(self.actions)):
                        if self.actions[i][0]==2 and self.actions[i][1]==direnum[d]:
                            self.value[i]+=self.isenemyterritory

        #解体に関する評価値を求める
        direx=[ self.masonpos[0] , self.masonpos[0]+1,  self.masonpos[0] , self.masonpos[0]-1]
        direy=[self.masonpos[1]-1,  self.masonpos[1] , self.masonpos[1]+1,  self.masonpos[1] ]
        direnum=[2,4,6,8]
        for d in range(4):
            if 0<=direx[d]<=width-1 and 0<=direy[d]<=height-1:
                if walls[direy[d]][direx[d]]==2:
                    for action, val in zip(self.actions, self.value):
                        if action[0]==3 and action[1]==direnum[d]:
                            val+=self.isstructure

                    direx2=[ direx[d] , direx[d]+1,  direx[d] , direx[d]-1]
                    direy2=[direy[d]-1,  direy[d] , direy[d]+1,  direy[d] ]
                    nearterri=False
                    for d2 in range(4):
                        if territories[direy2[d2]][direx2[d2]]==2 or territories[direy2[d2]][direx2[d2]]==3:
                            nearterri=True
                            break
                    if nearterri:
                        for i in range(len(self.actions)):
                            if self.actions[i][0]==3 and self.actions[i][1]==direnum[d]:
                                self.value[i]+=self.isnearrampart
        
        


            
        


    #移動行動の評価
    def moveassess(self, structures, height, width, distinations):
        directionx=[-1,0,1,1,1,0,-1,-1]
        directiony=[-1,-1,-1,0,1,1,1,0]

        distance=[]
        for i in self.actions:
            distance.append(0)

        list=[]
        for d in distinations:
            r=self.RouteSerch(structures, height, width, self.masonpos, d)
            if r!=-1:
                list.append(r)
        

        #各方向の最も近い距離を求める
        for data in list:
            if len(data)>1:
                for i in range(8):
                    if data[1][0]-data[0][0]==directionx[i] and data[1][1]-data[0][1]==directiony[i]:
                        for k in range(len(self.actions)):
                            if self.actions[k][0]==1 and self.actions[k][1]==i+1:
                                if distance[k]==0 or distance[k]>len(data)-1:
                                    distance[k]=len(data)-1
        

        return distance


        #for data in list:
        #    print(data)
    
        

if __name__=='__main__':
    main()
