
class fileClass:   #this class should only be used for instantiating new files and for GUI component displays
    def __init__(self, file_title, file_path):

        #file_path = file path of file brought in
        self.file_title = file_title
        self.file_path = file_path
         #title of file with file path removed and file extension removed 
        #Example: 1_MR230210_Cond1_0.6V_20 ccm H2 wet_flat blocks_CF 4 ply BD_num 2 threaded aluminum_02-13-2023
        file_details = self.file_title.split("_")
        self.excel_sheet = None


        self.test_data_from_fileName = {
                "Test Number": f"{file_details[0]}", 
                "Cell ID": f"{file_details[1]}", 
                "Test Type/Iterations" : f"{file_details[2]}",
                "Test Voltage" : f"{file_details[3]}",
                "Hydrogen Flow" : f"{file_details[4]}",
                "Other Test Data" : f'{"".join(file_details[5:-1])}',
                "Test Date" : f"{file_details[-1]}"
        }

        self.cell_criteria = {
                "Test Time" : " ",
                "Surface Area": 0, 
                "Hydrogen Flow" : " ",
                "Initial Current Density": " ", 
                "Startup OCV" : " ",
                "Steady State Current" : " ",
                "Steady State Current Density" : " ",
                "Max Power Density" : " ",
                "Voltage at Max Power Density" : " ",
                "Time at Max Power Density" : " "}


        #file_path= file path of the file currently being accessed 
          # Example filePath -->
        ''' /Users/tyler/Desktop/Data Processing/MR230210 Summary/MR230210 - 
        2x1 Array in Carbon Fiber 4 Ply/1_MR230210_Cond1_0.6V_20 ccm H2 wet_flat blocks_CF 4 ply BD_num 2 threaded aluminum_02-13-2023.fcd'''

       

    def __str__(self):
        data_string = ""

        for key,values in self.test_data_from_fileName.items():
                data_string += f"{key} : {values} | "

        return self.file_title + "\n" + self.file_path + " " + data_string
    
    def get_hydrogen_flow(self):
        self.cell_criteria["Hydrogen Flow"] = self.excel_sheet.loc[:,"Flow_Anode (cc/min)"]
        print("Hydorgen Flow",  self.cell_criteria["Hydrogen Flow"], "ccm")

    def get_OCV(self):
        self.cell_criteria["Startup OCV"] = self.excel_sheet.loc[0,"E_Stack (V)"]
        print("Startup OCV" , self.cell_criteria["Startup OCV"], "(V)")
    
    def get_current_density(self):
        if len(self.excel_sheet) <= 360:
            current_density_column = self.excel_sheet.loc[len(self.excel_sheet)-1,"I (mA/cmÂ²)"]
        else:
            current_density_column = self.excel_sheet.loc[360,"I (mA/cmÂ²)"]
        self.cell_criteria["Initial Current Density"] = current_density_column
        print("Initial Current Density" , self.cell_criteria["Initial Current Density"],  "(mA/cmÂ²)")

    def get_ss_current_density(self):
        self.cell_criteria["Steady State Current Density"] = self.excel_sheet.loc[len(self.excel_sheet)-1,"I (mA/cmÂ²)"]
        print("Steady State Current Density", self.cell_criteria["Steady State Current Density"], "(mA/cmÂ²)" )

    def get_ss_current(self):
        self.cell_criteria["Steady State Current"] = self.excel_sheet.loc[len(self.excel_sheet)-1,"I (A)"]
        print("Steady State Current ", self.cell_criteria["Steady State Current"], " (A)")

    def get_max_power_density(self):
        max_power_density = max(self.excel_sheet.loc[:,"Power (mW/cmÂ²)"])
        self.cell_criteria["Max Power Density"] = max_power_density
        max_index = self.excel_sheet["Power (mW/cmÂ²)"].idxmax()
        voltage_at_max_power_density = self.excel_sheet.loc[max_index,"E_Stack (V)"]
        self.cell_criteria["Voltage at Max Power Density"] = voltage_at_max_power_density
        time_at_max_power_density = self.excel_sheet.loc[max_index,"Time (Sec)"]
        self.cell_criteria["Time at Max Power Density"] = time_at_max_power_density
        print("Max power density", self.cell_criteria["Max Power Density"], "(mW/cmÂ²)")    

    def is_cond(self):
        return False

    def is_OCV(self):
        return False

    def is_SC(self):
        return False


class OCV_tests(fileClass):
    def __init__(self, file_title, file_path, test_type = "OCV"):
       super().__init__(file_title, file_path)
       self.test_type = test_type # Conditioning, SC, OCV

    def __str__(self):
        return super().__str__() + " " + self.test_type

    def is_OCV(self):
        return True
        

class sc_tests(fileClass):
    def __init__(self, file_title, file_path, test_type = "Scan Current"):
        super().__init__(file_title, file_path)
        self.test_type = test_type# Conditioning, SC, OCV

    def __str__(self):
        return super().__str__() + " " + self.test_type

    def is_SC(self):
        return True
       
class cond_tests(fileClass):
    def __init__(self, file_title, file_path, test_type = "Conditioning"):
        super().__init__(file_title, file_path)
        self.test_type = test_type # Conditioning, SC, OCV

    def __str__(self):
        return super().__str__() + " " + self.test_type

    def is_cond(self):
        return True


    




    