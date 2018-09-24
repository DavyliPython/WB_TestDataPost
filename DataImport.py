
from PyQt4.QtGui import *
from PyQt4.QtCore import *


import os
import sys


class importWizard(QWizard):
    def __init__(self, parent = None):
        super(importWizard, self).__init__(parent)
        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowTitle("Import Wizard")

        self.intro  = IntroPage(self)
        self.importd = ImportPage(self)
        self.filter = FilterPage(self)

        self.addPage(self.intro)
        self.addPage(self.importd)
        self.addPage(self.filter)

    def accept(self):
        super(importWizard,self).accept()
        self.return_filelist = self.importd.fnames

        if self.filter.check29.isChecked():
            self.return_posttype = 1
        else:
            self.return_posttype = 2


class IntroPage(QWizardPage):
    def __init__(self, parent = None):
        super(IntroPage, self).__init__(parent)
        self.setTitle("Introduction")
        label = QLabel("This wizard is used to import the test data and select the test type. "
                       "Please move all the test data in one folder, muti-folder selection is "
                       "not support currently!!")

        label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

class ImportPage(QWizardPage):
    def __init__(self, parent =None):
        super(ImportPage, self).__init__(parent)
        self.setTitle("Test Data Import")

        label = QLabel("Please select the test data files need to be posted"
                               )
        label.setWordWrap(True)
        self.labellayout = QVBoxLayout()
        self.labellayout.addWidget(label)

        self.fileList = QListWidget()
        self.fileList.clear()

        self.addbtn = QPushButton("&Add...")
        self.connect(self.addbtn, SIGNAL("clicked()"), self.fileOpenDia)

        self.btnlayout = QVBoxLayout()
        self.btnlayout.addWidget(self.addbtn)
        self.btnlayout.addStretch()
        self.btnlayout.setAlignment(Qt.AlignTop)

        layout = QGridLayout()
        layout.addLayout(self.labellayout,0,0,)
        layout.addWidget(self.fileList,1,0,)
        layout.addLayout(self.btnlayout,1,1)
        self.setLayout(layout)

        self.registerField('files*', self.fileList)

    def fileOpenDia(self):
        self.fileList.clear()
        dir = "."
        self.fd = QFileDialog()
        self.fnames = self.fd.getOpenFileNames(self, "Select Test Data", dir, "Test ({0})".format("*.txt"))

        for fname in self.fnames:
            fname1 = os.path.basename(unicode(fname))
            self.fdir = os.path.dirname(unicode(fname))
            self.fileList.addItem(fname1)
        self.fileList.setCurrentRow(0)

class FilterPage(QWizardPage):
    def __init__(self, parent = None):
        super(FilterPage, self).__init__(parent)
        self.setTitle("Select Test Type:")
        label = QLabel("Please select the test type as the filter:")
        label.setWordWrap(True)
        self.labellayout = QVBoxLayout()
        self.labellayout.addWidget(label)
        self.check29 = QRadioButton("Performance Inlet 2.9 Psi Test")
        self.check49 = QRadioButton("Performance Inlet 4.9 Psi Test")
        layout = QGridLayout()

        self.check49.setChecked(True)

        layout.addLayout(self.labellayout,0,0,)
        layout.addWidget(self.check29,1,0)
        layout.addWidget(self.check49,2,0)


        self.setLayout(layout)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    form = importWizard()
    form.show()
    app.exec_()