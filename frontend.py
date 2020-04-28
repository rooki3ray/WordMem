#-*-coding:utf-8-*-
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QProgressBar, QPushButton, QLabel, QSystemTrayIcon, QMenu, QAction
import os
import sys
import math
import time
from wordList import * 
import ctypes
import threading
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("WordMem")

class MainWindow(QtWidgets.QDialog):        #主窗口
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setStyleSheet("#MainWindow{border-image:url(./style/MainWindow/background.png)}")
        self.setWindowIcon(QtGui.QIcon("./style/Window/icon.png"))
        self.resize(450, 600)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(self.width(), self.height()); 

        self.miniButton = QtWidgets.QPushButton(self)    # 最小化按钮
        self.miniButton.setGeometry(QtCore.QRect(380, 10, 20, 20))
        self.miniButton.clicked.connect(self.showMinimized)
        self.miniButton.setStyleSheet('''border-image:url(./style/Window/minimize.png); border-radius:12px;''')  

        self.closeButton = QtWidgets.QPushButton(self)    # 关闭按钮
        self.closeButton.setGeometry(QtCore.QRect(420, 10, 20, 20))
        self.closeButton.clicked.connect(self.closeEvent)
        self.closeButton.setStyleSheet('''border-image:url(./style/Window/close.png); border-radius:12px;''')  

        self.deButton = QtWidgets.QPushButton(self)      # 默认空按钮，避免回车激活其他按钮
        self.deButton.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.deButton.setDefault(True)

        ft = QtGui.QFont()
        ft.setFamily('幼圆')
        ft.setBold(True) 
        ft.setPointSize(15) 
        ft.setWeight(75) 
        self.beginButton = QtWidgets.QPushButton(self)    # 背单词按钮
        self.beginButton.setGeometry(QtCore.QRect(110, 320, 220, 50))
        self.beginButton.setObjectName("begin")
        self.beginButton.setCursor(Qt.PointingHandCursor)
        self.beginButton.clicked.connect(self.beginButtonClicked)
        self.beginButton.setFont(ft)
        self.beginButton.setStyleSheet('''background:#6DDF6D;border-radius:5px;''')

        self.addButton = QtWidgets.QPushButton(self)      # 添加按钮
        self.addButton.setGeometry(QtCore.QRect(110, 390, 220, 50))
        self.addButton.setObjectName("add")
        self.addButton.setCursor(Qt.PointingHandCursor)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.addButton.setFont(ft)
        self.addButton.setStyleSheet('''background:#F76677;border-radius:5px;''')
 
        self.tray = QSystemTrayIcon() #创建系统托盘对象
        self.tray.setIcon(QtGui.QIcon('style\\Window\\icon.png')) #设置系统托盘图标
        self.tray.activated[QSystemTrayIcon.ActivationReason].connect(self.iconActivated) #设置托盘点击事件处理函数
        self.tray_menu = QMenu(QApplication.desktop()) #创建菜单
        self.RestoreAction = QAction(u'还原 ', self, triggered=self.show) #添加一级菜单动作选项(还原主窗口)
        self.QuitAction = QAction(u'退出 ', self, triggered=self.quit) #添加一级菜单动作选项(退出程序)
        self.tray_menu.addAction(self.RestoreAction) #为菜单添加动作
        self.tray_menu.addAction(self.QuitAction)
        self.tray.setContextMenu(self.tray_menu) #设置系统托盘菜单
        self.tray.show()
        # self.tray.showMessage(u"标题", '托盘信息内容', icon=1) 

        self.tipButton = QtWidgets.QPushButton(self)      # 信息按钮
        self.tipButton.setGeometry(QtCore.QRect(110, 460, 220, 50))
        self.tipButton.setObjectName("info")
        self.tipButton.setCursor(Qt.PointingHandCursor)
        self.tipButton.clicked.connect(self.tipButtonClicked)
        self.tipButton.setFont(ft)
        self.tipButton.setStyleSheet('''background:#F7D674;border-radius:5px;''')

        ft2 = QtGui.QFont()
        ft2.setFamily('Consolas')
        ft2.setBold(True) 
        ft2.setPointSize(33) 
        ft2.setWeight(75) 
        self.target = QLabel(self)            # 今日进度
        self.target.setGeometry(QtCore.QRect(160, 90, 130, 50))
        self.target.setAlignment(QtCore.Qt.AlignCenter)
        self.target.setText(str(math.ceil(len(w.unknownList)/(w.target*0.6)))+'天')
        self.target.setStyleSheet("color:white")
        self.target.setFont(ft2) 

        self.pbar = QProgressBar(self)                      # 总进度条
        self.pbar.setGeometry(QtCore.QRect(50, 210, 380, 15))
        self.pbar.setValue(len(w.rememberList)/len(w.wordList)*100)
        
        ft3 = QtGui.QFont()
        ft3.setFamily('宋体')
        ft3.setBold(True) 
        ft3.setPointSize(12) 
        ft3.setWeight(75) 
        self.label1 = QLabel(self)                          # 总进度
        self.label1.setGeometry(QtCore.QRect(50, 240, 100, 25))
        self.label1.setText("当前进度：")
        self.label1.setStyleSheet("color:white")
        self.label1.setAlignment(QtCore.Qt.AlignLeft)
        self.label1.setFont(ft3)
        self.label2 = QLabel(self)
        self.label2.setGeometry(QtCore.QRect(300, 240, 100, 25))
        self.label2.setText(str(len(w.rememberList))+"/"+str(len(w.wordList)))
        self.label2.setStyleSheet("color:white")
        self.label2.setAlignment(QtCore.Qt.AlignRight)
        self.label2.setFont(ft3)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "WordMem"))
        self.beginButton.setText(_translate("beginButton", "开 始 学 习"))
        self.addButton.setText(_translate("addButton", "查询/添加单词"))
        self.tipButton.setText(_translate("infoButton", "Tip 形 式"))

    #界面上关闭按钮
    def closeEvent(self, event):
        # event.ignore()  # 忽略关闭事件
        self.hide()  # 隐藏窗体

    def quit(self):
        try:
            self.tipWindow.flag=False
        except AttributeError:
            pass
        app.exit()
         
    def iconActivated(self, reason):  # 托盘图标点击处理
        if reason == QSystemTrayIcon.DoubleClick:   # 双击处理
            if self.isHidden():
                self.show()
            else:
                self.hide()

    def beginButtonClicked(self):
        self.rememberWindow = rememberWindow()
        self.rememberWindow.show()

    def addButtonClicked(self):
        self.addWindow = addWindow()
        self.addWindow.show()

    def tipButtonClicked(self):
        self.hide()
        self.tipWindow = tipWindow()
        self.tipWindow.show()

