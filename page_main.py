from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QStackedWidget, QTableWidget, QHeaderView, \
    QAbstractItemView, QFileDialog

from movie_label import MyLabel
from page_detial import MoiveDetial
from spider.runner import Runner


class Params():
    def __init__(self):
        self.tid = ''
        self.pg = 1
        self.filter = False
        self.extend = {}


class Main_Page(QWidget):
    backSignal = pyqtSignal()

    def __init__(self):
        super(QWidget, self).__init__()
        self.spider = None
        self.params = Params()

        self.setWindowTitle("TVBoxPC")
        self.setFixedSize(1000, 700)
        self.setObjectName("mainpage")
        self.setStyleSheet("#mainpage{background-color:white;}")
        self.Layout = QVBoxLayout(self)

        self.header_wid = QWidget(self)
        self.header_wid.setGeometry(0, 0, self.width(), 70)
        self.header_wid.setObjectName("header")
        self.header_wid.setStyleSheet("#header{border-bottom:1px solid #999;}")
        self.spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.header_Hlayout = QHBoxLayout(self.header_wid)

        self.body_Swid = QStackedWidget(self)
        self.body_Swid.setGeometry(0, 70, self.width(), self.height() - 100)
        self.body_Swid.setObjectName("Wid1")
        self.body_Swid.setStyleSheet("#Wid1{border:0px;}")
        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive | QHeaderView.Stretch)
        self.body_Swid.addWidget(self.table)
        # self.header = QWidget(self)

        self.header = QWidget(self)  # 设置右边栏向上按钮的框
        self.header.setGeometry(0, self.body_Swid.height() - 100, self.body_Swid.width(), 100)
        # self.RproPage.setObjectName("RightdownPage")
        self.Up = QHBoxLayout(self.header)  # 设置装向下按钮的框
        self.upBt = QPushButton("选择py文件")
        self.Up.addWidget(self.upBt)
        self.upBt.clicked.connect(self.showDialog1)
        self.Layout.addWidget(self.header_wid)
        self.Layout.addWidget(self.header_wid)
        self.Layout.addWidget(self.body_Swid)
        self.BottomFrame()
        self.Layout.addWidget(self.RproPage)
        # self.ReloadSpider('py_cctvvd.py')
        self.show()
        # 定义打开文件夹目录的函数

    def showDialog1(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname[0]:
            self.ReloadSpider(fname[0])
    def ReloadSpider(self,spath):
        self.spider = Runner(spath)
        self.Header(self.spider.homeContent(True))
        self.Reloadpage(self.spider.homeVideoContent())

    def ReloadVod(self):
        Vodinfo = self.spider.categoryContent(self.params.tid, self.params.pg, self.params.filter, self.params.extend)
        self.Reloadpage(Vodinfo)

    def GetSpider(self):
        return self.spider

    # 顶部标签
    def Header(self, Classinfo):
        while self.header_Hlayout.count():
            self.header_Hlayout.itemAt(0).widget().setParent(None)
        if 'class' not in Classinfo:
            return
        for _ in Classinfo['class']:
            type_name = _['type_name']
            type_id = _['type_id']
            moive_all = QPushButton(type_name, self.header_wid)
            # self.moive_all.setObjectName("MoiveAll")
            # self.moive_all.setStyleSheet("#MoiveAll:hover{color: red;}#MoiveAll{border:0px;}")
            # self.moive_all.setCursor(Qt.PointingHandCursor)
            self.header_Hlayout.addWidget(moive_all)
            # self.header_Hlayout.addItem(self.spacerItem)
            # self.header_Hlayout.setSpacing(10)
            moive_all.clicked.connect(
                lambda checked, arg=type_id: self.changeClass(arg))  # lambda:arg=type_id self.changeClass(arg))

    def changeClass(self, tid):
        self.params.tid = tid
        self.params.pg = 1
        self.params.filter = False
        self.params.extend = {}
        self.ReloadVod()

    def Reloadpage(self, Vodinfo):
        self.table.clear()
        if 'list' not in Vodinfo:
            return
        self.columnCount = 6
        self.ColumnWidth = 50
        self.RowHeight = 300
        VodCount = len(Vodinfo['list'])
        self.rowCount = int(VodCount / self.columnCount) + 1
        self.table.setColumnCount(self.columnCount)
        self.table.setRowCount(self.rowCount)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setDragEnabled(False)
        for i in range(self.columnCount):  # 让列宽和图片相同
            self.table.setColumnWidth(i, self.ColumnWidth)
        for i in range(self.rowCount):  # 让行高和图片相同
            self.table.setRowHeight(i, self.RowHeight)
        for n, _ in enumerate(Vodinfo['list']):
            vod_id = _['vod_id']
            vod_name = _['vod_name']
            vod_pic = _['vod_pic']
            self.formApage = MyLabel(self.table, vod_id, "Apage")
            self.formApage.SetGImg(6, 6, 118, 182, vod_pic)  # 传入图片原大小(6, 6, 118, 182, src)
            # self.formApage.setCursor(Qt.PointingHandCursor)
            self.formApage.SetTitle(vod_name, 10)
            # self.formApage.SetContent("111", 14, 0, 0)
            self.table.setCellWidget(n / self.columnCount, n % self.columnCount, self.formApage)  # 设置标签在框架的位置
            # self.formApage.setToolTip(self.MoiveName[idx])
            self.formApage.PressSignal.connect(self.ApageDetial)  # 接受被点击后的信号

    # 发送打开细节页面的槽函数
    def ApageDetial(self, idx):  # 接受信号的槽函数,注意发送信号参数要与槽函数参数一致
        self.MDetial = MoiveDetial(idx, self.GetSpider())

    # 右边栏翻页设置
    def BottomFrame(self):
        self.RproPage = QWidget(self)  # 设置右边栏向上按钮的框
        self.RproPage.setGeometry(0, self.body_Swid.height() - 100, self.body_Swid.width(), 100)
        # self.RproPage.setObjectName("RightdownPage")
        self.Upvbox = QHBoxLayout(self.RproPage)  # 设置装向下按钮的框
        self.upBtn = QPushButton("上一页")
        self.downBtn = QPushButton("下一页")
        self.Upvbox.addWidget(self.upBtn)
        self.Upvbox.addWidget(self.downBtn)
        self.upBtn.clicked.connect(self.upCount)
        self.downBtn.clicked.connect(self.downCount)

    def downCount(self, mark):
        self.params.pg += 1
        self.ReloadVod()

    def upCount(self, mark):
        if self.params.pg >= 2:
            self.params.pg -= 1
            self.ReloadVod()
