# encoding:utf-8
import LogWriterClassVer
import traceback
class RootCommand(object):#謎そしてクソコードなのでだれか直して頼む
    def __init__(self,api,memberList,command,arg1='none',arg2='none',arg3='none',arg4='none',arg5='none'):
        self.l=LogWriterClassVer.LogWriterClassVer()
        self.command=command
        self.arg1=arg1
        self.arg2=arg2
        self.arg3=arg3
        self.arg4=arg4
        self.arg5=arg5
        self.api=api
        self.commandValidity=False
        self.memberList=memberList
        self.autoTweetPlaceAtTL=True
        self.responcePlaceAtDM=True
    def GetAutoTweetState(self):
            return self.autoTweetPlaceAtTL
    def GetResponcePlace(self):
            return self.responcePlaceAtDM
    def CheckValidity(self):
        if(self.command=="ChangePlace"):
            if(self.arg1=="AutoTweet"):
                if(self.arg2=="DM" or self.arg2=="TL"):
                    self.AllValidityChanger(True)
            if(self.arg1=="Responce"):
                if(self.arg2=="DM" or self.arg2=="TL"):
                    self.AllValidityChanger(True)
        if(self.command=="CallUser"):
            if(self.arg1=="Direct" or self.arg1=="Hthan" or self.arg1=="Lthan" or self.arg1== "Equals" or self.arg1=="All"):
                self.api.PostDirectMessage(screen_name=self.api.VerifyCredentials().screen_name,text="妥当性:Maybe Safe \r\n CallUserコマンドはミスってても事前に妥当性を確認することができません。\r\n 気を付けてくださいね！")
                self.AllValidityChanger(True)
    def Renew(self,command,arg1='none',arg2='none',arg3='none',arg4='none',arg5='none'):#実際のコマンド実行はこちらで
        self.command=command
        self.arg1=arg1
        self.arg2=arg2
        self.arg3=arg3
        self.arg4=arg4
        self.arg5=arg5
        self.l.LogWrite("print","command,arg1,arg2,arg3,arg4,arg5 is "+str(command)+","+str(arg1)+","+str(arg2)+","+str(arg3)+","+str(arg4)+","+str(arg5))
        self.CheckValidity()
        self.ChallengeCommand()
    def ReList(self,api,memberList):
        self.memberList=memberList
        self.api=api
    def AllValidityChanger(self,cbool):
        self.commandValidity=cbool

    def ChallengeCommand(self):
        if(self.commandValidity):
           if(self.command=="ChangePlace"):
                if(self.arg1=="AutoTweet"):
                    if(self.arg2=="DM"):
                        self.autoTweetPlaceAtTL=False
                    elif(self.arg2=="TL"):
                        self.autoTweetPlaceAtTL=True
                    else:
                        self.api.PostDirectMessage(screen_name=self.api.VerifyCredentials().screen_name,text="arg2 invalid DM or TL plz")
                if(self.arg1=="Responce"):
                    if(self.arg2=="DM"):
                        self.responcePlaceAtDM=True
                    elif(self.arg2=="TL"):
                        self.responcePlaceAtDM=False
                    else:
                        self.api.PostDirectMessage(screen_name=self.api.VerifyCredentials().screen_name,text="arg2 invalid DM or TL plz")
           if(self.command=="CallUser"):
                count=0
                if(self.arg1=="All"):
                    for i in self.memberList:
                        try:
                            if(not(i.twiiterID=="none")):
                                if(i.money>0):
                                    self.api.PostDirectMessage(screen_name=i.twiiterID,text="【一斉送信】KBISよりお知らせです。\r\n\r\n"+i.name+"さんは現在 "+str(i.money)+"円 を滞納しています。\r\nお早めのお支払をお願い致します。")
                                elif(i.money==0):
                                    self.api.PostDirectMessage(screen_name=i.twiiterID,text="【一斉送信】KBISよりお知らせです。\r\n\r\n現在"+i.name+"さんの滞納/返金はありません。")
                                else:
                                    self.api.PostDirectMessage(screen_name=i.twiiterID,text="【一斉送信】KBISよりお知らせです。\r\n"+i.name+"さんには現在 "+str(i.money)+"円 の返金があります。\r\nご都合のよいときに会計担当へお知らせください。")
                                count=count+1
                                self.l.LogWrite("print",str(count))
                        except:
                            self.l.LogWrite("print",str(i.twiiterID)+"("+i.name+")"+"への送信に失敗")
                            self.l.LogWrite("print",traceback.format_exc())
                    self.api.PostDirectMessage(screen_name=self.api.VerifyCredentials().screen_name,text=str(count)+"人に送信しました")
                if(self.arg1=="Direct"):
                    key=False
                    for i in self.memberList:
                        if(i.twiiterID==self.arg2):
                            try:
                                self.api.PostDirectMessage(screen_name=i.twiiterID,text="KBISよりお知らせです。\r\n"+i.name+" さんは現在【"+str(i.money)+"円】を滞納しています。\r\n徴収額は活動頻度に関わらず部員全員に平等に割り振られています。お支払をお願いいたします。")
                                self.api.PostDirectMessage(screen_name=self.api.VerifyCredentials().screen_name,text="送信に成功しました（多分）")
                            except:
                                self.l.LogWrite("print",str(i.twiiterID)+"("+i.name+")"+"への送信に失敗")
                                self.l.LogWrite("print",traceback.format_exc())
                            key=True
                    if(not key):
                        self.api.PostDirectMessage(screen_name=self.api.VerifyCredentials().screen_name,text="該当するユーザーが見つかりませんでした。")
                        self.l.LogWrite("CantFind",self.arg2)
                if(self.arg1=="Hthan"):
                    count=0
                    try:
                        self.l.LogWrite("print","trying:"+str(int(self.arg2)))
                    except:
                        self.api.PostDirectMessage(screen_name=self.api.VerifyCredentials().screen_name,text="【注意】arg2は数字を入れてください")
                        return
                    for i in self.memberList:
                        try:
                            if(not (i.twiiterID=="none") and (i.money>int(self.arg2))):
                                self.api.PostDirectMessage(screen_name=i.twiiterID,text="KBISより、一定額以上を滞納されている方へのお知らせです。\r\n\r\n"+i.name+"さんは現在"+str(i.money)+"円 を滞納しています。\r\n1週間以内を目処にお支払をお願い致します。ご相談は会計担当まで。")
                                count=count+1
                        except:
                            self.l.LogWrite("print",str(i.twiiterID)+"("+i.name+")"+"への送信に失敗")
                            self.l.LogWrite("print",traceback.format_exc())
                    self.api.PostDirectMessage(screen_name=self.api.VerifyCredentials().screen_name,text=str(count)+"人に送信しました")
                if(self.arg1=="Lthan"):
                    count=0
                    try:
                        self.l.LogWrite("print","trying:"+str(int(self.arg2)))
                    except:
                        self.api.PostDirectMessage(screen_name=self.api.VerifyCredentials().screen_name,text="【注意】arg2は数字を入れてください")
                        return
                    for i in self.memberList:
                        try:
                            if(not (i.twiiterID=="none") and (i.money<int(self.arg2))):
                                self.api.PostDirectMessage(screen_name=i.twiiterID,text="KBISより、滞納額が一定以下の方へお知らせです。\r\n\r\n"+i.name+"さんは現在"+str(i.money)+"円 を滞納しています。\r\nご都合の良いときにお支払をお願い致します。")
                                count=count+1
                        except:
                            self.l.LogWrite("print",str(i.twiiterID)+"("+i.name+")"+"への送信に失敗")
                            self.l.LogWrite("print",traceback.format_exc())
                    self.api.PostDirectMessage(screen_name=self.api.VerifyCredentials().screen_name,text=str(count)+"人に送信しました")                    
                if(self.arg1=="Equals"):
                    count=0
                    try:
                        self.l.LogWrite("print","trying:"+str(int(self.arg2)))
                    except:
                        self.api.PostDirectMessage(screen_name=self.api.VerifyCredentials().screen_name,text="【注意】self.arg2は数字を入れてください")
                        return
                    for i in self.memberList:
                        if(not (i.twiiterID=="none") and (i.money==int(self.arg2))):
                            try:
                                self.api.PostDirectMessage(screen_name=i.twiiterID,text="KBISよりお知らせです。\r\n"+i.name+" さんは現在【"+str(i.money)+"円】を滞納しています。\r\n徴収額は活動頻度に関わらず部員全員に平等に割り振られています。お支払をお願いいたします。")
                                count=count+1
                            except:
                                self.l.LogWrite("print",str(i.twiiterID)+"("+i.name+")"+"への送信に失敗")
                                self.l.LogWrite("print",traceback.format_exc())
                    self.api.PostDirectMessage(screen_name=self.api.VerifyCredentials().screen_name,text=str(count)+"人に送信しました")  