class rememberWindow(QtWidgets.QDialog):    # 单词记忆窗口
    def __init__(self):
        super(rememberWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("rememberWindow")
        self.setStyleSheet("#rememberWindow{border-image:url(./style/RemWindow/background.png);}")
        self.setWindowIcon(QtGui.QIcon("./style/Window/icon.png"))
        self.resize(450, 600)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(self.width(), self.height()); 

        self.miniButton = QtWidgets.QPushButton(self)    # 最小化按钮
        self.miniButton.setGeometry(QtCore.QRect(380, 10, 20, 20))
        self.miniButton.clicked.connect(self.showMinimized)
        self.miniButton.setStyleSheet('''border-image:url(./style/Window/minimize.png); border-radius:12px;''')  

        self.closeButton = QtWidgets.QPushButton(self)    # 关闭按钮
        self.closeButton.setGeometry(QtCore.QRect(420, 10, 20, 20))
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStyleSheet('''border-image:url(./style/Window/close.png); border-radius:12px;''')  
        
        self.deButton = QtWidgets.QPushButton(self)      # 默认空按钮，避免回车激活其他按钮 
        self.deButton.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.deButton.setDefault(True)

        ft = QtGui.QFont()
        ft.setFamily('Consolas')
        ft.setBold(True) 
        ft.setPointSize(25) 
        ft.setWeight(75) 
        self.word = QLabel(self)            # 当前单词
        self.word.setGeometry(QtCore.QRect(35, 40, 380, 40))
        self.word.setText(w.thisword.enWord)
        self.word.setAlignment(QtCore.Qt.AlignCenter)
        self.word.setStyleSheet('''color:white;''')
        self.word.setFont(ft)

        self.pronunciation = QtWidgets.QPushButton(self)    # 发音
        self.pronunciation.setGeometry(QtCore.QRect(215, 125, 20, 20))
        self.pronunciation.setStyleSheet('''border-image:url(./style/RemWindow/pronunciation.png); border-radius:12px;''')
        self.pronunciation.clicked.connect(w.pronunciation) # 播放发音

        self.phonetic = QLabel(self)            # 音标
        self.phonetic.setGeometry(QtCore.QRect(35, 80, 380, 40))
        self.phonetic.setText(w.thisword.phonetic)
        self.phonetic.setAlignment(QtCore.Qt.AlignCenter)
        self.phonetic.setStyleSheet('''color:white;''')
        self.phonetic.setFont(ft)

        ft2 = QtGui.QFont()
        ft2.setFamily('幼圆')
        ft2.setBold(True) 
        ft2.setPointSize(15) 
        ft2.setWeight(75) 
        self.transButton = QtWidgets.QPushButton(self)      # 释义
        self.transButton.setGeometry(QtCore.QRect(10, 160, 430, 340))
        self.transButton.setObjectName("translationButton")
        self.transButton.setCursor(Qt.PointingHandCursor)
        self.transButton.clicked.connect(self.transButtonClicked)
        self.transButton.setFont(ft2)
        self.transButton.setStyleSheet('''background-color:transparent; color:white; border:none;''')
        # self.transButton.setGraphicsEffect(op)
        self.flag=0     # 记录按钮状态
        # self.transButton.setStyleSheet("border-image:url(./images/style/MyChat/sendtxtbutton.png);")
    
        self.remButton = QtWidgets.QPushButton(self)        # 认识按钮
        self.remButton.setGeometry(QtCore.QRect(10, 510, 200, 50))
        self.remButton.setObjectName("rememberButton")
        self.remButton.setStyleSheet('''border:none; background-color:#43C494;''')
        self.remButton.setFont(ft2)
        self.remButton.clicked.connect(self.remButtonClicked)

        self.nremButton = QtWidgets.QPushButton(self)       # 不认识按钮
        self.nremButton.setGeometry(QtCore.QRect(240, 510, 200, 50))
        self.nremButton.setObjectName("notrememberButton")
        self.nremButton.setStyleSheet('''border:none; background-color:#43C494;''')
        self.nremButton.setFont(ft2)
        self.nremButton.clicked.connect(self.nremButtonClicked)

        self.p = QLabel(self)           # 今日进度
        self.p.setGeometry(QtCore.QRect(10, 570, 90, 15))
        # self.p.setStyleSheet('''border:none; background-color:#43C494;''')
        self.p.setText('今日进度:'+str(len(w.todayrememberList))+"/"+str(len(w.todayList)))
        self.p.setStyleSheet('''color:white;''')
        ft2.setPointSize(8)
        self.p.setFont(ft2)

        self.pbar = QProgressBar(self)     # 进度条
        self.pbar.setGeometry(QtCore.QRect(110, 570, 340, 15))
        self.pbar.setValue(len(w.todayrememberList)/len(w.todayList)*100)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("rememberWindow", "WordMem"))
        self.transButton.setText(_translate("translatonButton", '点击屏幕显示释义'))
        self.remButton.setText(_translate("rememberButton", '认识'))
        self.nremButton.setText(_translate("notrememberButton", '不认识'))

    def transButtonClicked(self):   # 释义按钮状态切换
        if self.flag==0:   #flag用以记录按钮状态 
            self.flag = 1
            self.transButton.setText(w.thisword.cnTranslation)
        else:
            self.flag = 0
            self.transButton.setText('点击屏幕显示释义')

    def remButtonClicked(self):
        flag = w.IRemember()
        if flag:
            self.transButton.setText('您已经完成了今日任务！')
        else:
            self.word.setText(w.thisword.enWord)
            self.transButton.setText('点击屏幕显示释义')
            self.flag=0
        self.pbar.setValue(len(w.todayrememberList)/len(w.todayList)*100)
        self.p.setText('今日进度:'+str(len(w.todayrememberList))+"/"+str(len(w.todayList)))

    def nremButtonClicked(self):
        w.IDonotRemember()
        self.word.setText(w.thisword.enWord)
        self.transButton.setText('点击屏幕显示释义')
        self.flag=0
        self.pbar.setValue(len(w.todayrememberList)/len(w.todayList)*100)
        self.p.setText('今日进度:'+str(len(w.todayrememberList))+"/"+str(len(w.todayList)))
    
