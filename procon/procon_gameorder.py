import procon_class as goc
import time

def main():

    #start_time=10
    start_time=1
    turn_time=10
    start=False

    ctime=time.time()
    while 1:
        if not start and time.time()-ctime > start_time:
            ctime=time.time()
            start=True
            print("start")

            goc.Functions.init()#データを初期化し、dataフォルダから読み込む
            goc.Functions.fileinit()
            goc.Functions.Save()#データをcurrent_statusフォルダへ保存する
        
        if start and time.time()-ctime > turn_time:
            ctime=time.time()
            print("turn")

            goc.Functions.Otherload()#行動計画の読み込みとリセット、ターンインクリメント
            goc.Functions.FieldAction()#アクションの実行
            goc.Functions.Save()#データをcurrent_statusフォルダへ保存する



if __name__=='__main__':
    main()