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
dir=''
apiR=APIKeyReader.Reader('../KEYS')
api=apiR.GetApi()
w=WordBox.WordBox()
try:
    print('mode:{0}'.format(sys.argv[1]))
    routine=Routine.Routine(api,True,dir)
except:
    traceback.print_exc()
    routine=Routine.Routine(api,False,dir)
    pass
