import gameorder as go

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
    go.game("start", 1)
    go.game("action", [1,1,1])
    go.game("send", 0)
    print(go.game("get","turn"))
    l=go.game("get","masons")
    for i in l:
        print(i)
    #print(LegalMove(25,25,1,go.game("get","walls"),go.game("get","masons"),go.game("get","structures")))

   
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
