# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_5_Import.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_winImportData(object):
    def setupUi(self, winImportData):
        winImportData.setObjectName("winImportData")
        winImportData.setWindowModality(QtCore.Qt.WindowModal)
        winImportData.resize(686, 535)
        self.label = QtWidgets.QLabel(winImportData)
        self.label.setGeometry(QtCore.QRect(30, 20, 81, 16))
        self.label.setObjectName("label")
        self.btnBrowse_in = QtWidgets.QPushButton(winImportData)
        self.btnBrowse_in.setGeometry(QtCore.QRect(430, 18, 71, 28))
        self.btnBrowse_in.setObjectName("btnBrowse_in")
        self.btnImport = QtWidgets.QPushButton(winImportData)
        self.btnImport.setGeometry(QtCore.QRect(530, 480, 131, 41))
        self.btnImport.setObjectName("btnImport")
        self.label_4 = QtWidgets.QLabel(winImportData)
        self.label_4.setGeometry(QtCore.QRect(520, 23, 81, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(winImportData)
        self.label_5.setGeometry(QtCore.QRect(640, 23, 31, 16))
        self.label_5.setObjectName("label_5")
        self.groupBox = QtWidgets.QGroupBox(winImportData)
        self.groupBox.setGeometry(QtCore.QRect(10, 260, 661, 81))
        self.groupBox.setObjectName("groupBox")
        self.qleRows = QtWidgets.QLineEdit(self.groupBox)
        self.qleRows.setGeometry(QtCore.QRect(510, 20, 71, 22))
        self.qleRows.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.qleRows.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qleRows.setReadOnly(True)
        self.qleRows.setObjectName("qleRows")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(440, 20, 80, 22))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(20, 50, 80, 22))
        self.label_13.setObjectName("label_13")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(240, 20, 80, 22))
        self.label_9.setObjectName("label_9")
        self.qleColumns = QtWidgets.QLineEdit(self.groupBox)
        self.qleColumns.setGeometry(QtCore.QRect(330, 20, 71, 22))
        self.qleColumns.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.qleColumns.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qleColumns.setReadOnly(True)
        self.qleColumns.setObjectName("qleColumns")
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setGeometry(QtCore.QRect(30, 20, 80, 22))
        self.label_14.setObjectName("label_14")
        self.qleFileSize = QtWidgets.QLineEdit(self.groupBox)
        self.qleFileSize.setGeometry(QtCore.QRect(110, 20, 71, 22))
        self.qleFileSize.setText("")
        self.qleFileSize.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qleFileSize.setReadOnly(True)
        self.qleFileSize.setObjectName("qleFileSize")
        self.qleRate = QtWidgets.QLineEdit(self.groupBox)
        self.qleRate.setGeometry(QtCore.QRect(110, 50, 71, 22))
        self.qleRate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qleRate.setReadOnly(True)
        self.qleRate.setObjectName("qleRate")
        self.label_23 = QtWidgets.QLabel(self.groupBox)
        self.label_23.setGeometry(QtCore.QRect(220, 50, 101, 22))
        self.label_23.setObjectName("label_23")
        self.teDataFromTime = QtWidgets.QTimeEdit(self.groupBox)
        self.teDataFromTime.setGeometry(QtCore.QRect(330, 50, 71, 22))
        self.teDataFromTime.setToolTipDuration(-1)
        self.teDataFromTime.setInputMethodHints(QtCore.Qt.ImhPreferNumbers|QtCore.Qt.ImhTime)
        self.teDataFromTime.setObjectName("teDataFromTime")
        self.label_24 = QtWidgets.QLabel(self.groupBox)
        self.label_24.setGeometry(QtCore.QRect(480, 50, 31, 22))
        self.label_24.setObjectName("label_24")
        self.teDataToTime = QtWidgets.QTimeEdit(self.groupBox)
        self.teDataToTime.setGeometry(QtCore.QRect(510, 50, 71, 22))
        self.teDataToTime.setInputMethodHints(QtCore.Qt.ImhPreferNumbers|QtCore.Qt.ImhTime)
        self.teDataToTime.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.teDataToTime.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
        self.teDataToTime.setObjectName("teDataToTime")
        self.progressBar = QtWidgets.QProgressBar(winImportData)
        self.progressBar.setGeometry(QtCore.QRect(10, 490, 511, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.qleFilePath_in = QtWidgets.QLineEdit(winImportData)
        self.qleFilePath_in.setGeometry(QtCore.QRect(110, 20, 310, 22))
        self.qleFilePath_in.setReadOnly(True)
        self.qleFilePath_in.setObjectName("qleFilePath_in")
        self.tblreviewdata = QtWidgets.QTableWidget(winImportData)
        self.tblreviewdata.setGeometry(QtCore.QRect(10, 60, 661, 192))
        self.tblreviewdata.setInputMethodHints(QtCore.Qt.ImhNone)
        self.tblreviewdata.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tblreviewdata.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tblreviewdata.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)
        self.tblreviewdata.setObjectName("tblreviewdata")
        self.tblreviewdata.setColumnCount(0)
        self.tblreviewdata.setRowCount(0)
        self.lbRate_2 = QtWidgets.QLabel(winImportData)
        self.lbRate_2.setGeometry(QtCore.QRect(190, 100, 41, 16))
        self.lbRate_2.setText("")
        self.lbRate_2.setObjectName("lbRate_2")
        self.leRows = QtWidgets.QLineEdit(winImportData)
        self.leRows.setGeometry(QtCore.QRect(605, 20, 31, 22))
        self.leRows.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.leRows.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.leRows.setReadOnly(True)
        self.leRows.setObjectName("leRows")
        self.groupBox_2 = QtWidgets.QGroupBox(winImportData)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 350, 661, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_15 = QtWidgets.QLabel(self.groupBox_2)
        self.label_15.setGeometry(QtCore.QRect(10, 20, 101, 22))
        self.label_15.setObjectName("label_15")
        self.sbRate = QtWidgets.QSpinBox(self.groupBox_2)
        self.sbRate.setGeometry(QtCore.QRect(110, 20, 41, 22))
        self.sbRate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbRate.setMaximum(200)
        self.sbRate.setSingleStep(1)
        self.sbRate.setProperty("value", 1)
        self.sbRate.setObjectName("sbRate")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(190, 20, 101, 22))
        self.label_7.setObjectName("label_7")
        self.teFromTime = QtWidgets.QTimeEdit(self.groupBox_2)
        self.teFromTime.setGeometry(QtCore.QRect(300, 20, 71, 22))
        self.teFromTime.setToolTipDuration(-1)
        self.teFromTime.setInputMethodHints(QtCore.Qt.ImhPreferNumbers|QtCore.Qt.ImhTime)
        self.teFromTime.setObjectName("teFromTime")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(390, 20, 31, 22))
        self.label_8.setObjectName("label_8")
        self.teToTime = QtWidgets.QTimeEdit(self.groupBox_2)
        self.teToTime.setGeometry(QtCore.QRect(420, 20, 71, 22))
        self.teToTime.setInputMethodHints(QtCore.Qt.ImhPreferNumbers|QtCore.Qt.ImhTime)
        self.teToTime.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.teToTime.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
        self.teToTime.setObjectName("teToTime")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 20, 131, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.qleToRow = QtWidgets.QLineEdit(self.groupBox_2)
        self.qleToRow.setGeometry(QtCore.QRect(420, 50, 71, 20))
        self.qleToRow.setInputMethodHints(QtCore.Qt.ImhTime)
        self.qleToRow.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qleToRow.setObjectName("qleToRow")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(230, 50, 61, 22))
        self.label_11.setObjectName("label_11")
        self.qleFromRow = QtWidgets.QLineEdit(self.groupBox_2)
        self.qleFromRow.setGeometry(QtCore.QRect(300, 50, 71, 22))
        self.qleFromRow.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.qleFromRow.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.qleFromRow.setObjectName("qleFromRow")
        self.label_16 = QtWidgets.QLabel(self.groupBox_2)
        self.label_16.setGeometry(QtCore.QRect(390, 50, 31, 22))
        self.label_16.setObjectName("label_16")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(10, 90, 91, 16))
        self.label_10.setObjectName("label_10")
        self.qleFilePath_out = QtWidgets.QLineEdit(self.groupBox_2)
        self.qleFilePath_out.setGeometry(QtCore.QRect(100, 90, 310, 22))
        self.qleFilePath_out.setReadOnly(True)
        self.qleFilePath_out.setObjectName("qleFilePath_out")
        self.btnBrowse_out = QtWidgets.QPushButton(self.groupBox_2)
        self.btnBrowse_out.setGeometry(QtCore.QRect(420, 86, 71, 28))
        self.btnBrowse_out.setObjectName("btnBrowse_out")
        self.btnExport = QtWidgets.QPushButton(self.groupBox_2)
        self.btnExport.setGeometry(QtCore.QRect(520, 60, 131, 41))
        self.btnExport.setObjectName("btnExport")
        self.actionBrowse = QtWidgets.QAction(winImportData)
        self.actionBrowse.setObjectName("actionBrowse")

        self.retranslateUi(winImportData)
        QtCore.QMetaObject.connectSlotsByName(winImportData)

    def retranslateUi(self, winImportData):
        _translate = QtCore.QCoreApplication.translate
        winImportData.setWindowTitle(_translate("winImportData", "Import Test Data"))
        self.label.setText(_translate("winImportData", "Test Data File:"))
        self.btnBrowse_in.setText(_translate("winImportData", "..."))
        self.btnImport.setText(_translate("winImportData", "Import Data"))
        self.label_4.setText(_translate("winImportData", "Preview the first "))
        self.label_5.setText(_translate("winImportData", "lines"))
        self.groupBox.setTitle(_translate("winImportData", "Data Summary"))
        self.label_12.setText(_translate("winImportData", "Total Rows:"))
        self.label_13.setText(_translate("winImportData", "Data Rate ( Hz)"))
        self.label_9.setText(_translate("winImportData", "Total Columns:"))
        self.label_14.setText(_translate("winImportData", "File Size ( Kb)"))
        self.label_23.setText(_translate("winImportData", "Time Starting from:"))
        self.teDataFromTime.setDisplayFormat(_translate("winImportData", "hh:mm:ss"))
        self.label_24.setText(_translate("winImportData", "To:"))
        self.teDataToTime.setDisplayFormat(_translate("winImportData", "hh:mm:ss"))
        self.leRows.setText(_translate("winImportData", "10"))
        self.groupBox_2.setTitle(_translate("winImportData", "Export Setting"))
        self.label_15.setText(_translate("winImportData", "Sampling Rate ( Hz)"))
        self.label_7.setText(_translate("winImportData", "Time Starting from:"))
        self.teFromTime.setDisplayFormat(_translate("winImportData", "hh:mm:ss"))
        self.label_8.setText(_translate("winImportData", "To:"))
        self.teToTime.setDisplayFormat(_translate("winImportData", "hh:mm:ss"))
        self.pushButton_3.setText(_translate("winImportData", "Reset"))
        self.label_11.setText(_translate("winImportData", "From Row:"))
        self.qleFromRow.setText(_translate("winImportData", "1"))
        self.label_16.setText(_translate("winImportData", "To:"))
        self.label_10.setText(_translate("winImportData", "Output to File:"))
        self.btnBrowse_out.setText(_translate("winImportData", "..."))
        self.btnExport.setText(_translate("winImportData", "Export Data"))
        self.actionBrowse.setText(_translate("winImportData", "Browse"))

