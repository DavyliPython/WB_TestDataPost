###__Version__ V1.0



from PyQt5.QtWidgets import QApplication

import sys


#from clsDataImport import clsImportData
from clsDataView import clsDataView




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = clsDataView()

    sys.exit(app.exec_())
