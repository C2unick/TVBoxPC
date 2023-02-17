import subprocess

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, \
    QTableWidget, QHeaderView, QAbstractItemView

PotPlayer_path = 'D:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe'

def secureget(dic='', key=''):
    if dic == None:
        return False
    if key in dic:
        return dic[key]
    else:
        return False


# 电影信息细节窗口设置为【模态阻塞对话框】
class MoiveDetial(QDialog):
    def __init__(self, vod_id=None, site_sp=None):
        super(QWidget, self).__init__()
        self.spider = site_sp
        jo = self.spider.detailContent([vod_id])
        self.vod_content = secureget(jo, 'list')
        if len(self.vod_content) > 0:
            self.vod_content = self.vod_content[0]

        secureget(self.vod_content, 'vod_play_from')
        jo = secureget(self.vod_content, 'vod_play_url')
        self.playurl = jo.split('$$$')

        self.setWindowTitle("电影详情")
        self.setFixedSize(800, 700)  # 设置页面大小
        self.setStyleSheet("QDialog{background-color:white;}")
        self.SetDetialTop()
        # "  // 播放源 多个用$$$分隔
        # 		"vod_play_from": "qiepian$$$yun3edu",
        #         // 播放列表 注意分隔符 分别是 多个源$$$分隔，源中的剧集用#分隔，剧集的名称和地址用$分隔
        # 		"vod_play_url": "第1集$1902-1-1#第2集$1902-1-2#第3集$1902-1-3#第4集$1902-1-4#第5集$1902-1-5#第6集$1902-1-6#第7集$1902-1-7#第8集$1902-1-8$$$第1集$1902-2-1#第2集$1902-2-2#第3集$1902-2-3#第4集$1902-2-4#第5集$1902-2-5#第6集$1902-2-6#第7集$1902-2-7#第8集$1902-2-8"
        # 	}]"
        self.SetDetailBottom()
        self.VLayout()  # 放入垂直布局中
        self.exec_()  # 设置阻塞窗口

    def SetDetialTop(self):  # 上半页面细节设置，主要思路为：用表格的方式把所有内容放入其中
        # self.MTitileLabel = QLabel(self)  # 存放标题
        # self.MTitileLabel.setText(secureget(self.vod_content, 'vod_name'))
        # self.MTitileLabel.setFont(QFont("Microsoft YaHei", 14, 700))
        self.PicLabel = QLabel(self)  # 设置放图片的标签
        try:
            if secureget(self.vod_content, 'vod_pic'):
                res = requests.get(secureget(self.vod_content, 'vod_pic'))
                img = QImage.fromData(res.content)
                pix = QPixmap.fromImage(img)
                self.PicLabel.setPixmap(pix.scaled(160, 250))
        except:
            pass

        self.textEdit = QTextEdit()
        for k, v in self.vod_content.items():
            if v and k not in ['vod_pic', 'vod_id', 'vod_play_from', 'vod_play_url']:
                self.textEdit.append("%s:%s" % (k, v))
        self.topwidget = QWidget(self)
        self.topwidget.setObjectName("GWid")
        self.topwidget.setStyleSheet("#GWid{border:1px solid #f5f5f5;}")
        self.topwidget.setGeometry(0, 0, self.width(), self.height() - 300)
        self.GLayout = QHBoxLayout(self.topwidget)
        # self.GLayout.addWidget(self.MTitileLabel)#标题
        self.GLayout.addWidget(self.PicLabel)  # 加入图片
        self.GLayout.addWidget(self.textEdit)  # 加入图片

    # 下半细节设置
    def SetDetailBottom(self):

        self.DGWid = QWidget()
        if len(self.playurl) < 1:
            return
        eplist = self.playurl[0].split('#')

        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive | QHeaderView.Stretch)
        self.columnCount = 1
        self.ColumnWidth = 50
        self.RowHeight = 300
        VodCount = len(eplist)
        self.rowCount = int(VodCount / self.columnCount) + 1
        self.table.setColumnCount(self.columnCount)
        self.table.setRowCount(self.rowCount)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setDragEnabled(False)
        for n, _ in enumerate(eplist):
            if _ == '':
                continue
            ep_name = _.split('$')[0]
            ep_url = _.split('$')[1]
            self.formApage = QPushButton()
            self.formApage.setFixedHeight(30)
            self.formApage.setText(ep_name)
            self.table.setCellWidget(n / self.columnCount, n % self.columnCount, self.formApage)  # 设置标签在框架的位置
            self.formApage.clicked.connect(lambda: self.playvod(ep_url))

    def playvod(self, url):
        playcontent = self.spider.playerContent("", url, {})
        # player = mpv_caller.MPV(player_operation_mode='pseudo-gui',
        #                         script_opts='osc-layout=box,osc-seekbarstyle=bar,osc-deadzonesize=0,osc-minmousemove=3',
        #                         input_default_bindings=True,
        #                         input_vo_keyboard=True,
        #                         osc=True)
        playurl = secureget(playcontent, 'url')
        if not playurl:
            return
        playheader = secureget(playcontent, 'header')
        if playheader:
            playua = secureget(playheader, 'User-Agent')
            if not playua:
                playua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.46'
            playref = secureget(playheader, 'Referer')
            if playref:
                subprocess.Popen([PotPlayer_path, playurl, '/user_agent=' + playua, '/referer=' + playref])
            else:
                subprocess.Popen([PotPlayer_path, playurl, '/user_agent=' + playua])
        else:
            subprocess.Popen([PotPlayer_path, playurl])

    def VLayout(self):
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.topwidget)
        self.CTitle = QLabel(self)
        self.CTitle.setText("--------------- 播放列表 ---------------")
        self.CTitle.setAlignment(Qt.AlignCenter)
        self.CTitle.setObjectName("title")
        self.CTitle.setStyleSheet("#title{border:1px solid #f9f9f9;}")
        self.vbox.addWidget(self.CTitle)
        self.vbox.addWidget(self.table)