class EmittingStream(QtCore.QObject):   # 用于输出重定向
        textWritten = QtCore.pyqtSignal(str)
        def write(self, text):
            self.textWritten.emit(str(text))

class addWindow(QtWidgets.QDialog):
    def __init__(self):
        super(addWindow, self).__init__()
        self.setupUi()
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten) # 用于输出重定向
        sys.stderr = EmittingStream(textWritten=self.normalOutputWritten) # 用于输出重定向

    def setupUi(self):
        self.setObjectName("addWindow")
        self.setStyleSheet("#addWindow{border-image:url(./style/AddWindow/background.png);}")
        self.setWindowIcon(QtGui.QIcon("./style/Window/icon.png"))
        self.resize(450, 600)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(self.width(), self.height()); 

        self.miniButton = QtWidgets.QPushButton(self)    # 最小化按钮
        self.miniButton.setGeometry(QtCore.QRect(380, 10, 20, 20))
        self.miniButton.clicked.connect(self.showMinimized)
        self.miniButton.setStyleSheet('''border-image:url(./style/Window/minimize.png); border-radius:12px;''')  

        self.closeButton = QtWidgets.QPushButton(self)    # 关闭按钮
        self.closeButton.setGeometry(QtCore.QRect(420, 10, 20, 20))
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStyleSheet('''border-image:url(./style/Window/close.png); border-radius:12px;''')  

        self.deButton = QtWidgets.QPushButton(self)       # 默认空按钮，避免回车激活其他按钮   
        self.deButton.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.deButton.setDefault(True)
        ft = QtGui.QFont()
        ft.setFamily('consolas')
        ft.setBold(True) 
        ft.setPointSize(12) 
        ft.setWeight(75)
        ft2 = QtGui.QFont()
        ft2.setFamily('幼圆')
        ft2.setBold(True) 
        ft2.setPointSize(15) 
        ft2.setWeight(75) 

        self.title = QLabel(self)                          # 标题
        self.title.setGeometry(QtCore.QRect(155, 10, 140, 30))
        self.title.setStyleSheet('''color:white;''')
        self.title.setFont(ft2)
        ft2.setPointSize(12)
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.5)
        self.searchWord = QtWidgets.QLineEdit(self)     # 搜索单词输入
        self.searchWord.setGeometry(QtCore.QRect(40, 60, 250, 30))
        self.searchWord.setObjectName("search")
        self.searchWord.setPlaceholderText("请输入单词")
        self.searchWord.setAlignment(QtCore.Qt.AlignTop)
        self.searchWord.setFont(ft)
        self.searchWord.returnPressed.connect(self.searchButtonClicked)
        self.searchWord.setStyleSheet('''background-color:transparent; color:white; border:2px solid white; width:300px; border-radius:10px; padding:2px 4px;''')
        # self.searchWord.setGraphicsEffect(op)

        self.searchButton = QtWidgets.QPushButton(self)     # 搜索单词按钮
        self.searchButton.setGeometry(QtCore.QRect(310, 60, 100, 30))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setStyleSheet('''background:#6DDF6D;border-radius:5px;''')
        self.searchButton.setFont(ft2)
        self.searchButton.setDefault(False)
        self.searchButton.clicked.connect(self.searchButtonClicked)        

        self.tableWidget = QtWidgets.QTableWidget(self)     # 查询结果
        self.tableWidget.setGeometry(QtCore.QRect(40, 100, 370, 300))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setStyleSheet('''background-color:transparent; color:white; border:2px solid white; width:300px; border-radius:10px; padding:2px 4px;''')
        self.tableWidget.setFont(ft2)

        self.addEnword = QtWidgets.QLineEdit(self)      # 添加单词的英文输入
        self.addEnword.setGeometry(QtCore.QRect(40, 420, 250, 30))
        self.addEnword.setObjectName("search")
        self.addEnword.setPlaceholderText("请输入单词")
        self.addEnword.setAlignment(QtCore.Qt.AlignTop)
        self.addEnword.setFont(ft)
        self.addEnword.returnPressed.connect(self.addButtonClicked)
        self.addEnword.setStyleSheet('''background-color:transparent; color:white; border:2px solid white; width:300px; border-radius:10px; padding:2px 4px;''')
        self.addCnword = QtWidgets.QLineEdit(self)      # 添加单词的释义输入
        self.addCnword.setGeometry(QtCore.QRect(40, 460, 250, 30))
        self.addCnword.setObjectName("search")
        self.addCnword.setPlaceholderText("请输入释义")
        self.addCnword.setAlignment(QtCore.Qt.AlignTop)
        self.addCnword.setFont(ft)
        self.addCnword.returnPressed.connect(self.addButtonClicked)
        self.addCnword.setStyleSheet('''background-color:transparent; color:white; border:2px solid white; width:300px; border-radius:10px; padding:2px 4px;''')

        self.addButton = QtWidgets.QPushButton(self)        # 添加单词按钮
        self.addButton.setGeometry(QtCore.QRect(310, 430, 120, 50))
        self.addButton.setObjectName("addButton")
        self.addButton.setFont(ft2)
        self.addButton.setDefault(False)
        self.addButton.clicked.connect(self.addButtonClicked) 

        self.log = QtWidgets.QTextEdit(self)               # 日志输出
        self.log.setGeometry(QtCore.QRect(40, 500, 370, 95))
        self.log.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.log.setStyleSheet('''background-color:transparent; color:white; border-radius:10px;background:transparent;''')
        self.log.setFocusPolicy(QtCore.Qt.NoFocus) 
        
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("addWindow", "WordMem"))
        self.title.setText(_translate("title", "查询/添加单词"))
        self.searchButton.setText(_translate("searchButton", "搜 索"))
        self.addButton.setText(_translate("addButton", "添加单词"))

    def normalOutputWritten(self, text):    # 输出重定向
        cursor = self.log.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.log.setTextCursor(cursor)
        self.log.ensureCursorVisible()

    def searchButtonClicked(self):
        wd = self.searchWord.text()
        if wd == '':
            pass
        else:
            result = w.fuzzsearch(wd)   # 模糊查询得到结果
            count = self.tableWidget.rowCount()+1
            for i in range(count):
                self.tableWidget.removeRow(0)   # 清空表格
            if len(result)==0:
                print('[INFO] 查询失败!单词库中没有相似单词!')
            else:
                for index, r in enumerate(result):
                    self.tableWidget.insertRow(index)
                    # print(r[0],r[1])
                    ewItem = QtWidgets.QTableWidgetItem(r[0])#（）里面为表格中的元素
                    ewItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    cwItem = QtWidgets.QTableWidgetItem(r[1])#（）里面为表格中的元素
                    cwItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tableWidget.setItem(index, 0, ewItem)#设置index行0列的内容为Value
                    self.tableWidget.setItem(index, 1, cwItem)#设置index行0列的内容为Value
                    self.tableWidget.setColumnWidth(0,165)#设置0列的宽度
                    self.tableWidget.setColumnWidth(1,193)#设置1列的宽度
                    self.tableWidget.setRowHeight(index,30)#设置index行的高度
                print('[INFO] 查询成功!')

    def addButtonClicked(self):
        enword = self.addEnword.text()
        cnword = self.addCnword.text()
        cn = w.update_db(en_word=enword, cn_word=cnword, mode='add')
        self.addCnword.setText(cn)

