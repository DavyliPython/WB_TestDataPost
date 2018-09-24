from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidget, QTreeWidgetItem, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QMenu, Qt, QAction, QCursor, QApplication
from PyQt5 import QtWidgets

import sys
import os


class ImportWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(ImportWizard, self).__init__(parent)
        self.addPage(Page1(self))
        #self.addPage(Page2(self))
        self.setWindowTitle("PyQt5 Wizard Example - pythonspot.com")
        self.resize(640, 480)

class Page1(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Python", "/path/to/filename1")
        self.comboBox.addItem("PyQt5", "/path/to/filename2")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.comboBox)
        self.setLayout(layout)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    MW = ImportWizard()
    MW.show()
    sys.exit(app.exec_())
    print("DONE")