

def dataRate(Fname):
    with open(Fname, 'r') as f:
        line_limit = 20
        i = 0
        #startingLine = 5   #starting from row
        #for i in range (startingLine):
        #     next(f)  # skip the first 20 rows

        line = f.readline()
        temp_list = line.split()

        if temp_list[0].upper() != "TIME":
            print("bad data file format")
            return (-1)

        lastMillisecond = 0
        second_list = []
        for line in f:

            temp_list = line.split()
            iTime = temp_list[0]      # 12:17:44:531
            iMillisecond = int(iTime.split(":")[3])      # 531

            #if iMillisecond.isdigit():
                #print(temp_list[0])
                #print(temp_num)
            if iMillisecond < lastMillisecond:
                iMillisecond += 1000  # add 1000ms to the millisecond
            second_list.append(iMillisecond)
            if i == line_limit:break
            # else:
            #     print("bad data file format")
            #     return (-1)
            i += 1

            lastMillisecond = iMillisecond
    #print(second_list)

    idataRate = 1000/(max(second_list) - min(second_list))* (len(second_list)-1)


    return int(idataRate)

fname = 'C:/Mydisk/Projects/VPD/100kn/16Hz-100kn-pitch rol and Yawl.txt'

print(dataRate(fname))