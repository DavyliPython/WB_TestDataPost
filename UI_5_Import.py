# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_5_Import.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Import(object):
    def setupUi(self, Import):
        Import.setObjectName("Import")
        Import.resize(700, 842)
        self.label = QtWidgets.QLabel(Import)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Import)
        self.pushButton.setGeometry(QtCore.QRect(610, 10, 61, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Import)
        self.pushButton_2.setGeometry(QtCore.QRect(470, 60, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_3 = QtWidgets.QLabel(Import)
        self.label_3.setGeometry(QtCore.QRect(260, 60, 51, 16))
        self.label_3.setObjectName("label_3")
        self.spinBox = QtWidgets.QSpinBox(Import)
        self.spinBox.setGeometry(QtCore.QRect(310, 60, 71, 22))
        self.spinBox.setMaximum(2000)
        self.spinBox.setSingleStep(20)
        self.spinBox.setObjectName("spinBox")
        self.pushButton_3 = QtWidgets.QPushButton(Import)
        self.pushButton_3.setGeometry(QtCore.QRect(570, 60, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_4 = QtWidgets.QLabel(Import)
        self.label_4.setGeometry(QtCore.QRect(30, 90, 121, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Import)
        self.label_5.setGeometry(QtCore.QRect(390, 60, 51, 16))
        self.label_5.setObjectName("label_5")
        self.groupBox = QtWidgets.QGroupBox(Import)
        self.groupBox.setGeometry(QtCore.QRect(30, 350, 631, 231))
        self.groupBox.setObjectName("groupBox")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_7.setGeometry(QtCore.QRect(380, 180, 221, 22))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(340, 180, 26, 22))
        self.label_12.setObjectName("label_12")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_6.setGeometry(QtCore.QRect(70, 180, 255, 22))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(20, 150, 95, 20))
        self.checkBox_3.setObjectName("checkBox_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_4.setGeometry(QtCore.QRect(140, 120, 351, 22))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(350, 60, 26, 22))
        self.label_8.setObjectName("label_8")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(20, 30, 95, 20))
        self.checkBox.setObjectName("checkBox")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(30, 60, 33, 22))
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(30, 120, 91, 22))
        self.label_9.setObjectName("label_9")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(20, 90, 95, 20))
        self.checkBox_2.setObjectName("checkBox_2")
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(20, 180, 33, 22))
        self.label_11.setObjectName("label_11")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 60, 255, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_5.setGeometry(QtCore.QRect(390, 60, 221, 22))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_6 = QtWidgets.QLabel(Import)
        self.label_6.setGeometry(QtCore.QRect(70, 600, 91, 16))
        self.label_6.setObjectName("label_6")
        self.lineEdit_3 = QtWidgets.QLineEdit(Import)
        self.lineEdit_3.setGeometry(QtCore.QRect(180, 600, 221, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_10 = QtWidgets.QLabel(Import)
        self.label_10.setGeometry(QtCore.QRect(30, 660, 91, 16))
        self.label_10.setObjectName("label_10")
        self.lineEdit_8 = QtWidgets.QLineEdit(Import)
        self.lineEdit_8.setGeometry(QtCore.QRect(110, 660, 541, 22))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.pushButton_4 = QtWidgets.QPushButton(Import)
        self.pushButton_4.setGeometry(QtCore.QRect(210, 710, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Import)
        self.pushButton_5.setGeometry(QtCore.QRect(110, 710, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.progressBar = QtWidgets.QProgressBar(Import)
        self.progressBar.setGeometry(QtCore.QRect(50, 760, 621, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.lineEdit = QtWidgets.QLineEdit(Import)
        self.lineEdit.setGeometry(QtCore.QRect(100, 20, 491, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.tableWidget = QtWidgets.QTableWidget(Import)
        self.tableWidget.setGeometry(QtCore.QRect(30, 120, 611, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(Import)
        QtCore.QMetaObject.connectSlotsByName(Import)

    def retranslateUi(self, Import):
        _translate = QtCore.QCoreApplication.translate
        Import.setWindowTitle(_translate("Import", "Import..."))
        self.label.setText(_translate("Import", "Test Data File:"))
        self.pushButton.setText(_translate("Import", "..."))
        self.pushButton_2.setText(_translate("Import", "Preview"))
        self.label_3.setText(_translate("Import", "Read "))
        self.pushButton_3.setText(_translate("Import", "Clear"))
        self.label_4.setText(_translate("Import", "Data Preview:"))
        self.label_5.setText(_translate("Import", "lines"))
        self.groupBox.setTitle(_translate("Import", "GroupBox"))
        self.label_12.setText(_translate("Import", "End:"))
        self.checkBox_3.setText(_translate("Import", "By Row"))
        self.label_8.setText(_translate("Import", "End:"))
        self.checkBox.setText(_translate("Import", "By Time"))
        self.label_7.setText(_translate("Import", "Start:"))
        self.label_9.setText(_translate("Import", "Colume No."))
        self.checkBox_2.setText(_translate("Import", "By Column"))
        self.label_11.setText(_translate("Import", "Start:"))
        self.label_6.setText(_translate("Import", "Output Rate"))
        self.label_10.setText(_translate("Import", "Output File:"))
        self.pushButton_4.setText(_translate("Import", "Interupt"))
        self.pushButton_5.setText(_translate("Import", "Preview"))

