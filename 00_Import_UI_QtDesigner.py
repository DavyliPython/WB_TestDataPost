from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidget, QTreeWidgetItem, QWizard, QWizardPage, QSpinBox, QLabel,QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QMenu, Qt, QAction, QCursor, QApplication, QRect, QCoreApplication

import sys
import os
# from PyQt5.Qt import *


import import_ui as import_UI
import numpy as np
import pyqtgraph

class DataImportWizard(QWizard):
    def __init__(self, parent = None):
        super(DataImportWizard, self).__init__(parent)

        self.addPage(Page1())
        self.addPage(Page2())

        self.resize(938, 660)
        self.setWindowModality(Qt.WindowModal)
        self.setWizardStyle(QWizard.ModernStyle)

        self.show()

class Page1(QWizardPage):
    def __init__(self):
        super(Page1,self).__init__()
        self.setTitle("Class Information")
        self.setSubTitle("Specify basic information about the class for "
                         "which you want to generate skeleton source code files.")

        self.spinBox = QSpinBox(self)
        self.spinBox.setGeometry(QRect(350, 190, 241, 40))
        self.spinBox.setMaximum(20000)
        self.spinBox.setProperty("value", 200)
        self.spinBox.setObjectName("spinBox")
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(70, 190, 281, 40))
        self.label_2.setObjectName("label_2")
        self.widget = QWidget(self)
        self.widget.setGeometry(QRect(50, 80, 851, 86))
        self.widget.setObjectName("widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Wizard", "Data Import"))
        self.label_2.setText(_translate("Wizard", "Lines to preview:"))
        self.label.setText(_translate("Wizard", "Please select test data File:"))
        self.pushButton.setText(_translate("Wizard", "Browe..."))
        # self.label_3.setText(_translate("Wizard", "Test Data:"))
        # self.groupBox.setTitle(_translate("Wizard", "Time Select:"))
        # self.label_5.setText(_translate("Wizard", "End Time:"))
        # self.label_7.setText(_translate("Wizard", "Start Time:"))
        # self.groupBox_2.setTitle(_translate("Wizard", "Rate Change"))
        # self.label_4.setText(_translate("Wizard", "Rate in File:"))
        # self.label_6.setText(_translate("Wizard", "Change To:"))
        # self.comboBox.setItemText(0, _translate("Wizard", "1/2 Rate"))
        # self.comboBox.setItemText(1, _translate("Wizard", "1/4 Rate"))
        # self.comboBox.setItemText(2, _translate("Wizard", "1/8 Rate"))
        # self.comboBox.setItemText(3, _translate("Wizard", "1/16 Rate"))
        # self.comboBox.setItemText(4, _translate("Wizard", "1/32 Rate"))



class Page2(QWizardPage):
    def __init__(self):
        super(Page2,self).__init__()

    # def OpenFile(self):
    #     fname = QFileDialog.getOpenFileName(self, 'Open file',
    #                                         'D:/backup/00_Learn/01_Work/01_Code/05_TestDataPost/archive/')
    #     if fname[0]:
    #         print(fname)
    #         self.shortfname = os.path.basename(fname[0])
    #         self.lineEdit.setText(fname[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MW = DataImportWizard()
    sys.exit(app.exec_())
    print("DONE")
