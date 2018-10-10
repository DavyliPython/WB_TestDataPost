

def dataRate(Fname):
    with open(Fname, 'r') as f:
        minLineNumber = 10
        maxLineNumber = 20
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
        millisecondListValue = 0
        n = 0   # increase of time in millisecond
        idataRate = 0
        for line in f:

            temp_list = line.split()
            iTime = temp_list[0]      # 12:17:44:531
            iMillisecond = int(iTime.split(":")[3])      # 531

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
                    idataRate =1
                    return (idataRate)   # the case of 1 hz sample rate, normal exit

                else:
                    idataRate = int(1000 / (max(second_list) - min(second_list)) * (len(second_list) - 1))

                if idataRate & (idataRate - 1) == 0 : return (idataRate)   # for case of the power of 2 only (2, 4, 6, 8), normal exit

            if i > maxLineNumber:    # not a correct sample rate
                idataRate = -1        # abnormal exit
                break


    #print(second_list)

    #idataRate = 1000/(max(second_list) - min(second_list))* (len(second_list)-1)
    #print (second_list)

    return idataRate

fname = r'C:/00_Work/Work_Python/06_TestPost/test_data2_output.txt'

print(dataRate(fname))