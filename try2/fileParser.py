from operator import itemgetter,attrgetter
import pandas as pd
import os
from fileClass import fileClass, sc_tests, OCV_tests,cond_tests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem
fileList = []
test_files = {}

#this module enables the creation of fileClass objects for viewing on the front end 
#the module then creates subclasses of this class, used for the creation of the xlsx files and updating to the database 



def file_chooser(folder, path, widget):  #### this function will be used to parse incoming files, creating objects for the frontend using                                     ### the base class of fileClass and then creating subclasses for processing data
    for file in folder:
        if file != '.DS_Store':
            if "/" in file: 
                fileTitle = file[file.rindex('/')+1:-4] #this is the file title without the path or file extensions
            else:
                fileTitle = file[:(len(file)-4)]  #for each file in self.fname[0], where the list of file paths is held
            if file not in fileList:   #checking to make sure current file path is not in list to hold filepaths
                try:
                    file = path + file
                    new_file = fileClass(fileTitle, file)
                    print(new_file)
                    accessor = new_file.test_data_from_fileName
                    test_type = accessor["Test Type/Iterations"]
                    if accessor["Test Number"].isdigit() and len(accessor["Test Number"]) <=2 and not test_type.isdigit():
                        if len(accessor["Cell ID"]) == 8 or len(accessor["Cell ID"]) == 10:    #checking format
                            fileList.append(file)
                            if "SC" or "Cond" or "OCV" in test_type and len(test_type) <=6:
                                if "SC" in test_type:
                                    test = sc_tests(fileTitle, file)
                                    test_files[test.file_title] = test
                                elif "Cond" in test_type:
                                    test = cond_tests(fileTitle, file)
                                    test_files[test.file_title] = test
                                elif "OCV" in test_type:
                                    test = OCV_tests(fileTitle,  file)
                                    test_files[test.file_title] = test
                            else:
                                widget.setText(f"{fileTitle} was not an OCV, SC, or Cond file")
                                widget.exec_()  
                        else:
                            widget.setText(f"{fileTitle} had improper naming convention and was removed")
                            widget.exec_() 
                except IndexError:     
                    widget.setText(f"{fileTitle} had improper naming convention and was removed")
                    widget.exec_() 
                    continue
            else: 
               widget.setText(f"{fileTitle} already selected")
               widget.exec_()
               continue 
               # return                       

    return test_files


def fileAnalyzer(): #feeder to be used as a select method potentially 
    for file_object in test_files.values():   
        with open(file_object.file_path, "r", encoding='latin_1') as working_file: #opening and reading the incoming file as working_file
            cleaned_data = []  #opening and reading the incoming file as working_file
            for line in working_file:              #for each line in this file 
                area = " "
                dataInfo = line.strip().split('\t')
                if "Time:" in dataInfo[0] and ("Date" not in dataInfo[0]) and ("Slope" not in dataInfo[0]):
                    dates = [] 
                    time = dataInfo[0]
                    dateString = time.split(":", maxsplit = 1)
                    for x in dateString:
                        dates.append(x.strip())#strip this line of unneeded info and split it by tab. Returns a list of each item split
                    file_object.cell_criteria["Test Time"] = dates[1]
                if "SurfaceArea:" in dataInfo[0]:
                    area = (dataInfo[0].split(":", maxsplit = 1))[1]
                    file_object.cell_criteria["Surface Area"] = area.strip() + " cm²"
                    print(file_object.cell_criteria["Surface Area"])
                if len(dataInfo) > 10 and dataInfo[0]=="Time (Sec)":  #if the len of the list is greather than ten
                    cleaned_data.append(dataInfo)
                elif len(dataInfo) > 10:
                    dataInfo = list(map(float,dataInfo))
                    cleaned_data.append(dataInfo) 
            if cleaned_data[0][0] == "Time (Sec)" : 
                file_object.excel_sheet = pd.DataFrame(cleaned_data[1:], columns=cleaned_data[0])
                file_object.testing_time = pd.DataFrame([dates[1]], columns = [dates[0]])  #will be able to remove
                file_object.get_current_density()
                file_object.get_max_power_density()
                file_object.get_OCV()
                file_object.get_ss_current_density()
                file_object.get_ss_current()
                print("\n\n")
            
        


            