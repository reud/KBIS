import  twitter
import  DataBases
import WatchLogReader
import  LogWriterClassVer
import  time
developer_screen_name='r_e_u_d'
import os
class Routine(object):
    def __init__(self,api:twitter.Api,db:DataBases.DataBases,devmode:bool,dir:str):
        """:type : twitter.Api"""
        self.database=db
        self.api=api
        self.devmode=devmode
        self.dir=dir #use for ignoreList
    def FirstRoutine(self):
        print('start first routine')
        if(not self.devmode):
            self.api.PostDirectMessage(text="KBIS起動",screen_name=self.api.VerifyCredentials().screen_name)
        else:
            self.api.PostDirectMessage(text="(dev)KBIS起動",screen_name=developer_screen_name)
        self.logwriter=LogWriterClassVer.LogWriterClassVer()
        self.logwriter.LogWrite("print","KBISが起動しました。devmode:{0}".format(self.devmode))
        self.ignoreList = []
        if(not self.devmode):#本環境ではファイルから読み込む(ファイルあるの前提とする。)
            self.logwriter.LogWrite("print","Logファイルを読み込みます。")
            IgnoreListFile = open('../Tools/IgnoreList.txt')
            temp = IgnoreListFile.readline().strip()
            while (temp):
                print("ignoreリストからロード:" + str(temp))
                self.ignoreList.append(temp)
                temp = IgnoreListFile.readline()
            try:
                IgnoreListFile.close()
            except:
                print("IgnoreListFile.close() was failed")
        else:#devmodeでは初回起動時までの差分は全て無視するのでダイレクトメールを取得してignoreListにぶち込む(ignoreListなしで起動できる！)
            self.directmails=self.api.GetDirectMessages()
            for dm in self.directmails:
                self.ignoreList.append(dm.id)
                self.logwriter.LogWrite(arg1="Writing...id:{0}".format(dm.id))
            #ignoreListを更新する
            try:
                os.remove('../Tools/IgnoreList.txt')
            except:#どうせファイルないくらいしかエラー起きないのでスルー
                pass
            #ignoreListファイルの更新
            strings=""
            self.ignLisFile=open('../Tools/IgnoreList.txt','a')
            for t in range(len(self.ignoreList) - 1):
                strings += str(self.ignoreList[t]) + "\n"
            strings += str(self.ignoreList[len(self.ignoreList) - 1])
            strings = strings.replace("\n\n", "\n")
            self.ignLisFile.write(strings)
            self.ignLisFile.close()
            #きっと書き込みが終了してるでしょう・・・
        print('60秒後にKBISのルーチンが開始されます。')
        return

    def GoRoutine(self):
        time.sleep(60)
        self.DirectMailReader()
        pass
    def Init(self):
        self.FirstRoutine()
        self.GoRoutine()
    def DirectMailReader(self):
        self.directmails=self.api.GetDirectMessages()
        #ここからignoreListに対応するダイレクトメールを削除
        for ignoreNum in self.ignoreList:
            for directmail in self.directmails:
                if(directmail.id==ignoreNum):
                    self.directmails.remove(directmail)
                    print('ignoreListにあったDMです。削除しています・・・　内容...:{0}'.format(directmail.text))
                    break#見つけたらfor文ごと終了させる。
        if(len(self.directmails)!=0):#DMを読み取る処理
            print('DMの件数は{0}件です。'.format(len(self.directmails)))
        else:
            print('DMはありません')


