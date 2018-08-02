from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QMenu, Qt, QAction, QCursor, QApplication

import sys
import os

import UI3 as UI
import pyqtgraph

#Davy Try Push


import copy


class testDataPost(QMainWindow, UI.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # 类成员变量初始化
        self.colorDex = ['#7CFC00', '#B22222', '#E0FFFF', '#FFFF00', '#66FF00']

        self.chartPlotItem = []
        self.chartVBs = []
        self.chartAxials = []
        self.chartCurve = []

        # pyqtGraph 相关设置，必须要在self.setupUi之前
        pyqtgraph.setConfigOption('background', 'w')  # before loading widget
        self.setupUi(self)
        self.initUI()
        self.show()
        self.showMaximized()

        self.item_title_c = {
            'NWPLO': '正常系统左主起外侧机轮刹车压力',
            'NWPLI': '正常系统左主起内侧机轮刹车压力',
            'NWPRO': '正常系统右主起外侧机轮刹车压力',
            'NWPRI': '正常系统右主起内侧机轮刹车压力',
            'AWPL': '备份系统左侧刹车压力',
            'AWPR': '备份系统右侧刹车压力',
            'BRKMLO1': '左外刹车力矩1',
            'BRKMLO2': '左外刹车力矩2',
            'BRKMLI1': '左内刹车力矩1',
            'BRKMLI2': '左内刹车力矩2',
            'BRKMRO1': '右外刹车力矩1',
            'BRKMRO2': '右外刹车力矩2',
            'BRKMRI1': '右内刹车力矩1',
            'BRKMRI2': '右内刹车力矩2',
            'WSPDLO1': '左主起外侧机轮速度1',
            'WSPDLO2': '左主起外侧机轮速度2',
            'WSPDLI1': '左主起内侧机轮速度1',
            'WSPDLI2': '左主起内侧机轮速度2',
            'WSPDRO1': '右主起外侧机轮速度1',
            'WSPDRO2': '右主起外侧机轮速度2',
            'WSPDRI1': '右主起内侧机轮速度1',
            'WSPDRI2': '右主起内侧机轮速度2',
            'NBCVILO': '正常系统左主起外侧机轮刹车BCV电流',
            'NBCVILI': '正常系统左主起内侧机轮刹车BCV电流',
            'NBCVIRO': '正常系统右主起外侧机轮刹车BCV电流',
            'NBCVIRI': '正常系统右主起内侧机轮刹车BCV电流',
            'ABCVIL': '备份系统左侧机轮刹车BCV电流',
            'ABCVIR': '备份系统右侧机轮刹车BCV电流',
        }

        self.item_title = {
            'NWPLO': 'NML LO BRK PRESSURE',
            'NWPLI': 'NML LI BRK PRESSURE',
            'NWPRO': 'NML RO BRK PRESSURE',
            'NWPRI': 'NML RI BRK PRESSURE',
            'AWPL': 'ALT L BRK PRESSURE',
            'AWPR': 'ALT R BRK PRESSURE',
            'BRKMLO1': 'LO Brake torque1',
            'BRKMLO2': 'LO Brake torque2',
            'BRKMLI1': 'LI Brake torque1',
            'BRKMLI2': 'LI Brake torque2',
            'BRKMRO1': 'RO Brake torque1',
            'BRKMRO2': 'RO Brake torque2',
            'BRKMRI1': 'RI Brake torque1',
            'BRKMRI2': 'RI Brake torque2',
            'WSPDLO1': 'LO Wheel Speed(NML)',
            'WSPDLO2': 'LO Wheel Speed(ALT)',
            'WSPDLI1': 'LI Wheel Speed(NML)',
            'WSPDLI2': 'LI Wheel Speed(ALT)',
            'WSPDRO1': 'RO Wheel Speed(NML)',
            'WSPDRO2': 'RO Wheel Speed(ALT)',
            'WSPDRI1': 'RI Wheel Speed(NML)',
            'WSPDRI2': 'RI Wheel Speed(ALT)',
            'NBCVILO': 'NBCV LO',
            'NBCVILI': 'NBCV LI',
            'NBCVIRO': 'NBCV RO',
            'NBCVIRI': 'NBCV RI',
            'ABCVIL': 'ABCV L',
            'ABCVIR': 'ABCV R',
        }

        self.item_unit = {
            'NWPLO': 'PSI',
            'NWPLI': 'PSI',
            'NWPRO': 'PSI',
            'NWPRI': 'PSI',
            'AWPL': 'PSI',
            'AWPR': 'PSI',
            'BRKMLO1': 'LBS.IN',
            'BRKMLO2': 'LBS.IN',
            'BRKMLI1': 'LBS.IN',
            'BRKMLI2': 'LBS.IN',
            'BRKMRO1': 'LBS.IN',
            'BRKMRO2': 'LBS.IN',
            'BRKMRI1': 'LBS.IN',
            'BRKMRI2': 'LBS.IN',
            'WSPDLO1': 'KNOT',
            'WSPDLO2': 'KNOT',
            'WSPDLI1': 'KNOT',
            'WSPDLI2': 'KNOT',
            'WSPDRO1': 'KNOT',
            'WSPDRO2': 'KNOT',
            'WSPDRI1': 'KNOT',
            'WSPDRI2': 'KNOT',
            'NBCVILO': 'mA',
            'NBCVILI': 'mA',
            'NBCVIRO': 'mA',
            'NBCVIRI': 'mA',
            'ABCVIL': 'mA',
            'ABCVIR': 'mA',
        }

    def initUI(self):
        # 添加打开菜单
        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.openFile)
        openFile.setIcon(QIcon('import.ico'))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        toolBar = self.addToolBar("File")
        toolBar.addAction(openFile)

        # 设置PlotWidget
        self.dataPlot.plotItem.showGrid(True, True, 0.5)
        self.dataPlotRange.setMouseEnabled(x=False, y=False)  # dataPlotRange 不能移动
        self.dataPlot.setAutoVisible(y=True)

        # 设置treeWidget的相关
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.showContextMenu)
        self.treeWidget.treeContextMenu = QMenu(self)
        self.actionA = self.treeWidget.treeContextMenu.addAction(u'Plot')
        self.actionA.triggered.connect(
            lambda: self.chartPlot(self.treeWidget.currentItem(), self.treeWidget.selectedItems()))

        self.treeWidget.setColumnCount(4)
        self.treeWidget.setHeaderLabels(['#', 'File Name', 'Corrective Name', 'Unit'])
        self.treeWidget.setColumnWidth(0, 30)
        self.treeWidget.setColumnWidth(1, 100)
        self.treeWidget.setColumnWidth(2, 200)

    def showContextMenu(self):
        self.treeWidget.treeContextMenu.move(QCursor.pos())
        self.treeWidget.treeContextMenu.show()

    def updateViews(self):
        for i in range(0, len(self.chartVBs)):
            self.chartVBs[i].setGeometry(self.chartPlotItems[0].vb.sceneBoundingRect())
            self.chartVBs[i].linkedViewChanged(self.chartPlotItems[0].vb, self.chartVBs[i].XAxis)

    def chartPlot(self, currentItem, selectedItems):

        if self.chartVBs:
            for i in range(0, len(self.chartVBs)):
                print('remove VBs')
                self.chartPlotItems[0].scene().removeItem(self.chartVBs[i])
                self.chartPlotItems[0].scene().removeItem(self.chartAxials[i])
                self.chartPlotItems[0].scene().removeItem(self.chartCurve[i])

        if self.chartPlotItems:
            print('remove plot item')
            self.dataPlot.removeItem(self.first_curve)

        self.updateViews()


        # reset the class member
        self.chartPlotItems = []
        self.chartVBs = []
        self.chartAxials = []
        self.chartCurve = []

        # print(currentItem, selectedItems)
        if len(selectedItems) == 1:
            self.CI_Plot(currentItem)
        else:
            self.SI_Plot(currentItem, selectedItems)

        ################
        self.item_Selected = int(self.treeWidget.currentItem().text(0))

        pen1 = pyqtgraph.mkPen(color='b')
        pen2 = pyqtgraph.mkPen(color='r')

        self.dataPlotRange.plot(range(self.dataSummary[self.item_Selected].__len__()),
                                [float(x) for x in self.dataSummary[self.item_Selected]], pen=pen2, clear=True)
        self.dataPlotRange.setZValue(1)

        self.region = pyqtgraph.LinearRegionItem()
        self.region.setZValue(10)
        self.dataPlotRange.addItem(self.region, ignoreBounds=True)

        self.region.setRegion([self.dataRow * 0.4, self.dataRow * 0.6])

        self.region.sigRegionChanged.connect(self.regionUpdate)
        self.dataPlot.plotItem.vb.sigRangeChanged.connect(self.updateRegion)
        ################
        self.vLine = pyqtgraph.InfiniteLine(angle=90, movable=False)
        self.hLine = pyqtgraph.InfiniteLine(angle=0, movable=False)
        self.dataPlot.addItem(self.vLine, ignoreBounds=True)
        self.dataPlot.addItem(self.hLine, ignoreBounds=True)
        print('line done')

        self.dataPlot.plotItem.scene().sigMouseMoved.connect(self.mouseMove)

    def mouseMove(self, evt):
        # print('dong')
        pos = evt  # [0]  ## using signal proxy turns original arguments into a tuple
        # print(evt)
        if self.dataPlot.plotItem.sceneBoundingRect().contains(pos):
            print('if1')
            mousePoint = self.dataPlot.plotItem.vb.mapSceneToView(pos)
            print('if2')
            index = int(mousePoint.x())
            print('if3')
            if index > 0 and index < len(self.dataSummary[self.item_Selected]):
                # print('if4')
                # print(index)
                # print(mousePoint.x())
                # print(self.dataSummary[self.item_Selected][index])
                self.label.setText(
                    "<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'> Y1=%0.1f</span>," % (
                        mousePoint.x(), float(self.dataSummary[self.item_Selected][index])))
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

    def regionUpdate(self):
        minX, maxX = self.region.getRegion()
        self.dataPlot.setXRange(minX, maxX, padding=0)

    def updateRegion(self, window, viewRange):
        # print(window)
        # print(viewRange)
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'D:/backup/00_Learn/01_Work/01_Code/05_TestDataPost/archive/')
        if fname[0]:
            # print(fname)
            self.shortfname = os.path.basename(fname[0])
            self.loadData(fname)
            self.treeUpdate()

    def loadData(self, fname):
        f1 = open(fname[0], 'r')
        first_line = f1.readline().strip('\n')
        self.treeItem = first_line.split('\t')
        self.dataSummary = [[] for col in range(self.treeItem.__len__())]
        self.numTree = self.treeItem.__len__()

        line = f1.readline().strip('\n')
        while line:
            temp_line = line.split('\t')
            for i in range(0, len(temp_line), 1):
                self.dataSummary[i].append(temp_line[i])
            line = f1.readline().strip('\n')

        self.dataRow = self.dataSummary[1].__len__()
        # print(self.treeItem)

    def treeUpdate(self):

        treeRoot = QTreeWidgetItem(self.treeWidget)
        treeRoot.setText(1, self.shortfname)

        for i in range(0, len(self.treeItem), 1):
            child = QTreeWidgetItem(treeRoot)
            child.setText(0, str(i + 1))
            child.setText(1, self.treeItem[i])
            if (self.treeItem[i] in self.item_title.keys()):
                child.setText(2, self.item_title[self.treeItem[i]])
                child.setText(3, self.item_unit[self.treeItem[i]])

    def CI_Plot(self, currentItem):

        temp = self.dataPlot.plotItem
        temp.setLabels(left='axis 1')

        temp.setLabel('bottom', 'Time', units='s', **{'font-size': '20pt'})
        temp.getAxis('bottom').setPen(pyqtgraph.mkPen(color='#000000', width=1))
        # temp.showAxis('right')
        temp_2_plot = self.dataSummary[int(currentItem.text(0))]
        # print(temp_2_plot)
        pen1 = pyqtgraph.mkPen(color='b') #, width=2)
        self.first_curve = temp.plot([float(x) for x in temp_2_plot], pen=pen1)
        self.chartPlotItems.append(temp)

    def SI_Plot(self, currentItem, selectedItems):
        self.CI_Plot(currentItem)
        self.chartPlotItems[0].vb.sigResized.connect(self.updateViews)
        j = 2
        # print(j)
        for i in range(0, len(selectedItems)):

            if selectedItems[i] != currentItem:
                # print('3')
                temp_vb = pyqtgraph.ViewBox()

                ax_temp = pyqtgraph.AxisItem('right')

                # self.chartPlotItems[0].layout.clear()

                self.chartPlotItems[0].layout.addItem(ax_temp, 2, j)
                self.chartPlotItems[0].scene().addItem(temp_vb)
                ax_temp.linkToView(temp_vb)
                temp_vb.setXLink(self.chartPlotItems[0])
                ax_temp.setLabel('axial ' + str(j), color=self.colorDex[i])
                # print('4')
                temp_2_plot = self.dataSummary[int(selectedItems[i].text(0))]
                # print(temp_2_plot[:100])
                temp_plotcurve = pyqtgraph.PlotCurveItem([float(x) for x in temp_2_plot], pen=self.colorDex[i])
                temp_vb.addItem(temp_plotcurve)

                self.chartVBs.append(temp_vb)
                self.chartAxials.append(ax_temp)
                self.chartCurve.append(temp_plotcurve)
                # print('5')

                j = j + 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MW = testDataPost()
    sys.exit(app.exec_())
    print("DONE")