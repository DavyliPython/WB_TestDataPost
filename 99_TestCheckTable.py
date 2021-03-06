import sys
import signal

#import QT
#from PyQt4 import QtCore,QtWidgets
from PyQt5 import QtWidgets, QtCore
#---------------------------------------------------------------------------------------------------------
# Custom checkbox header
#---------------------------------------------------------------------------------------------------------
#Draw a CheckBox to the left of the first column
#Emit clicked when checked/unchecked
class CheckBoxHeader(QtWidgets.QHeaderView):
    clicked=QtCore.pyqtSignal(bool)

    def __init__(self,orientation=QtCore.Qt.Horizontal,parent=None):
        super(CheckBoxHeader,self).__init__(orientation,parent)
        #self.setResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.isChecked=False

    def paintSection(self,painter,rect,logicalIndex):
        painter.save()
        super(CheckBoxHeader,self).paintSection(painter,rect,logicalIndex)
        painter.restore()
        if logicalIndex==0:
            option=QtWidgets.QStyleOptionButton()
            option.rect= QtCore.QRect(3,5,20,20)  #may have to be adapt
            option.state=QtWidgets.QStyle.State_Enabled | QtWidgets.QStyle.State_Active
            if self.isChecked:
                option.state|=QtWidgets.QStyle.State_On
            else:
                option.state|=QtWidgets.QStyle.State_Off
            self.style().drawControl(QtWidgets.QStyle.CE_CheckBox,option,painter)

    def mousePressEvent(self,event):
        if self.isChecked:
            self.isChecked=False
        else:
            self.isChecked=True
        self.clicked.emit(self.isChecked)
        self.viewport().update()

#---------------------------------------------------------------------------------------------------------
# Table Model, with checkBoxed on the left
#---------------------------------------------------------------------------------------------------------
#On row in the table
class RowObject(object):
    def __init__(self):
        self.col0="column 0"
        self.col1="column 1"

class Model(QtCore.QAbstractTableModel):
    def __init__(self,parent=None):
        super(Model,self).__init__(parent)
        #Model= list of object
        self.myList=[RowObject(),RowObject()]
        #Keep track of which object are checked
        self.checkList=[]

    def rowCount(self,QModelIndex):
        return len(self.myList)

    def columnCount(self,QModelIndex):
        return 2

    def addOneRow(self,rowObject):
        frow=len(self.myList)
        self.beginInsertRows(QtCore.QModelIndex(),row,row)
        self.myList.append(rowObject)
        self.endInsertRows()

    def data(self,index,role):
        row=index.row()
        col=index.column()
        if role==QtCore.Qt.DisplayRole:
            if col==0:
                return self.myList[row].col0
            if col==1:
                return self.myList[row].col1
        elif role==QtCore.Qt.CheckStateRole:
            if col==0:
                if self.myList[row] in self.checkList:
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked

    def setData(self,index,value,role):
        row=index.row()
        col=index.column()
        if role==QtCore.Qt.CheckStateRole and col==0:
            rowObject=self.myList[row]
            if rowObject in self.checkList:
                self.checkList.remove(rowObject)
            else:
                self.checkList.append(rowObject)
            index=self.index(row,col+1)
            self.dataChanged.emit(index,index)
        return True

    def flags(self,index):
        if index.column()==0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
        return QtCore.Qt.ItemIsEnabled

    def headerData(self,section,orientation,role):
        if role==QtCore.Qt.DisplayRole:
            if orientation==QtCore.Qt.Horizontal:
                if section==0:
                    return "Title 1"
                elif section==1:
                    return "Title 2"

    def headerClick(self,isCheck):
        self.beginResetModel()
        if isCheck:
            self.checkList=self.myList[:]
        else:
            self.checkList=[]
        self.endResetModel()

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)

    #to be able to close with ctrl+c
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    tableView=QtWidgets.QTableView()
    model=Model(parent=tableView)
    header=CheckBoxHeader(parent=tableView)
    header.clicked.connect(model.headerClick)

    tableView.setModel(model)
    tableView.setHorizontalHeader(header)
    tableView.show()

    sys.exit(app.exec_())