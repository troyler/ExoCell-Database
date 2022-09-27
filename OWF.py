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
        self.analysisButton.clicked.connect(lambda: self.fileRunner(self.namingBreakdown))  
        self.fileTableBreak= QtWidgets.QTableWidget(4,4)

        self.horizontalLayout = QHBoxLayout()

        self.fileOpenerLayout = QVBoxLayout()
        self.fileOpenerLayout.addWidget(self.fileListWidget)
        self.fileOpenerLayout.addWidget(self.openFileButton)

        self.fileViewerLayout = QVBoxLayout()
        self.fileViewerLayout.addWidget(self.namingLabel)
        self.fileViewerLayout.addWidget(self.fileTableBreak)

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


    
#function to birng in file paths as strings
    def fileChooser(self):   
        self.fname = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file", "", "FCD Files (*.fcd)") #tuple ([list of strings], string)
        for self.file in self.fname[0]:   #for each file in self.fname[0], where the list of file paths is held
            if self.file not in currentDirectoryList:   #checking to make sure current file path is not in list to hold filepaths
                currentDirectoryList.append(self.file)  #adding the file to the list holding the file paths outside of self.fname
                self.fileTitle = self.file[self.file.rindex('/')+1:-4]   #removing the path to obtain just the filename
                print(self.fileTitle)
                self.namingBreakdown[self.file] = [self.fileTitle, self.fileTitle[0:8]]    #getting the first 8 characters of the filename
                self.fileListWidget.addItem(self.fileTitle)
            else: 
                return
        self.fileViewerFunc()

    def filenameBreakdown(self):
        pass


    


    def fileViewerFunc(self):
        x = 0
        self.tableHeaders = ["File Name", "File Type", "Date"]
        self.fileViewerLayout.removeWidget(self.fileTableBreak)
        self.fileTableBreak= QtWidgets.QTableWidget(len(currentDirectoryList), len(self.tableHeaders))
        self.fileTableBreak.setHorizontalHeaderLabels(self.tableHeaders)
        while x < len(currentDirectoryList):
            self.fileTableBreak.setItem(x,0, QTableWidgetItem(currentDirectoryList[x])) 
            self.fileTableBreak.setItem(x,1, QTableWidgetItem(self.namingBreakdown[currentDirectoryList[x]][0]))
            self.fileTableBreak.setItem(x,2, QTableWidgetItem(self.namingBreakdown[currentDirectoryList[x]][1]))  #need to make dictionary based on naming convention to parse here
            x+= 1
        self.fileViewerLayout.addWidget(self.fileTableBreak)
        self.fileViewerLayout.addWidget(self.analysisButton)
        #print(currentDirectoryList)


    def saveLocation(self):
        self.savingLocation = QtWidgets.QFileDialog.getSaveFileName(self, "Open file") #tuple ([list of strings], string)
        self.locationPath = self.savingLocation[0]
        self.saveLocationLabel.setText(self.locationPath)


    def fileRunner(self, x):
        y = 0
        while y < len(currentDirectoryList):
            self.fileAnalyzer(currentDirectoryList[y], x[currentDirectoryList[y]][0])
            y+= 1

          #  df1 = pd.DataFrame([["AAA", "BBB"]], columns=["Spam", "Egg"])  
#>>> df2 = pd.DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])  
#>>> with pd.ExcelWriter("path_to_file.xlsx") as writer:
#...     df1.to_excel(writer, sheet_name="Sheet1")  
#...     df2.to_excel(writer, sheet_name="Sheet2")  


    def fileAnalyzer(self, incoming, name):
            cleanData = []
            with open(incoming, "r", encoding='latin_1') as workingFile:   #opening and reading the incoming file as workingFile
                for line in workingFile:              #for each line in this file 
                    dataInfo = line.strip().split('\t')     #strip this line of unneeded info and split it by tab. Append each item split to a list
                    print(dataInfo)
                    if len(dataInfo) > 10:
                        cleanData.append(dataInfo)
            if cleanData[0][0] == "Time (Sec)" :  
                    fileDictionary[name] = pd.DataFrame(cleanData[1:], columns=cleanData[0])
                    occurence = fileDictionary[name]

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
        print(fileDictionary)
    

           
       #         summaryFiles.to_excel(writer, sheet_name = "Summary Files", engine="xlsxwriter")
       #         scPlots.to_excel(writer, sheet_name = "Scan Current Plots", engine="xlsxwriter")
       #         condPlots.to_excel(writer, sheet_name = "Conditioning Plots", engine="xlsxwriter")
       #         workbook = writer.book
       #         if "Cond" in currentFileName:
       #             data = fileDictionary[currentFileName]
       #             sheetName = "Conditioning Plots"
       #             worksheet = writer.sheets[sheetName]
       #             chart=workbook.add_chart({'type':'scatter'})
       #             x = data['Time (Sec)']
       #             y = data['I (mA/cm²)']
       #             print(y)
       #             max_row = len(x)
       #             chart.add_series({
       #             'name':       "Sample Plot",
       #             'categories': [sheetName, 1, x, x],
       #             'values':     [sheetName, y, y],
       #             'marker':     {'type': 'circle', 'size': 4}})
       #             worksheet.insert_chart("D2", chart)
       #         print("saving")
       #         x+=1


    



window = MainWindow()
window.show()

sys.exit(app.exec_())