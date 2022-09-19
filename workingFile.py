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
    


    def fileChooser(self):
        self.fname = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file", "", "FCD Files (*.fcd)")
        if self.fname:
            for self.file in self.fname[0]:
                self.fileTitle = self.file[self.file.rindex('/')+1:]
                self.fileHolder.addItem(self.fileTitle)
                if self.file not in self.currentDirectorylist:
                    self.currentDirectorylist.append([self.file, self.fileTitle])


    
    def fileRunner(self, x):
        for thingy in enumerate(x):
            self.fileParser(thingy[1][0],thingy[1][1])

        
    def fileParser(self, incoming, name):
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



if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    app.exec_()