import unittest
import sys
import os


from App import MainWindow
from fileInformer import fileInfo,sc_tests,OCV_tests,cond_tests
from fileChooser import file_chooser




class TestForErrors(unittest.TestCase):

    def testFolder(self):
        test_files = {}
        folder = os.listdir("/Users/tyler/Desktop/ExoCell/FCD Files")
        result = file_chooser(folder)
        for each in folder:
            thisPass = result.get(each)
            if "None" not in thisPass.__str__() :
                print(thisPass.__str__())
                print(thisPass.test_number)


        


if __name__ == '__main__':
    unittest.main()