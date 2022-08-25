import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton
from PyQt5.QtCore import Qt, QUrl
from asyncore import read
from distutils.command import clean
from pathlib import Path
from re import X
import os
from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
import matplotlib.ticker as ticker
from bokeh.plotting import figure, save, gridplot, output_file


class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(600, 600)



class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 600)

        self.listbox_view = ListBoxWidget(self)

        self.btn = QPushButton('Get Value', self)
        self.btn.setGeometry(850, 400, 200, 50)
        self.btn.clicked.connect(lambda: print(self.readFiles()))

    def getSelectedItem(self):
 
        item = QListWidgetItem(self.listbox_view.currentItem())
        reading = (r'{}').format(item.text())    
        filenames = glob.glob(reading + "/*.fcd")
        return filenames

    def readFiles(self):
        fileDictionary = {}
        cleanData = []
        for filename in self.getSelectedItem():
            fileTitle = filename[filename.rindex('/')+1:]
            with open(filename, "r", encoding='latin_1') as file:
                for line in file:
                    dataInfo = line.strip().split('\t')
                    if len(dataInfo) > 10:
                            cleanData.append(dataInfo)
            if cleanData[0][0] == "Time (Sec)" :  #mainly for QA 
                fileDictionary[fileTitle] = pd.DataFrame(cleanData[1:], columns=cleanData[0])
                occurence = fileDictionary[fileTitle]
                
        

            


    





if __name__ == '__main__':
    app = QApplication([])

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())