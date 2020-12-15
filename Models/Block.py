from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


import random
import sys
import enum


class Block(QWidget):

    def __init__(self, x, y, *args, **kwargs):
        super(Block, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(40, 40))

        self.x = x
        self.y = y
        self.BType = BlockType.EmptyBlock

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = event.rect()

        color = self.palette().light().color()
        color.setAlpha(100)

        outer, inner = color, color

        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        outer, inner = Qt.gray, Qt.lightGray

        if self.BType == BlockType.Food:
            p.drawPixmap(r, QPixmap(QImage("resources/food.png")))



class BlockType(enum.IntEnum):

    EmptyBlock = 0
    Head = 1
    Body = 2
    Tail = 3
    Food = 4
