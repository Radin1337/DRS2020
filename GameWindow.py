from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random
import sys


# creating game window
class GameWindow(QMainWindow):
    GameWindowH = 600
    GameWindowW = 800

    def __init__(self, settingswind):
        super(GameWindow, self).__init__()
        # adding board as a central widget

        # setting title to the window
        self.setWindowTitle('Game window')
        self.setMinimumHeight(self.GameWindowH)
        self.setMinimumWidth(self.GameWindowW)
        self.setMaximumHeight(self.GameWindowH)
        self.setMaximumWidth(self.GameWindowW)
        # setting geometry to the window
        # screen = QDesktopWidget().screenGeometry()
        # self.setGeometry(100, 100, screen.width(), screen.height())
        # self.setStyleSheet("background-image: url(resources/mapa.jpg);")
        self.setWindowIcon(QIcon('resources/icon.png'))
        oImage = QImage("resources/mapa.jpg")
        sImage = oImage.scaled(QSize(800, 600))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = WindowRole
        self.setPalette(palette)
        self.center()
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()  # Here we take our full screen geometry
        size = self.geometry()  # Here we take our app geometry
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))
