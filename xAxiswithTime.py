import pyqtgraph as pg
import pandas as pd
from datetime import datetime

class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        # show hour:minute:second on the x axis
        return [datetime.fromtimestamp(value).strftime('%H:%M:%S') for value in values]

def sTimeToDateTime(inTime):
    # inTime: '13:43:02:578' string type
    # outTime: 2018-08-22 13:43:02.578000  datetime object

    itime = inTime.split(':')
    # add current date to the TIME for the sake of format of datetime class. could use real date of the data created
    rtime = datetime.now().date().isoformat() +' ' + itime[0] + ':'+ itime[1] + ':' + itime[2] + '.' + itime[3]  #with date
    return datetime.strptime(rtime, '%Y-%m-%d %H:%M:%S.%f')  # convert the time from string to the datetime format


dataFile =  r'C:\onedrive\OneDrive - Honeywell\VPD\test data\32Hz-BRK-ANA004.txt'

df = pd.read_csv(dataFile, delim_whitespace = True, error_bad_lines = False)

# get the list of time column
sTime = list(df['TIME'])

# convert the time in string to date time object
iTime = [sTimeToDateTime(i) for i in sTime]


app = pg.QtGui.QApplication([])


xAxis = TimeAxisItem(orientation='bottom')
pw = pg.PlotWidget(axisItems = {'bottom':xAxis})

pw.plot(x=[x.timestamp() for x in iTime ], y= list(df['BCVIIN']), pen = 'r')
pw.plot(x=[x.timestamp() for x in iTime ], y= list(df['BCVIINR']), pen = 'b')
pw.plot(x=[x.timestamp() for x in iTime ], y= list(df['BCVIINR']), pen = 'w')
pw.plot(x=[x.timestamp() for x in iTime ], y= list(df['BCVIOUT']), pen = 'g')
pw.show()

app.exec_()