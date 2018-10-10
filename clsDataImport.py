from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidget, QTreeWidgetItem, QWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QMenu, Qt, QAction, QCursor, QApplication, QDialog
import PyQt5.QtGui



import sys
import os
import pandas as pd

from UI_5_Import import Ui_Import

from clsDataStr import clsTestData

class clsImportData(QDialog, Ui_Import):
    ''''
    '''

    def __init__(self, dataparam, testdata):  # dataparam - parameter class
        super().__init__()



        self.setupUi(self)
        self.initImpUI()
        self.pushButton.clicked.connect(self.openDateFile)


        self.dataparam = dataparam  # data parameter class for conversion use
        self.lTESTDAT = testdata



        self.sDataFilePath = "C://"
        self.iFileSize = 0
        self.iDataRate = 0
        self.sStartTime = "00:00:00"
        self.sEndTime = '00:00:00'
        self.iStartRow = 1
        self.iEndRow = 0

        self.parColImported = []  # parameter column to be imported to main window for review
        self.dfImptedData = pd.DataFrame()   # the dataframe to keep the imported data set








    def initImpUI(self):
        self.tblreviewdata.setEditTriggers(PyQt5.QtGui.QAbstractItemView.NoEditTriggers) # disable to edit the table
        self.tblreviewdata.setSelectionBehavior(self.tblreviewdata.SelectColumns)   # select columns only
        self.tblreviewdata.doubleClicked.connect(self.addSelectedColumn)


    def setDataFilePath(self, filepath):
        self.sDataFilePath = filepath
        self.qleFilePath.setText(self.sDataFilePath)

    def setDataRate(self, datarate):
        self.iDataRate = datarate
        self.qleRate.setText(str(self.iDataRate))

    def setFileSize(self,filesize):
        self.iFileSize = filesize
        self.qleFileSize.setText(str(self.iFileSize))

    def setStartTime(self, starttime):
        self.sStartTime = starttime
        self.qleStartTime.setText(str(self.sStartTime))

    def setEndTime(self,endtime):
        self.sEndTime = endtime
        self.qleEndTime.setText(self.sEndTime)

    def setStartRow(self,startrow):
        self.iStartRow = startrow
        self.qleStartRow.setText(str(self.iStartRow))

    def setEndRow(self,endrow):
        self.iEndRow = endrow
        self.qleEndRow.setText(str(self.iEndRow))




    def openDateFile(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\onedrive\\OneDrive - Honeywell\\VPD\\test data\\8hz_test_sample.txt', "Text Files (*.txt);;All Files (*)")



        if fname[0]:
            self.setDataFilePath(fname[0])

            self.setDataRate(self.getDataRate(self.sDataFilePath))
            self.setFileSize(self.getDataFileSize(self.sDataFilePath))

            self.scanDateFile(self.sDataFilePath)


            self.setStartTime(self.sStartTime)
            self.setEndTime(self.sEndTime)
            self.setStartRow(1)
            self.setEndRow(100)

        # self.getDataLineNo(dataFilePath)



    def getDataFileSize(self,dfPath):
        '''TODO
            input:  string, path to the file
            return: int, file size in KB
        '''
        sizeoffile = os.path.getsize(dfPath) / 1024  # file size in KB

        # print (sizeoffile)
        return round(sizeoffile, 1)  # keep on digit of decimal

    def getEndRow(self, dfPath):
        '''TODO
            input: string, path to the file
            output: int, line number of the date, approx estimation is acceptable


        '''
        pass

    def getStartTime(self, dfPath):
        '''TODO
            input: string, path to the file
            output: string, format: hh:mm:ss.sss, the time of the first line

        '''
        return '00:00:00'

    def getEndTime(self,dfPath):
        '''TODO
            input: string, path to the file
            output: string, format: hh:mm:ss.sss, the time of the last line

        '''
        return '00:10:00'

    def getDataRate(self,Fname):
        '''
            input: string, path to the file
            output: int, rate in Hz

        '''
        with open(Fname, 'r') as f:
            minLineNumber = 10
            maxLineNumber = 20
            i = 0

            line = f.readline()
            temp_list = line.split()

            if temp_list[0].upper() != "TIME":
                print("bad data file format")
                return (-1)

            lastMillisecond = 0
            second_list = []
            millisecondListValue = 0
            n = 0  # increase of time in millisecond
            idataRate = 0
            for line in f:

                temp_list = line.split()
                iTime = temp_list[0]  # 12:17:44:531
                iMillisecond = int(iTime.split(":")[3])  # 531

                if iMillisecond >= lastMillisecond:  # get the increase: n
                    n = iMillisecond - lastMillisecond
                else:
                    n = iMillisecond + 1000 - lastMillisecond

                millisecondListValue += n

                second_list.append(millisecondListValue)

                lastMillisecond = iMillisecond

                i += 1

                if i >= minLineNumber:
                    if max(second_list) - min(second_list) == 0:
                        idataRate = 1
                        return (idataRate)  # the case of 1 hz sample rate, normal exit

                    else:
                        idataRate = int(1000 / (max(second_list) - min(second_list)) * (len(second_list) - 1))

                    if idataRate & (idataRate - 1) == 0:
                        return (idataRate)  # for case of the power of 2 only (2, 4, 6, 8), normal exit

                if i > maxLineNumber:  # not a correct sample rate
                    idataRate = -1  # abnormal exit
                    break

        #print (idataRate)
        return idataRate

    def scanDateFile(self,datafilepath):
        self.dfData = pd.read_csv(datafilepath, delim_whitespace=True, error_bad_lines=False)
        data2review = self.dfData.head(10)
        self.sStartTime = self.dfData['TIME'].iloc[0]
        self.sEndTime = self.dfData['TIME'].iloc[-1]
        #self.iEndRow = (self.sEndTime - self.sStartTime)/self.iDataRate

        # change the head of table
        self.tblreviewdata.setHorizontalHeaderLabels(list(self.dfData))
        #self.tblreviewdata.horizontalHeaderItem().setTextAlignment(Qt.AlignHCenter)

        # populate data to the table
        self.tblreviewdata.setRowCount(len(data2review.index))
        self.tblreviewdata.setColumnCount(len(data2review.columns))
        for i, row in data2review.iterrows():
            for j in range (len(data2review.columns)): #, val in row
                tblItem = QTableWidgetItem(str(row.iloc[j]))
                self.tblreviewdata.setItem(i, j, tblItem)
                #else:
                #    self.tableView.setItem(i, j, QTableWidgetItem(str(val)))

        # initiate test data class
        filename = os.path.basename(datafilepath)
        testdata = clsTestData(filename,self.dfData['TIME'])
        self.lTESTDAT.append(testdata)


    def addSelectedColumn(self):
        #self.parColImported.append('i')  #(self.tblreviewdata.selectColumn())
        indexes = self.tblreviewdata.selectedIndexes()

        for index in indexes:
            columnhead = list(self.dfData)[index.column()]   # get the column index
            if columnhead not in self.parColImported and columnhead !='TIME':
                self.parColImported.append(columnhead) # add the column head to the selected list

        for i in self.parColImported:
            self.lTESTDAT[len(self.lTESTDAT) - 1 ].addColumnData(i, self.dfData[i])