
class fileInfo:
    def __init__(self, file_path, cell_id, test_name, test_number, test_date, other):
        self.file_path = file_path #absolute path
        self.cell_id = cell_id # e.g. MM221005
        self.test_name = test_name #test name (e.g. Cond2)
        self.test_number = test_number #e.g. 7
        self.test_date = test_date #date tested 
        self.other = other

    def __str__(self):
        return self.file_path + "\n" + self.cell_id + " " + self.test_name + " " + self.test_number + " " + self.test_date + " " + self.other 



class OCV_tests(fileInfo):
    def __init__(self,file_path, cell_id, test_name, test_type, test_number, test_date, other):
        self.test_type = test_type # Conditioning, SC, OCV
        fileInfo.__init__(self, file_path, cell_id, test_name, test_number, test_date, other)

    def __str__(self):
        return super().__str__() + " " + self.test_type


class sc_tests(fileInfo):
    def __init__(self,file_path, cell_id, test_name, test_type, test_number, date, other):
        self.test_type = test_type # Conditioning, SC, OCV
        fileInfo.__init__(self, file_path, cell_id, test_name, test_number, date, other)

    def __str__(self):
        return super().__str__() + " " + self.test_type
       
class cond_tests(fileInfo):
    def __init__(self,file_path, cell_id, test_name, test_type, test_number, date, other):
        self.test_type = test_type # Conditioning, SC, OCV
        fileInfo.__init__(self, file_path, cell_id, test_name, test_number, date, other)

    def __str__(self):
        return super().__str__() + " " + self.test_type
        




    