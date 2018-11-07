from PyQt5.QtWidgets import QMainWindow, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QMenu, Qt, QAction, QCursor, QMessageBox
from PyQt5.QtCore import QEvent, pyqtSignal

#import pyqtgraph as pg
from pyqtgraph import setConfigOption, PlotWidget, InfiniteLine, TextItem, graphicsItems, ViewBox, PlotCurveItem, AxisItem
from pandas import DataFrame, read_csv

import sys
from os import path
from datetime import datetime


from mainUI import Ui_MainWindow
from clsDataImport import clsImportData



class clsDataView(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # 类成员变量初始化
        self.colorDex = ['#7CFC00', '#B22222', '#E0FFFF', '#FFFF00', '#66FF00']

        self.lPlottedItems = []         # list of plotItems in the dataplot area
        self.currentPlotWin = ''        # keep current selected plot window for next curve plotting
        self.curLabelofYvalue = None          # the label of Y value in current plot area
        self.lPlotWindows = ['Plot1']            # list of plot window
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

        self.minTimestamp = 1514764800.0      # the minimum of 20180101 08:00:00, ie. 1514764800.0 = datetime.datetime.strptime('2018-1-1 8:00:0', '%Y-%m-%d %H:%M:%S').timestamp()
        self.maxTimestamp = 1514800800.0 # datetime.strptime('2018-1-1 18:00:0', '%Y-%m-%d %H:%M:%S').timestamp()
        self.minYvalue = -20000
        self.maxYvalue = 20000

            # r'C:\onedrive\OneDrive - Honeywell\VPD\parameters code.csv'
        self.dataparam = dataParam(self.resource_path('parameters_code.csv'))   # data parameter definition
        #self.dataparam = dateParam()
        paramlist = self.dataparam.getParamName()
        #self.dataparam.getParamInfo('ABCVIINR', 'paramDesc')
        #self.dfData = pd.DataFrame()    # pandas dataframes to be plot

        # pyqtGraph 相关设置，必须要在self.setupUi之前
        setConfigOption('background', 'w')  # before loading widget

        # # set the time axis of X
        ### TODO: need to comment the self.dataplot line in the mainUI.py if it is recreated
        ###        or there is a error the plot widget being with no name of Plot1
        xAxis = self.TimeAxisItem(orientation='bottom')
        self.dataPlot = PlotWidget(self, axisItems={'bottom': xAxis}, name='Plot1')  ### TODO: need to comment the self.dataplot line in the mainUI.py if it is recreated

        self.setupUi(self)
        self.initUI()


        self.show()
        #self.showMaximized()   # max the window


    def initUI(self):

        # 添加打开菜单
        selFileAction = QAction('&Open', self)  # QAction(QIcon('open.png'), '&Open', self)
        selFileAction.setShortcut('Ctrl+O')
        selFileAction.setStatusTip('Open new File')
        selFileAction.triggered.connect(self.openFile)     # open data file
        selFileAction.setIcon(QIcon(self.resource_path('import.png')))

        exitAction = QAction('&Exit', self)    #QtGui.QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit the application')
        #exitAction.triggered.connect(QtGui.qApp.quit)
        exitAction.triggered.connect(self.exitAPP)     # exit the application
        exitAction.setIcon(QIcon(self.resource_path('exit.png')))

        clearAction = QAction('Clear', self)   # QtGui.QAction(QIcon('Clear.png'), 'Clear', self)
        clearAction.triggered.connect(self.clearPlotArea)
        clearAction.setIcon(QIcon(self.resource_path('clear.png')))

        addPlotAction = QAction( 'Add a Plot', self)  #QtGui.QAction(QIcon('Addplot.png'), 'Add a Plot', self)
        addPlotAction.triggered.connect(self.addPlotAera)
        addPlotAction.setIcon(QIcon(self.resource_path('addplot.png')))

        removePlotAction = QAction('Remove the Plot', self) # QtGui.QAction(QIcon('Addplot.png'), 'Remove a Plot', self)
        removePlotAction.triggered.connect(self.removeDataPlotWin)
        removePlotAction.setIcon(QIcon(self.resource_path('remvplot.png')))

        viewAllAction = QAction("View All", self)
        viewAllAction.triggered.connect(self.autoRangeAllWins)
        viewAllAction.setIcon(QIcon(self.resource_path('viewall.png')))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')         # add menu File
        fileMenu.addAction(selFileAction)            # link menu bar to openfile action with a menu item
        fileMenu.addAction(exitAction)               # add menu item exit

        plotMenu = menubar.addMenu("Plot")           # add menu Plot
        plotMenu.addAction(clearAction)               # add menu item of 'Clear' plot
        plotMenu.addAction(addPlotAction)             # add menu item of 'Add a Plot'
        plotMenu.addAction(removePlotAction)          # add menu item of 'Add a Plot'

        helpMenu = menubar.addMenu("Help")  # add menu help
        helpAction = QAction('?', helpMenu)
        helpAction.triggered.connect(self.helpme)
        helpMenu.addAction(helpAction)

        toolBar = self.addToolBar("Open")
        toolBar.addAction(selFileAction)             # link tool bar to openfile action

        toolBar.addAction(clearAction)
        toolBar.addAction(addPlotAction)
        toolBar.addAction(removePlotAction)
        toolBar.addAction(viewAllAction)




        # toolBar = self.addToolBar('Exit')
        # toolBar.addAction(selExitAction)  # link menu bar to openfile action

        # 设置dataPlot  class: PlotWidget
        self.dataPlot.plotItem.showGrid(True, True, 0.5)
        #self.dataPlot.plotItem.addLegend()

        self.dataPlot.setAutoVisible(y=True)


        # 设置treeWidget的相关  class: QTreeWidget
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.showContextMenu)
        self.treeWidget.treeContextMenu = QMenu(self)
        self.actionA = self.treeWidget.treeContextMenu.addAction(u'Plot')
        self.actionA.triggered.connect(
            lambda: self.plotData(self.currSelctPlotWgt, self.treeWidget.selectedItems()))
        self.treeWidget.setColumnCount(4)
        self.treeWidget.setHeaderLabels(['#', 'Parameter', 'Parameter Name', 'Unit'])
        self.treeWidget.setColumnWidth(0, 10)
        self.treeWidget.setColumnWidth(1, 50)
        self.treeWidget.setColumnWidth(2, 100)

        ### drag and drop
        self.treeWidget.setDragDropMode(self.treeWidget.DragOnly)


        # set up context menu of list widget
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.showListContextMenu)
        self.listWidget.listContextMenu = QMenu(self)
        self.actionB = self.listWidget.listContextMenu.addAction(u'Remove')
        self.actionB.triggered.connect(
            lambda: self.removeItemInPlot(self.listWidget.selectedItems()))


        #################### get the test data from the import window
        self.winImpData = clsImportData(self.dataparam, self.lTestDATA)     # instance of the ImportData window

        # # x axis for time
        # xAxis = self.TimeAxisItem("bottom")
        xAxis = self.dataPlot.plotItem.axes['bottom']['item']
        # plotitem and viewbox
        ## at least one plotitem is used whioch holds its own viewbox and left axis
        viewBox = self.dataPlot.plotItem.vb  # reference to viewbox of the plotitem
        viewBox.scaleBy(y=None)

        # # link x axis to view box
        xAxis.linkToView(viewBox)

        self.dataPlot.plotItem.scene().sigMouseMoved.connect(self.mouseMove)
        #self.dataPlot.plotItem.scene().sigMouseClicked.connect(self.mouseClick)

        # self.dataPlot.HoverEnterEvent = self.hoverEnterEvent

        ## drag and drop
        # self.dataPlot.dragEnterEvent = self.dragEnterEvent
        # self.dataPlot.plotItem.setAcceptDrops(True)
        # self.dataPlot.plotItem.dropEvent = self.dropEvent


        vLine = InfiniteLine(angle=90, movable=False, name='vline')
        hLine = InfiniteLine(angle=0, movable=False, name='hline')

        self.dataPlot.addItem(vLine, ignoreBounds=True)
        self.dataPlot.addItem(hLine, ignoreBounds=True)

        # set the default plot range
        self.dataPlot.setXRange(self.minTimestamp,self.maxTimestamp,padding=20)
        self.dataPlot.setYRange(-10, 10, padding=20)

        self.dataPlot.plotItem.getViewBox().setLimits()

        self.dataPlot.plotItem.getAxis('left').setWidth(w=30)
        self.dataPlot.plotItem.hideButtons()


        #self.dataPlot.plotItem.scene().sigMouseLeave.connect(self.mouseLeave) # ##TODO: cleaning house job
        self.dataPlot.installEventFilter(self)

        txtY_value = TextItem("", fill=(0, 0, 255, 80), anchor=(0,1),color='w')
        txtY_value.setParentItem(viewBox)

        self.curLabelofYvalue = txtY_value
        # #self.dataPlot.addItem(self.lableY_value)
        # labelY_value.setPos(self.minTimestamp,100.0)


        self.configPlotArea(self.dataPlot)

        # set current selection plot window background
        self.currSelctPlotWgt = self.dataPlot
        self.currSelctPlotWgt.setBackground(0.95)

    def eventFilter(self, source, event):
        #print (event.type())
        if event.type() == QEvent.Enter: #HoverEnter:
            #print("Enter " + source.plotItem.vb.name)
            self.currSelctPlotWgt.setBackground('default')
            self.currSelctPlotWgt = source
            self.currSelctPlotWgt.setBackground(0.95)
            plotAreaName = source.plotItem.vb.name
            #self.lPlottedItems.append({'Plot': plotWgtName, 'Curvename': curve_name, 'Filename': filename})

            labelofYvalueExisting = False
            plotAreaDirty = False
            for i in self.lPlottedItems:
                if i['Plot'] == plotAreaName:  # there is at least a curve in the plot
                    plotAreaDirty = True
                    break

            if plotAreaDirty:

                # get the lable of labelY_value
                for item in source.getViewBox().childItems():
                    if isinstance(item, graphicsItems.TextItem.TextItem):  # the text label is linked to the viewbox, not showing up
                        self.curLabelofYvalue = item
                        source.addItem(self.curLabelofYvalue)                 # add the text label to show it up
                        labelofYvalueExisting = True
                        break
                if not labelofYvalueExisting:
                    for item in source.plotItem.items:                      # the text label is in the plot item list
                        if isinstance(item, graphicsItems.TextItem.TextItem):
                            self.curLabelofYvalue = item
                            break


        if event.type() == QEvent.Leave: # and source is self.dataPlot:
            #print("Leave " + source.plotItem.vb.name)

            for item in source.plotItem.items:
                if isinstance(item, graphicsItems.TextItem.TextItem):
                    source.plotItem.removeItem(item)                    # remove the item
                    item.setParentItem(source.getViewBox())             # keep the link of the text label in the view box
                    break

            # move the hline to 0
            for iLine in source.items():  # loop for the hline
                if hasattr(iLine, 'name'):
                    if iLine.name() == 'hline':
                        iLine.setPos(self.minTimestamp)
                        break

        # print(event.type())
        # if event.type() == QEvent.GraphicsSceneDragEnter:
        #     self.currSelctPlotWgt.setBackground('default')
        #     self.currSelctPlotWgt = source
        #     self.currSelctPlotWgt.setBackground(0.95)

        return super(clsDataView,self).eventFilter(source,event)


    def configPlotArea(self, plotWin):

        vLine = InfiniteLine(angle=90, movable=False, name='vline')
        hLine = InfiniteLine(angle=0, movable=False, name='hline')
        plotWin.addItem(vLine, ignoreBounds=True)
        plotWin.addItem(hLine, ignoreBounds=True)
        #self.dataPlotRange.addItem(self.region, ignoreBounds=True)



    def showContextMenu(self):
        self.treeWidget.treeContextMenu.move(QCursor.pos())
        self.treeWidget.treeContextMenu.show()

    def dragEnterEvent(self, evt):
        evt.accept()

        # for i in range(self.dataPlotLayout.count()):
        #     plotAera = self.dataPlotLayout.itemAt(i).widget()
        #     print(plotAera.underMouse())
        #     if plotAera.underMouse():
        #         self.currSelctPlotWgt = plotAera
        #
        #         break

        # if self.currSelctPlotWgt.underMouse():

        # else:
        #     evt.ignore()

    def hoverEnterEvent(self,evet):
        pass

    def dropEvent(self, evt):
        #self.emit(mouseEnter event)
        #if self.currSelctPlotWgt.underMouse():
        for i in range(self.dataPlotLayout.count()):
            plotAera = self.dataPlotLayout.itemAt(i).widget()
            print(plotAera.plotItem.vb.name)
            print (plotAera.underMouse())
            if plotAera.underMouse():
                self.currSelctPlotWgt = plotAera
                self.plotData(plotAera, self.treeWidget.selectedItems())
                break

        self.plotData(self.currSelctPlotWgt, self.treeWidget.selectedItems())

    def showListContextMenu(self):
        self.listWidget.listContextMenu.move(QCursor.pos())
        self.listWidget.listContextMenu.show()


    def autoRangeAllWins(self):
        for i in range(self.dataPlotLayout.count()):
            plotItem = self.dataPlotLayout.itemAt(i).widget()

            plotItem.getViewBox().autoRange()

    def mouseClick(self, evnt):
        if self.currSelctPlotWgt:
            self.currSelctPlotWgt.setBackground('default')
            if evnt.currentItem is not None:
                try:
                    self.currSelctPlotWgt = evnt.currentItem._viewWidget()    # get the current selected widget
                    self.currSelctPlotWgt.setBackground(0.95)
                except Exception as e:
                    pass
                    #QMessageBox.critical(self, "Error", e.__str__())

    def clearPlotArea(self):
        #self.dataPlot.plotItem.clear()
        choice = QMessageBox.question(self, 'Plot1', "Remove all items in the first plot 1?",
                                            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:

            for item in self.dataPlot.items():
                self.dataPlot.removeItem(item)

            lstitems = self.listWidget.findItems('Plot1', Qt.MatchStartsWith)
            if len(lstitems) > 0:
                for iitem in lstitems:
                    self.listWidget.takeItem(self.listWidget.row(iitem))

            for item in self.currSelctPlotWgt.scene().items():
                if isinstance(item, graphicsItems.LegendItem.LegendItem):  #  remove items in the scene including the legend
                    self.currSelctPlotWgt.scene().removeItem(item)

            #self.dataPlotRange.plotItem.clear()
            self.bPlotted = False
            self.configPlotArea(self.dataPlot)


    def addPlotAera(self):
        plotname = 'Plot' + str(len(self.lPlotWindows) + 1)
        axis = self.TimeAxisItem(orientation='bottom')
        vb = ViewBox()
        newdataPlot = PlotWidget(self, viewBox=vb, axisItems={'bottom': axis}, name = plotname)
        self.dataPlotLayout.addWidget(newdataPlot)
        self.configPlotArea(newdataPlot)

        newdataPlot.plotItem.scene().sigMouseClicked.connect(self.mouseClick)
        newdataPlot.plotItem.scene().sigMouseMoved.connect(self.mouseMove)

        ## drag and drop
        # newdataPlot.dragEnterEvent = self.dragEnterEvent
        # newdataPlot.plotItem.setAcceptDrops(True)
        # newdataPlot.plotItem.dropEvent = self.dropEvent

        # set the default plot range
        newdataPlot.setXRange(self.minTimestamp,self.maxTimestamp,padding=20)
        newdataPlot.setYRange(-10, 10, padding=20)

        newdataPlot.plotItem.getAxis('left').setWidth(w=30)
        newdataPlot.plotItem.hideButtons()

        newdataPlot.installEventFilter(self)

        newdataPlot.plotItem.showGrid(True, True, 0.5)

        vb.scaleBy(y=None)

        # make it the current selection plot area
        self.currSelctPlotWgt.setBackground('default')
        self.currSelctPlotWgt = newdataPlot  # set the current selection to plot1
        self.currSelctPlotWgt.setBackground(0.95)

        # link x axis to view box of the first data plot
        viewBox = self.dataPlot.plotItem.vb  # reference to viewbox of the plot 1
        axis.linkToView(viewBox)
        #axis.linkToView(vb)

        # Link plot 1 X axia to the view box
        lastplotItem = self.dataPlotLayout.itemAt(self.dataPlotLayout.count()-2).widget()
        lastplotItem.getViewBox().setXLink(newdataPlot)
        #lastplotItem.getViewBox().autoRange()

        txtY_value = TextItem("", fill=(0, 0, 255, 80), anchor=(0, 1), color='w')
        txtY_value.setParentItem(newdataPlot.plotItem.getViewBox())

        self.autoRangeAllWins()
        self.lPlotWindows.append(plotname)


    def removeDataPlotWin(self):
        curreSelctPlotWgtName = self.currSelctPlotWgt.getViewBox().name
        if curreSelctPlotWgtName != 'Plot1' and curreSelctPlotWgtName in self.lPlotWindows:  # can't delete plot1
            choice = QMessageBox.question(self, curreSelctPlotWgtName, "Remove the selected plot window?",
                                                QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:

                for item in self.currSelctPlotWgt.items():   # delete the items of the plot
                    self.currSelctPlotWgt.removeItem(item)

                lstitems = self.listWidget.findItems(curreSelctPlotWgtName, Qt.MatchStartsWith)  # delete the list in the list widget
                if len(lstitems) > 0:
                    for iitem in lstitems:
                        self.listWidget.takeItem(self.listWidget.row(iitem))

                for item in self.currSelctPlotWgt.scene().items():  #  remove everything in the scene including the legend
                    self.currSelctPlotWgt.scene().removeItem(item)



                self.dataPlotLayout.removeWidget(self.currSelctPlotWgt)
                self.currSelctPlotWgt.deleteLater()    #setHidden(True)     # hide the selected widget, should be deleted, to be updated with delect command
                self.currSelctPlotWgt = None
                self.lPlotWindows.remove(curreSelctPlotWgtName)    # remove the plot name from list of plot windows

                self.currSelctPlotWgt = self.dataPlot   # set the current selection to plot1
                self.currSelctPlotWgt.setBackground(0.95)

    def plotData(self, plotItem, selectedItems):
        '''selectedItems: items selected in tree view
           dfData: data frame of the selected data
        '''

        #plotItem = self.dataPlot.plotItem

        # viewbox = pg.ViewBox()
        # plotItem.scene().addItem(viewbox)

        #plotItem = self.currSelctPlotWgt
        plotItem.addLegend()

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
                curve_name = data_head + '>>' + iItem.text(2) + '>>' + iItem.text(3)    # parameter/parameter desc/unit

                # y axis
                data_2_plot = list(dfData[data_head])

                # get the list of time column, for x axis
                sTime = list(dfData['TIME'])

                # convert the time in string to date time object
                iTime = [self.sTimeToDateTime(j) for j in sTime]

                i += 1  # for color index use

                # example
                # pw.plot(x=[x.timestamp() for x in iTime ], y= list(df['BCVIIN']), pen = 'r')
                try:
                    plotcurve = PlotCurveItem(x=[x.timestamp() for x in iTime], y= data_2_plot, name = curve_name, pen=self.colorDex[i%5])
                    plotItem.addItem(plotcurve)
                except Exception as e:
                    QMessageBox.critical(self, "Error", "Error with data to plot.\n" + e.__str__())

                if not self.bPlotted:
                    self.bPlotted = True
                plotWgtName = self.currSelctPlotWgt.getViewBox().name
                if not plotWgtName: print("check the plotwidget definition in the mainUI.py, comment it!!!!")
                self.lPlottedItems.append({'Plot': plotWgtName, 'Curvename': curve_name, 'Filename': filename })
                self.listWidget.addItem(plotWgtName + '||' + curve_name + '||' + filename )

                # labl = QLabel(curve_name)
                # plotItem.addItem(labl)

                for lgditem in plotItem.scene().items():  # remove the legend
                    if isinstance(lgditem, graphicsItems.LegendItem.ItemSample):  #
                        lgditem.hide()   # hide the sample of legend  # plotItem.scene().items()[5].item is the curve itself
                        break

                self.autoRangeAllWins()


    def removeItemInPlot(self, selectedItem):
        try:
            if selectedItem[0]:
                [plotname,itemname,filename] = selectedItem[0].text().split('||')  #selectedItems()[0].text().split('||')

                for i in range(self.dataPlotLayout.count()):     # plot name = plot1 or plot2
                    plotWin = self.dataPlotLayout.itemAt(i).widget()
                    if plotname == plotWin.getViewBox().name:    # get the plot item
                        break

                for j in plotWin.plotItem.curves:    # get the curve item
                    curvename = j.name()
                    if curvename == itemname:
                        curveFound = True
                        break
                if curveFound:
                    plotWin.removeItem(j)               # delete the curve from the plot
                    #plotWin.scene().removeItem(plotWin.plotItem.legend)
                    for item in plotWin.scene().items():    # remove the legend
                        if isinstance(item, graphicsItems.LegendItem.LegendItem):      #isinstance(plotWin.scene().items()[6], pg.graphicsItems.LegendItem.LegendItem)
                            if item.items[0][1].text == curvename:                      # get the legend of the curve
                                plotWin.scene().removeItem(item)
                                break
                    self.listWidget.takeItem( self.listWidget.row(selectedItem[0]))    # remove the item from the list
                    for iPlottedItem in self.lPlottedItems:
                        if iPlottedItem['Filename'] == filename and iPlottedItem['Curvename'] == curvename:
                            self.lPlottedItems.remove(iPlottedItem)
                            break

                self.autoRangeAllWins()

        except Exception as e:
            print(e.__str__())



    def mouseMove(self, evt):
        #evtsender = self.sender()
        try:
            pos = evt  # get the point of mouse
            y_value = {}    # to keep the y values of all curves

        except Exception as e:
            print('exception @ mousemove 1' + e.__str__())

        if self.bPlotted:
            try:
                mousePoint = self.currSelctPlotWgt.plotItem.vb.mapSceneToView(pos)  # map the mouse position to the view position
                # mpOffset = plotWin.plotItem.vb.mapSceneToView(QPointF(0.0, 0.0))   # offset the mouse point
                x = self.minTimestamp
                timeIndex = datetime.fromtimestamp(x).strftime('%H:%M:%S:%f')[:12]
                if mousePoint.x() < self.minTimestamp - 3600 or mousePoint.x() > self.maxTimestamp + 2 * 3600:
                    #self.curLabelofYvalue.setPos(self.minTimestamp, mousePoint.y())
                    self.currSelctPlotWgt.plotItem.removeItem(self.curLabelofYvalue)  # remove the item
                    self.curLabelofYvalue.setParentItem(self.currSelctPlotWgt.getViewBox())
                    self.currSelctPlotWgt.plotItem.vb.autoRange()
                    return
                if mousePoint.y() < self.minYvalue or mousePoint.y() > self.maxYval:
                    #self.curLabelofYvalue.setPos(mousePoint.x(), self.minYvalue)
                    self.currSelctPlotWgt.plotItem.removeItem(self.curLabelofYvalue)  # remove the item
                    self.curLabelofYvalue.setParentItem(self.currSelctPlotWgt.getViewBox())
                    self.currSelctPlotWgt.plotItem.vb.autoRange()
                    #self.currSelctPlotWgt.scale(1,1,[{self.minTimestamp,self.minYvalue}])
                    return
            except Exception as e:
                pass

            try:
                #currentPlotArea = self.currSelctPlotWgt
                # move the vline in all plot area
                for i in range(self.dataPlotLayout.count()):  # loop for each plot area
                    plotWin = self.dataPlotLayout.itemAt(i).widget()
                    if plotWin.plotItem.sceneBoundingRect().contains(pos):  # mouse point in the plot aera
                        #print('Plot name: %s' % plotWin.getViewBox().name)
                        #print('view pos x: %0.1f + y: %0.1f' % (mousePoint.x(), mousePoint.y()))
                        # map the mouse position to the view position
                        mousePoint = plotWin.plotItem.vb.mapSceneToView(pos)
                        x = mousePoint.x()
                        # convert x coord from timestamp to time string
                        timeIndex = datetime.fromtimestamp(x).strftime('%H:%M:%S:%f')[:12]
                        #print('time: %s' % timeIndex)


                        for iLine in plotWin.items():  # loop for the vline
                            if hasattr(iLine, 'name'):
                                if iLine.name() == 'vline':
                                    iLine.setPos(mousePoint.x())
                                    break


                        #if plotWin.underMouse():  # check if the mouse is on the widget, True: current plot the mouse is in
                            #currentPlotArea = plotWin

                # move both hline in current plot area
                for iLine in self.currSelctPlotWgt.items():  # loop for the vline and hline
                    mousePoint = self.currSelctPlotWgt.plotItem.vb.mapSceneToView(pos)
                    if hasattr(iLine, 'name'):
                        if iLine.name() == 'hline':
                            iLine.setPos(mousePoint.y())
                            break

            except Exception as e:
                print('exception @ mousemove 2' + e.__str__())

            # get the y value of all plotted curves
            try:
                if self.lPlottedItems.__len__() > 0:
                    curr_Y = [round(mousePoint.y(),2)]
                    for iCurve in self.lPlottedItems:
                        plotname = iCurve['Plot']
                        filename = iCurve["Filename"]
                        curvename = iCurve["Curvename"].split('>>')[0]

                        for dataset in self.lTestDATA:
                            dfData = dataset.data
                            startTime = datetime.strptime('2018 ' + dfData['TIME'].iloc[0],
                                                          '%Y %H:%M:%S:%f').timestamp()
                            endTime = datetime.strptime('2018 ' + dfData['TIME'].iloc[-1],
                                                        '%Y %H:%M:%S:%f').timestamp()
                            rate = dataset.rate

                            if x > startTime and x < endTime:
                                row = round((x - startTime) * rate)  # the the row number
                                #print('row number: %d' % row)
                                y = dfData[curvename].iloc[row]  # dfData[curvename].iloc()[row]
                                #print('y: %f' % y)
                                y_value[curvename] = y  # keep the curve value in y to the list

                                if self.currSelctPlotWgt.getViewBox().name == plotname:  # the data set of current plot area
                                    curr_Y.append(round(y,2))

            except Exception as e:
                print('exception @ mousemove 3' + e.__str__())

            # display the y value of all curves
            try:
                self.labelTime.setText("<span style='font-size: 11pt'>Time=%s" % (timeIndex))

                if y_value:
                    # show the values of all curves shown in plots
                    self.labelValueY.setText("<span style='font-size: 11pt; color: red'>" + str(
                        ["%s=%0.1f" % (k, v) for k, v in y_value.items()]))
            except Exception as e:
                print('exception @ mousemove 4' + e.__str__())

            # show the label in current plot area

            try:
                if curr_Y.__len__() > 0:
                    # labelY_value = pg.TextItem("v")
                    # currentPlotArea.addItem(labelY_value)
                    # currentPlotArea.setPos(mousePoint.x(), mousePoint.y())
                    self.curLabelofYvalue.setText((''.join(str(e) + '\n' for e in curr_Y))[:-1])   # [:-1] to remove the last '\n'
                    self.curLabelofYvalue.setPos(mousePoint.x(), mousePoint.y())
                    #print(self.curLabelofYvalue.__str__)
                    #self.dataPlot.addItem(labelY_value)
            except Exception as e:
                print('exception @ mousemove 5' + e.__str__())



    def openFile(self):
        self.winImpData.exec_()  # Run the imp data window in modal
        self.treeUpdate()

    def exitAPP(self):
        choice = QMessageBox.question(self, 'Exit', "Close the application?",
                                           QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def treeUpdate(self):
        QTreeWidget.clear(self.treeWidget)
        for tdataset in self.lTestDATA:
            fname = tdataset.fileName           #os.path.basename(self.winImpData.sDataFilePath)
            rate = tdataset.rate

            treeRoot = QTreeWidgetItem(self.treeWidget)
            treeRoot.setText(1, fname)
            treeRoot.setText(2, str(rate) + 'Hz')

            self.treeItem = tdataset.header  # list(self.winImpData.dfData)
            self.numTree = tdataset.column     #self.treeItem.__len__()

            for i in range(1, len(self.treeItem)):
                child = QTreeWidgetItem(treeRoot)
                child.setText(0, str(i))
                child.setText(1, self.treeItem[i])
                child.setText(2, self.dataparam.getParamInfo(self.treeItem[i],'paramDesc'))
                child.setText(3, self.dataparam.getParamInfo(self.treeItem[i],'unit'))

    def helpme(self):
        QMessageBox.information(self,'Wheel & Brake Test Data Explorer', 'Technical support:\nHON MS&C Shanghai.')

    ### for PyInataller use to bundle data file into one file
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if hasattr(sys, '_MEIPASS'):
            return path.join(sys._MEIPASS, relative_path)
        return path.join(path.abspath("."), relative_path)
        # base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        # return os.path.join(base_path, relative_path)


    class TimeAxisItem(AxisItem): #### class TimeAxisItem is used for overloading x axis as time
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
        try:
            outTime = datetime.strptime('2018 ' + inTime, '%Y %H:%M:%S:%f')  # convert the time from string to the datetime format
        except Exception as e:
            QMessageBox.critical(self, "Error", "TIME format error.\n" + e.__str__())
            outTime = datetime.now()
        return outTime

class dataParam:
    def __init__(self, paramFile):   # os.getcwd() + \\parameters_code.csv
        self.paramFile = paramFile #the path to the parameter file: r'C:\onedrive\OneDrive - Honeywell\VPD\parameters code.csv'
        self.columName = ['param', 'paramDesc', 'paramDescChs', 'unit', 'unitM', 'unitChs', 'rate']
        self.paramDF = DataFrame()
        try:
            self.paramDF = read_csv(self.paramFile, names=self.columName, index_col=0, header=0)
        except Exception as e:
            print("The file: '" + self.paramFile + "' not exists! Default column headers are used")
            pass
            #QMessageBox.critical(self. "Error", "Error in reading the parameter file.\n" + e.__str__())


    def getParamName(self):
        return list(self.paramDF.index)

    def getParamInfo(self, paramName, colName):
        # paramName: parameter name
        # colName: column name - 'param', 'paramDesc', 'paramDescChs', 'unit', 'unitM', 'unitChs', 'rate'
        #x = paramDF.loc[paramName, columName]
        # for non exisint param name, return ""
        if paramName in list(self.paramDF.index):
            return self.paramDF.loc[paramName, colName]
        else:
            return ''


