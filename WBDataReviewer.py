from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QMenu, Qt, QAction, QCursor, QApplication

import sys


#from clsDataImport import clsImportData
from clsDataView import clsDataView




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = clsDataView()
    #winImpData = clsImportData()

    sys.exit(app.exec_())
