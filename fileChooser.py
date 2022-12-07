from fileInformer import fileInfo,OCV_tests,sc_tests,cond_tests
from operator import itemgetter
import pandas as pd
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem

fileList = []
test_files = {}

def file_chooser(folder):     
    for file in folder:
        if file != '.DS_Store':
            if "/" in file: 
                fileTitle = file[file.rindex('/')+1:-4] #this is the file title without the path or file extensions
            else:
                fileTitle = file  #for each file in self.fname[0], where the list of file paths is held
            if file not in fileList:   #checking to make sure current file path is not in list to hold filepaths
                temp_location = " "
                temp_file_path = []
                temp_cell_id = " "     #setting temp values to update and use for instantiating object for files
                temp_test_name = " "
                temp_test_type = " "
                temp_test_number = ""
                temp_date = ""
                temp_other = ""
                temp_excel_sheet = " "
                temp_file_path = fileTitle.split("_")
                if temp_file_path[0].isdigit() and len(temp_file_path[0]) <= 2 and temp_file_path[2].isdigit() is False:  #checking format
                    temp_cell_id = temp_file_path[1]   
                    temp_test_name = temp_file_path[2]
                    temp_test_number = temp_file_path[0]            #updating temp values 
                    temp_other = " ".join(temp_file_path[3:-1])
                    temp_date = temp_file_path[-1]
                    temp_location = file
                    if len(temp_cell_id) == 8:    #checking format
                        fileList.append(file)
                        if "SC" or "Cond" or "OCV" in temp_test_name and len(temp_test_name) <=6:
                            if "SC" in temp_test_name:
                                temp_test_type  = "SC"
                                test = sc_tests(fileTitle, temp_cell_id, temp_test_name, temp_test_type, temp_test_number, temp_date, temp_other, temp_location, temp_excel_sheet)
                                test_files[test.file_path] = test
                            elif "Cond" in temp_test_name:
                                temp_test_type  = "Conditioning"
                                test = cond_tests(fileTitle, temp_cell_id, temp_test_name, temp_test_type, temp_test_number, temp_date, temp_other, temp_location, temp_excel_sheet)
                                test_files[test.file_path] = test
                            elif "OCV" in temp_test_name:
                                temp_test_type  = "OCV"
                                test = OCV_tests(fileTitle, temp_cell_id, temp_test_name, temp_test_type, temp_test_number, temp_date, temp_other, temp_location, temp_excel_sheet)
                                test_files[test.file_path] = test
                       

    return test_files


def fileViewerFunc(test_files, widget):
    x=0
    y= 0

    horizontalHeaders = ["Test Number" , "Test Type/Iteration", "Cell ID", "Test Date", "File Title", "Test", "Other Info"]
    widget.setColumnCount(len(horizontalHeaders))
    widget.setRowCount(len(test_files))
    file_objects = list(test_files.values())
    while x < len(file_objects):
        file = file_objects[x]
        #file_path, cell_id, test_name, test_type, test_number, test_date, other
        widget.setHorizontalHeaderLabels(horizontalHeaders)
        widget.setItem(x,0,QTableWidgetItem(test_files.get(file.file_path).test_number))
        widget.setItem(x,1,QTableWidgetItem(test_files.get(file.file_path).test_name))
        widget.setItem(x,2,QTableWidgetItem((test_files.get(file.file_path)).cell_id))
        widget.setItem(x,3,QTableWidgetItem((test_files.get(file.file_path)).test_date))
        widget.setItem(x,4,QTableWidgetItem(file.file_path))
        widget.setItem(x,5,QTableWidgetItem((test_files.get(file.file_path)).test_type))
        widget.setItem(x,6,QTableWidgetItem(test_files.get(file.file_path).other))
        x+=1


def fileAnalyzer(incoming, name):
        with open(incoming, "r", encoding='latin_1') as workingFile: #opening and reading the incoming file as workingFile
            cleanData = []  #opening and reading the incoming file as workingFile
            for line in workingFile:              #for each line in this file 
                dataInfo = line.strip().split('\t')     #strip this line of unneeded info and split it by tab. Returns a list of each item split
           #  # # # print(dataInfo)
                if len(dataInfo) > 10 and dataInfo[0]=="Time (Sec)":  #if the len of the list is greather than ten
                    cleanData.append(dataInfo)
                elif len(dataInfo) > 10:
                    dataInfo = list(map(float,dataInfo))
                    cleanData.append(dataInfo) 
            if cleanData[0][0] == "Time (Sec)" : 
                    name.excel_sheet = pd.DataFrame(cleanData[1:], columns=cleanData[0])





