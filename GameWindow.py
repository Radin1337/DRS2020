import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


from Models.Food import Food
from Models.Snake import *
from Models.Block import Block, BlockType
import random
import sys


# creating game window
from Models.Snake import Snake


class GameWindow(QMainWindow):
    GameWindowH = 600
    GameWindowW = 800

    def __init__(self, settingswind):
        super(GameWindow, self).__init__()

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

        self.Food = []
        self.Snakes = []

        vb = QVBoxLayout()
        w = QWidget()
        hb = QHBoxLayout()

        self.whoIsPlayingLabel = QLabel()
        self.whoIsPlayingLabel.setText("Playing: Player 1")
        self.whoIsPlayingLabel.setAlignment(Qt.AlignHCenter)
        vb.addWidget(self.whoIsPlayingLabel)

        hb.addLayout(vb)
        self.grid = QGridLayout()

        hb.addLayout(self.grid)
        w.setLayout(hb)
        w.layout().setContentsMargins(0, 0, 0, 0)
        w.layout().setSpacing(0)
        self.setCentralWidget(w)
        self.timer = QBasicTimer()
        self.timer.start(2000, self)

        self.init_map()
        self.init_snakes()
        self.show()

    def init_map(self):
        # Add positions to the map
        for x in range(0, 15):
            for y in range(0, 15):
                w = Block(x, y)
                self.grid.addWidget(w, x, y)

    # Possibly we are gonna need to move this to some worker class thread but this is for starting purposes only.
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.drop_food()
        self.update()

    def drop_food(self):
        x, y = random.randint(0, 14), random.randint(0, 14)
        snake = self.Snakes[0]
        if(snake.head.x == x and snake.head.y == y) or (snake.tail.x == x and snake.tail.y == y):
            self.drop_food()
        else:
            for bodypart in snake.body:
                if bodypart.x == x and bodypart.y == y:
                    self.drop_food()
                else:
                    w = self.grid.itemAtPosition(x, y).widget()
                    self.Food.append(Food(w))

    def init_snakes(self):
        s = Snake()
        s.init_snake(self.grid)
        self.Snakes.append(s)
        self.update()

    def keyPressEvent(self, e: QKeyEvent):
        # If statement that checks length of snake list is just for testing and not breaking the app it will change in future

        if len(self.Snakes) != 0:

            #clean_block = self.grid.itemAtPosition(self.Snakes[0].tail.x, self.Snakes[0].tail.y).widget()
            #clean_block.BType = BlockType.EmptyBlock
            # print(self.Snakes[0].last_move)

            if e.key() == Qt.Key_Up:
                for i in range(0, len(self.Snakes[0].body) - 1):
                    if self.Snakes[0].head.x == self.Snakes[0].body[i].x + 1:
                        print("Game over")
                        self.clear_snake(0)
                if self.Snakes[0].head.x == 0:
                    print("Game over")
                    self.clear_snake(0)
                elif self.Snakes[0].last_move == 'd':
                    print("Game over")
                    self.clear_snake(0)
                else:
                    self.Snakes[0].move(self.grid, 'u')
                    self.eat_food()

                    self.Snakes[0].last_move = 'u'

            if e.key() == Qt.Key_Down:
                for i in range(0, len(self.Snakes[0].body) - 1):
                    if self.Snakes[0].head.x == self.Snakes[0].body[i].x - 1:
                        print("Game over")
                        self.clear_snake(0)
                if self.Snakes[0].head.x == 14:
                    print("Game over")
                    self.clear_snake(0)
                elif self.Snakes[0].last_move == 'u':
                    print("Game over")
                    self.clear_snake(0)
                else:
                    self.Snakes[0].move(self.grid, 'd')
                    self.eat_food()
                    self.Snakes[0].last_move = 'd'
            if e.key() == Qt.Key_Left:
                for i in range(0, len(self.Snakes[0].body) - 1):
                    if self.Snakes[0].head.y == self.Snakes[0].body[i].y + 1:
                        print("Game over")
                        self.clear_snake(0)
                if self.Snakes[0].head.y == 0:
                    print("Game over")
                    self.clear_snake(0)
                elif self.Snakes[0].last_move == 'r':
                    print("Game over")
                    self.clear_snake(0)
                else:
                    self.Snakes[0].move(self.grid, 'l')
                    self.eat_food()
                    self.Snakes[0].last_move = 'l'
            if e.key() == Qt.Key_Right:
                for i in range(0, len(self.Snakes[0].body) - 1):
                    if self.Snakes[0].head.y == self.Snakes[0].body[i].y - 1:
                        print("Game over")
                        self.clear_snake(0)
                if self.Snakes[0].head.y == 14:
                    print("Game over")
                    self.clear_snake(0)
                elif self.Snakes[0].last_move == 'l':
                    print("Game over")
                    self.clear_snake(0)
                else:
                    self.Snakes[0].move(self.grid, 'r')
                    self.eat_food()
                    self.Snakes[0].last_move = 'r'

        self.update()
        time.sleep(0.05)

    def clear_snake(self, snake_id):
        snake = self.Snakes[snake_id]
        block = self.grid.itemAtPosition(snake.head.x, snake.head.y).widget()
        block.BType = BlockType.EmptyBlock
        block = self.grid.itemAtPosition(snake.tail.x, snake.tail.y).widget()
        block.BType = BlockType.EmptyBlock

        for bodypart in snake.body:
            block = self.grid.itemAtPosition(bodypart.x, bodypart.y).widget()
            block.BType = BlockType.EmptyBlock

        self.Snakes.remove(self.Snakes[snake_id])

    def eat_food(self):
        # ovo radi, ali bukvalno nemam reci
        for i, val in enumerate(self.Food):
            if self.Snakes[0].head.x == self.Food[i].x and self.Snakes[0].head.y == self.Food[i].y:
                self.Food.remove(self.Food[i])
                self.Snakes[0].body_increase(self.grid)
