#conding:UTF-8
import requests
import  random
import traceback
class Notify(object):
    def MessageCall(message:str):
        url='https://notify-api.line.me/api/notify'
        TOKEN='mEm6j3rWnJMzbJXVnZWNblAbEc00cRDcY76bmR8Ai84'
        headers={"Authorization":"Bearer "+TOKEN}
        message_sample= {"message" :  'your message'}
        params_message={"message":message}
        request_sample=requests.post(url,headers=headers,params=params_message)


