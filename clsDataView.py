from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QMenu, Qt, QAction, QCursor, QApplication

import pyqtgraph
import pandas as pd

import sys
import os
from datetime import datetime

from mainUI import Ui_MainWindow
from clsDataImport import clsImportData



class clsDataView(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # 类成员变量初始化
        self.colorDex = ['#7CFC00', '#B22222', '#E0FFFF', '#FFFF00', '#66FF00']

        self.chartPlotItem = []         # chart of plot
        self.chartVBs = []              # Chart of View box, in graphiclayout
        self.chartAxials = []           # chart of axial?
        self.chartCurve = []            # chart of Curve?
        self.shortfname = ''           # data file name without path

        self.lTestDATA = []      # the test data to be reviewed, each item is a class of data structure
                                    #  [testData1, testData2 ...]
                                    #  [(filename, column name, dataframe of data)
        self.parColPlotted = []           # parameter column in plotting

            # r'C:\onedrive\OneDrive - Honeywell\VPD\parameters code.csv'
        self.dataparam = dataParam()   # data parameter definition
        #self.dataparam = dateParam()
        paramlist = self.dataparam.getParamName()
        self.dataparam.getParamInfo('ABCVIINR', 'paramDesc')
        #self.dfData = pd.DataFrame()    # pandas dataframes to be plot

        # pyqtGraph 相关设置，必须要在self.setupUi之前
        pyqtgraph.setConfigOption('background', 'w')  # before loading widget


        self.setupUi(self)
        self.initUI()


        self.show()
        #self.showMaximized()





    def initUI(self):
        # 添加打开菜单
        selFileAction = QAction(QIcon('open.png'), 'Open', self)
        selFileAction.setShortcut('Ctrl+O')
        selFileAction.setStatusTip('Open new File')
        selFileAction.triggered.connect(self.openFile)     # open data file
        selFileAction.setIcon(QIcon('import.ico'))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(selFileAction)            # link menu bar to openfile action

        toolBar = self.addToolBar("File")
        toolBar.addAction(selFileAction)             # link tool bar to openfile action

        # 设置dataPlot  class: PlotWidget
        self.dataPlot.plotItem.showGrid(True, True, 0.5)
        self.dataPlotRange.setMouseEnabled(x=False, y=False)  # dataPlotRange 不能移动
        self.dataPlot.setAutoVisible(y=True)

        # 设置treeWidget的相关  class: QTreeWidget
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.showContextMenu)
        self.treeWidget.treeContextMenu = QMenu(self)
        self.actionA = self.treeWidget.treeContextMenu.addAction(u'Plot')
        self.actionA.triggered.connect(
            #lambda: self.chartPlot(self.treeWidget.currentItem(), self.treeWidget.selectedItems()))
            lambda: self.plotData(self.treeWidget.selectedItems()))
        self.treeWidget.setColumnCount(4)
        self.treeWidget.setHeaderLabels(['#', 'Parameter', 'Parameter Name', 'Unit'])
        self.treeWidget.setColumnWidth(0, 10)
        self.treeWidget.setColumnWidth(1, 70)
        self.treeWidget.setColumnWidth(2, 150)

        #################### get the test data from the import window
        self.winImpData = clsImportData(self.dataparam, self.lTestDATA)     # instance of the ImportData window





        # layout
        self.L = pyqtgraph.GraphicsLayout()
        self.dataPlot.setCentralWidget(self.L)

        # x axis for time
        xAxis = self.TimeAxisItem("bottom")

        self.L.addItem(xAxis, row=2, col=6, rowspan=1, colspan=1)

        # plotitem and viewbox
        ## at least one plotitem is used whioch holds its own viewbox and left axis
        viewbox = self.dataPlot.plotItem.vb  # reference to viewbox of the plotitem

        # link x axis to view box
        xAxis.linkToView(viewbox)

        #  col 1 to 5 kept for y axis
        self.L.addItem(self.dataPlot.plotItem, row=1, col=6, rowspan=1, colspan=1)  # add plotitem to layout
        self.dataPlot.plotItem.hideAxis("bottom")
        #self.dataPlot.plotItem.hideAxis("left")


    def showContextMenu(self):
        self.treeWidget.treeContextMenu.move(QCursor.pos())
        self.treeWidget.treeContextMenu.show()

    def updateViews(self):
        pass
        # for i in range(0, len(self.chartVBs)):
        #     self.chartVBs[i].setGeometry(self.chartPlotItems[0].vb.sceneBoundingRect())
        #     self.chartVBs[i].linkedViewChanged(self.chartPlotItems[0].vb, self.chartVBs[i].XAxis)

    def plotData(self, selectedItems):
        '''selectedItems: items selected in tree view
           dfData: data frame of the selected data
        '''

        #dfData = self.winImpData.dfData

        plotItem = self.dataPlot.plotItem
        #viewbox =  pyqtgraph.ViewBox()
        plotItem.getAxis('bottom').setPen(pyqtgraph.mkPen(color='#000000', width=1))
        i = 0
        for iItem in selectedItems:
            filename = iItem.parent().text(1)    # get the parent item name
            for iData in self.lTestDATA:
                if filename == iData.getFileName():
                    dfData = iData.dfTestData
                    break

            i += 1
            data_head = iItem.text(1)
            # y axis
            data_2_plot = list(dfData[data_head])

            # get the list of time column
            sTime = list(dfData['TIME'])

            # convert the time in string to date time object
            iTime = [self.sTimeToDateTime(j) for j in sTime]

            #pen1 = pyqtgraph.mkPen(color='b')  # , width=2)

            # Axis
            #a2 = pyqtgraph.AxisItem("left")
            #a3 = pyqtgraph.AxisItem("left")
            #a4 = pyqtgraph.AxisItem("left")
            #a5 = pyqtgraph.AxisItem("left")
            #a6 = pyqtgraph.AxisItem("left")

            #xAxis = self.TimeAxisItem("bottom")

            # ViewBoxes
            #v2 = pyqtgraph.ViewBox()
            # v3 = pyqtgraph.ViewBox()
            # v4 = pyqtgraph.ViewBox()
            # v5 = pyqtgraph.ViewBox()
            # v6 = pyqtgraph.ViewBox()


            # # layout
            # L = pyqtgraph.GraphicsLayout()
            # self.dataPlot.setCentralWidget(L)

            # add axis to layout
            ## watch the col parameter here for the position
            #L.addItem(a2, row=2, col=5, rowspan=1, colspan=1)
            # L.addItem(a3, row=2, col=4, rowspan=1, colspan=1)
            # L.addItem(a4, row=2, col=3, rowspan=1, colspan=1)
            # L.addItem(a5, row=2, col=2, rowspan=1, colspan=1)
            # L.addItem(a6, row=2, col=1, rowspan=1, colspan=1)
            #self.L.addItem(xAxis, row=2, col=6, rowspan=1, colspan=1)

            # plotitem and viewbox
            ## at least one plotitem is used whioch holds its own viewbox and left axis
            #v1 = plotItem.vb  # reference to viewbox of the plotitem
            #v1.addItem(xAxis)
            #self.L.addItem(plotItem, row=2, col=6, rowspan=1, colspan=1)  # add plotitem to layout

            # add viewboxes to layout
            #self.L.scene().addItem(v2)
            # L.scene().addItem(v3)
            # L.scene().addItem(v4)
            # L.scene().addItem(v5)
            # L.scene().addItem(v6)


            # link axis with viewboxes
            # xAxis.linkToView(v2)
            # a2.linkToView(v2)
            # a3.linkToView(v3)
            # a4.linkToView(v4)
            # a5.linkToView(v5)
            # a6.linkToView(v6)



            # link viewboxes
            # v2.setXLink(v1)
            # v3.setXLink(v2)
            # v4.setXLink(v3)
            # v5.setXLink(v4)
            # v6.setXLink(v5)

            # axes labels
            #plotItem.getAxis("left").setLabel('axis 1 in ViewBox of PlotItem', color='#FFFFFF')
            #a2.setLabel('axis 2 in Viewbox 2', color='#2E2EFE')
            # a3.setLabel('axis 3 in Viewbox 3', color='#2EFEF7')
            # a4.setLabel('axis 4 in Viewbox 4', color='#2EFE2E')
            # a5.setLabel('axis 5 in Viewbox 5', color='#FFFF00')
            # a6.setLabel('axis 6 in Viewbox 6', color='#FE2E64')
            #plotItem.getAxis("bottom").setLabel('Time', color='#FF0F0F')
            plotItem.hideAxis("bottom")

            # example
            # pw.plot(x=[x.timestamp() for x in iTime ], y= list(df['BCVIIN']), pen = 'r')
            plotcurve = pyqtgraph.PlotCurveItem(x=[x.timestamp() for x in iTime ], y= data_2_plot, pen=self.colorDex[i%5])
            plotItem.addItem(plotcurve)




            #
            # ax_temp = pyqtgraph.AxisItem('right')
            #
            # # self.chartPlotItems[0].layout.clear()
            #
            # self.chartPlotItems[0].layout.addItem(ax_temp, 2, j)
            # self.chartPlotItems[0].scene().addItem(temp_vb)
            # ax_temp.linkToView(temp_vb)
            # temp_vb.setXLink(self.chartPlotItems[0])
            # ax_temp.setLabel('axial ' + str(j), color=self.colorDex[i])
            # # print('4')
            # temp_2_plot = self.dataSummary[int(selectedItems[i].text(0))]
            # # print(temp_2_plot[:100])
            # temp_plotcurve = pyqtgraph.PlotCurveItem([float(x) for x in temp_2_plot], pen=self.colorDex[i])
            # temp_vb.addItem(temp_plotcurve)
            #
            # self.chartVBs.append(temp_vb)
            # self.chartAxials.append(ax_temp)
            # self.chartCurve.append(temp_plotcurve)
            # # print('5')
            #
            # j = j + 1


    # def chartPlot(self, currentItem, selectedItems):
    #
    #     if self.chartVBs:   # eixting chart viewbox
    #         for i in range(0, len(self.chartVBs)):
    #             print('remove VBs')
    #             self.chartPlotItems[0].scene().removeItem(self.chartVBs[i])
    #             self.chartPlotItems[0].scene().removeItem(self.chartAxials[i])
    #             self.chartPlotItems[0].scene().removeItem(self.chartCurve[i])
    #
    #     if self.chartPlotItems:
    #         print('remove plot item')
    #         self.dataPlot.removeItem(self.first_curve)
    #
    #     #self.updateViews()
    #
    #
    #     # reset the class member
    #     self.chartPlotItems = []
    #     self.chartVBs = []           #VB
    #     self.chartAxials = []
    #     self.chartCurve = []
    #
    #     # print(currentItem, selectedItems)
    #     if len(selectedItems) == 1:
    #         self.CI_Plot(currentItem)
    #     else:
    #         self.SI_Plot(currentItem, selectedItems)
    #
    #     ################
    #     self.item_Selected = int(self.treeWidget.currentItem().text(0))
    #
    #     pen1 = pyqtgraph.mkPen(color='b')
    #     pen2 = pyqtgraph.mkPen(color='r')
    #
    #     self.dataPlotRange.plot(range(self.dataSummary[self.item_Selected].__len__()),
    #                             [float(x) for x in self.dataSummary[self.item_Selected]], pen=pen2, clear=True)
    #     self.dataPlotRange.setZValue(1)
    #
    #     self.region = pyqtgraph.LinearRegionItem()
    #     self.region.setZValue(10)
    #     self.dataPlotRange.addItem(self.region, ignoreBounds=True)
    #
    #     self.region.setRegion([self.dataRow * 0.4, self.dataRow * 0.6])
    #
    #     self.region.sigRegionChanged.connect(self.regionUpdate)
    #     self.dataPlot.plotItem.vb.sigRangeChanged.connect(self.updateRegion)
    #     ################
    #     self.vLine = pyqtgraph.InfiniteLine(angle=90, movable=False)
    #     self.hLine = pyqtgraph.InfiniteLine(angle=0, movable=False)
    #     self.dataPlot.addItem(self.vLine, ignoreBounds=True)
    #     self.dataPlot.addItem(self.hLine, ignoreBounds=True)
    #     print('line done')
    #
    #     self.dataPlot.plotItem.scene().sigMouseMoved.connect(self.mouseMove)

    # def mouseMove(self, evt):
    #     # print('dong')
    #     pos = evt  # [0]  ## using signal proxy turns original arguments into a tuple
    #     # print(evt)
    #     if self.dataPlot.plotItem.sceneBoundingRect().contains(pos):
    #         print('if1')
    #         mousePoint = self.dataPlot.plotItem.vb.mapSceneToView(pos)
    #         print('if2')
    #         index = int(mousePoint.x())
    #         print('if3')
    #         if index > 0 and index < len(self.dataSummary[self.item_Selected]):
    #             # print('if4')
    #             # print(index)
    #             # print(mousePoint.x())
    #             # print(self.dataSummary[self.item_Selected][index])
    #             self.label.setText(
    #                 "<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'> Y1=%0.1f</span>," % (
    #                     mousePoint.x(), float(self.dataSummary[self.item_Selected][index])))
    #         self.vLine.setPos(mousePoint.x())
    #         self.hLine.setPos(mousePoint.y())

    # def regionUpdate(self):
    #     minX, maxX = self.region.getRegion()
    #     self.dataPlot.setXRange(minX, maxX, padding=0)
    #
    # def updateRegion(self, window, viewRange):
    #     # print(window)
    #     # print(viewRange)
    #     rgn = viewRange[0]
    #     self.region.setRegion(rgn)

    def openFile(self):

         self.winImpData.exec_()  # Run the imp data window in modal

        #fname = 'C:\\onedrive\\OneDrive - Honeywell\\VPD\\test data\\32Hz-429-100kn.txt'

         self.treeUpdate()




    def loadData1(self,fname):  #data in a 2-dim array   not used
        f1 = open(fname, 'r')
        first_line = f1.readline().strip('\n')
        self.treeItem = first_line.split()
        self.dataSummary = [[] for col in range(self.treeItem.__len__())]
        self.numTree = self.treeItem.__len__()

        line = f1.readline().strip('\n')
        while line:
            temp_line = line.split()
            for i in range(0, len(temp_line), 1):
                self.dataSummary[i].append(temp_line[i])
            line = f1.readline().strip('\n')

        self.dataRow = self.dataSummary[1].__len__()
        # print(self.treeItem)



    def treeUpdate(self):
        QTreeWidget.clear(self.treeWidget)
        for tdataset in self.lTestDATA:
            fname = tdataset.getFileName()         #os.path.basename(self.winImpData.sDataFilePath)
            # if self.shortfname == '':
            #     self.shortfname = fname
            # elif self.shortfname == fname:
            #     return

            treeRoot = QTreeWidgetItem(self.treeWidget)
            treeRoot.setText(1, fname)

            self.treeItem = tdataset.getColumnList()  # list(self.winImpData.dfData)
            self.numTree = tdataset.getColNum     #self.treeItem.__len__()




            for i in range(1, len(self.treeItem), 1):
                child = QTreeWidgetItem(treeRoot)
                child.setText(0, str(i))
                child.setText(1, self.treeItem[i])
                child.setText(2, self.dataparam.getParamInfo(self.treeItem[i],'paramDesc'))
                child.setText(3, self.dataparam.getParamInfo(self.treeItem[i],'unit'))

    # def CI_Plot(self, currentItem):
    #
    #     temp = self.dataPlot.plotItem
    #     temp.setLabels(left='axis 1')
    #
    #     temp.setLabel('bottom', 'Time', units='s', **{'font-size': '20pt'})
    #     temp.getAxis('bottom').setPen(pyqtgraph.mkPen(color='#000000', width=1))
    #     # temp.showAxis('right')
    #     temp_2_plot = self.dataSummary[int(currentItem.text(0))]
    #     # print(temp_2_plot)
    #     pen1 = pyqtgraph.mkPen(color='b') #, width=2)
    #     self.first_curve = temp.plot([float(x) for x in temp_2_plot], pen=pen1)
    #     #self.chartPlotItems.append(temp)

    # def SI_Plot(self, currentItem, selectedItems):
    #     self.CI_Plot(currentItem)
    #     #self.chartPlotItems[0].vb.sigResized.connect(self.updateViews)
    #     j = 2
    #     # print(j)
    #     for i in range(0, len(selectedItems)):
    #
    #         if selectedItems[i] != currentItem:
    #             # print('3')
    #             temp_vb = pyqtgraph.ViewBox()
    #
    #             ax_temp = pyqtgraph.AxisItem('right')
    #
    #             # self.chartPlotItems[0].layout.clear()
    #
    #             self.chartPlotItems[0].layout.addItem(ax_temp, 2, j)
    #             self.chartPlotItems[0].scene().addItem(temp_vb)
    #             ax_temp.linkToView(temp_vb)
    #             temp_vb.setXLink(self.chartPlotItems[0])
    #             ax_temp.setLabel('axial ' + str(j), color=self.colorDex[i])
    #             # print('4')
    #             temp_2_plot = self.dataSummary[int(selectedItems[i].text(0))]
    #             # print(temp_2_plot[:100])
    #             temp_plotcurve = pyqtgraph.PlotCurveItem([float(x) for x in temp_2_plot], pen=self.colorDex[i])
    #             temp_vb.addItem(temp_plotcurve)
    #
    #             self.chartVBs.append(temp_vb)
    #             self.chartAxials.append(ax_temp)
    #             self.chartCurve.append(temp_plotcurve)
    #             # print('5')
    #
    #             j = j + 1



    class TimeAxisItem(pyqtgraph.AxisItem): #### class TimeAxisItem is used for overloading x axis as time
        def tickStrings(self, values, scale, spacing):
            # show hour:minute:second on the x axis
            return [datetime.fromtimestamp(value).strftime('%H:%M:%S') for value in values]

    def sTimeToDateTime(self, inTime):  # convert time from string to datetime object
        # inTime: '13:43:02:578' string type
        # outTime: 2018-08-22 13:43:02.578000  datetime object

        itime = inTime.split(':')
        # add current date to the TIME for the sake of format of datetime class. could use real date of the data created
        rtime = datetime.now().date().isoformat() + ' ' + itime[0] + ':' + itime[1] + ':' + itime[2] + '.' + itime[3]  # with date
        return datetime.strptime(rtime, '%Y-%m-%d %H:%M:%S.%f')  # convert the time from string to the datetime format


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


