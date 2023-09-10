import procon_class as goc
import pygame, sys, os,csv
from pygame.locals import *

#start :初期設定を行う(0:グラフィカル 1:なし)
#update:画面を更新する(0)
#get   :情報を取得する
#       turn, walls, territories, width, height, mason, structures, masons
#action:情報を送信する(第二引数に配列を用いる)
#       1 職人番号
#       2 アクション(0:滞在 1:移動 2:建築 3:解体)
#       3 方向
#send  :送信し、ゲームを進行する
#       0

def main():
    #goc.Functions.init()

    #game("action", [1,3,8])
    #game("send", 0)
    #print(game("get","turn"))
    l=game("get","masons")
    for i in l:
        print(i)
    #print(LegalMove(25,25,1,game("get","walls"),game("get","masons"),game("get","structures")))

def game(command, value):
    cwd=os.getcwd()
    os.chdir(cwd+"/current_status")
    if command=="get":
        if value=="turn":
            with open("others.csv") as file:
                data=list(csv.reader(file))
            return int(data[0][0])
        
        elif value=="walls":
            walls=[]
            with open("walls.csv") as file:
                data=list(csv.reader(file))
            for i in range(goc.Functions.height):
                walls.append([])
                for k in range(goc.Functions.width):
                    walls[i].append(int(data[i][k]))
            return walls
        
        elif value=="territories":
            territories=[]
            with open("territories.csv") as file:
                data=list(csv.reader(file))
            for i in range(goc.Functions.height):
                territories.append([])
                for k in range(goc.Functions.width):
                    territories[i].append(int(data[i][k]))
            return territories
        
        elif value=="width":
            return goc.Functions.width
        
        elif value=="height":
            return goc.Functions.height
        
        elif value=="mason":
            return goc.Functions.mason
        
        elif value=="structures":
            structures=[]
            with open("structures.csv") as file:
                data=list(csv.reader(file))
            for i in range(goc.Functions.height):
                structures.append([])
                for k in range(goc.Functions.width):
                    structures[i].append(int(data[i][k]))
            return structures
        
        elif value=="masons":
            masons=[]
            with open("masons.csv") as file:
                data=list(csv.reader(file))
            for i in range(goc.Functions.height):
                masons.append([])
                for k in range(goc.Functions.width):
                    masons[i].append(int(data[i][k]))
            return masons

    if command=="action":
        with open("others.csv") as file:
            data=list(csv.reader(file))
        with open("others.csv", mode="w",newline='') as file:
            file.writelines(data[0][0]+"\n")
            file.writelines(data[1][0]+"\n")
            for i in range(goc.Functions.mason):
                if int(data[2+i][0])==value[0]:
                    file.writelines(str(value[0])+", "+str(value[1])+", "+str(value[2])+"\n")
                else:
                    file.writelines(data[2+i][0]+","+data[2+i][1]+","+data[2+i][2]+"\n")
    
    #if command=="send":
    #    goc.Functions.FieldAction()
    
    os.chdir("../")


def LegalMove(height, width, mason, walls, masons, structures):
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


if __name__=='__main__':
    main()
