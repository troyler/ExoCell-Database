def fileViewerFunc(test_files, widget):
    x=0
    y= 0
   # test_files_sorted = sorted(test_files.values(), key= attrgetter('test_number'))
   # print(test_files_sorted)

    horizontalHeaders = ["Test Number" , "Test Type/Iteration", "Cell ID", "Test Date", "File Title", "Test", "Other Info"]
    widget.setColumnCount(len(horizontalHeaders))
    widget.setRowCount(len(test_files))
    file_objects = list(test_files.values())
    while x < len(file_objects):
        file = file_objects[x]
        #file_path, cell_id, test_name, test_type, test_number, test_date, other
        widget.setHorizontalHeaderLabels(horizontalHeaders)
        widget.setItem(x,0,QTableWidgetItem((test_files.get(file.file_path).test_number)))
        widget.setItem(x,1,QTableWidgetItem(test_files.get(file.file_path).test_name))
        widget.setItem(x,2,QTableWidgetItem((test_files.get(file.file_path)).cell_id))
        widget.setItem(x,3,QTableWidgetItem((test_files.get(file.file_path)).test_date))
        widget.setItem(x,4,QTableWidgetItem(file.file_path))
        widget.setItem(x,5,QTableWidgetItem((test_files.get(file.file_path)).test_type))
        widget.setItem(x,6,QTableWidgetItem(test_files.get(file.file_path).other))
        x+=1