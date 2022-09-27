import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QAction
import random


class Widget2(QWidget):
    def __init__(self):
        super().__init__()
        w2btn = QPushButton('Another Widget ' +
                            str(random.randrange(5, 100, 5)), self)
        w2btn.clicked.connect(self.w2btnclicked)
        w2btn.resize(w2btn.sizeHint())
        w2btn.move(50, 50)
        
    def w2btnclicked(self):
        print("Widget 2 btn clicked")
class Widget1(QWidget):

    def __init__(self):
        super().__init__()
        self.start = 50
        self.end = 50
        quit = QAction("Quit", self)
        quit.triggered.connect(self.close)
                
        addbtn = QPushButton('Add Window', self)
        addbtn.clicked.connect(self.addbtnclicked)
        addbtn.resize(addbtn.sizeHint())
        addbtn.move(50, 50)

        quitbtn = QPushButton('Quit', self)
        quitbtn.clicked.connect(QApplication.instance().quit)
        quitbtn.resize(quitbtn.sizeHint())
        quitbtn.move(50, 100)        
        self.popups = []
        
    def addbtnclicked(self):        
        print("Add Button Clicked!!")
        wdgt2 = Widget2()
        wdgt2.show()
        
        if self.start > 1600:
            self.start = 50
            self.end = self.end + 250
        wdgt2.setGeometry(self.start, self.end, 200, 200)
        self.popups.append(wdgt2)
        self.start = self.start + 250
    
    def closeEvent(self, event):
        print("In Close Event")
        QApplication.closeAllWindows()

def main():
    app = QApplication(sys.argv)
    ex = Widget1()
    ex.show()
    ex.setGeometry(800, 600, 200, 200)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()