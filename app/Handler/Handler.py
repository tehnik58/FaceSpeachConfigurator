from PyQt5.QtWidgets import QApplication

import sys
from Window.Window import MyWindowClass

def create_window():
    app = QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()