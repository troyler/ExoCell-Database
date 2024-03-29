from fileInformer import fileInfo,OCV_tests,sc_tests,cond_tests
from operator import itemgetter,attrgetter
import pandas as pd
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem
fileList = []


def file_chooser(folder, test_files, widget):  
    for file in folder:
        if file != '.DS_Store':
            if "/" in file: 
                fileTitle = file[file.rindex('/')+1:-4] #this is the file title without the path or file extensions
            else:
                fileTitle = file  #for each file in self.fname[0], where the list of file paths is held
            if file not in fileList:   #checking to make sure current file path is not in list to hold filepaths
                try:
                    temp_key_criteria = {
                    "Cell Size": " ", 
                    "Hydrogen Flow" : " ",
                    "Initial Current Density": " ", 
                    "Startup OCV" : " ",
                    "Steady State Current" : " ",
                    "Steady State Current Density" : " ",
                    "Max Power Density" : " "}
                    temp_surface_area = " "
                    temp_location = " "
                    temp_file_path = []
                    temp_cell_id = " "     #setting temp values to update and use for instantiating object for files
                    temp_test_name = " "
                    temp_test_type = " "
                    temp_hydrogen_flow = " "
                    temp_test_number = ""
                    temp_date = ""
                    temp_other = ""
                    temp_excel_sheet = " "
                    temp_file_path = fileTitle.split("_")
                    if temp_file_path[0].isdigit() and len(temp_file_path[0]) <= 2 and temp_file_path[2].isdigit() is False:  #checking format
                        temp_cell_id = temp_file_path[1]   
                        temp_test_name = temp_file_path[2]
                        temp_test_number = temp_file_path[0]            #updating temp values 
                        temp_hydrogen_flow = temp_file_path[4]
                        if "ccm" not in temp_hydrogen_flow:
                            temp_hydrogen_flow = temp_file_path[3]
                        temp_other = " ".join(temp_file_path[3:-1])
                        temp_date = temp_file_path[-1]
                        temp_location = file
                        if len(temp_cell_id) == 8 or len(temp_cell_id) == 10:    #checking format
                            fileList.append(file)
                            if "SC" or "Cond" or "OCV" in temp_test_name and len(temp_test_name) <=6:
                                if "SC" in temp_test_name:
                                    temp_test_type  = "SC"
                                    test = sc_tests(temp_key_criteria,fileTitle, temp_cell_id, temp_test_name, temp_test_type, temp_test_number, temp_date, temp_other, temp_location, temp_hydrogen_flow, temp_surface_area, temp_excel_sheet)
                                    test_files[test.file_path] = test
                                elif "Cond" in temp_test_name:
                                    temp_test_type  = "Conditioning"
                                    test = cond_tests(temp_key_criteria,fileTitle, temp_cell_id, temp_test_name, temp_test_type, temp_test_number, temp_date, temp_other, temp_location, temp_hydrogen_flow, temp_surface_area, temp_excel_sheet)
                                    test_files[test.file_path] = test
                                elif "OCV" in temp_test_name:
                                    temp_test_type  = "OCV"
                                    test = OCV_tests(temp_key_criteria, fileTitle, temp_cell_id, temp_test_name, temp_test_type, temp_test_number, temp_date, temp_other, temp_location, temp_hydrogen_flow, temp_surface_area, temp_excel_sheet)
                                    test_files[test.file_path] = test
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


