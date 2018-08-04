# coding:utf-8
import twitter
import codecs
import __future__
import os
import sys
import openpyxl
import oauth2
import webbrowser
import time
import datetime
class LogWriterClassVer(object):
    def __init__(self,FilePath:str):
        self.path=FilePath
    def LogWrite(self,type1="print",arg1="none",arg2="none",arg3="none"):#第一引数はタイプ　第二引数はいろいろ
        try:
            LOGFILE=open(self.path,'a')#ここのパスを変えてください
        except:
            print("Log.txtの読み込みに失敗")
            return
        type1=str(type1)
        print("type1="+type1)
        time=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S ")
        if(type1=="send"):#arg1=true or false arg2=name  
            LOGFILE.write(str(time)+"Requwirement Result:"+str(arg1)+"From:"+str(arg2)+" Info"+str(arg3)+"\n")
        elif(type1=="switch"):#arg1=true or false
            pass
            #LOGFILE.write(str(time)+"AutoTweetSwitch:"+str(arg1)+"\n")
        elif(type1=="tweet"):
            LOGFILE.write(str(time)+" SutoTweeted"+"\n")
        elif(type1=="login"):
            LOGFILE.write(str(time)+"Turn on app"+"\n")
        elif(type1=="reset"):
            LOGFILE.write(str(time)+"Switch reseted"+"\n")
        elif(type1=="check"):#arg1=ダイレクトメールチェックの可否
            pass
            #LOGFILE.write(str(time)+"DirectmailCheck:"+str(arg1)+"\n")
        elif(type1=="TrueSU"):#arg1は要求者 arg2はコマンド　arg3は引数
            LOGFILE.write(str(time)+" :"+str(arg1)+"is root user and require"+str(arg2)+"."+"\n Arguments:"+str(arg3)+"\n")
        elif(type1=="FalseSU"):#arg1は要求者
            LOGFILE.write(str(time)+" no su user Requwired"+str(arg1))
        elif(type1=="CantFind"):#arg1は要求先
            LOGFILE.write(str(time)+" :CantFindUser at Direct　From:"+str(arg1))
        elif(type1=="print"):#arg1は文字列
            LOGFILE.write(str(time)+"Output to console:\n"+str(arg1))
            LOGFILE.write("\n///////END\n")
            print(str(arg1))
        else:
            LOGFILE.write(str(time)+"Invalid Requirement"+" type1="+type1)
        LOGFILE.close()
        return


