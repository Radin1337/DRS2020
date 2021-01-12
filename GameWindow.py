import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import socket

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
from CollisionWorker import CollisionWorker
from CollisionProcess import CollisionProcess
from ServerCommsWorker import ServerCommsWorker

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server


class GameWindow(QMainWindow):
    GameWindowH = 600
    GameWindowW = 800

    def __init__(self, numberOfPlayers, numberOfSnakes, lastwind):
        super(GameWindow, self).__init__()
        self.setGeometry(lastwind.geometry())
        self.myUniqueID = lastwind.myUniqueID
        self.currentIDPlaying = -1  # to block and unblock gameplay
        self.timeCounter = -1

        self.timerForMove = QBasicTimer()
        self.firstTimeGotID = True
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
        self.s = lastwind.s
        vb = QVBoxLayout()
        w = QWidget()
        hb = QHBoxLayout()

        self.iAmLabel = QLabel()
        self.iAmLabel.setFont(QFont('Times', 14))
        self.iAmLabel.setText("I am Player {0}".format(self.myUniqueID+1))
        self.iAmLabel.setAlignment(Qt.AlignHCenter)
        vb.addWidget(self.iAmLabel)
        self.whoIsPlayingLabel = QLabel()
        self.whoIsPlayingLabel.setWordWrap(True)
        self.whoIsPlayingLabel.setFont(QFont('Times', 14))
        self.whoIsPlayingLabel.setText("Playing: Game is starting...")
        self.whoIsPlayingLabel.setAlignment(Qt.AlignHCenter)

        vb.addWidget(self.whoIsPlayingLabel)

        hb.addLayout(vb)
        self.grid = QGridLayout()

        hb.addLayout(self.grid)
        w.setLayout(hb)
        w.layout().setContentsMargins(0, 0, 0, 0)
        w.layout().setSpacing(0)
        self.setCentralWidget(w)
        self.iAmLabel.move(QPoint(0, 0))
        self.whoIsPlayingLabel.move(QPoint(0, 5))

        self.init_map()

        self.Players = {PlayerID: [] for PlayerID in range(0, numberOfPlayers)}
        self.init_snakes()

        self.Food = []
        self.Snakes = []

        for i in range(numberOfPlayers):
            self.Snakes.extend(self.Players[i])

        self.in_queue_eatfood = Queue()
        self.out_queue_eatfood = Queue()

        self.EatFoodProcess = ProcessEatFood(self.in_queue_eatfood, self.out_queue_eatfood)
        self.EatFoodProcess.start()

        self.eatFoodWorker = WorkerEatFood(self.Food, self.Snakes, self.in_queue_eatfood, self.out_queue_eatfood,
                                           self.grid)
        self.eatFoodWorker.update.connect(self.receive_from_eatfood_worker)
        self.eatFoodWorker.start()
        self.signalCounter = 0

        self.KeyStrokes = []
        # Setting up process and worker to check up on collisions
        self.in_queue_collision = Queue()
        self.out_queue_collision = Queue()

        self.CollisionProcess = CollisionProcess(self.in_queue_collision, self.out_queue_collision)
        self.CollisionProcess.start()

        #self.SnakeOnMove = self.Players[self.myUniqueID][0]
        self.PlayerSnakeId = [self.myUniqueID, 0]
        self.CollisionWorker = CollisionWorker(self.Players, self.PlayerSnakeId, self.grid, self.KeyStrokes,
                                               self.Snakes, self.in_queue_collision, self.out_queue_collision)
        self.CollisionWorker.update.connect(self.receive_from_collision_worker)
        self.CollisionWorker.start()
        self.signalFromCollision = 0

        self.comms_to_send_queue = Queue()
        self.comms_to_receive_queue = Queue()
        self.CommsWorker = ServerCommsWorker(self.s, self.comms_to_send_queue, self.comms_to_receive_queue)
        self.CommsWorker.update.connect(self.receive_from_communication_worker)
        self.CommsWorker.start()

        self.show()

    def init_map(self):
        # Add positions to the map
        for x in range(0, 15):
            for y in range(0, 15):
                w = Block(x, y)
                self.grid.addWidget(w, x, y)

    def init_players(self):
        for i in range(0, self.numOfPlayers):
            self.ListOfPlayers.append(i)

    def init_snakes(self):
        for player_id, snakes in self.Players.items():
            for snake_id in range(0, self.numOfSnakes):
                s = Snake()
                s.init_snake(self.grid, player_id, snake_id)
                snakes.append(s)
        self.update()

    def closeEvent(self, event):
        close = QMessageBox.question(self,
                                     "QUIT",
                                     "Sure?",
                                     QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            self.eatFoodWorker.thread.terminate()
            self.EatFoodProcess.terminate()
            self.CollisionWorker.thread.terminate()
            self.CollisionProcess.terminate()
            self.CommsWorker.thread.terminate()
            self.s.close()
            event.accept()
        else:
            event.ignore()

    # Possibly we are gonna need to move this to some worker class thread but this is for starting purposes only.
    def timerEvent(self, event):
        if self.timerForMove.timerId() == event.timerId():  # One second passed
            self.timeCounter = self.timeCounter - 1
            playerNumber = self.currentIDPlaying + 1
            self.whoIsPlayingLabel.setText("Playing: Player {0}\nTime left:{1}".format(playerNumber,
                                                                                       self.timeCounter))

    def drop_food(self, x, y):
        b = self.grid.itemAtPosition(x, y).widget()

        if b.BType == BlockType.EmptyBlock:
            self.Food.append(Food(b))
            self.update()
        else:
            self.drop_food(x+1, y+1) #ovde cemo vrv zahtevati od servera drugi drop

    def keyPressEvent(self, e: QKeyEvent):
        if self.myUniqueID == self.currentIDPlaying:
            if len(self.Players[self.myUniqueID]) != 0:
                # ovde takodje trebaju provere da se registruju samo dozvoljeni tasteri
                cought_key = e.key()
                if cought_key == Qt.Key_Up or cought_key == Qt.Key_Down or cought_key == Qt.Key_Left or cought_key == Qt.Key_Right:
                    self.KeyStrokes.append(cought_key)
                    sendString = "Command/{0}/{1}/{2};".format(QKeySequence(e.key()).toString(), self.myUniqueID, 0)  # kasnije resiti id zmije
                    self.comms_to_send_queue.put(sendString)
                time.sleep(0.05)

    @pyqtSlot()
    def receive_from_eatfood_worker(self):
        print("Signal received ")
        print(self.signalCounter)

        # self.Snakes[0].body_increase(self.grid)
        print("\n Food count ")
        print(len(self.Food))
        self.signalCounter = self.signalCounter + 1

    @pyqtSlot()
    def receive_from_collision_worker(self):
        # print("Signal from collision worker recieved")
        self.update()
        # print(self.signalFromCollision)
        self.signalFromCollision = self.signalFromCollision + 1

    @pyqtSlot()
    def receive_from_communication_worker(self):
        print("Signal from comm worker received")
        raw_data = self.comms_to_receive_queue.get()
        messages = raw_data.split(";")

        for message in messages[:-1]:
            # print("Received: ", message)
            if "Playing" in message:
                # da obavi i poslednji korak prethodnog igraca pre nego se igra nastavi i promene bitni parametri
                time.sleep(0.5)
                self.KeyStrokes.clear() # moze se desiti da zaostanu neki key-evi u listi i dodje do desinhronizacije
                splitlist = message.split("/")
                playerNumber = int(splitlist[1])
                self.currentIDPlaying = playerNumber
                playerNumber = playerNumber+1  # for nice print
                self.timeCounter = 10
                self.whoIsPlayingLabel.setText("Playing: Player {0}\nTime left:{1}".format(playerNumber, self.timeCounter))
                if self.firstTimeGotID:
                    self.timerForMove.start(1000, self)
                    self.firstTimeGotID = False
                self.PlayerSnakeId[0] = self.currentIDPlaying
                self.PlayerSnakeId[1] = 0
            elif "DropFood" in message:
                splitlist = message.split("/")
                xf = int(splitlist[1])
                yf = int(splitlist[2])
                self.drop_food(xf, yf)
            elif "Command" in message:
                splitlist = message.split("/")
                key = splitlist[1]
                commandPlayerID = int(splitlist[2])
                commandSnakeID = int(splitlist[3])
                print("Command received: {0}, Player ID: {1}, Snake ID:{2}".format(key, commandPlayerID,
                                                                                   commandSnakeID))
                self.PlayerSnakeId[0] = commandPlayerID
                self.PlayerSnakeId[1] = commandSnakeID

                if key == 'Left':
                    self.KeyStrokes.append(Qt.Key_Left)
                elif key == 'Right':
                    self.KeyStrokes.append(Qt.Key_Right)
                elif key == 'Up':
                    self.KeyStrokes.append(Qt.Key_Up)
                elif key == 'Down':
                    self.KeyStrokes.append(Qt.Key_Down)

            elif message == "":
                pass
            else:
                print("Message not recognized")