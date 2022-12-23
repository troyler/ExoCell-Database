
class fileInfo:
    def __init__(self, file_path, cell_id, test_name, test_number, test_date, other, location):
        self.location = location
        self.file_path = file_path #absolute path
        self.cell_id = cell_id # e.g. MM221005
        self.test_name = test_name #test name (e.g. Cond2)
        self.test_number = test_number #e.g. 7
        self.test_date = test_date #date tested 
        self.other = other

    def __str__(self):
        return self.file_path + "\n" + self.cell_id + " " + self.test_name + " " + self.test_number + " " + self.test_date + " " + self.other + " " + self.location


class OCV_tests(fileInfo):
    def __init__(self,file_path, cell_id, test_name, test_type, test_number, test_date, other, location, excel_sheet):
        self.test_type = test_type # Conditioning, SC, OCV
        self.excel_sheet = excel_sheet
        fileInfo.__init__(self, file_path, cell_id, test_name, test_number, test_date, other, location)
    
    def get_hydrogen_flow(self):
        anode_column = self.excel_sheet.loc[:,"Flow_Anode (cc/min)"]
        print(anode_column)

    def __str__(self):
        return super().__str__() + " " + self.test_type

    def is_OCV(self):
        return True
        

class sc_tests(fileInfo):
    def __init__(self,file_path, cell_id, test_name, test_type, test_number, test_date, other, location, excel_sheet):
        self.test_type = test_type # Conditioning, SC, OCV
        self.excel_sheet = excel_sheet
        fileInfo.__init__(self, file_path, cell_id, test_name, test_number, test_date, other, location)

    def get_hydrogen_flow(self):
        anode_column = self.excel_sheet.loc[:1,"Flow_Anode (cc/min)"]
        print(anode_column)

    def get_OCV(self):
        self.startup_ocv = self.excel_sheet.loc[0,"E_Stack (V)"]
        print(self.test_name , "Startup OCV" , self.startup_ocv, "(V)")

    def get_max_power_density(self):
        self.max_power_density = max(self.excel_sheet.loc[:,"Power (mW/cmÂ²)"])
        print("Max power density", self.test_name,  self.max_power_density, "(mW/cmÂ²)")


    def __str__(self):
        return super().__str__() + " " + self.test_type

    def is_SC(self):
        return True
    
    def is_cond(self):
        return False
       
class cond_tests(fileInfo):
    def __init__(self,file_path, cell_id, test_name, test_type, test_number, test_date, other, location, excel_sheet):
        self.test_type = test_type # Conditioning, SC, OCV
        self.excel_sheet = excel_sheet
        fileInfo.__init__(self, file_path, cell_id, test_name, test_number, test_date, other, location)

    def get_hydrogen_flow(self):
        anode_column = self.excel_sheet.loc[:,"Flow_Anode (cc/min)"]
        print(anode_column, self.test_name)
    
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

    def __str__(self):
        return super().__str__() + " " + self.test_type

    def is_cond(self):
        return True

    




    