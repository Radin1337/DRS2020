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
        self.BType = BlockType.Tail
        parent.RDegrees = moved
        self.last_pos_x = parent.x
        self.last_pos_y = parent.y
        self.degree = parent.RDegrees


class Snake:
    def __init__(self):
        self.head = None
        self.body = []
        self.tail = None
        self.eat = 0
        # Ovde kazes right, a u gameWindow proveravas 'r'
        self.last_move = 'right'

    def move(self, grid, direction):
        # Smestamo postojece delove tela u lokalne promenljive

        saved_head = self.head
        saved_body = []
        for i in range(0, len(self.body)):
            saved_body.append(self.body[i])
        saved_tail = self.tail

        # Proveravamo smer kretanja zmije i shodno tome menjamo poziciju glave
        # -------------------------------------
        # Bolja preglednost koda sa x/y, verovatno ce doci do izmene naziva u samim klasama
        x = saved_head.last_pos_x
        y = saved_head.last_pos_y
        # -------------------------------------

        if direction == 'u':
            # Proveriti da li je glava druge zmije na "grid.itemAtPosition(x-1, y).widget()", ako jeste sta cemo?
            new_head_position = grid.itemAtPosition(x - 1, y).widget()
            self.head = Head(new_head_position, RotateDegrees.Up)
        elif direction == 'd':
            # Proveriti da li je glava druge zmije na "grid.itemAtPosition(x-1, y).widget()", ako jeste sta cemo?
            new_head_position = grid.itemAtPosition(x + 1, y).widget()
            self.head = Head(new_head_position, RotateDegrees.Down)
        elif direction == 'l':
            # Proveriti da li je glava druge zmije na "grid.itemAtPosition(x-1, y).widget()", ako jeste sta cemo?
            new_head_position = grid.itemAtPosition(x, y - 1).widget()
            self.head = Head(new_head_position, RotateDegrees.Left)
        elif direction == 'r':
            # Proveriti da li je glava druge zmije na "grid.itemAtPosition(x-1, y).widget()", ako jeste sta cemo?
            new_head_position = grid.itemAtPosition(x, y + 1).widget()
            self.head = Head(new_head_position)

        # Ovde se mogu potencijalno testirati uslovi za kraj igre
        # 1. funckija - glava van table, 2. funckija - glava se nalazi gde je i telo/rep BILO KOJE zmije

        # Cuvamo vrednosti opet zbog bolje preglednosti dalje
        old_degree = saved_head.degree
        new_degree = self.head.degree
        blk_type = BlockType.Body
        # Ako je zmija u prethodnom koraku presla preko hrane dodajemo novo telo iza glave.
        # A u suprotnom sve pomeramo za jedno mesto
        if self.eat == 1:
            new_body_position = grid.itemAtPosition(x, y).widget()

            if old_degree != new_degree:
                right_degree = self.body_rotation(old_degree, new_degree)
                blk_type = BlockType.CurvedBody
            else:
                right_degree = old_degree

            self.body.append(Body(new_body_position, right_degree, blk_type))
            self.eat = 0
        else:
            for i in range(0, len(self.body) - 1):
                new_body_position = grid.itemAtPosition(self.body[i + 1].last_pos_x,
                                                        self.body[i + 1].last_pos_y).widget()
                self.body[i] = Body(new_body_position, self.body[i + 1].degree, self.body[i + 1].BlkType)

            new_body_position = grid.itemAtPosition(x, y).widget()
            if old_degree != new_degree:
                right_degree = self.body_rotation(old_degree, new_degree)
                blk_type = BlockType.CurvedBody
            else:
                right_degree = old_degree
            self.body[len(self.body) - 1] = Body(new_body_position, right_degree, blk_type)

            # Odredjujemo novu poziciju  repa
            new_tail_position = grid.itemAtPosition(saved_body[0].last_pos_x, saved_body[0].last_pos_y).widget()
            tail_degree = self.tail_rotation(saved_body, saved_head, saved_tail)
            self.tail = Tail(new_tail_position, tail_degree)

            # Brisemo stari rep
            clean_block = grid.itemAtPosition(saved_tail.last_pos_x, saved_tail.last_pos_y).widget()
            clean_block.BType = BlockType.EmptyBlock

    @staticmethod
    def tail_rotation(saved_body, saved_head, saved_tail):
        if saved_body[0].BlkType == BlockType.CurvedBody:
            xclanak = saved_body[0].last_pos_x
            yclanak = saved_body[0].last_pos_y
            if len(saved_body) > 1:
                xtelo = saved_body[1].last_pos_x
                ytelo = saved_body[1].last_pos_y
            else:
                xtelo = saved_head.last_pos_x
                ytelo = saved_head.last_pos_y
            xdif = xclanak - xtelo
            ydif = yclanak - ytelo

            if xdif == 1 and ydif == 0:
                return RotateDegrees.Up
                # telo desno od clanka
            elif xdif == -1 and ydif == 0:
                return RotateDegrees.Down
                # telo ispod clanka
            elif xdif == 0 and ydif == -1:
                return RotateDegrees.Right
                # telo iznad clanka
            elif xdif == 0 and ydif == 1:
                return RotateDegrees.Left
        else:
            return saved_tail.degree

    @staticmethod
    def body_rotation(old_degree, new_degree):
        if (old_degree == RotateDegrees.Right and new_degree == RotateDegrees.Down) or \
                (old_degree == RotateDegrees.Down and new_degree == RotateDegrees.Left) or \
                (old_degree == RotateDegrees.Left and new_degree == RotateDegrees.Up) or \
                (old_degree == RotateDegrees.Up and new_degree == RotateDegrees.Right):
            return old_degree
        else:
            return old_degree + 90

    """x = self.head.last_pos_x
        y = self.head.last_pos_y
        d = self.head.degree

        # Dodaje novi blok sa telom jedan blok iza glave
        # Poveca telo posle svakih n poteza (n = trenutna duzina tela)
        # Nekad se rep ne rotira kako treba u trenutku povecavanja
        if self.eat == 1:
            new_pos = grid.itemAtPosition(self.head.last_pos_x, self.head.last_pos_y).widget()
            self.body.append(Body(new_pos))
            self.eat = 0

        tail_pos = grid.itemAtPosition(self.body[0].last_pos_x,
                                       self.body[0].last_pos_y).widget()
        xclanak = self.body[0].last_pos_x
        yclanak = self.body[0].last_pos_y
        if len(self.body) > 1:
            xtelo = self.body[1].last_pos_x
            ytelo = self.body[1].last_pos_y
        else:
            xtelo = self.head.last_pos_x
            ytelo = self.head.last_pos_y
        xdif = xclanak - xtelo
        ydif = yclanak - ytelo

        tail_degree = self.tail.degree
        rotirati_rep = False

        if self.body[0].BlkType == BlockType.CurvedBody:
            rotirati_rep = True

            # telo levo od clanka
            if xdif == 1 and ydif == 0:
                tail_degree = 270
            # telo desno od clanka
            elif xdif == -1 and ydif == 0:
                tail_degree = 90
            # telo ispod clanka
            elif xdif == 0 and ydif == -1:
                tail_degree = 0
            # telo iznad clanka
            elif xdif == 0 and ydif == 1:
                tail_degree = 180



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

        self.tail = Tail(tail_pos, tail_degree)


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
            self.body[len(self.body) - 1] = Body(body_pos, d)"""

    def init_snake(self, grid, x):
        head_pos = grid.itemAtPosition(x, 2).widget()
        """body_pos1 = grid.itemAtPosition(0, 3).widget()
        body_pos2 = grid.itemAtPosition(0, 2).widget()"""
        body_pos3 = grid.itemAtPosition(x, 1).widget()
        tail_pos = grid.itemAtPosition(x, 0).widget()

        self.head = Head(head_pos)
        self.body.append(Body(body_pos3))
        """self.body.append(Body(body_pos2))
        self.body.append(Body(body_pos1))"""
        self.tail = Tail(tail_pos)

        return self

    # Cemu ovo u kodu blago meni?
    def body_increase(self, grid):
        # new_body_pos = grid.ItemAtPosition(5, 5).widget()
        # self.body.append(Body(new_body_pos))
        print("EAT")
        self.eat = 1
