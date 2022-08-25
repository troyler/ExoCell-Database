from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5 import uic
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        container = Q

        self.setWindowTitle("TFFC")

        self.button = QPushButton("Press")
        self.button.clicked.connect(self.fileOpener)


    def fileOpener(self):
        self.button.setText("1")




app = QApplication([]) 

window= MainWindow()
window.show()

app.exec_()