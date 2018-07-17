# coding :utf-8
import sqlite3
import openpyxl
import traceback
import os

class DataBases(object):
    def __init__(self, EXCEL_PATH):
        self.MAXGEN = 99
        self.MINGEN = 15
        self.EXCELFILE = EXCEL_PATH
        try:
            os.remove(":memory:")
        except:
            pass
        self.twitterBook = '../Tools/Twitter対応リスト.xlsx'
        self.moneyBook='../Tools/237585_個人支払出納管理簿.xlsx'
        self.connect = sqlite3.connect(":memory:")
        self.cursor = self.connect.cursor()
        create_table = '''create table users(gen int,realname TEXT,twittername TEXT,money int,remarks TEXT,authority TEXT,UNIQUE (realname,twittername)) '''
        self.sql = 'insert into users (gen,realname,twittername,money,remarks,authority) values (?,?,?,?,?,?)'
        workbook = openpyxl.load_workbook(self.moneyBook)
        self.cursor.execute(create_table)
        for i in range(self.MINGEN, self.MAXGEN):
            try:
                sheet = workbook['{0}G'.format(i)]
                self.cursor.executemany(self.sql, self.CreateUsersFromSheet(sheet, i))
            except:
                traceback.print_exc()
                break
        if (not sheet): print('null get')
        print(str(sheet))
        print('Hello DB')
        select_sql = 'select * from users'
        for row in self.cursor.execute(select_sql):
            print(row)
    def CreateUsersFromSheet(self, sheet, gen):  # SQLに追加できるように手に入れたデータを変換する
        userList = []
        for user in range(1, 300):
            # moneyCreating
            sum = 0
            for debt in range(8, 200):
                if (sheet.cell(row=(user + 3), column=debt).value):
                    try:
                        sum += int(sheet.cell(row=(user + 3), column=debt).value)
                    except:
                        traceback.print_exc()
                        print('May error is datetime its ok')
            # Twitterアカウントとの結びつけ
            twitterbook = openpyxl.load_workbook(self.twitterBook)
            sheetTB = twitterbook['Sheet1']
            exist = False
            authorityExist = False
            for i in range(1, 999):
                if (sheet.cell(row=(user + 3), column=2).value == sheetTB.cell(row=(i+1), column=1).value):
                    twitterName = sheetTB.cell(row=(i+1), column=2).value
                    if (sheetTB.cell(row=i, column=3).value):
                        authority = sheetTB.cell(row=i, column=3).value
                        authorityExist = True
                    exist = True

            if (not exist): twitterName = 'none'
            if (not authorityExist): authority = 'none'
            #
            if(sheet.cell(row=(user + 3), column=2).value ):
                userList.append((gen, sheet.cell(row=(user + 3), column=2).value, twitterName, sum,sheet.cell(row=(user + 3), column=5).value, authority))
        return userList
    def renew(self):
        self.cursor = self.connect.cursor()
        #create_table = '''create table users(gen int,realname TEXT,twittername TEXT,money int,remarks TEXT,authority TEXT,UNIQUE (realname,twittername))'''
        workbook = openpyxl.load_workbook(self.moneyBook)
        self.cursor.execute(create_table)
        for i in range(self.MINGEN, self.MAXGEN):
            try:
                sheet = workbook['{0}G'.format(i)]
                self.cursor.executemany(self.sql, self.CreateUsersFromSheet(sheet, i))
            except:
                traceback.print_exc()
                break
        if (not sheet): print('null get')
        print(str(sheet))
        print('Hello DB')
        select_sql = 'select * from users'
        for row in self.cursor.execute(select_sql):
            print(row)
    def Search(self,word1:str,word2:str)-> list:
        self.cursor=self.connect.cursor()
        createTwitterUserTable='''create table if not exists TwitterExistsUser(gen int,realname TEXT,twittername TEXT,money int,remarks TEXT,authority TEXT,UNIQUE (realname,twittername)) '''
        self.cursor.execute(createTwitterUserTable)
        uReturnist=[]
        select_sql = '''select * from users where twittername is not null'''
        print('\n\n\n\nsearch start'+str(self.cursor.execute(select_sql)))
        for row in self.cursor.execute(select_sql):
            uReturnist.append(row)
            #print(row)
        select_sql='''insert or ignore into TwitterExistsUser(gen,realname,twittername,money,remarks,authority) values (?,?,?,?,?,?)'''
        self.cursor.executemany(select_sql,uReturnist)
        self.cursor.executemany(select_sql,uReturnist)
        select_sql = '''select * from TwitterExistsUser'''
        for row in self.cursor.execute(select_sql):
            print(row)
        print('FinishOutput')



        returnList=[]
        #(word1,word2)
        #(at,本名 or twitterID or all)
        #(Lthan,money)
        #(Hthan,money)
        #(equals,money)
        if(word1=='at'):
            if(word2=='all'):
                at_all_sql='''select * from TwitterExistsUser'''
                for data in self.cursor.execute(at_all_sql):
                    returnList.append(data)
                return returnList
            else:#本名 or twitterID
                print('{0}をTwitterIDから検索中...'.format(word2))
                twitterID_sql='''select twittername from TwitterExistsUser'''
                for data in self.cursor.execute(twitterID_sql):
                    #なんかカッコとかついてるので取る
                    ddata0=str(data).replace('(','')
                    ddata1=ddata0.replace(')','')
                    ddata2=ddata1.replace('\'','')
                    ddata_final=ddata2.replace(',','')
                    #ここでddata_finalがアレ
                    print(ddata_final)
                    if(ddata_final==word2):
                        print('twitterIDが一致しました。 そのユーザを取得します。')

                        userSearch_sql='''select * from TwitterExistsUser where twittername='{0}' '''.format(word2)
                        if (not self.cursor.execute(userSearch_sql)):
                            raise ValueError('kasu')
                        reacher=False
                        for i in self.cursor.execute(userSearch_sql):
                            if(reacher):
                                raise AssertionError('二つ以上の要素を持ってしまう致命的なエラー')
                            returnList.append(i)
                            print(i)
                            reacher=True
                        return returnList
                print('TwitterIDは一致しませんでした。本名から検索します。')
                #
                print('{0}を本名から検索中...'.format(word2))
                realname_sql='''select realname from TwitterExistsUser'''
                for data in self.cursor.execute(realname_sql):
                    #なんかカッコとかついてるので取る
                    ddata0=str(data).replace('(','')
                    ddata1=ddata0.replace(')','')
                    ddata2=ddata1.replace('\'','')
                    ddata_final=ddata2.replace(',','')
                    #ここでddata_finalがアレ
                    print(ddata_final)
                    if(ddata_final==word2):
                        print('本名が一致しました。 そのユーザを取得します。')
                        userSearch_sql='''select * from TwitterExistsUser where realname='{0}' '''.format(word2)
                        if (not self.cursor.execute(userSearch_sql)):
                            raise ValueError('kasu')
                        reacher=False
                        for i in self.cursor.execute(userSearch_sql):
                            if(reacher):
                                raise AssertionError('二つ以上の要素を持ってしまう致命的なエラー')
                            returnList.append(i)
                            print(i)
                            reacher=True
                        return returnList
        raise ValueError('一致するものが見つかりませんでした。')

