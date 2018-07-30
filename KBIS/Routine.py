# encoding: utf-8
import  twitter
import  DataBases
import WatchLogReader
import  LogWriterClassVer
import  time
import  WordBox
developer_screen_name='r_e_u_d'
import os
import traceback
class Routine(object):
    def __init__(self,api:twitter.Api,db:DataBases.DataBases,devmode:bool,dir:str):
        """:type : twitter.Api"""
        self.wordbox=WordBox.WordBox()
        self.database=db
        self.api=api
        self.devmode=devmode
        self.dir=dir #use for ignoreList
    def DatabaseOutPutter(self,arg1:str,arg2):#KBISにデータベースの検索結果を載せる関数 (ここでは文字列を返す)
        lists=self.database.Search(arg1,arg2)
        line=f'{len(lists)}個の要素が検索されました。\r\n'
        for list in lists:
            line+=f'{list}\r\n'
        return line
    def FirstRoutine(self):
        print('start first routine')
        if(not self.devmode):
            self.api.PostDirectMessage(text="KBIS起動",screen_name=self.api.VerifyCredentials().screen_name)
        else:
            #self.api.PostDirectMessage(text="(dev)KBIS起動",screen_name=developer_screen_name)
            pass
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
        while(True):
            time.sleep(20)
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
        #ここからDMの処理
        #devmode中はsudo機能とdev機能のどちらもdeveloperが使用可能 sudo calluserは自分に結果を通知
        #本環境は
        #権限はdev→sudo→registered→All もイメージ
        #[info]--情報要求 (registered User)
        #[register:[苗字] [名前]] 新規登録(All User)
        #[change:(新しいscreen_name)] ユーザーID変更(registered User)
        #[dev:speak (saying)] ツイート(developer)   dev only fin
        #[sudo:CallUser (arg**)] 絞り込み複数通知   sudo only (Hthan と Lthanのみ) fin
        #[m:(String)] 普通に話しかける用(一回のみ)　(All User)
        #[conv] (All User) 何回か繰り返す会話用　(全てのコマンドが無視されます)
        #[exit] (a user -> if use conv) conv使った会話が終了したら
        #[sudo:reload] データベースを再更新します。   sudo only
        #[sudo:getDB (arg**)] CallUserと引数は同じで、指定したレコードを取得します。   sudo only fin
        #[help]ユーザの権限に合わせた使えるコマンドの案内をします。
        #[q:(String)] 開発者に通知にバグとか要望とか教えて下さい！
        #
        #ignoreListに入れる

        for directmail in self.directmails:
            self.ignoreList.append(directmail.id)
            print(f'DirectMessageの内容{directmail.text}')
            if(directmail.text.find("dev:")==0):
                directmail.text=directmail.text.replace('dev:','')
                #ここでdevが本当にdeveloperか確認する
                if(developer_screen_name==directmail.sender_screen_name):
                    if(directmail.text.find('speak ')==0):#speakの場合　ここの階層に新規コマンドを追加して下さい。 ex. dev:speak HelloWorld
                        directmail.text=directmail.text.replace('speak ','')
                        if(not self.devmode):
                            self.api.PostUpdate(text=directmail.text)
                        else:
                            print(f'speakコマンド:{directmail.text}')
                else:#developerじゃない場合
                    self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text='あなたはこのコマンドを実行する権限を持っていません。')
            elif(directmail.text.find("sudo:")==0):
                directmail.text=directmail.text.replace('sudo:','')
                authority=False
                #ここから権限のチェック　正しければauthority=Trueになる。
                if(self.devmode):
                    if(developer_screen_name==directmail.sender_screen_name):
                        authority=True
                for i in self.database.Search('get','root'):
                    for strings in i:#ここから未テスト
                        if(strings==directmail.sender_screen_name):
                            authority=True
                #ここまで
                if(authority):
                    if(directmail.text.find('getDB')==0):
                        directmail.text=directmail.text.replace('getDB','')
                        splitedWords=directmail.text.split()
                        if(splitedWords[0]=='Lthan' or splitedWords[0]=='Hthan'):
                            try:
                                number=int(splitedWords[1])
                                line=self.DatabaseOutPutter(splitedWords[0],number)
                                self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text=line)
                            except:
                                self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text=f'引数が間違っていると思われます。At arg2. arg1={splitedWords[0]} and arg2={splitedWords[1]}')
                                traceback.print_exc()
                            pass#途中
                    if(directmail.text.find('CallUser ')==0):
                        directmail.text=directmail.text.replace('CallUser ','')
                        splitedWords=directmail.text.split(' ')
                        if(splitedWords[0]=='Lthan' or splitedWords[0]=='Hthan'):
                            try:
                                number=int(splitedWords[1])
                                lists=self.database.Search(splitedWords[0],number)
                                if(self.devmode):
                                    for list in lists:
                                        name=str(list[1])
                                        money=int(list[3])
                                        print(f'CallUser要求を行いました(dev)\r\n{self.wordbox.GetString(name,money,True,directmail.text)}')
                                else:
                                    for list in lists:
                                        name=str(list[1])
                                        money=int(list[3])
                                        dmTo=str(list[2])
                                        self.api.PostDirectMessage(screen_name=dmTo,text=self.wordbox.GetString(name,money,True,directmail.text))
                            except:
                                self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text=f'検索結果が0または引数が間違っていると思われます。At arg2. arg1={splitedWords[0]} and arg2={splitedWords[1]}')
                        elif(splitedWords[0]=='at'):
                            try:
                                for list in self.database.Search('at',splitedWords[1]):
                                    if(self.devmode):
                                        print(list)
                                        name=str(list[1])
                                        money=int(list[3])
                                        print(list+f'にCallUser要求を行いました(dev)\r\n{self.wordbox.GetString(name,money,True,directmail.text)}')
                                    else:
                                        name = str(list[1])
                                        money = int(list[3])
                                        dmTo = str(list[2])
                                        self.api.PostDirectMessage(screen_name=dmTo,
                                                                    text=self.wordbox.GetString(name, money, True,
                                                                                                   directmail.text))
                                        pass
                            except:
                                self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text='引数が不正か、要素が見つかりませんでした。')
                        else:
                             self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text=f'引数が間違っていると思われます。At arg1. arg1={splitedWords[0]} and arg2={splitedWords[1]}')
                    if(directmail.text.find('reload')==0):
                        self.database.renew()


                    pass
                else:
                    self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text='あなたはこのコマンドを実行する権限を持っていません。')
            else:
                if(directmail.text.find('info')==0):
                    try:
                        for list in self.database.Search(('at'),directmail.sender_screen_name):
                            name = str(list[1])
                            money = int(list[3])
                            dmTo = str(list[2])
                            self.api.PostDirectMessage(screen_name=dmTo,text=self.wordbox.GetString(name,money))
                    except:
                        self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text='あなたのデータは発見出来ませんでした。\r\n今までにKBISを使ったことない場合は\r\nregister:[苗字] [名前]\r\nと入力しKBISのデータベースに登録を行ってください。')
                if(directmail.text.find('register:')==0):
                    directmail.text=directmail.text.replace('register:','')
                    sendstr=self.database.RegisterOrChanger(directmail.text,directmail.sender_screen_name,True)
                    self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text=sendstr)
                    self.database.renew()

            if(directmail.text.find("sudo:")==0):
                pass




        else:
            print('DMはありません')



