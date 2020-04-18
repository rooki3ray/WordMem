# #coding=utf-8

# from urllib import request
# from urllib import parse
# import json
# from bs4 import BeautifulSoup

# Request_URL="http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
# form_data={}
# form_data['i']='内存'
# form_data['from'] = 'AUTO'
# form_data['to'] = 'AUTO'
# form_data['smartresult'] = 'dict'
# form_data['doctype']='json'
# form_data['version']='2.1'
# form_data['keyfrom']='fanyi.web'
# form_data['action']='FY_BY_CLICKBUTTION'
# form_data['typoResult']='false'

# data=parse.urlencode(form_data).encode('utf-8')
# response=request.urlopen(Request_URL,data)
# html=response.read().decode('utf-8')
# translate_results = json.loads(html)
# # 找到翻译结果
# translate_result = translate_results["translateResult"][0][0]['tgt']
# # 打印翻译结果
# print("翻译的结果是：%s" % translate_result)

import requests
import re

# def phonetic_spelling(word):
#     word=word.replace(" ","_")
#     phoneticSpelling=""
#     #url的格式有规律
#     request=requests.get("https://en.oxforddictionaries.com/definition/"+word)
#     html=request.text
#     #查看网页发现音标所处的行HTML格式有规律 使用正则表达式描述
#     regularExpression = r'<span\s+class="phoneticspelling">/([^\/]*)/</span>'
#     matchObject = re.search(regularExpression,html,re.I)
#     if matchObject and matchObject.group(1):
#         phoneticSpelling = matchObject.group(1)
#         return '['+phoneticSpelling+']'
def phonetic_spelling(en='', cn='', mode='p'):
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
        return translation

# #测试
a = phonetic_spelling(en='indexing',mode='p')
b= a
print(a)
# #测试
# print(phonetic_spelling('Programme'))

# import pygame
# import time

# musicPath = "pronunciation\\cross.mp3"
# pygame.mixer.init()#初始化

# track = pygame.mixer.music.load(musicPath)#加载音乐
# pygame.mixer.music.play()#播放 

# # userIn = input()#输入空格暂停
# # if userIn == ' ':
# #     pygame.mixer.music.pause()
# # else:
# time.sleep(1)#表示音频的长度
# pygame.mixer.music.stop()


# import numpy as np
# b=np.random.choice(a=5, size=3, replace=False, p=None)
# print(b)
# import sys 
# from PyQt5 import QtWidgets, QtCore 
# app = QtWidgets.QApplication(sys.argv) 
# widget = QtWidgets.QWidget() 
# widget.resize(400, 100) 
# widget.setWindowTitle("This is a demo for PyQt Widget.") 
# widget.show() 
# exit(app.exec_())
# class a:
#     def __init__(self,c,d):
#         self.c=c
#         self.d=d
# q=a(1,2)
# w=a(3,4)
# e=[q,w]

# a=[1,2,3]
# for index, value in enumerate(a):
#     if value==1:
#         a[index]=0
#         print(type(index))
# print(a)
# a='mm12'
# print(a.isalpha())
# for i in a:
#     if i.isalpha():
#         print(i)
