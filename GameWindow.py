from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random
import sys


# creating game window
class GameWindow(QMainWindow):
    def __init__(self, settingswind):
        super(GameWindow, self).__init__()
        # adding board as a central widget

        # setting title to the window
        self.setWindowTitle('Game window')

        # setting geometry to the window
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(100, 100, screen.width(), screen.height())
        self.setStyleSheet("background-image: url(resources/mapa.jpg);")

        self.center()
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()  # Here we take our full screen geometry
        size = self.geometry()  # Here we take our app geometry
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))
