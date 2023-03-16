import unittest
import os
import sys
from fileClass import fileClass
from fileParser import file_chooser, fileAnalyzer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox



class TestForErrors(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        self.msg = "holder"
        self.path = '/Users/tyler/Desktop/Data Processing/MR230210 Summary/MR230210 - 2x1 Array in Carbon Fiber 4 Ply/'
        self.sample_folder = os.listdir('/Users/tyler/Desktop/Data Processing/MR230210 Summary/MR230210 - 2x1 Array in Carbon Fiber 4 Ply/')
        #self.test_files = {}


    def test_file_chooser(self):
        
        result = file_chooser(self.sample_folder, self.path, self.msg)
        print("Result" , result)
        fileAnalyzer()




if __name__ == '__main__':
    unittest.main()



