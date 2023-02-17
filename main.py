import sys

from PyQt5.QtWidgets import *

from page_main import Main_Page

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Main_Page()
    a.show()
    sys.exit(app.exec_())
