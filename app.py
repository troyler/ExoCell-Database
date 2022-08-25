import sys
from PyQt5.QtWidgets import (
QWidget, QGridLayout,QPushButton, QApplication, QFileDialog, QLabel)

class basicWindow(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        self.button = QPushButton("Open Files")
        self.button.clicked.connect(self.OpenFiles())
        label = QLabel("Files:")
        grid_layout.addWidget(self.button, 0, 0)
        grid_layout.addWidget(label, 0,1)

       
        self.setWindowTitle('Basic Grid Layout')

    def OpenFiles(self):
        fname = QFileDialog.getOpenFileNames(self, "Open files", "", "*.fcd")
        print(fname)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = basicWindow()
    windowExample.show()
    sys.exit(app.exec_())