from pandas import DataFrame

class clsTestData:    # the structure to store the filtered data
    def __init__(self, filename):
        self.fileName = filename   # short file name string
        self.rate = 0    # sampling rate - frequency
        self.column = 0  # column number in the data frame
        self.row = 0  # rows number
        self.header = []   # list of columns header
        self.data = DataFrame()  # data frame for test data



    def setFileName(self, filename):
        self.fileName = filename
    def getFileName(self):
        return self.fileName

    def getColumnList(self):
        return self.header


    def addColumnData(self,colName,colDataList):  # add data of one column
        if colName not in self.header:
            self.column += 1
            self.header.append(colName)
            self.data[colName] = colDataList  # dataframe of data

    def getColNum(self):
        return self.column
    def removeColumnData(self,colName):
        if colName == 'TIME':
            return
        if colName in self.header:
            self.column -= 1
            self.header.remove(colName)
            del self.data[colName]
