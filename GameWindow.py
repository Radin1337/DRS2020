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
from Worker import Worker
from WorkerEatFood import WorkerEatFood
from multiprocessing import Queue
from ProcessEatFood import ProcessEatFood

class GameWindow(QMainWindow):
    GameWindowH = 600
    GameWindowW = 800

    def __init__(self, numberOfPlayers, numberOfSnakes):
        super(GameWindow, self).__init__()

        self.numOfPlayers = numberOfPlayers
        self.numOfSnakes = numberOfSnakes

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

        self.ListOfPlayers = []
        self.init_players()

        self.Players = {PlayerID: [] for PlayerID in self.ListOfPlayers}
        self.init_snakes()

        self.Food = []
        self.Snakes = []

        for i in range(numberOfPlayers):
            self.Snakes.extend(self.Players["id"+str(i+1)])

        self.in_queue_eatfood = Queue()
        self.out_queue_eatfood = Queue()

        self.EatFoodProcess = ProcessEatFood(self.in_queue_eatfood, self.out_queue_eatfood)
        self.EatFoodProcess.start()

        self.eatFoodWorker = WorkerEatFood(self.Food, self.Snakes, self.in_queue_eatfood, self.out_queue_eatfood, self.grid)
        self.eatFoodWorker.update.connect(self.receive_from_eatfood_worker)
        self.eatFoodWorker.start()
        self.signalCounter = 0
        
    
        #self.SnakeOnMove = self.Players[self.ListOfPlayers[player_id]][snake_id]

        self.show()

    def init_map(self):
        # Add positions to the map
        for x in range(0, 15):
            for y in range(0, 15):
                w = Block(x, y)
                self.grid.addWidget(w, x, y)

    def init_players(self):
        for i in range(0, self.numOfPlayers):
            self.ListOfPlayers.append("id" + str(i + 1))

    def init_snakes(self):
        for player_id, snakes in self.Players.items():
            for snake_id in range(0, self.numOfSnakes):
                s = Snake()
                s.init_snake(self.grid, player_id, snake_id)
                snakes.append(s)
        self.update()

    # Possibly we are gonna need to move this to some worker class thread but this is for starting purposes only.
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.drop_food()
        self.update()

    def drop_food(self):
        x, y = random.randint(0, 14), random.randint(0, 14)
        b = self.grid.itemAtPosition(x, y).widget()

        if b.BType == BlockType.EmptyBlock:
            self.Food.append(Food(b))
        else:
            self.drop_food()

    def keyPressEvent(self, e: QKeyEvent):
        # If statement that checks length of snake list is just for testing and not breaking the app it will change in future
        if len(self.Players[self.ListOfPlayers[0]]) != 0:

            if e.key() == Qt.Key_Up:
                self.Players[self.ListOfPlayers[0]][0].move(self.grid, 'u')
            elif e.key() == Qt.Key_Down:
                self.Players[self.ListOfPlayers[0]][0].move(self.grid, 'd')
            elif e.key() == Qt.Key_Left:
                self.Players[self.ListOfPlayers[0]][0].move(self.grid, 'l')
            elif e.key() == Qt.Key_Right:
                self.Players[self.ListOfPlayers[0]][0].move(self.grid, 'r')

            if self.Players[self.ListOfPlayers[0]][0].head is None:
                self.Snakes.remove(self.Snakes[0])
                self.Players[self.ListOfPlayers[0]].remove(self.Players[self.ListOfPlayers[0]][0])

        self.update()
        time.sleep(0.05)

    @pyqtSlot()
    def receive_from_eatfood_worker(self):
        print("Signal received ")
        print(self.signalCounter)
        
        # self.Snakes[0].body_increase(self.grid)
        print("\n Food count ")
        print(len(self.Food))
        self.signalCounter = self.signalCounter +1
