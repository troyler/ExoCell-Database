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


test_files = {}




class TestForErrors(unittest.TestCase):

    def testFolder(self):
        folder = os.listdir("/Users/tyler/Desktop/ExoCell/FCD Files")
        result = file_chooser(folder)
        print (result)
        for each in folder:
            thisPass = result.get(each)
            if "None" not in thisPass.__str__() :
                print(thisPass.file_path)
                self.assertEqual(thisPass.__str__()[0], thisPass.test_number[0])

    def test_hello(qtbot):
        widget = MainWindow()
        qtbot.addWidget(widget)

        # click in the Greet button and make sure it updates the appropriate label
        qtbot.mouseClick(widget.button_greet, QtCore.Qt.LeftButton)

        assert widget.greet_label.text() == "Hello!"


        


if __name__ == '__main__':
    unittest.main()