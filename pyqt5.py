import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TFFC Data Automation") #adding a title
        self.setLayout(qtw.QVBoxLayout()) #setting vertical

        my_label = qtw.QLabel("Data Automation")  #creating label
        my_label.setFont(qtg.QFont('Helvetica', 18))  #sizing
        self.layout().addWidget(my_label) #adding label widget to layout

        my_entry = qtw.QLineEdit()  #creating entry box
        my_entry.setObjectName("name_field")
        my_entry.setText(" ")
        self.layout().addWidget(my_entry)

        #creating button
        my_button = qtw.QPushButton('Press Me!', clicked = lambda: press_it())
        self.layout().addWidget(my_button)

        def press_it():
            my_label.setPicture(f'Hello {my_entry.text()}')
            my_entry.setText(" ")

        self.show()


app = qtw.QApplication([])
mw = MainWindow()

app.exec_()