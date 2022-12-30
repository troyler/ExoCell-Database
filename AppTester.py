import unittest
import sys
import os
import pytestqt
import re
import sys
from fileInformer import fileInfo, sc_tests, OCV_tests, cond_tests
from distutils.filelist import FileList
from fileChooser import file_chooser, fileViewerFunc, fileAnalyzer, get_steadyState_current
from SummaryWindow import AnotherWindow
from fileInformer import OCV_tests,sc_tests,cond_tests,fileInfo
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import pandas as pd

from App import *
from fileInformer import fileInfo,sc_tests,OCV_tests,cond_tests






class TestForErrors(unittest.TestCase):

    test_files = {}
    fileList = []
    keyCriteria = {"Cell Name" : " ", 
                    "Cell Size": " ", 
                    "Date Tested" : " ", 
                    "Hydrogen Flow" : " ",
                    "Compression Material": " ",
                    "Compression Pattern (shape, contact %)" : " ", 
                    "Compression Force" : " ",
                    "Initial Current Density": " ", 
                    "Startup OCV" : " ",
                    "Steady State Current" : " ",
                    "Steady State Current Density" : " ",
                    "Max Power Density" : " "}


    def testFolder(self):
        message = " "
        folders = os.listdir("/Users/tyler/Desktop/ExoCell/ExoCell Test Files/Test Folder")
        for folder in folders:
            files = []
            for file in folder:
                files.append(file)
            result = file_chooser(files, fileList, test_files, message)
            print(result)
            

        


if __name__ == '__main__':
    unittest.main()