from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Models.Block import Block, BlockType
from enum import IntEnum
import random
import sys


class Head(Block):
    def __init__(self, parent):
        Block.__init__(self, parent.x, parent.y)
        parent.BType = BlockType.Head
        self.last_pos_x = parent.x
        self.last_pos_y = parent.y


class Body(Block):
    def __init__(self, parent):
        Block.__init__(self, parent.x, parent.y)
        parent.BType = BlockType.Body
        self.last_pos_x = parent.x
        self.last_pos_y = parent.y


class Tail(Block):
    def __init__(self, parent):
        Block.__init__(self, parent.x, parent.y)
        parent.BType = BlockType.Tail
        self.last_pos_x = parent.x
        self.last_pos_y = parent.y


class Snake:
    def __init__(self):
        self.head = None
        self.body = []
        self.tail = None

    def move(self, grid, direction):
        tail_pos = grid.itemAtPosition(self.body[len(self.body) - 1].last_pos_x,
                                       self.body[len(self.body) - 1].last_pos_y).widget()
        self.tail = Tail(tail_pos)

        body_pos = grid.itemAtPosition(self.head.last_pos_x, self.head.last_pos_y).widget()
        self.body[len(self.body) - 1] = Body(body_pos)

        x = self.head.last_pos_x
        y = self.head.last_pos_y

        if direction == 'u':
            head_pos = grid.itemAtPosition(x-1, y).widget()
            self.head = Head(head_pos)
        elif direction == 'd':
            head_pos = grid.itemAtPosition(x+1, y).widget()
            self.head = Head(head_pos)
        elif direction == 'l':
            head_pos = grid.itemAtPosition(x, y-1).widget()
            self.head = Head(head_pos)
        elif direction == 'r':
            head_pos = grid.itemAtPosition(x, y+1).widget()
            self.head = Head(head_pos)

