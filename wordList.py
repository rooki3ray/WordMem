import sqlite3
import numpy as np
import time
from word import Word
import os
import sys
import wget
import requests
import re
import pygame

class wordlist:
    def __init__(self, filename='wordlist.txt', dbname='wordlist.db', target=50):
        self.wordList = []
        self.unknownList = []
        self.rememberList = []
        self.todayList = []
        self.todayunknownList = []
        self.todayrememberList = []
        self.filename = filename
        self.dbname = dbname
        self.target = target
        if not os.path.exists(dbname):
            self.read_wordlist_from_file()
            self.create_sql()
        else:
            self.read_from_sql(dbname)
        self.sort_by_alphabet()
        self.arrange_todaylist()
        self.nextword()

    def read_wordlist_from_file(self):
        wordid = []
        word = []
        translation = []
        try:
            with open(self.filename) as f:
                for line in f:
                    curLine = line.strip().split(' ')
                    wordid.append(int(curLine[0]))
                    word.append(curLine[1])
                    translation.append(curLine[2])
        except FileNotFoundError:
            print("No Such File!")
        d = []
        for i in wordid:
            p = self.get_from_youdao(en=word[i-1],mode='p')
            singleword = Word(id=i, enword=word[i-1], cntranslation=translation[i-1], phonetic=p)
            # print(p, i)
            # if p==None:
                # d.append(word[i-1])
            self.wordList.append(singleword)
        for i in self.wordList:
            # print(i.enWord)
            if i.finished:
                self.rememberList.append(i)
            else:
                self.unknownList.append(i)

    def create_sql(self):
        db = sqlite3.connect(self.dbname)
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS wordlist (
                         ID  INT NOT NULL,
                         ENGLISH  VARCHAR(100) NOT NULL,
                         CHINESE  VARCHAR(100) NOT NULL,
                         PHONETIC VARCHAR(100) NOT NULL,
                         LASTTIME VARCHAR(100) NOT NULL,
                         FINISHED INT)""")
        total_count = len(self.wordList)

        for word in self.wordList:
            try:
                cursor.execute("""INSERT INTO wordlist (ID, ENGLISH, CHINESE, PHONETIC, LASTTIME, FINISHED) 
                                VALUES ({i}, '{ew}', '{ce}', '{ph}', '{lt}', {f})""".format(
                                i=word.id, ew=word.enWord, ce=word.cnTranslation, ph=word.phonetic, lt=word.lastTime, f=word.finished))
                db.commit()
            except:
                # 如果发生错误则回滚
                db.rollback()
                print("[ERROR] 执行第", word.id, "个时发生错误。数据库已回滚", end=' ')
                print(word.enWord, word.phonetic)
        db.close()

    def read_from_sql(self, db_name):
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        r = cursor.execute("""SELECT * FROM wordlist""")
        result = r.fetchall()
        total_count = len(result)
        for i in result:
            self.wordList.append(Word(id=i[0], enword=i[1], cntranslation=i[2], phonetic=i[3], lasttime=i[4], finished=i[5]))
        db.close()
        for i in self.wordList:
            if i.finished:
                self.rememberList.append(i)
            else:
                self.unknownList.append(i)

    def __iter__(self):
        return iter(self.wordList)

    def __len__(self):
        return len(self.wordList)

    def arrange_todaylist(self):
        if len(self.rememberList) == 0:
            rem = 0
        elif len(self.rememberList) < self.target*0.4:
            rem = len(self.rememberList)
            for i in self.rememberList:
                self.todayList.append(i)
        else:
            rem = int(self.target*0.4)
            for i in np.random.choice(self.rememberList, size=rem, replace=False, p=None):
                self.todayList.append(i)

        unk = self.target - rem
        if len(self.unknownList) < unk:
            for i in self.unknownList:
                self.todayList.append(i)
        elif len(self.unknownList) >= unk:
            for i in np.random.choice(self.unknownList, size=unk, replace=False, p=None):
                self.todayList.append(i)
        else:
            pass
        for i in self.todayList:
            i.testedCount = 0
            i.correctCount = 0
            self.todayunknownList.append(i)

    def nextword(self):
        try:
            self.thisword = np.random.choice(self.todayunknownList, size=1, replace=False, p=None)[0]
        except ValueError:
            return False
        else:
            return True

    def IRemember(self):
        self.thisword.testedCount += 1
        self.thisword.correctCount += 1 
        for index, i in enumerate(self.todayunknownList):
            if i.enWord == self.thisword.enWord:
                self.todayunknownList[index] = self.thisword
                # print(self.todayunknownList[index].testedCount)
        if self.thisword.testedCount >= 4 and self.thisword.correctCount/self.thisword.testedCount >= 0.75:
            if self.thisword in self.todayunknownList: 
                self.todayunknownList.remove(self.thisword)
            if self.thisword not in self.todayrememberList: 
                self.todayrememberList.append(self.thisword)
            self.update_db(word=self.thisword, mode='update')
        return self.nextword()
    
    def IDonotRemember(self):
        self.thisword.testedCount +=1
        for index, i in enumerate(self.todayunknownList):
            if i.enWord == self.thisword.enWord:
                self.todayunknownList[index] = self.thisword
        return self.nextword()

    def update_db(self, word=None, en_word='', cn_word='', mode=''):
        db = sqlite3.connect(self.dbname)
        cursor = db.cursor()
        if mode=='update':
            try:
                # print("""UPDATE wordlist SET LASTTIME = '{t}', FINISHED = FINISHED + 1 WHERE ENGLISH = '{wd}'""".format(t=time.ctime(), wd=word.enWord))
                cursor.execute("""UPDATE wordlist SET LASTTIME = '{t}', FINISHED = FINISHED + 1 WHERE ENGLISH = '{wd}'""".format(t=time.ctime(), wd=word.enWord))
                db.commit()
            except:
                db.rollback()
                print("[ERROR] 发生错误!数据库已回滚!", end=' ')
                print(word)
        elif mode=='add':
            if en_word=='':
                print('[INFO] 请检查是否完整输入!')
                return
            else:
                if en_word.isalpha() and cn_word=='':
                    cn = self.get_from_youdao(en=en_word, mode='c')
                    print('[INFO] 请检查是否完整输入!', end='')
                    if len(cn):
                        print('已经为您查找到释义：'+cn)
                    else:
                        print('在词典中找不到该词！')
                    return cn
            if cn_word=='':
                print('[INFO] 请检查是否完整输入!')
                return
            if not en_word.isalpha():
                print('[ERROR] 请检查您的英文输入!')
                return
            if '.' not in cn_word:
                print('[ERROR] 请正确输入词性!如n. v. vt. vi. prep. a. ad.')
                return
            flag = 0
            for index, i in enumerate(self.wordList):
                if i.enWord == en_word:
                    flag = 1
                    break;
            if flag:
                print('[INFO] 该单词已存在！请直接查询~')
                return
            # r = cursor.execute("""SELECT TOP * FROM wordlist ORDER BY begin_date DESC""")
            # result = r.fetchall()
            p = self.get_from_youdao(en=en_word, mode='p')
            self.proun_download(en_word)
            newWord = Word(id=len(self.wordList)+1, enword=en_word.strip(), cntranslation=cn_word, phonetic=p)
            self.wordList.append(newWord)
            self.unknownList.append(newWord)
            cursor.execute("""INSERT INTO wordlist (ID, ENGLISH, CHINESE, PHONETIC, LASTTIME, FINISHED) 
                                VALUES ({i}, '{ew}', '{ct}', '{ph}', '{lt}', {f})""".format(
                                i=newWord.id, ew=newWord.enWord, ct=newWord.cnTranslation, ph=p, lt=newWord.lastTime, f=newWord.finished))
            db.commit()
            print("[INFO] [+en_word+', '+p+', '+cn_word+] 已经添加!", end='')
            print(" 录入时间：",time.ctime())
        db.close()

    def search(self, en_word):
        db = sqlite3.connect(self.dbname)
        cursor = db.cursor()
        r = cursor.execute("""select * from wordlist where ENGLISH  = '{ew}'""".format(ew=en_word))
        result = r.fetchall()
        if len(result):
            return [result[0][1],result[0][2]]
        else:
            return []

    def fuzzsearch(self, en_word):
        try:
            db = sqlite3.connect(self.db_name)
        except AttributeError:
            db = sqlite3.connect(os.path.join(sys.path[0], 'wordlist.db'))
        cursor = db.cursor()
        sql = """select ENGLISH, CHINESE from wordlist where ENGLISH like '%"""+en_word+"""%' --case-insensitive"""
        q = cursor.execute(sql)
        query = q.fetchall()
        if len(query):
            return query
        else:
            return []

    def sort_by_alphabet(self):
        self.wordList = sorted(self.wordList, key=lambda x: x.enWord[0])
        return self.wordList

    def proun_download(self, enword):
        img_url = 'https://fanyi.baidu.com/gettts?lan=uk&text='+enword+'&spd=3&source=web'
        wget.download(img_url ,"pronunciation\\"+enword+".mp3")
        print("[INFO] ")

    def pronunciation(self):
        musicPath = "pronunciation\\"+self.thisword.enWord+".mp3"
        pygame.mixer.init()#初始化
        track = pygame.mixer.music.load(musicPath)#加载音乐
        pygame.mixer.music.play()#播放 
        time.sleep(1)#表示音频的长度
        pygame.mixer.music.stop()

    def get_from_youdao(self, en='', cn='', mode='p'):
        en = en.replace(" ","_")
        phoneticSpelling = ""
        #url的格式有规律
        request = requests.get("http://dict.youdao.com/w/"+en)
        html = request.text
        if mode=='p':
            #查看网页发现音标所处的行HTML格式有规律 使用正则表达式描述
            regularExpression = r'<span\s+class="phonetic">(.*)</span>'
            matchObject = re.search(regularExpression,html,re.I)
            if matchObject:
                if matchObject.group(1):
                    phoneticSpelling = matchObject.group(1)
                    return phoneticSpelling.replace('\'','\'\'')
        elif mode=='c':
            translation = ''
            regularExpression = r"<li>([a-z].*)</li>"
            matchObject = re.findall(regularExpression,html,re.I)
            for i in matchObject:
                translation += i + ' '
            return translation.replace(' ', '')

    # def sort_by_date(self):
    #     self.wordList = sorted(self.wordList, key=lambda x: x.recorded_date())
    #     return self.wordList

    # def txtinit():
    #     if not os.path.exists('wordlist.txt'):
    #         with open('words.txt') as f1:
    #             with open('wordlist.txt', 'w') as f2:
    #                 for line in f1:
    #                     curLine = line.strip().split(" ")
    #                     f2.write(curLine[0].strip('.') + ' '+
    #                              curLine[1] + ' '+
    #                              ''.join(curLine[x] for x in range(2,len(curLine))) + '\n')

    # def txt2db():
    #
    #     with open('wordlist.txt') as f:
    #         for line in f:
    #             curLine = line.strip().split(' ')
    #             self.wordid.append(curLine[0])
    #             self.word.append(curLine[1])
    #             self.translation.append(curLine[2])

if __name__ == '__main__':
    a=wordlist()

    # print(a.thisword.enWord)
    # print(len(a.todayunknownList))

    # for i in a.todayList:
    #     print(i.enWord, i.testedCount)
    # print(a.fuzzsearch('memo'))
    # print(a.thisword.correctCount)
    # print(len(a.todayunknownList))
    # print(len(a.todayList))

    # print(a.thisword.enWord)
    
    # for i in a.todayunknownList:
    #     b = b+1
    #     print(i.enWord)
    # print(len(a.unknownList))
    # c=np.random.choice(a.wordList, size=2, replace=False, p=None)
    # print(c)
    # d=[]
    # for i in c:
    #     d.append(i)
    # print(d)

    
