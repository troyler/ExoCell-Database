from fileInformer import OCV_tests,sc_tests,cond_tests,fileInfo



def get_XLSX_in_table (self, save_location, summary_list, xlsx_files, widget):
        x= 0
        try:
            longPath = save_location[0][0][:save_location[0][0].rindex("/")+1]
            pathStep = longPath.split("/")
            self.relativePath = save_location[0][0][save_location[0][0].rindex("/")+1:]
        except IndexError:     
            self.selectMsg.setText("Error, must choose files")
            self.selectMsg.exec_()
            return
             
        for each in save_location[0]:
            if ".DS_Store" in each:
                save_location.remove(".DS_Store")
            if each not in xlsx_files:    
                while x < len(save_location[0]):
                    xlsx_file = save_location[0][x]
                    xlsx_files.append(xlsx_file)
                    shortName = xlsx_file[xlsx_file.rindex("/")+1:]
                    summary_list.append(shortName)
                    widget.addItem(shortName)
                    x+=1