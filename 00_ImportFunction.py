# -*- coding: utf-8 -*-

# Output rate is used as original rate / output rate, is shall be 1/2, 1/4, 1/8,...

import os
import numpy as np


def importFunction(Filename, Row_Start = 0 , Row_End = -1, ColumnOutputList=[], OutputRate=1, OutputFilename = 'Output'):
    pass
    f1 = open(Filename, 'r')
    f2 = open(OutputFilename,'w')
    # print(f1)
    temp_line = f1.readline()
    f2.writelines(temp_line)


    line = f1.readline()
    f2.writelines(line)

    i_row = 2
    while line:

        for i_hz in range(int(1.0/OutputRate)):
            line = f1.readline()
        if i_row > Row_Start :
            f2.writelines(line)
        if Row_End != -1 :
            if i_row > Row_End:
                break
        i_row = i_row + 1

    f1.closed
    f2.closed

def column_filter(line_in, filterlist):

    return_line = line_in
    return return_line



if __name__ == '__main__':
    fileName = 'C:/00_Work/Work_Python/06_TestPost/test_data2.txt'
    row_Start = 100
    row_End = -1
    columnOutputList = []
    outputRate = 1
    outputFilename = fileName[0:-4] + '_output.txt'
    columnOutputList = np.ones(10,int)
    aaa =  columnOutputList[2]
    if columnOutputList[2] == 1:
        print('haha')

    importFunction(fileName, row_Start, row_End,columnOutputList, outputRate, outputFilename)

