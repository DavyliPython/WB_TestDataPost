from PyQt5.QtWidgets import QMainWindow, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QMenu, Qt, QAction, QCursor
from PyQt5 import QtGui, QtCore

import pyqtgraph as pg
import pandas as pd

import sys
import os
from datetime import datetime
import time

from mainUI import Ui_MainWindow
from clsDataImport import clsImportData



class clsDataView(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # 类成员变量初始化
        self.colorDex = ['#7CFC00', '#B22222', '#E0FFFF', '#FFFF00', '#66FF00']

        self.lPlottedItems = []         # list of plotItems in the dataplot area
        self.currentPlotWin = ''        # keep current selected plot window for next curve plotting
        self.lPlotWindows = ['plot1']            # list of plot window
        self.lViewBoxes = []              # list of View box corresponding to the plotitem
        self.lAxisItems = []           # list of axis item of the layout of plotItem
        self.lPlottedCurves = []            # list of plotCurves of each plotItem
        self.lDataFileName = []          # data file name list
        self.shortfname = ''           # data file name without path
        self.bPlotted = False           # not curve is plotted   - could be replaced by len(lPlotItems) > 1
        self.dataInRange_x = []           # keep the x ['TIME'] of data in range  - first curve plotted
        self.dataInRange_y = []           # keep the y of data in range  - first curve plotted

        self.lTestDATA = []      # the test data to be reviewed, each item is a class of data structure
                                    #  [testData1, testData2 ...]
                                    #  [(filename, column name, dataframe of data)
        self.parColPlotted = []           # parameter column in plotting

        # for linear region use
        self.rgnXmin = 0
        self.rgnXmax = 1
        self.rgnXfactor = 1


            # r'C:\onedrive\OneDrive - Honeywell\VPD\parameters code.csv'
        self.dataparam = dataParam()   # data parameter definition
        #self.dataparam = dateParam()
        paramlist = self.dataparam.getParamName()
        self.dataparam.getParamInfo('ABCVIINR', 'paramDesc')
        #self.dfData = pd.DataFrame()    # pandas dataframes to be plot

        # pyqtGraph 相关设置，必须要在self.setupUi之前
        pg.setConfigOption('background', 'w')  # before loading widget

        # # set the time axis of X
        xAxis = self.TimeAxisItem(orientation='bottom')
        self.dataPlot = pg.PlotWidget(self, axisItems={'bottom': xAxis}, name='plot1')

        self.setupUi(self)
        self.initUI()


        self.show()
        #self.showMaximized()   # max the window


    def initUI(self):




        # 添加打开菜单
        selFileAction = QAction(QIcon('open.png'), '&Open', self)
        selFileAction.setShortcut('Ctrl+O')
        selFileAction.setStatusTip('Open new File')
        selFileAction.triggered.connect(self.openFile)     # open data file
        selFileAction.setIcon(QIcon('import.ico'))

        exitAction = QtGui.QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit the application')
        #exitAction.triggered.connect(QtGui.qApp.quit)
        exitAction.triggered.connect(self.exitAPP)     # exit the application

        clearAction = QtGui.QAction(QIcon('Clear.png'), 'Clear', self)
        clearAction.triggered.connect(self.clearPlotArea)

        addPlotAction = QtGui.QAction(QIcon('Addplot.png'), 'Add a Plot', self)
        addPlotAction.triggered.connect(self.addDataPlot)

        removePlotAction = QtGui.QAction(QIcon('Addplot.png'), 'Remove a Plot', self)
        removePlotAction.triggered.connect(self.removeDataPlot)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')         # add menu File
        fileMenu.addAction(selFileAction)            # link menu bar to openfile action with a menu item
        fileMenu.addAction(exitAction)               # add menu item exit

        plotMenu = menubar.addMenu("Plot")           # add menu Plot
        plotMenu.addAction(clearAction)               # add menu item of 'Clear' plot
        plotMenu.addAction(addPlotAction)             # add menu item of 'Add a Plot'
        plotMenu.addAction(removePlotAction)          # add menu item of 'Add a Plot'

        toolBar = self.addToolBar("Open")
        toolBar.addAction(selFileAction)             # link tool bar to openfile action

        # toolBar = self.addToolBar('Exit')
        # toolBar.addAction(selExitAction)  # link menu bar to openfile action

        # 设置dataPlot  class: PlotWidget
        self.dataPlot.plotItem.showGrid(True, True, 0.5)

        self.dataPlot.setAutoVisible(y=True)
        #self.dataPlot.plotItem.hideAxis("bottom")
        #self.dataPlot.plotItem.hideAxis("left")
        self.dataPlotRange.setMouseEnabled(x=False, y=False)  # dataPlotRange 不能移动
        self.dataPlotRange.plotItem.hideAxis('left')
        #self.dataPlotRange.plotItem.hideAxis('bottom')

        # 设置treeWidget的相关  class: QTreeWidget
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.showContextMenu)
        self.treeWidget.treeContextMenu = QMenu(self)
        self.actionA = self.treeWidget.treeContextMenu.addAction(u'Plot in plot1')


        self.actionA.triggered.connect(
            #lambda: self.chartPlot(self.treeWidget.currentItem(), self.treeWidget.selectedItems()))
            lambda: self.plotData(self.treeWidget.selectedItems(), 'plot1'))
        self.treeWidget.setColumnCount(4)
        self.treeWidget.setHeaderLabels(['#', 'Parameter', 'Parameter Name', 'Unit'])
        self.treeWidget.setColumnWidth(0, 10)
        self.treeWidget.setColumnWidth(1, 50)
        self.treeWidget.setColumnWidth(2, 100)

        #################### get the test data from the import window
        self.winImpData = clsImportData(self.dataparam, self.lTestDATA)     # instance of the ImportData window

        # layout
        self.L = pg.GraphicsLayout()
        self.dataPlot.setCentralWidget(self.L)

        # x axis for time
        xAxis = self.TimeAxisItem("bottom")

        #self.L.addItem(xAxis, row=2, col=6, rowspan=1, colspan=1)

        # plotitem and viewbox
        ## at least one plotitem is used whioch holds its own viewbox and left axis
        viewBox = self.dataPlot.plotItem.vb  # reference to viewbox of the plotitem

        # link x axis to view box
        xAxis.linkToView(viewBox)

        #  col 1 to 5 kept for y axis
        self.L.addItem(self.dataPlot.plotItem, row=1, col=6, rowspan=1, colspan=1)  # add plotitem to layout

        # # set the linear region
        self.lr = pg.LinearRegionItem(values=(0, 1))
        self.lr.setZValue(-10)
        self.dataPlotRange.addItem(self.lr)  # ignoreBounds=True
        self.lr.setRegion([0.4,0.6])
        #
        # self.lr.sigRegionChanged.connect(self.updatePlot)
        # viewBox.sigXRangeChanged.connect(self.updateRegion)

        self.dataPlot.plotItem.scene().sigMouseMoved.connect(self.mouseMove)
        #self.dataPlot.plotItem.scene().sigMouseClicked.connect(self.mouseClick)
        # self.region.setRegion()

        self.configPlotArea(self.dataPlot)





    def configPlotArea(self, plotWin):

        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        plotWin.addItem(self.vLine, ignoreBounds=True)
        plotWin.addItem(self.hLine, ignoreBounds=True)
        #self.dataPlotRange.addItem(self.region, ignoreBounds=True)






    def showContextMenu(self):
        self.treeWidget.treeContextMenu.move(QCursor.pos())
        self.treeWidget.treeContextMenu.show()

    def updateViews(self):
        pass
        # for i in range(0, len(self.chartVBs)):
        #viewbox = self.dataPlot.plotItem.vb
        #viewbox.setGeometry(viewbox.sceneBoundingRect())
        #viewbox.linkedViewChanged(viewbox, self.chartVBs[i].XAxis)

    def updatePlot(self):
        #self.dataPlot.setXRange(*self.lr.getRegion(), padding=0)
        if self.bPlotted:
            [x1, x2] = self.lr.getRegion()
            # try:
            #     xmin = self.rgnXmin + x1 * self.rgnXfactor
            #     xmax = self.rgnXmin + x2 * self.rgnXfactor
            # except Exception as e:
            #     xmin = x1
            #     xmax = x2
            #self.dataPlot.setXRange(x1, x2 )
            # (self.rgnXmin + self.rgnXfactor * len(iTime))(self.rgnXmin + self.rgnXfactor * len(iTime))

    def updateRegion(self):
        if self.bPlotted:
            #self.lr.setRegion([x for x in self.dataPlot.getViewBox().viewRange()[0]])
            pass

    def updatePlots(self):
        # for i in range(0, len(self.chartVBs)):
        #     self.chartVBs[i].setGeometry(self.chartPlotItems[0].vb.sceneBoundingRect())
        #     self.chartVBs[i].linkedViewChanged(self.chartPlotItems[0].vb, self.chartVBs[i].XAxis)
        for i in range(self.dataPlotLayout.count()):
            plotItem = self.dataPlotLayout.itemAt(i).widget()

            #plotItem.getViewBox().setGeometry(plotItem.getViewBox().sceneBoundingRect())
            #plotItem.getViewBox().linkedViewChanged(plotItem.getViewBox(), plotItem.getViewBox().XAxis)
            pass



    def mouseClick(self, evnt):

        pass


    def clearPlotArea(self):
        self.dataPlot.plotItem.clear()
        self.dataPlotRange.plotItem.clear()
        self.bPlotted = False
        self.configPlotArea(self.dataPlot)

        # re-setup the linear region of data plot range
        # set the linear region
        self.lr = pg.LinearRegionItem(values=(0, 1))
        self.lr.setZValue(-10)
        self.dataPlotRange.addItem(self.lr)  # ignoreBounds=True
        self.lr.setRegion([0.4,0.6])
        viewBox = self.dataPlot.plotItem.vb  # reference to viewbox of the plotitem
        #self.lr.sigRegionChanged.connect(self.updatePlot)
        #viewBox.sigXRangeChanged.connect(self.updateRegion)

    def addDataPlot(self):
        plotname = 'plot' + str(len(self.lPlotWindows) + 1)
        axis = self.TimeAxisItem(orientation='bottom')
        vb = pg.ViewBox()
        newdataPlot = pg.PlotWidget(self, viewBox=vb, axisItems={'bottom': axis}, name = plotname)
        self.dataPlotLayout.addWidget(newdataPlot)
        self.configPlotArea(newdataPlot)

        #vb.enableAutoRange()

        newdataPlot.plotItem.showGrid(True, True, 0.5)

        vb.scaleBy(y=None)


        # link x axis to view box of the first data plot
        viewBox = self.dataPlot.plotItem.vb  # reference to viewbox of the plot 1
        axis.linkToView(viewBox)
        #axis.linkToView(vb)

        # Link plot 1 X axia to the view box
        lastplotItem = self.dataPlotLayout.itemAt(self.dataPlotLayout.count()-2).widget()
        lastplotItem.getViewBox().setXLink(newdataPlot)


        self.lPlotWindows.append( plotname )

        #viewBox.sigResized.connect(self.updatePlots())

        newAction = self.treeWidget.treeContextMenu.addAction(u'Plot in ' + plotname)
        newAction.triggered.connect(
            lambda: self.plotData(self.treeWidget.selectedItems(), plotname))

    def removeDataPlot(self):
        pass


    def plotData(self, selectedItems, plotname):
        '''selectedItems: items selected in tree view
           dfData: data frame of the selected data
        '''

        #P = self.dataPlotLayout.tr(plotname)

        for i in range(self.dataPlotLayout.count()):
            plotItem = self.dataPlotLayout.itemAt(i).widget()
            if plotname == 'plot'+ str(i+1):
                break


        #plotItem = self.dataPlot.plotItem



        viewbox = pg.ViewBox()
        plotItem.scene().addItem(viewbox)

        #plotItem.getAxis('bottom').setPen(pg.mkPen(color='#000000', width=1))
        i = 0
        for iItem in selectedItems:
            if iItem.parent():     # not the root item
                filename = iItem.parent().text(1)    # get the parent item name - filename

                for iData in self.lTestDATA:          # find out the data from the data frame list by the filename
                    if filename == iData.fileName:
                        dfData = iData.data
                        break                       # break out of the loop for data


                data_head = iItem.text(1)           # get the column name of data for plotting
                # y axis
                data_2_plot = list(dfData[data_head])

                # get the list of time column, for x axis
                sTime = list(dfData['TIME'])

                # convert the time in string to date time object
                iTime = [self.sTimeToDateTime(j) for j in sTime]

                #plotItem.hideAxis("bottom")

                i += 1  # for color index use

                # example
                # pw.plot(x=[x.timestamp() for x in iTime ], y= list(df['BCVIIN']), pen = 'r')
                plotcurve = pg.PlotCurveItem(x=[x.timestamp() for x in iTime], y= data_2_plot, pen=self.colorDex[i%5])
                plotItem.addItem(plotcurve)

                if not self.bPlotted:
                    #viewbox.setXLink(plotcurve)

                    self.dataInRange_x = iTime
                    self.dataInRange_y = data_2_plot

                    self.rgnXmin = int(iTime[0].timestamp())   # for use of region widget, the convert factor for x axis
                    self.rgnXmax = int(iTime[-1].timestamp())
                    self.rgnXfactor = (self.rgnXmax-self.rgnXmin) / len(iTime)

                    self.dataPlotRange.plot(y=self.dataInRange_y)

                    [x1, x2] = self.lr.getRegion()
                    x1 *= len(iTime)
                    x2 *= len(iTime)
                    xmin = int(self.rgnXmin + x1 * self.rgnXfactor)
                    xmax = int(self.rgnXmin + x2 * self.rgnXfactor)
                    self.dataPlot.setXRange(self.rgnXmin, self.rgnXmax)
                    #self.dataPlotRange.setZValue(1)
                    self.lr.setRegion([xmin, xmax])

                    #self.lr.sigRegionChanged.connect(self.updatePlot)
                    #self.dataPlot.plotItem.vb.sigXRangeChanged.connect(self.updateRegion)





                self.bPlotted = True
                self.lPlottedItems.append({'filename': filename, 'Column': data_head})
                self.listWidget.addItem(data_head + ' || ' + filename)

                self.updatePlots()






           # # self.chartPlotItems[0].layout.clear()
            #
            # self.chartPlotItems[0].layout.addItem(ax_temp, 2, j)
            # self.chartPlotItems[0].scene().addItem(temp_vb)
            # ax_temp.linkToView(temp_vb)
            # temp_vb.setXLink(self.chartPlotItems[0])
            # ax_temp.setLabel('axial ' + str(j), color=self.colorDex[i])


    #     #self.updateViews()

    #     pen1 = pg.mkPen(color='b')
    #     pen2 = pg.mkPen(color='r')
    #


    def mouseMove(self, evt):

        if self.bPlotted:
            pos = evt  # [0]  ## using signal proxy turns original arguments into a tudfDataple
            # print(evt)
            dfData=self.lTestDATA[0].data
            startTime = datetime.strptime('2018 '+ dfData['TIME'].iloc[0], '%Y %H:%M:%S:%f').timestamp()
            endTime =  datetime.strptime('2018 '+ dfData['TIME'].iloc[-1], '%Y %H:%M:%S:%f').timestamp()
            if self.dataPlot.plotItem.sceneBoundingRect().contains(pos):
                print('item pos x: %0.1f + y: %0.1f' %(pos.x(), pos.y()) )
                mousePoint = self.dataPlot.plotItem.vb.mapSceneToView(pos)
                print('view pos x: %0.1f + y: %0.1f' %(mousePoint.x(), mousePoint.y()))
                x = int(mousePoint.x())

                timeIndex = datetime.fromtimestamp(x).strftime('%H:%M:%S')  # convert x coord from timestamp to time string
                #print('if3')
                if x >   startTime and x < endTime:
                    # print('if4')
                    # print(index)
                    # print(mousePoint.x())
                    # print(self.dataSummary[self.item_Selected][index])
                    #self.label.setText("X = %0.1f; Y = %0.1f " %(mousePoint.x(), mousePoint.y())) #"<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'> Y1=%0.1f</span> " % (mousePoint.x(), float(dfData[index])))
                    self.label.setText("<span style='font-size: 12pt'>Time=%s,   <span style='color: red'> Y1=%0.1f</span> " % (timeIndex, mousePoint.y()))

                self.vLine.setPos(mousePoint.x())
                self.hLine.setPos(mousePoint.y())



    def openFile(self):

         self.winImpData.exec_()  # Run the imp data window in modal

         self.treeUpdate()

    def exitAPP(self):
        choice = QtGui.QMessageBox.question(self, 'Exit', "Close the application?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def treeUpdate(self):
        QTreeWidget.clear(self.treeWidget)
        for tdataset in self.lTestDATA:
            fname = tdataset.fileName           #os.path.basename(self.winImpData.sDataFilePath)

            treeRoot = QTreeWidgetItem(self.treeWidget)
            treeRoot.setText(1, fname)

            self.treeItem = tdataset.header  # list(self.winImpData.dfData)
            self.numTree = tdataset.column     #self.treeItem.__len__()

            for i in range(1, len(self.treeItem)):
                child = QTreeWidgetItem(treeRoot)
                child.setText(0, str(i))
                child.setText(1, self.treeItem[i])
                child.setText(2, self.dataparam.getParamInfo(self.treeItem[i],'paramDesc'))
                child.setText(3, self.dataparam.getParamInfo(self.treeItem[i],'unit'))



    class TimeAxisItem(pg.AxisItem): #### class TimeAxisItem is used for overloading x axis as time
        def tickStrings(self, values, scale, spacing):
            strns = []
            #rng = max(values) - min(values)    # values are timestamp of date
            #946656000 = datetime.strptime('2000', '%Y').timestamp() ,  handel dates after 2000 only
            # if min(values) < 946656000:  # Windows can't handle dates before 1970,
            #     # 1514764800.0 = datetime.datetime.strptime('2018-1-1 8:00:0', '%Y-%m-%d %H:%M:%S').timestamp()
            #     # 1514766600.0 = datetime.datetime.strptime('2018-1-1 8:30:0', '%Y-%m-%d %H:%M:%S').timestamp()
            #     #defaultValues = range(1514736000.0, 1514768400.0, 720)
            #
            #     return pg.AxisItem.tickStrings(self, values, scale, spacing)

            for x in values:
                try:
                    if x < 946656000: x += 946656000     ## handle time starting from 1/1/2000
                    strns.append(datetime.fromtimestamp(x).strftime('%H:%M:%S'))
                except ValueError:  ## Windows can't handle dates before 1970
                    strns.append('')

            return strns

            # show hour:minute:second on the x axis
            #return [datetime.fromtimestamp(value).strftime('%H:%M:%S') for value in values]
                # 946656000 = datetime.strptime('2000', '%Y').timestamp()


    def sTimeToDateTime(self, inTime):  # convert time from string to datetime object
        # inTime: '13:43:02:578' string type
        # outTime: 2018-01-01 13:43:02.578000  datetime object

        # '2018 ' + startTime, '%Y %H:%M:%S'
        #itime = inTime[:8] + "." + inTime[10:12]   # convert 13:43:02:578 to 13:43:02.578
        # add date (2018-01-01)to the TIME for the sake of format of datetime class. could use real date of the data created

        return datetime.strptime('2018 ' + inTime, '%Y %H:%M:%S:%f')  # convert the time from string to the datetime format


class dataParam:
    def __init__(self, paramFile = os.getcwd() + '\\parameters code.csv'):
        self.paramFile = paramFile #r'C:\onedrive\OneDrive - Honeywell\VPD\parameters code.csv'
        self.columName = ['param', 'paramDesc', 'paramDescChs', 'unit', 'unitM', 'unitChs', 'rate']
        self.paramDF = pd.read_csv(self.paramFile, names=self.columName, index_col=0, header=0)


    def getParamName(self):
        return list(self.paramDF.index)

    def getParamInfo(self, paramName, colName):
        # paramName: parameter name
        # colName: column name - 'param', 'paramDesc', 'paramDescChs', 'unit', 'unitM', 'unitChs', 'rate'
        #x = paramDF.loc[paramName, columName]
        # TODO add an error trap for non exisint param name, return ""
        if paramName in list(self.paramDF.index):
            return self.paramDF.loc[paramName, colName]
        else:
            return ''


