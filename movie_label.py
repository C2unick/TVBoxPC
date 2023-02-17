import requests
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtWidgets import QLabel


#重载标签
class MyLabel(QLabel):
    PressSignal = pyqtSignal(str)#被点击后的信号
    #所有成员变量设置为私有成员
    __Idx = None#每个表单的编号
    __Src = None#设置图片路径
    __Title = None#电影标题
    __TextContent = None#电影内容
    __Width = None#内部文本的宽度和高度
    __Height = None
    __Position_X = None#内部文本的位置
    __Position_Y = None
    __mark = None#作为每一类型的的页面进行区分

    def __init__(self, wid, num=None, mark=None):
        super(MyLabel, self).__init__()
        self.__mark = mark
        self.__Idx = num

    #插入顶部图片并设置图片大小
    def SetGImg(self,position_x = 10, position_y=10, width=None, height=None, Isrc=None):
        self.__Width = width
        self.__Height = height
        self.__Position_X = position_x
        self.__Position_Y = position_y
        self.__Src = Isrc
        #把所以值给下列函数
        # print("{},{},{}".format(Isrc, width, height))
        try:
            if self.__Src:
                res = requests.get(self.__Src)
                img = QImage.fromData(res.content)
                pix = QPixmap.fromImage(img)
                self.lab_Img = QLabel(self)
                self.lab_Img.setGeometry(self.__Position_X, self.__Position_Y, self.__Width, self.__Height)
                # self.lab_Img.setObjectName("TopImg")#用于调试，可删除
                # self.lab_Img.setStyleSheet("#TopImg{background-color:#666;}")#用于调试，可删除
                self.lab_Img.setPixmap(pix.scaled(self.__Width, self.__Height))
        except:
            pass
    #设置标题
    def SetTitle(self, title=None, FontSize=None):
        # print("字体大小{}".format(FontSize), end=", ")
        # print(title, end=", ")
        self.__Title = title#赋值给成员
        self.TopTitle = QLabel(self)#实例化标题
        self.TopTitle.setText(title)#把标题设置进去
        position_y = 0
        position_x = 0
        width = 0
        height = 0
        if self.__mark == "Rpage":
            position_x = self.__Position_X + 10
            position_y = self.__Position_Y + self.__Height + self.__Position_Y/8
            width = self.__Width
            height = 40
        elif self.__mark == "Apage":
            position_x = self.__Position_X +5
            position_y = self.__Position_Y + self.__Height + self.__Position_Y/8
            width = self.__Width
            height = 30
        self.TopTitle.setGeometry(position_x, position_y, width, height)#设置标题位置
        self.TopTitle.setContentsMargins(0,0,0,0)
        self.TopTitle.setFont(QFont("SimHei", FontSize))#用代QFont设置字体
    #设置文本内容
    def SetContent(self, content=None, FontSize=None, width = None, height = None):
        # print("字体大小{}, 长度:{}".format(FontSize, len(content)), end=", ")#设置前57个字
        self.__TextContent = content
        if self.__mark == "Rpage":
            self.__TextContent = content[0:26]#读取前实当的个字符，手工计算
        elif self.__mark == "Apage":
            self.__TextContent = content[0:19]
        self.__TextContent += self.__TextContent + "..."
        position_y = self.__Position_Y + self.__Height + self.TopTitle.height()#由于放入下方的实参列表太长，就先进性计算
        self.Content = QLabel(self)
        self.Content.setText(self.__TextContent)
        self.Content.move(self.__Position_X, position_y)
        self.Content.resize(width, height)
        self.Content.setWordWrap(True)
        self.Content.setFont(QFont("SimHei", FontSize))
        self.__TextContent = content#把文字内容改回来

    def mousePressEvent(self, ev):
        # print(" {} ".format(self.__Idx))
        self.PressSignal.emit(str(self.__Idx))#被点击后会发送一个信号

    #通过函数获得内部成员变量
    def getImg(self):
        return self.__Src
    def getContent(self):
        return self.__TextContent
    def getTitle(self):
        return self.__Title
    def getIndex(self):
        return self.__Idx
