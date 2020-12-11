from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget, QComboBox, QMessageBox, QLabel, \
    QVBoxLayout, QInputDialog, QSpinBox, QGraphicsItem
from PyQt5.QtGui import QPixmap, QCursor, QKeyEvent, QFont, QImage, QBrush, QColor
from PyQt5.QtCore import Qt, QRectF
import sys

from DRS2020.GameWindow import  GameWindow


class SettingsWindow(QMainWindow):
        SettingsWindowH =500
        SettingsWindowW =800

        def __init__(self, mainwind):  # Here we initialize MainWindow class
            super(SettingsWindow, self).__init__()  # Here we initialize base class (Super class)  i.e QWidget
            self.resize(self.SettingsWindowH, self.SettingsWindowW)
            self.setMinimumHeight(self.SettingsWindowH)
            self.setMinimumWidth(self.SettingsWindowW)
            self.setMaximumHeight(self.SettingsWindowH)
            self.setMaximumWidth(self.SettingsWindowW)
            self.setWindowTitle("Choose number of players and snakes")
            self.setStyleSheet("background-color: black;")

            self.spin = QSpinBox(self)
            self.spin.setGeometry(350, 100, 100, 40)
            self.spin.valueChanged.connect(self.show_result)
            self.spin.setStyleSheet("background-color: lightgreen; border:2px solid blue;")
            #self.label = QLabel(self)
            self.label_1 = QLabel('Number of players', self)
            self.label_1.setFont(QFont('Calibri', 10))
            self.label_1.move(320, 80)
            self.label_1.resize(165, 20)
            self.label_1.setStyleSheet("background-color: lightgreen; ")

            self.spin_2 = QSpinBox(self)
            self.spin_2.setGeometry(350, 200, 100, 40)
            self.spin_2.valueChanged.connect(self.show_result_2)
            self.spin_2.setStyleSheet("background-color: lightgreen; border:2px solid blue;")
            # self.label = QLabel(self)
            self.label_2 = QLabel('Number of snakes', self)
            self.label_2.setFont(QFont('Calibri', 10))
            self.label_2.move(320, 180)
            self.label_2.resize(165, 20)
            self.label_2.setStyleSheet("background-color: lightgreen")

            self.continueButton = QtWidgets.QPushButton("", self)
            self.continueButton.setStyleSheet(
                "border:2px solid blue; color: " "blue;font-size: 27px; font-family: Calibri; "
                "background-image: url(resources/ContinueButton.jpg);")
            self.continueButton.setGeometry(275, 340, 250, 50)
            self.continueButton.setCursor(Qt.PointingHandCursor)
            self.continueButton.released.connect(self.run)

            # show all the widgets
            self.show()

        def show_result(self):
            # getting current value
            value = self.spin.value()
            # setting value of spin box to the label
           #self.label.setText("Value : " + str(value))

        def show_result_2(self):
            # getting current value
            value = self.spin_2.value()

        def run(self):
            #print("Run Run")
            self.gameWindow = GameWindow(self)
            self.hide()










