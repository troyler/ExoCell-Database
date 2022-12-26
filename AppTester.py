import unittest
import sys
import os

import re


from App import *
from fileInformer import fileInfo,sc_tests,OCV_tests,cond_tests
from fileChooser import file_chooser,fileAnalyzer




class TestForErrors(unittest.TestCase):

    def testFolder(self):
        print(194 + 155 + 229 + 92)
        folder = os.listdir("/Users/tyler/Desktop/ExoCell/FCD Files")
        result = file_chooser(folder)
        for each in folder:
            thisPass = result.get(each)
            if "None" not in thisPass.__str__() :
                print(thisPass.file_path)
                self.assertEqual(thisPass.__str__()[0], thisPass.test_number[0])


        


if __name__ == '__main__':
    unittest.main()