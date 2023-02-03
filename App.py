import sys
from fileInformer import fileInfo, sc_tests, OCV_tests, cond_tests
import re
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

#Software developed and written by Tyler Reinert
#Fuck you Ron

test_files = {}
fileList = []
cell_criteria = {
                "Surface Area": [], 
                "Hydrogen Flow" : [],
                 "Initial Current Density": [], 
                 "Startup OCV" : [],
                  "Steady State Current" : [],
                  "Steady State Current Density" : [],
                   "Max Power Density" : [],
                   "Voltage at Max Power Density" : [],
                   "Time at Max Power Density" : []}
                   
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
        self.clearButton = QtWidgets.QPushButton("Press to clear files")
        self.clearButton.clicked.connect(lambda: self.clearFiles(test_files))
        self.fileListWidget = QtWidgets.QListWidget()
        self.fileListWidget.setAlternatingRowColors(True)
        self.namingLabel = QtWidgets.QLabel("File Breakdown")
        self.analysisButton = QtWidgets.QPushButton("Create Excel Files")     
        self.analysisButton.clicked.connect(lambda: self.fileRunner(test_files))   
        self.fileTableBreak= QtWidgets.QTableWidget(6,6)


        self.input_cell_size = QtWidgets.QLineEdit()
        self.input_comp_material = QtWidgets.QLineEdit()
        self.input_comp_pattern = QtWidgets.QLineEdit()
        self.input_comp_force = QtWidgets.QLineEdit()

        self.input_cell_size.editingFinished.connect(lambda: self.enterPress(self.input_cell_size.text(), "Cell Size"))
        self.input_comp_material.editingFinished.connect(lambda: self.enterPress(self.input_comp_material.text(), "Compression Material"))
        self.input_comp_pattern.editingFinished.connect(lambda: self.enterPress(self.input_comp_pattern.text(),"Compression Pattern (shape, contact %)" ))
        self.input_comp_force.editingFinished.connect(lambda : self.enterPress(self.input_comp_force.text(), "Compression Force"))


        self.flo = QtWidgets.QFormLayout()
        self.flo.addRow("Cell Size\n", self.input_cell_size)
        self.flo.addRow("Compression Material\n", self.input_comp_material)
        self.flo.addRow("Compression Pattern (shape, contact %)\n", self.input_comp_pattern)
        self.flo.addRow("Compression Force\n", self.input_comp_force)






        self.horizontalLayout = QVBoxLayout()
        self.topVertLayout = QVBoxLayout()
        self.midVertLayout = QVBoxLayout()
    

        self.fileOpenerLayout = QHBoxLayout()
        self.fileOpenerLayout.addLayout(self.topVertLayout)
        self.fileOpenerLayout.addWidget(self.fileListWidget)
        self.topVertLayout.addWidget(self.openFileButton)
        self.topVertLayout.addWidget(self.clearButton)

        self.fileViewerLayout = QHBoxLayout()
        self.fileViewerLayout.addLayout(self.midVertLayout)
        self.fileViewerLayout.addWidget(self.fileTableBreak)
        self.midVertLayout.addWidget(self.analysisButton)
        self.midVertLayout.addWidget(self.button)

        self.fileSaveLayout = QHBoxLayout()
        self.fileSaveLayout.addLayout(self.flo)
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
    
    def textchanged(self,text):
                print("Changed: " + text)

    def enterPress(self, text, criteria):
        print("Enter pressed: " + text + criteria)
        keyCriteria[criteria] = text
        print(keyCriteria)
        

    def clearFiles(self, test_files):
        fileList.clear()
        test_files.clear()
        self.fileTableBreak.clear()
        cell_criteria = {
                "Surface Area": [], 
                "Hydrogen Flow" : [],
                 "Initial Current Density": [], 
                 "Startup OCV" : [],
                  "Steady State Current" : [],
                  "Steady State Current Density" : [],
                   "Max Power Density" : [],
                   "Voltage at Max Power Density" : [],
                   "Time at Max Power Density" : []}
        cell_criteria.update()
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
        keyCriteria.update()
        self.fileListWidget.clear()
        self.w.info = keyCriteria
        self.w.surface_area = cell_criteria
        

    
    def use_regex(self,input_text):
        pattern = re.compile(r"[0-9]_[A-Za-z0-9]+_[A-Za-z0-9]+_[0-9]*\.[0-9]+[a-zA-Z]+_([A-Za-z0-9]+( [A-Za-z0-9]+)+)_([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?(\s([A-Za-z0-9]+\s)+)[A-Za-z0-9]+_([0-9]+(-[0-9]+)+)", re.IGNORECASE)
        print(pattern.match(input_text))
        return pattern.match(input_text)

    def show_new_window(self):
        print(keyCriteria)
        print(cell_criteria)
        counter = 0
        tests = []
        file_objects = list(test_files.values())
        while counter < len(file_objects):
            file = file_objects[counter]
            tests.append(test_files.get(file.file_path).test_name)
            counter +=1 
        #file_path, cell_id, test_name, test_type, test_number, test_date, other
        if "Cond2" not in tests:
             self.msg.setText("No Cond 2, need cond2 for key info")
             self.msg.exec_()  
        self.w = AnotherWindow()
        desired_order_list = ["Cell Name", "Cell Size", "Date Tested", "Hydrogen Flow","Compression Material", "Compression Pattern (shape, contact %)", "Compression Force", "Initial Current Density", "Startup OCV", "Steady State Current", "Steady State Current Density", "Max Power Density"]
        reordered_dict = {k: keyCriteria[k] for k in desired_order_list}
        self.w.info = reordered_dict
        self.w.surface_area = cell_criteria
        self.w.show()
    
