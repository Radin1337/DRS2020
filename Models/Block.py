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
        self.RDegrees = RotateDegrees.Right

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
            p.drawPixmap(r, self.rotate_picture("resources/food.png"))
        elif self.BType == BlockType.Head:
            p.drawPixmap(r, self.rotate_picture("resources/head.png"))
        elif self.BType == BlockType.Body:
            p.drawPixmap(r, self.rotate_picture("resources/body.png"))
        elif self.BType == BlockType.Tail:
            p.drawPixmap(r, self.rotate_picture("resources/tail.png"))
        elif self.BType == BlockType.CurvedBody:
            p.drawPixmap(r, self.rotate_picture("resources/curvedbody.png"))

    def rotate_picture(self, path):
        picture = QPixmap(QImage(path))
        transform = QTransform().rotate(self.RDegrees)
        picture = picture.transformed(transform)

        return picture


class BlockType(enum.IntEnum):

    EmptyBlock = 0
    Head = 1
    Body = 2
    CurvedBody = 3
    Tail = 4
    Food = 5


class RotateDegrees(enum.IntEnum):
    Right = 0
    Down = 90
    Left = 180
    Up = 270
