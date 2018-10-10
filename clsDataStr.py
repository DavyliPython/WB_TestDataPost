import pandas as pd

class clsTestData:
    def __init__(self, filename, lstTime):
        self.strFileName = filename   # short file name string
        self.N = 1  # column number in the data frame, TIME column is counted in
        self.lstColumns = ['TIME']   # list of columns
        self.dfTestData = pd.DataFrame()
        self.dfTestData['TIME'] = lstTime  # dataframe of data


    def setFileName(self, filename):
        self.strFileName = filename
    def getFileName(self):
        return self.strFileName

    def getColumnList(self):
        return self.lstColumns

    def addColumnData(self,colName,colDataList):
        if colName not in self.lstColumns:
            self.N += 1
            self.lstColumns.append(colName)
            self.dfTestData[colName] = colDataList  # dataframe of data

    def getColNum(self):
        return self.N
    def removeColumnData(self,colName):
        if colName == 'TIME':
            return
        if colName in self.lstColumns:
            self.N -= 1
            self.lstColumns.remove(colName)
            del self.dfTestData[colName]