#function to bring in file paths as strings in a list

    def file_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file", "", "FCD Files (*.fcd)")[0] #tuple ([list of strings], string)
        result = file_chooser(fname, fileList, test_files, self.msg)
        self.fileListWidget.clear()
        x = 0  #make verbose names for variables for high readability and obvious purpose identification 
        file_objects = list(result.values())  #file_path, cell_id, test_name, test_type, test_number, test_date, other
        while x < len(file_objects):
            file = file_objects[x]
            self.fileListWidget.addItem(file.file_path)
            x+=1
        test_files.update(result)
        fileViewerFunc(test_files, self.fileTableBreak)
        return result

    def fileRunner(self, test_files):
        if len(test_files) > 0:
            x = 0
            file_objects = list(test_files.values())  
            while x < len(file_objects):
                file = file_objects[x]
                fileAnalyzer(test_files.get(file.file_path).location, test_files.get(file.file_path), test_files, keyCriteria, cell_criteria)
                x += 1
            checksum = 0
            for file in file_objects:
                if file.is_cond():
                    checksum += 1

            if checksum == len(test_files):
                get_steadyState_current(test_files, checksum, keyCriteria)    

            self.writingToExcel()
            
            self.fileViewerLayout.addWidget(self.button)
            #initial_current_density(test_files)
        else:
            self.msg.setText("Please choose files")
            self.msg.exec_()

    def saveLocation(self):
        self.locationPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Open file") #tuple ([list of strings], string)
        self.saveLocationLabel.setText(self.locationPath)


    def writingToExcel(self):
        if (self.locationPath != None):
            file_objects = list(test_files.values())  #file_path, cell_id, test_name, test_type, test_number, test_date, other
            x= 0
            while x < len(file_objects):
                file = file_objects[x]
                currentFileName = file.file_path
                with pd.ExcelWriter(f"{self.locationPath}/{currentFileName}.xlsx") as writer:
                    writer.if_sheet_exists = 'replace'
                    test_files.get(file.file_path).testing_time.to_excel(writer, sheet_name = f"{currentFileName[0:25]}", engine="xlsxwriter", index = False, startrow = 0)
                    test_files.get(file.file_path).excel_sheet.to_excel(writer, sheet_name = f"{currentFileName[0:25]}", engine="xlsxwriter", index = False, startrow = 3)
                    self.saveLocationStamp.setText(f"Saving {currentFileName} to")
                    writer.save()
                    print("saving")
                    x+=1
            self.saveLocationStamp.setText("Saving Complete")
        else:
            self.msg.setText("No save Location given")
            self.msg.exec_()

    
if  __name__ == "__main__":
   
    app = QApplication(sys.argv)  
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

