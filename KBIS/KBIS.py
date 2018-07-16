# coding:utf-8
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
path='../Tools/237585_個人支払出納管理簿.xlsx'
dir=''
l=LogWriterClassVer.LogWriterClassVer()
db=DataBases.DataBases(path)
db.Search('At','All')
apiR=APIKeyReader.Reader('../KEYS')
api=apiR.GetApi()

try:
    print('mode:{0}'.format(sys.argv[1]))
    routine=Routine.Routine(api,db,True,dir)
except:
    routine=Routine.Routine(api,db,False,dir)
routine.Init()