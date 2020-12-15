from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random
import sys


class Food(QFrame):
    x = 0
    y = 0
    picture = 'resources/food.png'
    deactivateFood = pyqtSignal()
    activateFood = pyqtSignal()

    def __init__(self, parent, id):
        super().__init__(parent)

        self.x = random.randint(0, 560)
        self.y = random.randint(0, 560)
        self.Label = QLabel(parent)
        Pixmap = QPixmap('resources/food.png')
        PixmapResized = Pixmap.scaled(40, 40)
        self.Label.setPixmap(PixmapResized)
        self.Label.move(self.x, self.y)

