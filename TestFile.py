# This file is used for testing purposes of new blocks of code
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication)
from PyQt5.QtGui import QPixmap
import sys


class UIGameMode(QWidget):
    def __init__(self, parent=None):
        super(UIGameMode, self).__init__(parent)
        self.initGameModeButtons()

    def initGameModeButtons(self):

        self.singlePlayerButton = QtWidgets.QPushButton("", self)
        self.startButton.setStyleSheet(
            "border:2px solid blue; color: " "blue;font-size: 27px; font-family: Calibri; "
            "background-image: url(resources/SPButton.jpg);")
        self.singlePlayerButton.setGeometry(275, 500, 250, 50)
        self.singlePlayerButton.released.connect(self.run)

# noinspection PyMethodMayBeStatic
    def run(self):
        # print("Run Run")
        self.settings = SettingsWindow(self)
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