def fileAnalyzer(incoming, name, test_files, keyCriteria, cell_criteria): #feeder to be used as a select method potentially 
    with open(incoming, "r", encoding='latin_1') as workingFile: #opening and reading the incoming file as workingFile
        cleanData = []  #opening and reading the incoming file as workingFile
        for line in workingFile:              #for each line in this file 
            area = " "
            dataInfo = line.strip().split('\t')
            if "Time:" in dataInfo[0] and ("Date" not in dataInfo[0]) and ("Slope" not in dataInfo[0]):
                dates = [] 
                time = dataInfo[0]
                dateString = time.split(":", maxsplit = 1)
                for x in dateString:
                    dates.append(x.strip()) #strip this line of unneeded info and split it by tab. Returns a list of each item split
            if "SurfaceArea:" in dataInfo[0]:
                area = (dataInfo[0].split(":", maxsplit = 1))[1]
                name.surface_area = area.strip() + " cm²"
                print(name.surface_area)
            if len(dataInfo) > 10 and dataInfo[0]=="Time (Sec)":  #if the len of the list is greather than ten
                cleanData.append(dataInfo)
            elif len(dataInfo) > 10:
                dataInfo = list(map(float,dataInfo))
                cleanData.append(dataInfo) 
        if cleanData[0][0] == "Time (Sec)" : 
            name.excel_sheet = pd.DataFrame(cleanData[1:], columns=cleanData[0])
            name.testing_time = pd.DataFrame([dates[1]], columns = [dates[0]])
            cell_criteria["Surface Area"].append(name.surface_area)
            


             #    "Initial Current Density": [], 
             #    "Startup OCV" : [],
             #     "Steady State Current" : [],
             #     "Steady State Current Density" : [],
             #      "Max Power Density" : []}
            keyCriteria["Cell Name"] = name.cell_id
            name.get_current_density()
            cell_criteria["Initial Current Density"].append(name.current_density)
            name.get_max_power_density()
            cell_criteria["Max Power Density"].append(name.max_power_density)
            name.get_OCV()
            cell_criteria["Voltage at Max Power Density"].append(name.voltage_at_max_power_density)
            cell_criteria["Time at Max Power Density"].append(name.time_at_max_power_density)
            cell_criteria["Startup OCV"].append(name.startup_ocv)
            cell_criteria["Hydrogen Flow"].append(name.hydrogen_flow)
            name.get_ss_current_density()
            cell_criteria["Steady State Current Density"].append(name.ss_current_density)
            name.get_ss_current()
            cell_criteria["Steady State Current"].append(name.ss_current)
            keyCriteria["Hydrogen Flow"] = name.hydrogen_flow
            if "ccm" in name.hydrogen_flow:
                keyCriteria["Hydrogen Flow"] = str(name.hydrogen_flow.split(" ")[0] + " (mL/min)")
                keyCriteria["Date Tested"] = name.test_date
        if "Cond2" in name.test_name:
            keyCriteria["Initial Current Density"] = str(name.current_density) + " (mA/cmÂ²) on file " + name.test_name 
            keyCriteria["Startup OCV"] = name.test_name + " " + str(name.startup_ocv) + " (V)"
            keyCriteria["Max Power Density"] = "(mW/cmÂ²)"
        if "SC" in name.test_name:   #feeder used to change option 
            name.get_OCV()
            name.get_max_power_density()
            temp_test_number = int(name.test_number) - 1
            if name.test_name == "SC1":
                keyCriteria["Startup OCV"] = str(name.startup_ocv) + " (V) on file " + str(name.test_name) 
                get_steadyState_current(test_files, temp_test_number, keyCriteria)
                keyCriteria["Max Power Density"] = name.test_name + " " + str(name.max_power_density) + " (mW/cmÂ²)"



def get_steadyState_current(test_files, temp_test_number, keyCriteria):
    counter = 0
    file_objects = list(test_files.values())  
    while counter < len(file_objects):
        file = file_objects[counter]
        if int(test_files.get(file.file_path).test_number) == temp_test_number:
            fileHolder = test_files.get(file.file_path)
            fileHolder.get_ss_current_density()
            fileHolder.get_ss_current()
            keyCriteria["Steady State Current"] = f"{fileHolder.ss_current}(A) on file {fileHolder.test_name}"
            keyCriteria["Steady State Current Density"] = f"{fileHolder.ss_current_density}(mA/cmÂ²) on file {fileHolder.test_name}"
            break
        else:
            counter+=1

        
    


        
