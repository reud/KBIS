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
        self.dbname = 'temp.db'
        try:
            os.remove(self.dbname)
        except:
            pass
        self.twitterBook = '../Tools/Twitter対応リスト.xlsx'
        self.moneyBook='../Tools/237585_個人支払出納管理簿.xlsx'
        self.connect = sqlite3.connect(self.dbname)
        self.cursor = self.connect.cursor()
        create_table = '''create table users(gen int,realname TEXT,twittername TEXT,money int,remarks TEXT,authority TEXT)'''
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
        self.connect.close()
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
            os.remove(self.dbname)
            self.connect = sqlite3.connect(self.dbname)
            self.cursor = self.connect.cursor()
            create_table = '''create table users(gen int,realname TEXT,twittername TEXT,money int,remarks TEXT,authority TEXT)'''
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
            self.connect.close()



