# encoding: utf-8
import  twitter
import  DataBases
import WatchLogReader
import  LogWriterClassVer
import  time
import  WordBox
developer_screen_name='reudest'
import os
import traceback
import  sys
import  RegularlyTweet
import LINENotifer
class Routine(object):
    def __init__(self,api:twitter.Api,devmode:bool,dir:str):
        """:type : twitter.Api"""
        if(devmode):
            self.logpath="Log.txt"
        else:
            self.logpath="../../KBIS_Workingplace/Log.txt"#カレントディレクトリが/KEYSになってる可能性が高い(原因は不明)
            #self.logpath="Log.txt"#カレントディレクトリが/KEYSになってる可能性が高い(原因は不明)

        print(self.logpath)
        self.logwriter=LogWriterClassVer.LogWriterClassVer(self.logpath)
        self.logwriter.LogWrite('print','起動成功')

        self.wordbox=WordBox.WordBox()
        self.database=DataBases.DataBases(devmode)
        LINENotifer.Notify.MessageCall('KBIS起動 2/5(DataBaseの構築成功)')
        self.api=api
        self.devmode=devmode
        self.dir=dir #use for ignoreList
        self.regularly_tweet=RegularlyTweet.Tweets(api,self.database.moneyBook,self.logpath)
        LINENotifer.Notify.MessageCall('KBIS起動 3/5(定期ツイートのインスタンス取得の成功)')
        self.Init()
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
        LINENotifer.Notify.MessageCall('KBIS起動 4/5(FirstRoutineを開始)')
        self.logwriter.LogWrite("print","KBISが起動しました。devmode:{0}".format(self.devmode))
        self.ignoreList = []
        if(not self.devmode):#本環境ではファイルから読み込む(ファイルあるの前提とする。)

            self.logwriter.LogWrite("print","Logファイルを読み込みます。")
            IgnoreListFile = open('../../KBIS_Workingplace/IgnoreList.txt')
            #IgnoreListFile = open('IgnoreList.txt')

            temp = IgnoreListFile.readline().strip()
            while (temp):
                print("ignoreリストからロード:" + str(temp))
                self.ignoreList.append(int(temp))
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
                if(self.devmode):
                    os.remove('../Tools/IgnoreList.txt')
                else:
                    os.remove('../../KBIS_Workingplace/IgnoreList.txt')
                    #os.remove('../Tools/IgnoreList.txt')

            except:#どうせファイルないくらいしかエラー起きないのでスルー
                pass

        LINENotifer.Notify.MessageCall('KBIS起動 5/5(完了)')
        print('60秒後にKBISのルーチンが開始されます。')
        return

    def GoRoutine(self):
        while(True):
            time.sleep(59)
            self.DirectMailReader()
            self.regularly_tweet.Check()
        pass
    def Init(self):
        self.FirstRoutine()
        self.GoRoutine()
    def DirectMailReader(self):

        try:
            self.directmails=self.api.GetDirectMessages()
        except:
            self.logwriter.LogWrite('print',traceback.format_exc())
            return
        #ここからignoreListに対応するダイレクトメールを削除
        for ignoreNum in self.ignoreList:
            for directmail in self.directmails:
                if(directmail.id==ignoreNum or directmail.sender_screen_name=='kbisnaikei'):
                    self.directmails.remove(directmail)
                    print('ignoreListにあったDMです。削除しています・・・　内容...:{0} from {1}'.format(directmail.text,directmail.sender_screen_name))
                    break#見つけたらfor文ごと終了させる。
                else:
                    #print(f'検索ちゅう・・・{directmail.id}and{ignoreNum}')
                    pass
        if(len(self.directmails)!=0):#DMを読み取る処理
            print('DMの件数は{0}件です。'.format(len(self.directmails)))
        for i in self.directmails:
            self.ignoreList.append(i.id)
        print("Ignoreファイルの更新を行います。")
        strings=''
        writingData = open('../../KBIS_Workingplace/IgnoreList.txt', 'w')
        for t in self.ignoreList:
            strings += str(t) + "\n"
        strings = strings.replace("\n\n", "\n")
        writingData.write(strings)
        writingData.close()
        print("Ignoreファイルの更新は終了しました。")
        #ここからDMの処理
        #devmode中はsudo機能とdev機能のどちらもdeveloperが使用可能 sudo calluserは自分に結果を通知
        #本環境は
        #権限はdev→sudo→registered→All のイメージ
        #[info]--情報要求 (registered User) fin
        #[register:[苗字] [名前]] 新規登録(All User) fin
        #[change:(新しいscreen_name)] ユーザーID変更(registered User) fin
        #[dev:speak (saying)] ツイート(developer)   dev only fin
        #[sudo:CallUser (arg**)] 絞り込み複数通知   sudo only (Hthan と Lthanのみ) fin
        #[m:(String)] 普通に話しかける用(一回のみ)　(All User)
        #[sudo:reload] データベースを再更新します。   sudo only　fin
        #[sudo:getDB (arg**)] CallUserと引数は同じで、指定したレコードを取得します。   sudo only fin
        #[help]ユーザの権限に合わせた使えるコマンドの案内をします。　
        #[q:(String)] 開発者に通知します。バグとか要望とか教えて下さい！
        #
        #ignoreListに入れる

        for directmail in self.directmails:
            print(f'DirectMessageの内容{directmail.text} from {directmail.sender_screen_name}')
            if(directmail.text.find("dev:")==0):
                directmail.text=directmail.text.replace('dev:','')
                #ここでdevが本当にdeveloperか確認する
                if(developer_screen_name==directmail.sender_screen_name):
                    if(directmail.text.find('speak ')==0):#speakの場合　ここの階層に新規コマンドを追加して下さい。 ex. dev:speak HelloWorld
                        directmail.text=directmail.text.replace('speak ','')
                        if(not self.devmode):
                            try:
                                self.api.PostUpdate(text=directmail.text)
                            except:
                                LINENotifer.Notify.MessageCall('speakコマンドの失敗')
                                LINENotifer.Notify.MessageCall(traceback.format_exc())
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
                try:
                    for i in self.database.Search('get','root'):
                        for strings in i:#ここから未テスト
                            if(strings==directmail.sender_screen_name):
                                authority=True
                except:
                    authority=False
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
                    elif(directmail.text.find('CallUser ')==0):
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
                                for list in self.database.Search('at',directmail.text.replace('at ','')):
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
                    elif(directmail.text.find('reload')==0):
                        self.database.renew()
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
                elif(directmail.text.find('register:')==0):
                    directmail.text=directmail.text.replace('register:','')
                    sendstr=self.database.RegisterOrChanger(directmail.text,directmail.sender_screen_name,True)
                    self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text=sendstr)
                    self.database.renew()
                elif(directmail.text.find('change:')==0):
                    directmail.text=directmail.text.replace('change:','')
                    sendstr=self.database.RegisterOrChanger(directmail.sender_screen_name,directmail.text)
                    self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text=sendstr)
                    self.database.renew()
                elif(directmail.text.find('m:')==0):
                    #普通に会話なのでなんもしなくていいんじゃない？
                    pass
                elif(directmail.text.find('q:')==0):
                    self.api.PostDirectMessage(screen_name=developer_screen_name,text='質問が届いています\r\n'+directmail.text.replace('q:',''))
                    self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text='開発者に伝えました！\r\nありがとうございました！')
                elif(directmail.text.find('help')==0):
                    self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text='[info]情報要求できます。\r\n'
                                                                                              '[register:(苗字)(半角スペース)(名前)]データベースに登録します。\r\n'
                                                                                              '[change:(新しいTwitterユーザ名)]データベースのあなたのTwitterアカウント情報を変更します。\r\n'
                                                                                              '[m:(文章)]文頭にm:がついたメッセージは構文判別されません（エラーが出ません）\r\n以下は管理者のコマンドです。'
                                                                                              'sudo:CallUser,getDB,reload ')
                else:
                    self.api.PostDirectMessage(screen_name=directmail.sender_screen_name,text='KBISが認識できない値を検出しました。 help と打って使用できるコマンドについて確認してください。')
        else:
            print('DMはありません')
    def ReNewIgnore(self):
        os.remove('IgnoreList.txt')
        ignorefile=open('IgnoreList.txt','a')
        


