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
            x, y = random.randint(0, 14), random.randint(0, 14)
            w = self.grid.itemAtPosition(x, y).widget()
            self.Food.append(Food(w))
            self.update()

    def init_snakes(self):
        s = Snake()
        s.init_snake(self.grid)
        self.Snakes.append(s)
        self.update()

    def keyPressEvent(self, e: QKeyEvent):
        self.clear_block(self.Snakes[0].tail.x, self.Snakes[0].tail.y)

        if e.key() == Qt.Key_Up:
            self.Snakes[0].move(self.grid, 'u')
        if e.key() == Qt.Key_Down:
            self.Snakes[0].move(self.grid, 'd')
        if e.key() == Qt.Key_Left:
            self.Snakes[0].move(self.grid, 'l')
        if e.key() == Qt.Key_Right:
            self.Snakes[0].move(self.grid, 'r')

        self.update()
        time.sleep(0.05)

    def clear_block(self, x, y):
        blk = Block(x, y)
        self.grid.removeWidget(self.grid.itemAtPosition(x, y).widget())
        self.grid.addWidget(blk, x, y)
