from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Models.Block import Block, BlockType, RotateDegrees
from enum import IntEnum
import random
import sys


class Head(Block):
    def __init__(self, parent, moved=RotateDegrees.Right):
        Block.__init__(self, parent.x, parent.y)
        parent.BType = BlockType.Head
        parent.RDegrees = moved
        self.last_pos_x = parent.x
        self.last_pos_y = parent.y
        self.degree = parent.RDegrees


class Body(Block):
    def __init__(self, parent, moved=RotateDegrees.Right, blk=BlockType.Body):
        Block.__init__(self, parent.x, parent.y)
        parent.BType = blk
        parent.RDegrees = moved
        self.last_pos_x = parent.x
        self.last_pos_y = parent.y
        self.degree = parent.RDegrees
        self.BlkType = parent.BType


class Tail(Block):
    def __init__(self, parent, moved=RotateDegrees.Right):
        Block.__init__(self, parent.x, parent.y)
        parent.BType = BlockType.Tail
        parent.RDegrees = moved
        self.last_pos_x = parent.x
        self.last_pos_y = parent.y
        self.degree = parent.RDegrees


class Snake:
    def __init__(self):
        self.head = None
        self.body = []
        self.tail = None

    def move(self, grid, direction):
        x = self.head.last_pos_x
        y = self.head.last_pos_y
        d = self.head.degree

        tail_pos = grid.itemAtPosition(self.body[0].last_pos_x,
                                       self.body[0].last_pos_y).widget()

        self.tail = Tail(tail_pos)

        for i in range(0, len(self.body)-1):
            body_pos = grid.itemAtPosition(self.body[i+1].last_pos_x,
                                           self.body[i+1].last_pos_y).widget()
            self.body[i] = Body(body_pos, self.body[i+1].degree, self.body[i+1].BlkType)

        body_pos = grid.itemAtPosition(self.head.last_pos_x, self.head.last_pos_y).widget()


        if direction == 'u':
            head_pos = grid.itemAtPosition(x-1, y).widget()
            self.head = Head(head_pos, RotateDegrees.Up)
            self.check_deg_diff(d, body_pos)
        elif direction == 'd':
            head_pos = grid.itemAtPosition(x+1, y).widget()
            self.head = Head(head_pos, RotateDegrees.Down)
            self.check_deg_diff(d, body_pos)
        elif direction == 'l':
            head_pos = grid.itemAtPosition(x, y-1).widget()
            self.head = Head(head_pos, RotateDegrees.Left)
            self.check_deg_diff(d, body_pos)
        elif direction == 'r':
            head_pos = grid.itemAtPosition(x, y+1).widget()
            self.head = Head(head_pos)
            self.check_deg_diff(d, body_pos)

    def check_deg_diff(self, d, body_pos):
        if d != self.head.degree:
            if (d == RotateDegrees.Right and self.head.degree == RotateDegrees.Down) or \
               (d == RotateDegrees.Down and self.head.degree == RotateDegrees.Left) or \
               (d == RotateDegrees.Left and self.head.degree == RotateDegrees.Up) or \
               (d == RotateDegrees.Up and self.head.degree == RotateDegrees.Right):
                self.body[len(self.body) - 1] = Body(body_pos, d, BlockType.CurvedBody)
            else:
                self.body[len(self.body) - 1] = Body(body_pos, d+90, BlockType.CurvedBody)
        else:
            self.body[len(self.body) - 1] = Body(body_pos, d)

    def init_snake(self, grid):
        head_pos = grid.itemAtPosition(0, 4).widget()
        body_pos1 = grid.itemAtPosition(0, 3).widget()
        body_pos2 = grid.itemAtPosition(0, 2).widget()
        body_pos3 = grid.itemAtPosition(0, 1).widget()
        tail_pos = grid.itemAtPosition(0, 0).widget()

        self.head = Head(head_pos)
        self.body.append(Body(body_pos3))
        self.body.append(Body(body_pos2))
        self.body.append(Body(body_pos1))
        self.tail = Tail(tail_pos)

        return self
