import pandas as pd
import time
import os



def checkFile(fname):
    sizeoffile = os.path.getsize(fname)/1024   # file size in KB

    #print (sizeoffile)
    return round(sizeoffile,  1)   # keep on digit of decimal



def timeFormat(inTime):
    # inTime: 13:43:02:578
    # outTime: 13:43:02.578

    itime = inTime.split(':')
    return itime[0] + ':' & itime[1] + ':' & itime[2] + '.' & itime[3]

def msBySemicolon(inTime):
    # inTime: 13:43:02
    # outTime: 13:43:02:000

    return inTime + ':000'

def locateByTime(dataFile,startTime=0, endTime=0):
    df = pd.read_csv(dataFile, delim_whitespace = True, error_bad_lines = False)

    #startTime = timeFormat(df['TIME'].iloc[0])
    #endTime = timeFormat(df['TIME'].iloc[-1])
    print(df.head(1))
    print(df.info())
    print("--- %s seconds ---" % (time.time() - start_time))

    df = pd.read_csv(dataFile, delim_whitespace=True, skiprows=df.count - 2, error_bad_lines=False)
    print(df.tail(1))
    print("--- %s seconds ---" % (time.time() - start_time))
    # with open(dataFile, "r") as f:
    #     last_line = f.readlines()[-10]
    # print(last_line)

    startTime =msBySemicolon( '12:17:44')
    endTime = msBySemicolon( '12:18:38')

    #print(df.head(2))
    #idf = df.loc[ df['TIME'] > startTime , :]           # get the time series
    #jdf = idf.loc[ idf['TIME'] < endTime, :]  # get the time series

    #print (jdf)



    return (0)



dataFile =  r'C:\onedrive\OneDrive - Honeywell\VPD\test data\8hz_test_sample.txt'

print ("The file size is {} KB".format(checkFile(dataFile)))

start_time = time.time()

#print (locateByTime(dataFile))
#print("--- %s seconds ---" % (time.time() - start_time))