class tipWindow(QtWidgets.QDialog):     # Tip浮窗模式窗口
    def __init__(self):
        super(tipWindow, self).__init__()
        self.setupUi()
        # func1 = threading.Thread(target=self.setupUi)
        # func2 = threading.Thread(target=self.nextword)
        # func1.start()
        # func2.start()
    def setupUi(self):
        self.setObjectName("tipWindow")
        self.setStyleSheet("#tipWindow{border-image:url(./style/AddWindow/background.png) }")
        self.setWindowIcon(QtGui.QIcon("./style/Window/icon.png"))
        self.resize(200, 160)
        self.loc_wid=QApplication.desktop().width()-200
        self.loc_hei=(QApplication.desktop().height()-160)/2
        self.move(self.loc_wid, self.loc_hei)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint|Qt.Tool|QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.width(), self.height()); 
        # self.setWindowOpacity(0.5)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        
        color = self.catch()        
        ft = QtGui.QFont()
        ft.setFamily('Consolas')
        ft.setBold(True) 
        ft.setPointSize(15) 
        ft.setWeight(75) 
        self.quitbutton = QPushButton(self)             # 退出tip
        self.quitbutton.setGeometry(QtCore.QRect(180, 0, 20, 150))
        self.quitbutton.setStyleSheet('''background-color:transparent; color:{c}; border-radius:12px;'''.format(c=color))
        self.quitbutton.clicked.connect(self.quit)
        self.quitbutton.setText("点\n击\n右\n侧\n退\n出")

        self.word = QLabel(self)            # 当前单词
        self.word.setGeometry(QtCore.QRect(0, 20, 180, 30))
        self.word.setText(w.thisword.enWord)
        self.word.setAlignment(QtCore.Qt.AlignCenter)
        self.word.setStyleSheet('''color:{c};'''.format(c=color))
        self.word.setFont(ft)

        self.pronunciation = QtWidgets.QPushButton(self)    # 发音
        self.pronunciation.setGeometry(QtCore.QRect(90, 85, 20, 20))
        self.pronunciation.setStyleSheet('''border-image:url(./style/RemWindow/pronunciation.png);border-radius:12px;''')
        self.pronunciation.clicked.connect(w.pronunciation) # 播放发音

        self.phonetic = QLabel(self)            # 音标
        self.phonetic.setGeometry(QtCore.QRect(0, 50, 180, 30))
        self.phonetic.setText(w.thisword.phonetic)
        self.phonetic.setAlignment(QtCore.Qt.AlignCenter)
        self.phonetic.setStyleSheet('''color:{c};'''.format(c=color))
        self.phonetic.setFont(ft)

        ft2 = QtGui.QFont()
        ft2.setFamily('幼圆')
        ft2.setBold(True) 
        ft2.setPointSize(15) 
        ft2.setWeight(75) 
        self.translation = QLabel(self)      # 释义
        self.translation.setGeometry(QtCore.QRect(0, 110, 180, 50))
        self.translation.setText(w.thisword.cnTranslation)
        self.translation.setWordWrap(True)
        self.translation.setAlignment(QtCore.Qt.AlignCenter)
        self.translation.setFont(ft2)
        self.translation.setStyleSheet('''background-color:transparent; color:{c}; border:none;'''.format(c=color))

        self.flag = True
        self.func = threading.Thread(target=self.nextword)  # 定时切换单词的线程
        self.func.setDaemon(True)
        self.func.start()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("tipWindow", "WordMem"))

    def quit(self):
        self.flag = False
        self.close()

    def nextword(self):     # 定时切换单词
        while self.flag:
            time.sleep(5)
            w.nextword()
            self.changecolor()
            self.word.setText(w.thisword.enWord)
            self.phonetic.setText(w.thisword.phonetic)
            self.translation.setText(w.thisword.cnTranslation)

    def changecolor(self):      # 字体自适应变色
        color = self.catch()
        self.quitbutton.setStyleSheet('''background-color:transparent; color:{c}; border-radius:12px;'''.format(c=color))
        self.word.setStyleSheet('''color:{c};'''.format(c=color))
        self.phonetic.setStyleSheet('''color:{c};'''.format(c=color))
        self.translation.setStyleSheet('''background-color:transparent; color:{c}; border:none;'''.format(c=color))

    def catch(self):        # 自动抓取浮窗中央颜色，并返回其反色(十六进制)
        x = self.loc_wid+100
        y = self.loc_hei+80
        pixmap = QtGui.QGuiApplication.primaryScreen().grabWindow(QApplication.desktop().winId(), x, y, 1, 1)
        if not pixmap.isNull():
            image = pixmap.toImage()
            if not image.isNull():
                if (image.valid(0, 0)):
                    color = QtGui.QColor(image.pixel(0, 0))
                    r, g, b, _ = color.getRgb()
                    # self.nowColor = color
                    return '#'+hex(255-r)[2:]+hex(255-g)[2:]+hex(255-b)[2:]
                    # self.ui.lineEditMove.setText('(%d, %d, %d) %s' % (r, g, b, color.name().upper()))
                    # self.ui.lineEditMove.setStyleSheet('QLineEdit{border:2px solid %s;}' % (color.name()))

if __name__=='__main__':
    w = wordlist()
    app = QtWidgets.QApplication(sys.argv)  #
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
