from ui.main import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel


class mainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)

        self.pushButton_1.clicked.connect(self.push1)
        self.pushButton_2.clicked.connect(self.push2)
        self.pushButton_3.clicked.connect(self.push3)
        self.pushButton_4.clicked.connect(self.push4)
        self.pushButton_5.clicked.connect(self.push5)
        self.pushButton_6.clicked.connect(self.push6)
        self.pushButton_7.clicked.connect(self.push7)
        self.pushButton_8.clicked.connect(self.push8)
        self.pushButton_9.clicked.connect(self.push9)
        self.pushButton_0.clicked.connect(self.push0)
        self.back.clicked.connect(self.delete)
        self.ok.clicked.connect(self.next)

        self.id = ""
        self.history_list = []
        
    def push1(self):
        self.id += "1"
        self.textEdit.setText(self.id)

    def push2(self):
        self.id += "2"
        self.textEdit.setText(self.id)

    def push3(self):
        self.id += "3"
        self.textEdit.setText(self.id)

    def push4(self):
        self.id += "4"
        self.textEdit.setText(self.id)

    def push5(self):
        self.id += "5"
        self.textEdit.setText(self.id)
    
    def push6(self):
        self.id += "6"
        self.textEdit.setText(self.id)

    def push7(self):
        self.id += "7"
        self.textEdit.setText(self.id)

    def push8(self):
        self.id += "8"
        self.textEdit.setText(self.id)

    def push9(self):
        self.id += "9"
        self.textEdit.setText(self.id)

    def push0(self):
        self.id += "0"
        self.textEdit.setText(self.id)

    def delete(self):
        self.id = self.id[:-1]
        self.textEdit.setText(self.id)

    def next(self):
        if len(self.id) != 12 or self.id[0] != "5":
            QMessageBox.critical(self, "Notice", "Invalid ID")
        else:
            if self.id in self.history_list:
                self.id = ""
                self.textEdit.setText("")
                QMessageBox.critical(self, "Notice", "Already Registered")
            else:
                QMessageBox.information(self, "Notice", "Give out Mask for ID : "+self.id)
                self.history_list.append(self.id)
                self.id = ""
                self.textEdit.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = mainWindow()
    myWindow.show()
    sys.exit(app.exec_())