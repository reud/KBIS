# coding:utf-8
from __future__ import unicode_literals
import twitter
import traceback
import os
class Reader(object):
    def __init__(self,dir):
        try:
            os.chdir(dir)
            print(os.getcwd()+r"/KEY を確認中...")
            if(os.name=='nt'):
                self.LOGFILE=open("KEY")
            else:
                self.LOGFILE=open("KEY")
            self.lines=self.LOGFILE.readlines()
            for line in self.lines:
                line=line.rstrip('\r\n')
            self.API_KEY=self.lines[0]
            self.API_SECRET=self.lines[1]
            self.ACCESS_TOKEN=self.lines[2]
            self.ACCESS_TOKEN_SECRET=self.lines[3]
            print("read as:\n{0}\n{1}\n{2}\n{3}\n".format(self.API_KEY,self.API_SECRET,self.ACCESS_TOKEN,self.ACCESS_TOKEN_SECRET))
            print("Change to Key now...")
            self.API_KEY=self.API_KEY.replace("API_KEY=","")
            self.API_SECRET=self.API_SECRET.replace("API_SECRET=","")
            self.ACCESS_TOKEN=self.ACCESS_TOKEN.replace("ACCESS_TOKEN=","")
            self.ACCESS_TOKEN_SECRET=self.ACCESS_TOKEN_SECRET.replace("ACCESS_TOKEN_SECRET=","")
            self.API_KEY=self.API_KEY[1:-2]
            self.API_SECRET=self.API_SECRET[1:-2]#kokomo
            self.ACCESS_TOKEN=self.ACCESS_TOKEN[1:-2]#koko yabai
            self.ACCESS_TOKEN_SECRET=self.ACCESS_TOKEN_SECRET[1:-1]
            print("read as:\n{0}\n{1}\n{2}\n{3}\n".format(self.API_KEY,self.API_SECRET,self.ACCESS_TOKEN,self.ACCESS_TOKEN_SECRET))

            self.api=twitter.Api(consumer_key=self.API_KEY,consumer_secret=self.API_SECRET,access_token_key=self.ACCESS_TOKEN,access_token_secret=self.ACCESS_TOKEN_SECRET)
            print("獲得したAPIの内容:"+str(self.api)+";{0}".format(isinstance(self.api,twitter.Api)))

            
        except:
            print("KEYの読み込みに失敗")
            traceback.print_exc()
            return      
    def GetApi(self):
        return self.api



