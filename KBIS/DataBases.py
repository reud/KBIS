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
            except KeyError:
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
                    except TypeError:
                        pass
            # Twitterアカウントとの結びつけ
            twitterbook = openpyxl.load_workbook(self.twitterBook)
            sheetTB = twitterbook['Sheet1']
            exist = False
            authority = None
            for i in range(1, 999):
                if (sheet.cell(row=(user + 3), column=2).value == sheetTB.cell(row=(i+1), column=1).value):
                    twitterName = sheetTB.cell(row=(i+1), column=2).value
                    if (sheetTB.cell(row=(i+1), column=3).value):
                        authority = sheetTB.cell(row=(i+1), column=3).value
                    exist = True

            #
            if(sheet.cell(row=(user + 3), column=2).value ):
                userList.append((gen, sheet.cell(row=(user + 3), column=2).value, twitterName, sum,sheet.cell(row=(user + 3), column=5).value, authority))
        return userList
    def renew(self):#一回全部消すか・・・
        workbook = openpyxl.load_workbook(self.moneyBook)
        select_sql = '''insert or ignore into users(gen,realname,twittername,money,remarks,authority) values (?,?,?,?,?,?)'''
        for i in range(self.MINGEN, self.MAXGEN):
            try:
                sheet = workbook['{0}G'.format(i)]
                self.cursor.executemany(select_sql, self.CreateUsersFromSheet(sheet, i))
            except KeyError:
                break
        select_sql = 'select * from users'
        for row in self.cursor.execute(select_sql):
            pass
    def Search(self,word1:str,word2:str)-> list:
        createTwitterUserTable='''create table if not exists TwitterExistsUser(gen int,realname TEXT,twittername TEXT,money int,remarks TEXT,authority TEXT,UNIQUE (realname,twittername)) '''
        self.cursor.execute(createTwitterUserTable)
        uReturnist=[]
        select_sql = '''select * from users where twittername is not null'''
        for row in self.cursor.execute(select_sql):
            uReturnist.append(row)
            #print(row)
        select_sql='''insert or ignore into TwitterExistsUser(gen,realname,twittername,money,remarks,authority) values (?,?,?,?,?,?)'''
        self.cursor.executemany(select_sql,uReturnist)
        select_sql = '''select * from TwitterExistsUser'''
        for row in self.cursor.execute(select_sql):
            pass
        returnList=[]
        #(word1,word2)
        #(at,本名 or twitterID or all)
        #(Lthan,money)
        #(Hthan,money)
        #(equals,money)
        #(get,root)
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
                            reacher=True
                        return returnList
        if(word1=='Lthan' or word1=='Hthan'):
            if(word1=='Lthan'):
                comparison='<'
            else:
                comparison='>'
            if(type(word2) is str):
                raise ValueError('SQLインジェクション的な操作は禁止されています。\n引数を確認して下さい。')
            call_sql=f'''select * from TwitterExistsUser where money{comparison}{word2}'''
            print(call_sql)
            for i in self.cursor.execute(call_sql):
                returnList.append(i)
            return returnList
        if(word1=='get'):
            if(word2=='root'):
                select_sql='''select * from TwitterExistsUser where authority=='su' '''
                print(select_sql)
                for i in self.cursor.execute(select_sql):
                    returnList.append(i)
                return returnList
        raise ValueError('一致するものが見つかりませんでした。')

