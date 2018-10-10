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

    def __init__(self, dataparam, listoftestdata):  # dataparam - parameter class
        super().__init__()



        self.setupUi(self)
        self.initImpUI()
        self.pushButton.clicked.connect(self.openDateFile)


        self.dataparam = dataparam  # data parameter class for conversion use
        self.lTESTDATA = listoftestdata   # list of testdata to be reviewed



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
        if fname[0]:     # process only the first selection, could be extended for multi selection function TODO

            if self.sDataFilePath != fname[0]:   # the file was not selected before
                self.setDataFilePath(fname[0])

                self.setDataRate(self.getDataRate(self.sDataFilePath))
                self.setFileSize(self.getDataFileSize(self.sDataFilePath))

                dfData = pd.read_csv(self.sDataFilePath, delim_whitespace=True, nrows = 100,  error_bad_lines=False)  # read 100 rows only

                # read the first 10 rows from the file
                self.data2review = dfData.head(9)
                self.dataHeader = list(dfData)  # data header list

                self.sStartTime = dfData['TIME'].iloc[0]
                self.sEndTime = dfData['TIME'].iloc[-1]

                self.setStartTime(self.sStartTime)
                self.setEndTime(self.sEndTime)
                self.setStartRow(1)
                self.setEndRow(100)

                # do the time consuming work of scan the data file
                self.populatePreviewTable()






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

    def populatePreviewTable(self):

         # change the head of table
        self.tblreviewdata.setHorizontalHeaderLabels(self.dataHeader)
        #self.tblreviewdata.horizontalHeaderItem().setTextAlignment(Qt.AlignHCenter)

        # populate data to the table
        self.tblreviewdata.setRowCount(len(self.data2review.index))
        self.tblreviewdata.setColumnCount(len(self.data2review.columns))
        for i, row in self.data2review.iterrows():
            for j in range (len(self.data2review.columns)): #, val in row
                tblItem = QTableWidgetItem(str(row.iloc[j]))
                self.tblreviewdata.setItem(i, j, tblItem)
                #else:
                #    self.tableView.setItem(i, j, QTableWidgetItem(str(val)))





    def addSelectedColumn(self):

        datafilename = os.path.basename(self.sDataFilePath)  # get the filename
        dfData = pd.read_csv(self.sDataFilePath, delim_whitespace=True, error_bad_lines=False)

        if not self.lTESTDATA:    # it is the first data set
            # create a new test data class instance
            strTestData = clsTestData(datafilename, dfData['TIME'])
            self.lTESTDATA.append(strTestData)  # add current selection data into the testdata list
        else:
            for i in self.lTESTDATA:   # check if the data file name is in the list
                if datafilename == i.getFileName():
                    strTestData = i
                else:
                    # create a new test data class instance
                    strTestData = clsTestData(datafilename, dfData['TIME'])
                    self.lTESTDATA.append(strTestData)  # add current selection data into the testdata list



        indexes = self.tblreviewdata.selectedIndexes()    # the indexes of current selections
        #parColImported = []
        for index in indexes:
            columnhead = list(dfData)[index.column()]   # get the column index
            if columnhead !='TIME' and columnhead not in strTestData.getColumnList() :
                strTestData.addColumnData(columnhead, dfData[columnhead])  # add column and data into the data set


