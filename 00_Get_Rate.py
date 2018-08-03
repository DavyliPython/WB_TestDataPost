

def dataRate(Fname):
    with open(Fname, 'r') as f:
        line_limit = 2000
        i = 0
        second_list = []
        for line in f:
            line_limit = 200
            temp_list = line.split('\t')
            temp_num = temp_list[0][0:8]
            if temp_list[0].isalpha():
                title = temp_list
            if temp_list[0][0:2].isdigit():
                #print(temp_list[0])
                #print(temp_num)
                i = i +1
                second_list.append(temp_num)
                if i == 1500:break
    #print(second_list)

    # cc_num = second_list[0]
    # cc_i = 0
    cc_rate_list = []
    # for item in second_list:
    #     if item ==
    for item in second_list:
        cc_rate_list.append(second_list.count(item))
        #print(second_list.count(item))

    return max(cc_rate_list)

fname = 'C:/00_Work/Work_Python/06_TestPost/test_data2.txt'

print(dataRate(fname))