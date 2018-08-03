import os


filename = 'C:/00_Work/Work_Python/06_TestPost/test_data.txt'


t1 = '09:17'
t2 = '09:18'

previews_lines = 500000

preData = []

f1 = open(filename, 'r')



temp_line = f1.readline().strip()
previewTitle = temp_line.split('\t')
print(previewTitle)

temp_line = f1.readline().strip()
for ii in range(0, previews_lines):
    preData.append(temp_line.split('\t'))
    temp_line = f1.readline().strip()

print(len(preData))

def dataPost_Time(Tstart, Tend, preData):
    tag1 = True
    tag2 = True
    for i in range(0, len(preData)):
        if tag1:
            #print(preData[i][0][0:5])
            if Tstart == preData[i][0][0:5]:
                print(preData[i][0][0:5])
                dataStartRow = i
                tag1 = False
                print(dataStartRow)

        if tag2:
            if Tend == preData[i][0][0:5]:
                dataEndRow = i
                tag2 = False
                print(dataEndRow)

        if not tag1 and not tag2: break


    return [dataStartRow, dataEndRow]

aaa = dataPost_Time(t1,t2,preData)
print(aaa)