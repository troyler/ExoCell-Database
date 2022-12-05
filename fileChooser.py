from fileInformer import fileInfo,OCV_tests,sc_tests,cond_tests
from operator import itemgetter
import os

fileList = []
currentDirectoryList = []
test_files = {}

def file_chooser(folder):   
    for file in folder:
        if file != '.DS_Store':
            if "/" in file: 
                fileTitle = file[file.rindex('/')+1:-4]  
            else:
                fileTitle = file #for each file in self.fname[0], where the list of file paths is held
            if file not in fileList:   #checking to make sure current file path is not in list to hold filepaths
                # self.use_regex(self.fileTitle)
                temp_file_path = []
                temp_cell_id = " "
                temp_test_name = " "
                temp_test_type = " "
                temp_test_number = ""
                temp_date = ""
                temp_other = ""
                temp_file_path = fileTitle.split("_")
                if temp_file_path[0].isdigit() and len(temp_file_path[0]) <= 2 and temp_file_path[2].isdigit() is False:
                    temp_cell_id = temp_file_path[1]
                    temp_test_name = temp_file_path[2]
                    temp_test_number = temp_file_path[0]
                    temp_other = "".join(temp_file_path[3:-1])
                    temp_date = temp_file_path[-1]
                    if len(temp_cell_id) == 8:
                        fileList.append(file)
                        currentDirectoryList.append((file, temp_test_number, temp_file_path))
                        if "SC" or "Cond" or "OCV" in temp_test_name and len(temp_test_name) <=6:
                            if "SC" in temp_test_name:
                                temp_test_type  = "SC"
                                test = sc_tests(fileTitle, temp_cell_id, temp_test_name, temp_test_type, temp_test_number, temp_date, temp_other)
                                test_files[test.file_path] = test
                            elif "Cond" in temp_test_name:
                                temp_test_type  = "Conditioning"
                                test = cond_tests(fileTitle, temp_cell_id, temp_test_name, temp_test_type, temp_test_number, temp_date, temp_other)
                                test_files[test.file_path] = test
                            elif "OCV" in temp_test_name:
                                temp_test_type  = "OCV"
                                test = OCV_tests(fileTitle, temp_cell_id, temp_test_name, temp_test_type, temp_test_number, temp_date, temp_other)
                                test_files[test.file_path] = test
                            
                            #self.fileListWidget.addItem(fileTitle)
                            #print(namingConv)
                            currentDirectoryList.sort(key=itemgetter(1))

                                #print(currentDirectoryList)
                                # self.fileViewerFunc()

    return test_files

