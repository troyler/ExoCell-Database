from secrets import choice
from PyQt5.QtWidgets import (QApplication,
 QWidget, 
 QMainWindow,
  QPushButton,
   QFileDialog, 
   QLabel,QVBoxLayout,
   QListWidget)
from PyQt5.QtCore import QSize, Qt
import sys #only need to access commaned line arguments

#subclass QMainWindow to customize your application's main window
class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        

        self.n_times_clicked = 0
        self.label = QLabel("Filessss")
        self.label

        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.button.move(10,20)
        self.button.clicked.connect(self.the_button_was_clicked)




        self.windowTitleChanged.connect(self.the_window_title_changed)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):  #open file dialog
       fname = QFileDialog.getOpenFileName(self, "Open file", "", "FCD Files (*.fcd)")
       


    def the_window_title_changed(self, window_title):
        print("Window title changed: %s" % window_title)

        if window_title == "Something went wrong" :
            self.button.setDisabled(True)

app = QApplication([])

window = ListBoxWidget #create a Qt widget, which will be our window
window.show() #windows are hidden by default

app.exec_() #start the event loop
