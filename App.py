import sys
from fileInformer import fileInfo, sc_tests, OCV_tests, cond_tests
import re
from distutils.filelist import FileList
from operator import itemgetter
from fileChooser import file_chooser, fileViewerFunc, fileAnalyzer
from SummaryWindow import AnotherWindow
from fileInformer import OCV_tests,sc_tests,cond_tests,fileInfo
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
import os

test_files = {}
xlsxFiles = []
fileDictionary = {}
currentDirectoryList =[]
fileList = []
namingConv = {}
summaryList = ["Files graphed in this sheet", "    "]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(0,300,1000,700)
        self.locationPath = None

        self.w = None  # No external window yet.
        self.button = QtWidgets.QPushButton("Push for Window")
        self.button.clicked.connect(lambda: self.show_new_window())

        self.msg = QtWidgets.QMessageBox()

        self.chooseSaveLocationButton = QtWidgets.QPushButton("Press to choose save location")
        self.chooseSaveLocationButton.clicked.connect(lambda: self.saveLocation())
        self.saveLocationStamp = QtWidgets.QLabel("Save Location")
        self.saveLocationLabel = QtWidgets.QLabel("-------------")
        self.saveLocationLabel.setWordWrap(True)
        self.saveLocationLabel.setMaximumWidth(150)

        self.setWindowTitle("TFFC Data Automation")
        self.openFileButton = QtWidgets.QPushButton("Press to open files")
        self.openFileButton.clicked.connect(lambda : self.file_open())
        self.fileListWidget = QtWidgets.QListWidget()
        self.fileListWidget.setAlternatingRowColors(True)
        self.namingLabel = QtWidgets.QLabel("File Breakdown")
        self.analysisButton = QtWidgets.QPushButton("Create Excel Files")     
        self.analysisButton.clicked.connect(lambda: self.fileRunner(test_files))   
        self.fileTableBreak= QtWidgets.QTableWidget(6,6)

        self.horizontalLayout = QHBoxLayout()
    

        self.fileOpenerLayout = QVBoxLayout()
        self.fileOpenerLayout.addWidget(self.fileListWidget)
        self.fileOpenerLayout.addWidget(self.openFileButton)

        self.fileViewerLayout = QVBoxLayout()
        self.fileViewerLayout.addWidget(self.namingLabel)
        self.fileViewerLayout.addWidget(self.fileTableBreak)
        self.fileViewerLayout.addWidget(self.analysisButton)
        self.fileViewerLayout.addWidget(self.button)

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
        self.popups = []
        

    def use_regex(self,input_text):
        pattern = re.compile(r"[0-9]_[A-Za-z0-9]+_[A-Za-z0-9]+_[0-9]*\.[0-9]+[a-zA-Z]+_([A-Za-z0-9]+( [A-Za-z0-9]+)+)_([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?(\s([A-Za-z0-9]+\s)+)[A-Za-z0-9]+_([0-9]+(-[0-9]+)+)", re.IGNORECASE)
        print(pattern.match(input_text))
        return pattern.match(input_text)

    def show_new_window(self):
        w = AnotherWindow()
        w.show()


    
#function to bring in file paths as strings in a list

    def file_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file", "", "FCD Files (*.fcd)")[0] #tuple ([list of strings], string)
        result = file_chooser(fname, self.fileListWidget)
        test_files.update(result)
        fileViewerFunc(test_files, self.fileTableBreak)
        print(result)
        return result

    def fileRunner(self, test_files):
        x = 0
        file_objects = list(test_files.values())  #file_path, cell_id, test_name, test_type, test_number, test_date, other
        while x < len(file_objects):
            file = file_objects[x]
            fileAnalyzer(test_files.get(file.file_path).location, test_files.get(file.file_path))
            x += 1
        self.writingToExcel()
        self.fileViewerLayout.addWidget(self.button)

    def saveLocation(self):
        self.locationPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Open file") #tuple ([list of strings], string)
        self.saveLocationLabel.setText(self.locationPath)


    def writingToExcel(self):
        if (self.locationPath != None):
            file_objects = list(test_files.values())  #file_path, cell_id, test_name, test_type, test_number, test_date, other
            x= 0
            while x < len(file_objects):
                file = file_objects[x]
                currentFileName =  file.file_path
                with pd.ExcelWriter(f"{self.locationPath}/{currentFileName}.xlsx") as writer:
                    writer.if_sheet_exists = 'replace'
                    test_files.get(file.file_path).excel_sheet.to_excel(writer, sheet_name = f"{currentFileName[0:25]}", engine="xlsxwriter", index = False)
                    self.saveLocationStamp.setText(f"Saving {currentFileName} to")
                    writer.save()
                    print("saving")
                    x+=1
            self.saveLocationStamp.setText("Saving Complete")
        else:
            print("No save Location given")

    
if  __name__ == "__main__":
   
    app = QApplication(sys.argv)  
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())