from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidget, QTreeWidgetItem, QWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QMenu, Qt, QAction, QCursor, QApplication, QDialog,QMessageBox, QTime
import PyQt5.QtGui



import sys
import os
import pandas as pd
from datetime import datetime

from UI_5_Import import Ui_winImportData

from clsDataStr import clsTestData

class clsImportData(QDialog, Ui_winImportData):
    ''''
    '''

    def __init__(self, dataparam, listoftestdata):  # dataparam - parameter class
        super().__init__()



        self.setupUi(self)
        self.initImpUI()
        self.btnBrowse_in.clicked.connect(self.openDateFile)
        self.btnImport.clicked.connect(self.ImportDataToDf)
        self.btnExport.clicked.connect(self.ExportDataToFile)
        self.btnBrowse_out.clicked.connect(self.getPathOfExport)

        self.sbRate.valueChanged.connect(self.rateValueChange)


        self.dataparam = dataparam  # data parameter class for conversion use
        self.lTESTDATA = listoftestdata   # list of testdata to be reviewed



        self.sDataFilePath = "C://"
        self.iFileSize = 0
        self.iDataRate = 0
        self.newRate = 0
        self.startTime = "00:00:00"         # the start time in the data file
        self.endTime = "00:00:00"           # the end time in the data file

        self.sStartTime = self.startTime     # the start time in the selection
        self.sEndTime = self.endTime         # the end time in the selection
        self.firstRow = 1     # the first row in the data file
        self.lastRow = 1      # the last row in the data file
        self.iStartRow = self.firstRow   # the first row in the selection
        self.iEndRow = self.lastRow      # the last row in the selection


        self.parColImported = []  # parameter column to be imported to main window for review
        self.dfImptedData = pd.DataFrame()   # the dataframe to keep the imported data set


    def initImpUI(self):

        self.tblreviewdata.setEditTriggers(PyQt5.QtGui.QAbstractItemView.NoEditTriggers) # disable to edit the table
        self.tblreviewdata.setSelectionBehavior(self.tblreviewdata.SelectColumns)   # select columns only
        #self.tblreviewdata.doubleClicked.connect(self.addSelectedColumn)
        self.tblreviewdata.setSelectionMode( PyQt5.QtGui.QAbstractItemView.MultiSelection)

        self.progressBar.setValue(0)


    def setDataFilePath(self, filepath):
        self.sDataFilePath = filepath
        self.qleFilePath_in.setText(filepath)
        self.qleFilePath_out.setText(os.path.dirname(filepath)+'/')

    def setDataRate(self):
        self.qleRate.setText(str(self.iDataRate))
        self.sbRate.setValue(self.iDataRate)


    def setStartTime(self):
        pass
        #self.teFromTime.setText(datetime.strftime(self.sStartTime)str(self.sStartTime))

    def setEndTime(self):
        pass
        #self.teToTime.setText(self.sEndTime)

    def setStartRow(self):
        self.qleFromRow.setText(str(self.iStartRow))

    def setEndRow(self):
        self.qleToRow.setText(str(self.iEndRow))




    def openDateFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\onedrive\\OneDrive - Honeywell\\VPD\\test data\\_8hz_test_sample.txt', "Text Files (*.txt);;All Files (*)")
        if fname[0]:     # process only the one selection

            if self.sDataFilePath != fname[0]:   # the file was not selected before
                self.setDataFilePath(fname[0])

                sizeoffile = os.path.getsize(self.sDataFilePath)
                if sizeoffile <= 0:
                    QMessageBox.critical(self, "Error", "Data rate should not be Zero")
                    return

                dfData = pd.read_csv(self.sDataFilePath, delim_whitespace=True, nrows=200,
                                     error_bad_lines=False)  # read 200 rows only

                self.iDataRate = self.estDataRate(list(dfData['TIME']))

                if self.iDataRate <= 0:
                    QMessageBox.critical(self, "Error", "Data rate should not be Zero")
                    return

                self.setDataRate()

                self.qleFileSize.setText(str(round(sizeoffile/1024, 1)))  # KB, keep on digit of decimal

                # read the first 10 rows from the file
                self.data2review = dfData.head(int(self.leRows.text()))   # leRows = for preview rows
                self.dataHeader = list(dfData)  # data header list

                self.startTime = dfData['TIME'].iloc[0][:8]
                self.sStartTime = self.startTime   # default selected time is same as the data start time
                #self.setStartTime()
                self.teDataFromTime.setTime(datetime.strptime('2018 ' + self.sStartTime, '%Y %H:%M:%S').time())
                self.teFromTime.setTime(datetime.strptime('2018 ' + self.sStartTime, '%Y %H:%M:%S').time())

                self.qleColumns.setText(str(dfData.shape[1]))

                self.iStartRow = self.firstRow
                #self.setStartRow()

                self.lastRow = self.estRowNum(self.sDataFilePath)
                self.iEndRow = self.lastRow
                self.qleRows.setText(str(self.lastRow))
                self.qleToRow.setText(str(self.lastRow))

                duration = round(self.iEndRow/self.iDataRate)  # estimate the seconds from row number and sample frequency
                self.endTime = self.estTimeByDuration(self.sStartTime, duration)
                self.sEndTime = self.endTime
                self.teDataToTime.setTime(datetime.strptime('2018 ' + self.endTime, '%Y %H:%M:%S').time())
                self.teToTime.setTime(datetime.strptime('2018 ' + self.endTime, '%Y %H:%M:%S').time())
                #self.setEndTime()



                # do the time consuming work of scan the data file
                self.populatePreviewTable()






    def getDataFileSize(self,dfPath):
        '''
            input:  string, path to the file
            return: int, file size in KB
        '''
        sizeoffile = os.path.getsize(dfPath) / 1024  # file size in KB

        # print (sizeoffile)
        return round(sizeoffile, 1)  # keep on digit of decimal


    def estTimeByDuration(self, starttime, duration):
        ''' estimate the end time from stat time with duration
            input:
                starttime: string,  "13:43:02"
                duration:  int, 50
            output:
                endtime: string, hh:mm:ss
        '''
        #duration = round(self.iEndRow/self.iDataRate)  # estimate the seconds from row number and sample frequency

        #itime = self.sStartTime[:8]    #  13:43:02
        dttime = datetime.strptime('2018 '+ starttime, '%Y %H:%M:%S')  # convert the time from string to the datetime format
        i = dttime.timestamp() + duration   # get the timestamp plus duration
        dttime = datetime.fromtimestamp(i)  # convert to datetime

        return dttime.time().strftime('%H:%M:%S')

    def offsetRowByTime(self, startTime, endTime, rate):
        ''' estimate the rows offset from stat time with duration
                    input:
                        startTime: string, "13:43:02"
                        endTime:  string,  "13:43:02"
                        rate: int, data sample rate, frequency
                    output:
                        offset in row: int, + for forward and - for backward
                '''
        i = datetime.strptime('2018 ' + startTime, '%Y %H:%M:%S') # get the time stamp
        j = datetime.strptime('2018 ' + endTime, '%Y %H:%M:%S')   # get the time stamp of end time
        duration = j - i     # duration, + for forward and - for backward

        return round(duration * rate)


    def estRowNum(self,filename):

        with open(filename, 'rb') as input_file:
            linesize = 0
            i = 0
            for line in input_file:
                if i == 0:
                    i += 1
                    continue
                linesize += len(line)
                i += 1
                if i >= 11:
                    break

            linesize /= 10
        filesize = os.path.getsize(self.sDataFilePath)
        rownumber = round (filesize/linesize)
        return  rownumber



    def estDataRate(self,lstTime):
        '''
            input: list of time
            output: int, rate in Hz

        '''

        minLineNumber = 10
        maxLineNumber = len(lstTime)
        i = 0

        lastMillisecond = 0
        second_list = []
        millisecondListValue = 0
        n = 0  # increase of time in millisecond
        idataRate = 0

        for iTime in lstTime:
            #iTime  12:17:44:531
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
                if j == 0:
                    tblItem = QTableWidgetItem(str(row.iloc[j]))
                else:
                    tblItem = QTableWidgetItem(str(round(row.iloc[j],3)))
                self.tblreviewdata.setItem(i, j, tblItem)
                #else:
                #    self.tableView.setItem(i, j, QTableWidgetItem(str(val)))





    def ImportDataToDf(self):
        #self.winImportData  send signal to hide the window
        datafilename = os.path.basename(self.sDataFilePath)  # get the filename

        if not self.tblreviewdata.selectedIndexes(): return  # no selection

        if datafilename:   # data file existing

            # get the selected column header
            dfData = pd.read_csv(self.sDataFilePath, delim_whitespace=True, nrows=1, error_bad_lines=False)  # read 1 line
            header = list(dfData)    # get the header to a list

            selectedColumnHeader = ['TIME']

            indexes = self.tblreviewdata.selectedIndexes()  # the indexes of current selections

            for i in range (0, len(indexes), self.tblreviewdata.rowCount()):
                columnhead = list(dfData)[indexes[i].column()]  # get the selected column header
                if columnhead != 'TIME' and columnhead not in selectedColumnHeader:
                    selectedColumnHeader.append(columnhead)  # add column header to the list


        # read the data file with changed rate and selected columns

            dfData = pd.read_csv(self.sDataFilePath, delim_whitespace=True, error_bad_lines=False,iterator=True)

            chunkSize = max(2048, self.iDataRate ) # 2048 # self.iDataRate  2K rows
            chunks = []
            extract_row_range = range(0, self.iDataRate,self.iDataRate//self.newRate)

            while True:
                try:
                    chunk = dfData.get_chunk(chunkSize)
                    chunkOfSelected = chunk[selectedColumnHeader]
                    chunkOfSelected = chunkOfSelected.iloc[extract_row_range,:]
                    chunks.append(chunkOfSelected)

                    self.progressBar.setValue(round(chunk.first_valid_index()/self.lastRow *100))

                except StopIteration:
                    print("data imported") #QMessageBox.critical (self, "Error", 'Iteration is stopped')
                    break


            dfData = pd.concat(chunks,ignore_index=True)

            # enclose the dfData into class clsTestData
            strTestData = clsTestData(datafilename)
            strTestData.header = selectedColumnHeader
            strTestData.column = dfData.shape[1]
            strTestData.row = dfData.shape[0]
            strTestData.rate = int(self.qleRate.text())
            strTestData.data = dfData

            if not self.lTESTDATA:  # it is the first data set
                self.lTESTDATA.append(strTestData)
            else:
                for i in self.lTESTDATA:   # check if the data file name is in the list
                    if datafilename == i.getFileName():
                        i.header = selectedColumnHeader
                        i.column = len(selectedColumnHeader)
                        i.row = len(dfData['TIME'])
                        i.rate = int(self.qleRate.text())
                        i.data = dfData
                    else:
                        self.lTESTDATA.append(strTestData)  # add current selection data into the testdata list


        self.close()



    def ExportDataToFile(self):
        pass

    def getPathOfExport(self):
        fname = QFileDialog.getSaveFileName(self,'Save as:',
                                            os.path.dirname(self.sDataFilePath),
                                            "Text Files (*.txt)")
        if fname[0]:  # process only the one selection

            print(fname[0])

    def rateValueChange(self):
        if int(self.sbRate.text()) != 0:
            self.sbRate.setSingleStep(int(self.sbRate.text())/2)
            self.newRate = int(self.sbRate.text())


