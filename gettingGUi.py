from PyQt5 import QtCore, QtGui, QtWidgets
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()

        self.setWindowTitle("TFFC Data Automation")
    

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.filePlace = QtWidgets.QWidget()
        self.fileButton = QtWidgets.QWidget()
        self.analysisButton = QtWidgets.QWidget()

        lay = QtWidgets.QGridLayout(central_widget)

      
        lay.addWidget(self.filePlace, 0, 2)
        lay.addWidget(self.fileButton, 1 ,2)
        lay.addWidget(self.analysisButton, 2, 2)

        lay = QtWidgets.QVBoxLayout(self.analysisButton)
        self.analysis = QtWidgets.QPushButton("Press to Analyze files")
        lay.addWidget(self.analysis)
        self.analysis.clicked.connect(lambda: self.fileRunner(self.currentDirectorylist))


        lay = QtWidgets.QVBoxLayout(self.filePlace)
        self.fileHolder = QtWidgets.QListWidget()
        lay.addWidget(self.fileHolder)

        lay = QtWidgets.QVBoxLayout(self.fileButton)
        self.button = QtWidgets.QPushButton("Press to open files")
        lay.addWidget(self.button)
        self.button.clicked.connect(lambda : self.fileChooser())

        self.fileDictionary= {}
        self.currentDirectorylist =[]


if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    app.exec_()