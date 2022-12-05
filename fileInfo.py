
class fileInfo():
    def __init__(self, file_path, test_name, file_type, test_number, date, other):
        self.file_path = file_path #absolute path
        self.test_name = test_name #test name (e.g. Cond2)
        self.file_type = file_type # 
        self.test_number = test_number
        self.date = date #date tested 
        self.other = other





class testInfo(fileInfo):
    def __init__(self, file_path, test_name, file_type, test_number, date, other):
        fileInfo.__init__(self, file_path, test_name, file_type, test_number, date, other)