from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidget, QTreeWidgetItem, QHeaderView, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QMenu, Qt, QAction, QCursor, QApplication

import sys
import os
# from PyQt5.Qt import *


import UI_5_Import as ui
import numpy as np

class dataPartition(QMainWindow, ui.Ui_Import):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.openFile)
        self.pushButton_2.clicked.connect(self.previewData)
        self.pushButton_3.clicked.connect(self.clearTable)
        self.pushButton_5.clicked.connect(self.dataPost)

        self.spinBox.setValue(100)
        self.spinBox.setMinimum(20)

        self.preData = []



        self.show()

    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','../')
        if fname[0]:
            #print(fname)
            self.shortfname = os.path.basename(fname[0])
        self.lineEdit.setText(fname[0])

    def previewData(self):

        previews_lines = int(self.spinBox.text())

        previews_data = []


        # Method 1. To get the lines of file
        # f1 = open(self.lineEdit.text(), 'r')
        # file_lines = len(f1.readlines())
        # print(file_lines)
        # f1.close()

        # Method 2. To get the lines of file
        # f1 = open(self.lineEdit.text(), 'r')
        # count = 0
        # while True:
        #     buffer = f1.read(1024*8192)
        #     if not buffer:
        #         break
        #     count += buffer.count('\n')
        # f1.close()
        # print(count)


        f1 = open(self.lineEdit.text(), 'r')
        #print(f1)
        temp_line =  f1.readline().strip()
        self.previewTitle = temp_line.split('\t')
        print(self.previewTitle)

        temp_line = f1.readline().strip()
        for ii in range(0,previews_lines):
            previews_data.append(temp_line.split('\t'))
            temp_line = f1.readline().strip()


        #print(previews_data)


        i = 0
        self.tableWidget.setColumnCount(len(self.previewTitle))
        self.tableWidget.setRowCount(previews_lines)
        for items in self.previewTitle:
            self.tableWidget.setItem(0,i, QTableWidgetItem(items))
            i = i + 1

        #print('aaa')
        #print(previews_data[1][1])

        for i in range(0, previews_lines):
            #print('bbb')
            for j in range(0, len(self.previewTitle)):
                #print(previews_data[i][j])
                self.tableWidget.setItem(i+1, j, QTableWidgetItem(previews_data[i][j]))


        self.tableWidget.resizeColumnsToContents()

    def clearTable(self):

        self.tableWidget.clear()


    def dataPost(self):
        self.dataStartRow = 0
        self.dataEndRow = 0 + 100

        self.dataStartColumn = []

        self.dataRead(self.lineEdit.text())
        print('hahah')
        #print(self.preData)

        self.dataStartRow, self.dataEndRow = self.dataPost_Time(self.lineEdit_2.text(),self.lineEdit_3.text(), self.preData)
        print(self.dataStartRow, self.dataEndRow)

    def dataRead(self, fname):
        f1 = open(fname, 'r')

        temp_line = f1.readline().strip()
        previewTitle = temp_line.split('\t')
        #print(previewTitle)

        temp_line = f1.readline().strip()

        for ii in range(0, 500000):
            self.preData.append(temp_line.split('\t'))
            temp_line = f1.readline().strip()

        # while temp_line:
        #     self.preData.append(temp_line.split('\t'))
        #     temp_line = f1.readline().strip()



    def dataPost_Time(self, Tstart, Tend, preData):
        tag1 = True
        tag2 = True
        print(len(preData))
        for i in range(0, len(preData)-1000):
            if tag1:
                # print(preData[i][0][0:5])
                if Tstart == preData[i][0][0:5]:
                    #print(preData[i][0][0:5])
                    dataStartRow = i
                    tag1 = False
                    print(dataStartRow)

            if tag2:
                if Tend == preData[i][0][0:5]:
                    dataEndRow = i
                    tag2 = False
                    print(dataEndRow)

            #if not tag1 and not tag2: break
            #print(i)

        return dataStartRow, dataEndRow











if __name__ == '__main__':
    app = QApplication(sys.argv)
    MW = dataPartition()
    #app.show()
    sys.exit(app.exec_())
    print("DONE")
