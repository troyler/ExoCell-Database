from ctypes import alignment
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPalette, QColor, QActionEvent
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl


fileDictionary = {}
currentDirectoryList =[]
namingConv = {}

app = QApplication(sys.argv) 
class MainWindow(QMainWindow):
    

    def __init__(self):
        super(MainWindow, self).__init__()

        
        self.namingBreakdown = {}

        self.chooseSaveLocationButton = QtWidgets.QPushButton("Press to choose save location")
        self.chooseSaveLocationButton.clicked.connect(lambda: self.saveLocation())
        self.saveLocationStamp = QtWidgets.QLabel("Save Location")
        self.saveLocationLabel = QtWidgets.QLabel("-------------")

        self.setWindowTitle("TFFC Data Automation")
        self.openFileButton = QtWidgets.QPushButton("Press to open files")
        self.openFileButton.clicked.connect(lambda : self.fileChooser())
        self.fileListWidget = QtWidgets.QListWidget()
        self.fileListWidget.setAlternatingRowColors(True)
        self.namingLabel = QtWidgets.QLabel("File Breakdown")
        self.analysisButton = QtWidgets.QPushButton("Analyze files")     
        self.analysisButton.clicked.connect(lambda: self.fileRunner(namingConv))  
        self.fileTableBreak= QtWidgets.QTableWidget(4,4)

        self.horizontalLayout = QHBoxLayout()

        self.fileOpenerLayout = QVBoxLayout()
        self.fileOpenerLayout.addWidget(self.fileListWidget)
        self.fileOpenerLayout.addWidget(self.openFileButton)

        self.fileViewerLayout = QVBoxLayout()
        self.fileViewerLayout.addWidget(self.namingLabel)
        self.fileViewerLayout.addWidget(self.fileTableBreak)
        self.fileViewerLayout.addWidget(self.analysisButton)

        self.fileSaveLayout = QVBoxLayout()
        self.fileSaveLayout.addWidget(self.saveLocationStamp)
        self.fileSaveLayout.addWidget(self.saveLocationLabel)
        self.fileSaveLayout.addWidget(self.chooseSaveLocationButton)

        self.horizontalLayout.addLayout(self.fileOpenerLayout)
        self.horizontalLayout.addLayout(self.fileSaveLayout)
        self.horizontalLayout.addLayout(self.fileViewerLayout)

        widget = QWidget()
        widget.setLayout(self.horizontalLayout)
        self.setCentralWidget(widget)
       # self.fileViewerFunc()


    
#function to bring in file paths as strings in a list
    def fileChooser(self):   
        fname = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file", "", "FCD Files (*.fcd)") #tuple ([list of strings], string)
        for file in fname[0]:   #for each file in self.fname[0], where the list of file paths is held
            if file not in currentDirectoryList:   #checking to make sure current file path is not in list to hold filepaths
                currentDirectoryList.append(file)   #adding the file to the list holding the file paths outside of self.fname
                self.fileTitle = file[file.rindex('/')+1:-4]  #removing the path to obtain just the filename
                fileSplit = file.split("_")
                if len(fileSplit[3]) == 8:
                    cellName = fileSplit[3]
                    testTypeCount = fileSplit[4].replace(" ", "")
                    if "SC" or "Cond" or "OCV" in testTypeCount and len(testTypeCount) <=6:
                        cellTestNumber = str(fileSplit[-1][0])
                        otherInfo = " ".join(fileSplit[4:-1])
                        namingConv[cellTestNumber] = {"Cell ID" : cellName,
                                                        "Test Iteration" : testTypeCount,
                                                        "Other Info" : otherInfo,
                                                        "File Location" : file,
                                                        "File Title": self.fileTitle}
                        print(cellName, testTypeCount, cellTestNumber, otherInfo)
                self.fileListWidget.addItem(self.fileTitle)
            else: 
                return
        print(namingConv)
        self.fileViewerFunc()



    def filenameBreakdown(self):
        pass



    def fileViewerFunc(self):
        x=0
        y= 0
        self.keys = sorted((namingConv.keys()))

        self.horizontalHeaders = ["Test Number" , "Test Type/Iteration", "Cell ID", "File Title", "Other Info"]
        self.fileTableBreak.setColumnCount(len(self.horizontalHeaders))
        self.fileTableBreak.setRowCount(len(currentDirectoryList))
        while x < len(currentDirectoryList):
            self.fileTableBreak.setHorizontalHeaderLabels(self.horizontalHeaders)
            self.fileTableBreak.setItem(x,0,QTableWidgetItem(self.keys[x]))
            self.fileTableBreak.setItem(x,1,QTableWidgetItem(namingConv[self.keys[x]]["Test Iteration"]))
            self.fileTableBreak.setItem(x,2,QTableWidgetItem(namingConv[self.keys[x]]["Cell ID"]))
            self.fileTableBreak.setItem(x,3,QTableWidgetItem(namingConv[self.keys[x]]["File Title"]))
            self.fileTableBreak.setItem(x,4,QTableWidgetItem(namingConv[self.keys[x]]["Other Info"]))
            x+=1
            y+=1
            
    def fileRunner(self, x):
        y = 0
        while y < len(currentDirectoryList):
            self.fileAnalyzer(namingConv[self.keys[y]]["File Location"], namingConv[self.keys[y]]["File Title"])
            y+= 1
        print(fileDictionary)
        self.writingToExcel()



    def fileAnalyzer(self, incoming, name):
        with open(incoming, "r", encoding='latin_1') as workingFile: 
            cleanData = []  #opening and reading the incoming file as workingFile
            for line in workingFile:              #for each line in this file 
                dataInfo = line.strip().split('\t')     #strip this line of unneeded info and split it by tab. Append each item split to a list
                if len(dataInfo) > 10:
                    cleanData.append(dataInfo)
            if cleanData[0][0] == "Time (Sec)" :  
                    fileDictionary[name] = pd.DataFrame(cleanData[1:], columns=cleanData[0])
                    #print(fileDictionary[name])

    def saveLocation(self):
        self.savingLocation = QtWidgets.QFileDialog.getSaveFileName(self, "Open file") #tuple ([list of strings], string)
        self.locationPath = self.savingLocation[0]
        self.saveLocationLabel.setText(self.locationPath)

    def writingToExcel(self):
        x= 0
        while x < len(currentDirectoryList):
            with pd.ExcelWriter(f"{self.locationPath}", mode = "a") as writer:
                writer.if_sheet_exists = 'replace'
                currentFileName = namingConv[self.keys[x]]["File Title"]
                fileDictionary[currentFileName].to_excel(writer, sheet_name = f"{currentFileName[0:30]}", index = False, engine = openpyxl)
                writer.save()
                print("saving")
                x+=1

  

               

        
 



window = MainWindow()
window.show()

sys.exit(app.exec_())