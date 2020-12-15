from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Models.Food import  Food

import random
import sys


# creating game window
class GameWindow(QMainWindow):
    GameWindowH = 600
    GameWindowW = 800

    def __init__(self, settingswind):
        super(GameWindow, self).__init__()

        self.board = Board(self)
        self.setCentralWidget(self.board)

        self.board.start()

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
        self.resize(self.GameWindowH, self.GameWindowW)
        self.setMinimumHeight(self.GameWindowH)
        self.setMinimumWidth(self.GameWindowW)
        self.setMaximumHeight(self.GameWindowH)
        self.setMaximumWidth(self.GameWindowW)
        self.setWindowTitle('Game window')

        self.show()


        # setting title to the window
        # adding board as a central widget

    def center(self):
        screen = QDesktopWidget().screenGeometry()  # Here we take our full screen geometry
        size = self.geometry()  # Here we take our app geometry
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


class Board(QFrame):
    BoardWidth = 40
    BoardHeight = 40
    Mls = 500

    def __init__(self, parent):
        super(Board, self).__init__(parent)

        self.timerFood = QBasicTimer()

        self.Food = []

        self.board = []

        self.InitFood()

        self.setFocusPolicy(Qt.StrongFocus)

    def start(self):
        self.timerFood.start(2000, self)

    # Timer event method will be triggered by our own created timer
    def timerEvent(self, event):
        if event.timerId() == self.timerFood.timerId():
            self.ShowNextFood()

    def InitFood(self):

        for i in range(5):
            self.Food.append(Food(self,i))

        for i in range(4):
            self.Food[i+1].Label.setVisible(False)

    def ShowNextFood(self):
        for i in range(5):
            if not self.Food[i].Label.isVisible():
                self.Food[i].Label.setVisible(True)
                break

