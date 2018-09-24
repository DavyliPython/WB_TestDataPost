from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidget, QTreeWidgetItem, QWizard
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QMenu, Qt, QAction, QCursor, QApplication

import sys
import os
# from PyQt5.Qt import *


import import_ui as import_UI
import numpy as np
import pyqtgraph

class DataImportWizard(QWizard, import_UI.Ui_Wizard):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Add connect with OpenFile
        self.pushButton.clicked.connect(self.OpenFile)
        self.wizardPage1
        # Show()
        self.show()


    def OpenFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'D:/backup/00_Learn/01_Work/01_Code/05_TestDataPost/archive/')
        if fname[0]:
            print(fname)
            self.shortfname = os.path.basename(fname[0])
            self.lineEdit.setText(fname[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MW = DataImportWizard()
    sys.exit(app.exec_())
    print("DONE")
