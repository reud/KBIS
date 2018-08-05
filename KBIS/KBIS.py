# encoding:utf-8
from __future__ import unicode_literals
#フォローは手作業でお願いしますね・・・
import twitter
import __future__
import os
import sys
import openpyxl
import oauth2
import webbrowser
import time
import datetime
import RootCommand
import traceback
import LogWriterClassVer
import APIKeyReader
import DataBases
import Routine
import WordBox
import  traceback
import LINENotifer
LINENotifer.Notify.MessageCall('KBIS起動 1/5 (完全に最初)')
dir=''
apiR=APIKeyReader.Reader('../KEYS')
api=apiR.GetApi()
w=WordBox.WordBox()
devmode=False

try:
    print('mode:{0}'.format(sys.argv[1]))
    devmode=True
except:
    print('mode:real')
if(devmode):
    l=LogWriterClassVer.LogWriterClassVer('Log.txt')
else:
    l=LogWriterClassVer.LogWriterClassVer('../../KBIS_Workingplace/Log.txt')
try:
    routine=Routine.Routine(api,devmode,dir)
except:
    LINENotifer.Notify.MessageCall(f'エラー発生\n{traceback.format_exc()}')
    traceback.print_exc()
    l.LogWrite('print',traceback.format_exc())
LINENotifer.Notify.MessageCall(f'起動終了しました。')
print('Finished Abnormally(Bad Endってかっこよくないですか？)')
