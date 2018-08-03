import datetime
starttime = datetime.datetime.now()


def dataPost(Fname, Row_StartT, Row_EndT, Column_list, Out_Rate):

    all_data = []
    out_data = []

    f1 = open(Fname, 'r')

    title = f1.readline().strip().split('\t')

    next_line = f1.readline().strip()

    start_tag = False
    end_tag = False

    while next_line:
        temp_list = next_line.split('\t')
        all_data.append(temp_list)
        if temp_list[0][0:5] == Row_StartT:
            start_tag = True
        if temp_list[0][0:5] == Row_EndT:
            end_tag = True
        if start_tag and not end_tag:
            out_data.append(temp_list)

        next_line = f1.readline().strip()

    #print(out_data)

def dataPost2(Fname, Row_StartT, Row_EndT, Column_list, Out_Rate):

    all_data = []
    out_data = []

    start_tag = False
    end_tag = False

    with open(Fname, 'r') as f:
        for line in f:
            temp_list = line.split('\t')
            if temp_list[0].isalpha():
                title = temp_list
            if temp_list[0][0:5] == Row_StartT:
                start_tag = True
            if temp_list[0][0:5] == Row_EndT:
                end_tag = True
            if start_tag and not end_tag:
                out_data.append(temp_list)

    f.close()
    f2 = open('output.txt', 'w+')

    for line in out_data:
        temp_line = ''
        #print(line)
        for item in line:
            temp_line += (item + '\t')
        temp_line = temp_line  + '\n'
        f2.writelines(temp_line)

    f2.close()


    #print(out_data)

fname = 'C:/00_Work/Work_Python/06_TestPost/test_data.txt'
start_time = '09:16'
end_time = '09:29'

dataPost2(fname, start_time,end_time, '0', 0)

endtime = datetime.datetime.now()

print((endtime-starttime).seconds)

