#file breakdown system 


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


fileDictionary = {"OCV": [], "SC": []}
currentDirectoryList =[]
namingBreakdown = {}


class MainWindow(QMainWindow):
    

    def __init__(self):
        super(MainWindow, self).__init__()



        self.setWindowTitle("TFFC Data Automation")
        self.openFileButton = QtWidgets.QPushButton("Press to open files")
        self.openFileButton.clicked.connect(lambda : self.fileChooser())
        self.fileListWidget = QtWidgets.QListWidget()
        self.fileListWidget.setAlternatingRowColors(True)
        self.namingLabel = QtWidgets.QLabel("File Breakdown")
        self.analysisButton = QtWidgets.QPushButton("Analyze files")     
        self.analysisButton.clicked.connect(lambda: self.fileRunner(namingBreakdown))  
        self.fileTableBreak= QtWidgets.QTableWidget(4,4)

        self.horizontalLayout = QHBoxLayout()

        self.fileOpenerLayout = QVBoxLayout()
        self.fileOpenerLayout.addWidget(self.fileListWidget)
        self.fileOpenerLayout.addWidget(self.openFileButton)

        self.fileViewerLayout = QVBoxLayout()
        self.fileViewerLayout.addWidget(self.namingLabel)
        self.fileViewerLayout.addWidget(self.fileTableBreak)

        self.horizontalLayout.addLayout(self.fileOpenerLayout)
        self.horizontalLayout.addLayout(self.fileViewerLayout)

        widget = QWidget()
        widget.setLayout(self.horizontalLayout)
        self.setCentralWidget(widget)


    
#function to birng in file paths as strings
    def fileChooser(self):   
        self.fname = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file", "", "FCD Files (*.fcd)") #tuple ([list of strings], string)
        for self.file in self.fname[0]:   #for each file in self.fname[0], where the list of file paths is held
            if self.file not in currentDirectoryList:   #checking to make sure current file path is not in list to hold filepaths
                currentDirectoryList.append(self.file)  #adding the file to the list holding the file paths outside of self.fname
                self.fileTitle = self.file[self.file.rindex('/')+1:]   #removing the path to obtain just the filename
                namingBreakdown[self.file] = [self.fileTitle, self.fileTitle[0:8]]    #getting the first 8 characters of the filename
                self.fileListWidget.addItem(self.fileTitle)   #adding the fileTitle to the listwidget
            else: 
                return
        self.fileViewerFunc()
        self.filenameBreakdown()
        print(namingBreakdown)

    def filenameBreakdown(self):
        for path in currentDirectoryList:
            pathFile = path[path.rindex('/')+1:-4]
            print(pathFile.split('_'))
            #cell = pathDeatiledList[3]
           # testVersion = pathDeatiledList[4]

            pathFileDate = pathFile[0:8]
            
           # namingBreakdown[testVersion] = {"Full Path": path, "File Name" : pathFile, "Test Date" : pathFileDate} #"Cell" : cell, "Test" : testVersion}


    
            


    def fileViewerFunc(self):
        x = 0
        self.tableHeaders = ["File Name", "Test Type", "Date"]
        self.fileViewerLayout.removeWidget(self.fileTableBreak)
        self.fileTableBreak= QtWidgets.QTableWidget(len(currentDirectoryList), len(self.tableHeaders))
        self.fileTableBreak.setHorizontalHeaderLabels(self.tableHeaders)
        while x < len(currentDirectoryList):
            self.fileTableBreak.setItem(x,0, QTableWidgetItem(currentDirectoryList[x])) 
            self.fileTableBreak.setItem(x,1, QTableWidgetItem(namingBreakdown[currentDirectoryList[x]][0]))
            self.fileTableBreak.setItem(x,2, QTableWidgetItem(namingBreakdown[currentDirectoryList[x]][1]))  #need to make dictionary based on naming convention to parse here
            x+= 1
        self.fileViewerLayout.addWidget(self.fileTableBreak)
        self.fileViewerLayout.addWidget(self.analysisButton)
        #print(currentDirectoryList)


    def saveLocation(self):
        return
    
    



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()