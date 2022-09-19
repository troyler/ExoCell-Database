from ctypes import alignment
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPalette, QColor, QActionEvent
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

app = QApplication([])
class MainWindow(QMainWindow):

    currentDirectorylist =[]
    namingBreakdown = {}
    
    

    def __init__(self):
        super(MainWindow, self).__init__()

        self.fileDictionary = {}

        widget = QWidget()
        self.setCentralWidget(widget)

        self.horizontalLayout = QHBoxLayout()
        self.fileOpenerLayout = QVBoxLayout()
        self.fileViewerLayout = QVBoxLayout()

        widget.setLayout(self.horizontalLayout)

        self.setWindowTitle("TFFC Data Automation")
        
        self.openFileButton = QtWidgets.QPushButton("Press to open files")
        self.openFileButton.clicked.connect(lambda: self.fileChooser())
        self.fileHolder = QtWidgets.QListWidget()
        self.fileHolder.setAlternatingRowColors(True)
        self.namingLabel = QtWidgets.QLabel("File Breakdown")


        self.horizontalLayout.addLayout(self.fileOpenerLayout)
        self.horizontalLayout.addLayout(self.fileViewerLayout)
        
        self.fileViewerLayout.addWidget(self.namingLabel)
        self.fileViewer = QtWidgets.QTableWidget(4,4)
        self.fileViewerLayout.addWidget(self.fileViewer)

        
        self.fileOpenerLayout.addWidget(self.fileHolder)
        self.fileOpenerLayout.addWidget(self.openFileButton)

        self.analysisButton = QtWidgets.QPushButton("Analyze files")     
        self.analysisButton.clicked.connect(self.fileRunner(self.fileDictionary))

        self.fileViewerFunc()
        



    

    def fileChooser(self):
        self.fname = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file", "", "FCD Files (*.fcd)") #tuple ([list of strings], string)
        for self.file in self.fname[0]:
            if self.file not in self.currentDirectorylist:
                self.fileTitle = self.file[self.file.rindex('/')+1:]
                self.namingBreakdown[self.file] = [self.fileTitle, self.fileTitle[0:8]]
                self.currentDirectorylist.append(self.file)
                self.fileHolder.addItem(self.fileTitle)
            else: 
                return
        self.fileViewerFunc()
            


    def fileViewerFunc(self):
        x = 0
        self.tableHeaders = ["File Name", "File Type", "Date"]
        self.fileViewerLayout.removeWidget(self.fileViewer)
        self.fileViewer = QtWidgets.QTableWidget(len(self.currentDirectorylist), len(self.tableHeaders))
        self.fileViewer.setHorizontalHeaderLabels(self.tableHeaders)
        while x < len(self.currentDirectorylist):
            self.fileViewer.setItem(x,0, QTableWidgetItem(self.currentDirectorylist[x])) 
            self.fileViewer.setItem(x,1, QTableWidgetItem(self.namingBreakdown[self.currentDirectorylist[x]][0]))
            self.fileViewer.setItem(x,2, QTableWidgetItem(self.namingBreakdown[self.currentDirectorylist[x]][1]))  #need to make dictionary based on naming convention to parse here
            x+= 1
        self.fileViewerLayout.addWidget(self.fileViewer)
        self.fileViewerLayout.addWidget(self.analysisButton)
        print(self.currentDirectorylist)


    def saveLocation(self):
        return


    def fileRunner(self, x):
        y = 0
        while y < len(self.currentDirectorylist):
            self.fileAnalyzer(self.currentDirectorylist[y], x[self.currentDirectorylist[y]][0])
            y+= 1

    def fileAnalyzer(self, incoming, name):
        cleanData = []
        with open(incoming, "r", encoding='latin_1') as workingFile:
            for line in workingFile:
                dataInfo = line.strip().split('\t')
                if len(dataInfo) > 10:
                    cleanData.append(dataInfo)
        if cleanData[0][0] == "Time (Sec)" :  #mainly for QA 
            self.fileDictionary[name] = pd.DataFrame(cleanData[1:], columns=cleanData[0])
        occurence = self.fileDictionary[name]

        testTitle = name
        timeTitle = occurence.columns[0]
        voltageTitle = occurence.columns[5]
        currentDensityTitle = occurence.columns[2]
        powerDensityTitle = occurence.columns[4]

        if "OCV" in incoming:
            x = occurence['Time (Sec)']
            x = np.array(list(map(float, x)))
            y = occurence['E_Stack (V)']
            y = np.array(list(map(float, y)))
            self.plotMechs(x, y,timeTitle, voltageTitle, testTitle)

        elif "Cond" in incoming:
            x = (occurence['Time (Sec)'])
            x = np.array(list(map(float, x)))
            y = occurence['I (mA/cm²)']
            y = np.array(list(map(float, y)))
            self.plotMechs(x, y,timeTitle,currentDensityTitle, testTitle)

        elif "SC" in incoming:
            x = (occurence['I (mA/cm²)'])
            y = occurence['E_Stack (V)']
            z = occurence['Power (mW/cm²)']
            x = np.array(list(map(float, x)))
            y = np.array(list(map(float, y)))
            z = np.array(list(map(float, z)))
            plt.yticks(np.arange(0, 1.1, 0.1))
            self.plotMechs(x, y, currentDensityTitle,voltageTitle, testTitle)
            self.plotMechs(x, z, currentDensityTitle, powerDensityTitle, testTitle)
    
    def plotMechs(self, x, y, xtitle, ytitle, fileTitle):
        
        plt.scatter(x,y, marker=".", s=1)

        plt.xlabel(xtitle, fontsize=15)
        plt.ylabel(ytitle, fontsize=15)
        plt.title(f" {fileTitle} ", fontsize=20,pad=10)

        plt.grid(True)
        plt.show()
        plt.figure()



    



window = MainWindow()
window.show()

app.exec()