
class fileInfo:
    def __init__(self, keyCriteria, file_path, cell_id, test_name, test_number, test_date, other, location, hydrogen_flow, surface_area):
        keyCriteria = {
                "Cell Size": " ", 
                 "Initial Current Density": " ", 
                 "Startup OCV" : " ",
                  "Steady State Current" : " ",
                  "Steady State Current Density" : " ",
                   "Max Power Density" : " "}
        self.keyCriteria = keyCriteria
        self.location = location
        self.surface_area = surface_area
        self.file_path = file_path #absolute path
        self.cell_id = cell_id # e.g. MM221005
        self.test_name = test_name #test name (e.g. Cond2)
        self.test_number = test_number #e.g. 7
        self.test_date = test_date #date tested 
        self.other = other
        self.hydrogen_flow = hydrogen_flow

    def __str__(self):
        return self.file_path + "\n" + self.cell_id + " " + self.test_name + " " + self.test_number + " " + self.test_date + " " + self.other + " " + self.location

    
    def get_hydrogen_flow(self):
        anode_column = self.excel_sheet.loc[:,"Flow_Anode (cc/min)"]
        self.hydrogen_flow = anode_column
        print(anode_column, self.test_name)

    def get_OCV(self):
        self.startup_ocv = self.excel_sheet.loc[0,"E_Stack (V)"]
        print(self.test_name , "Startup OCV" , self.startup_ocv, "(V)")
    
    def get_current_density(self):
        if len(self.excel_sheet) <= 360:
            current_density_column = self.excel_sheet.loc[len(self.excel_sheet)-1,"I (mA/cmÂ²)"]
        else:
            current_density_column = self.excel_sheet.loc[360,"I (mA/cmÂ²)"]
        self.current_density = current_density_column
        print("Initial Current Density" , self.test_name , self.current_density, "(mA/cmÂ²)")

    def get_ss_current_density(self):
        self.ss_current_density = self.excel_sheet.loc[len(self.excel_sheet)-1,"I (mA/cmÂ²)"]
        print("Steady State Current Density" ,self.test_name, self.ss_current_density, "(mA/cmÂ²)" )

    def get_ss_current(self):
        self.ss_current = self.excel_sheet.loc[len(self.excel_sheet)-1,"I (A)"]
        print("Steady State Current " ,self.test_name, self.ss_current, "(A)")

    def get_max_power_density(self):
        self.max_power_density = max(self.excel_sheet.loc[:,"Power (mW/cmÂ²)"])
        max_index = self.excel_sheet["Power (mW/cmÂ²)"].idxmax()
        self.voltage_at_max_power_density = self.excel_sheet.loc[max_index,"E_Stack (V)"]
        self.time_at_max_power_density = self.excel_sheet.loc[max_index,"Time (Sec)"]
        print(max_index)
        print("Max power density", self.test_name,  self.max_power_density, "(mW/cmÂ²)")    

    def is_cond(self):
        return False

    def is_OCV(self):
        return False

    def is_SC(self):
        return False


class OCV_tests(fileInfo):
    def __init__(self, keyCriteria, file_path, cell_id, test_name, test_type, test_number, test_date, other, location, hydrogen_flow, surface_area, excel_sheet):
        self.test_type = test_type # Conditioning, SC, OCV
        self.excel_sheet = excel_sheet
        fileInfo.__init__(self, keyCriteria, file_path, cell_id, test_name, test_number, test_date, other, location, hydrogen_flow, surface_area)

    def __str__(self):
        return super().__str__() + " " + self.test_type

    def is_OCV(self):
        return True
        

class sc_tests(fileInfo):
    def __init__(self, keyCriteria, file_path, cell_id, test_name, test_type, test_number, test_date, other, location, hydrogen_flow, surface_area, excel_sheet):
        self.test_type = test_type # Conditioning, SC, OCV
        self.excel_sheet = excel_sheet
        fileInfo.__init__(self, keyCriteria, file_path, cell_id, test_name, test_number, test_date, other, location, hydrogen_flow, surface_area)

    def __str__(self):
        return super().__str__() + " " + self.test_type

    def is_SC(self):
        return True
       
class cond_tests(fileInfo):
    def __init__(self, keyCriteria, file_path, cell_id, test_name, test_type, test_number, test_date, other, location, hydrogen_flow, surface_area, excel_sheet):
        self.test_type = test_type # Conditioning, SC, OCV
        self.excel_sheet = excel_sheet
        fileInfo.__init__(self, keyCriteria, file_path, cell_id, test_name, test_number, test_date, other, location, hydrogen_flow, surface_area)

    def __str__(self):
        return super().__str__() + " " + self.test_type

    def is_cond(self):
        return True


    




    