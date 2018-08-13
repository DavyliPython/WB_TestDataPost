# -*- coding: utf-8 -*-

#
# Completed at Aug 8th.
# importFunction(Filename, Row_Start, Row_End, ColumnFilter, ColumnOutpulist, OutputRate, OutputFilename
#
#  Filename, input file name.
#  Row_Start, Row_End, start row, end row, if the Row_End = -1, to the end of file.
#  ColumnFilter, Use the column filter or not, ColumnFilter = 0, not use, ColumnFilter = 1, use.
#  OutputRate, Output rate is used as original rate / output rate, is shall be 1/2, 1/4, 1/8,...
#  OutputFilename output file name.
#  Function column_filter used for column filter.

#import os
import numpy as np


def importFunction(Filename, Row_Start = 0 , Row_End = -1, ColumnFilter = 0, ColumnOutputList=[], OutputRate=1, OutputFilename = 'Output'):
    pass

    if ColumnFilter == 0:
        f1 = open(Filename, 'r')
        f2 = open(OutputFilename,'w')
        # print(f1)
        line = f1.readline()
        f2.writelines(line)


        # line = f1.readline()
        # f2.writelines(line)

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

    if ColumnFilter == 1:
        f1 = open(Filename, 'r')
        f2 = open(OutputFilename, 'w')
        # print(f1)
        line = f1.readline()
        f2.writelines(column_filter(line, ColumnOutputList))

        # line = f1.readline()
        # f2.writelines(column_filter(line, ColumnOutputList))

        i_row = 2
        while line:

            for i_hz in range(int(1.0 / OutputRate)):
                line = f1.readline()
            if not line:
                #print('nihao')
                break
            if i_row > Row_Start:
                f2.writelines(column_filter(line, ColumnOutputList))
            if Row_End != -1:
                if i_row > Row_End:
                    break
            i_row = i_row + 1

        f1.closed
        f2.closed

def column_filter(line_in, filterlist):
    line_temp = line_in.strip().split('\t')
    #print(line_temp)
    return_line = ''

    for i in range(len(filterlist)):
        if filterlist[i] == 1: return_line = return_line + line_temp[i] + '\t'

    return_line = return_line.strip('\t') + '\n'

    return return_line



if __name__ == '__main__':
    fileName = 'C:/00_Work/Work_Python/06_TestPost/test_data2.txt'
    row_Start = 100
    row_End = -1
    ColumnFilter = 1
    columnOutputList = []
    outputRate = 1/2.0
    outputFilename = fileName[0:-4] + '_output.txt'
    columnOutputList = np.ones(9,int)
    columnOutputList[2] = 0
    columnOutputList[6] = 0
    aaa =  columnOutputList[2]
    if columnOutputList[2] == 1:
        print('haha')

    importFunction(fileName, row_Start, row_End, ColumnFilter, columnOutputList, outputRate, outputFilename)

