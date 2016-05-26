# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reportsdialog.ui'
#
# Created: Wed May 25 13:43:29 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_reportsDialog(object):
    def setupUi(self, reportsDialog):
        reportsDialog.setObjectName(_fromUtf8("reportsDialog"))
        reportsDialog.resize(950, 580)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/podbicon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        reportsDialog.setWindowIcon(icon)
        self.configGroupBox = QtGui.QGroupBox(reportsDialog)
        self.configGroupBox.setGeometry(QtCore.QRect(0, 40, 951, 71))
        self.configGroupBox.setObjectName(_fromUtf8("configGroupBox"))
        self.goPushButton = QtGui.QPushButton(self.configGroupBox)
        self.goPushButton.setGeometry(QtCore.QRect(904, 24, 35, 35))
        self.goPushButton.setObjectName(_fromUtf8("goPushButton"))
        self.layoutWidget = QtGui.QWidget(self.configGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 881, 44))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.endDateLabel = QtGui.QLabel(self.layoutWidget)
        self.endDateLabel.setObjectName(_fromUtf8("endDateLabel"))
        self.gridLayout.addWidget(self.endDateLabel, 0, 2, 1, 1)
        self.startDateEdit = QtGui.QDateEdit(self.layoutWidget)
        self.startDateEdit.setObjectName(_fromUtf8("startDateEdit"))
        self.gridLayout.addWidget(self.startDateEdit, 1, 1, 1, 1)
        self.startDateLabel = QtGui.QLabel(self.layoutWidget)
        self.startDateLabel.setObjectName(_fromUtf8("startDateLabel"))
        self.gridLayout.addWidget(self.startDateLabel, 0, 1, 1, 1)
        self.reportTypeLabel = QtGui.QLabel(self.layoutWidget)
        self.reportTypeLabel.setObjectName(_fromUtf8("reportTypeLabel"))
        self.gridLayout.addWidget(self.reportTypeLabel, 0, 0, 1, 1)
        self.reportTypeComboBox = QtGui.QComboBox(self.layoutWidget)
        self.reportTypeComboBox.setObjectName(_fromUtf8("reportTypeComboBox"))
        self.gridLayout.addWidget(self.reportTypeComboBox, 1, 0, 1, 1)
        self.additionalDataLabel = QtGui.QLabel(self.layoutWidget)
        self.additionalDataLabel.setObjectName(_fromUtf8("additionalDataLabel"))
        self.gridLayout.addWidget(self.additionalDataLabel, 0, 3, 1, 1)
        self.additionalDataComboBox = QtGui.QComboBox(self.layoutWidget)
        self.additionalDataComboBox.setToolTip(_fromUtf8(""))
        self.additionalDataComboBox.setObjectName(_fromUtf8("additionalDataComboBox"))
        self.gridLayout.addWidget(self.additionalDataComboBox, 1, 3, 1, 1)
        self.endDateEdit = QtGui.QDateEdit(self.layoutWidget)
        self.endDateEdit.setObjectName(_fromUtf8("endDateEdit"))
        self.gridLayout.addWidget(self.endDateEdit, 1, 2, 1, 1)
        self.resultGroupBox = QtGui.QGroupBox(reportsDialog)
        self.resultGroupBox.setGeometry(QtCore.QRect(0, 120, 951, 411))
        self.resultGroupBox.setObjectName(_fromUtf8("resultGroupBox"))
        self.tableView = QtGui.QTableView(self.resultGroupBox)
        self.tableView.setGeometry(QtCore.QRect(10, 20, 931, 361))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.totalResultLabel = QtGui.QLabel(self.resultGroupBox)
        self.totalResultLabel.setGeometry(QtCore.QRect(858, 390, 81, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.totalResultLabel.setFont(font)
        self.totalResultLabel.setText(_fromUtf8(""))
        self.totalResultLabel.setObjectName(_fromUtf8("totalResultLabel"))
        self.totalLabel = QtGui.QLabel(self.resultGroupBox)
        self.totalLabel.setGeometry(QtCore.QRect(793, 390, 50, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.totalLabel.setFont(font)
        self.totalLabel.setObjectName(_fromUtf8("totalLabel"))
        self.donePushButton = QtGui.QPushButton(reportsDialog)
        self.donePushButton.setGeometry(QtCore.QRect(860, 540, 75, 23))
        self.donePushButton.setObjectName(_fromUtf8("donePushButton"))
        self.frame = QtGui.QFrame(reportsDialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 951, 31))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.clearToolButton = QtGui.QToolButton(self.frame)
        self.clearToolButton.setGeometry(QtCore.QRect(0, 0, 32, 32))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/clear.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearToolButton.setIcon(icon1)
        self.clearToolButton.setIconSize(QtCore.QSize(32, 32))
        self.clearToolButton.setObjectName(_fromUtf8("clearToolButton"))
        self.printToolButton = QtGui.QToolButton(self.frame)
        self.printToolButton.setGeometry(QtCore.QRect(920, 0, 32, 32))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/print.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.printToolButton.setIcon(icon2)
        self.printToolButton.setIconSize(QtCore.QSize(32, 32))
        self.printToolButton.setObjectName(_fromUtf8("printToolButton"))
        self.exportToolButton = QtGui.QToolButton(self.frame)
        self.exportToolButton.setGeometry(QtCore.QRect(890, 0, 32, 32))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/exportpdf.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportToolButton.setIcon(icon3)
        self.exportToolButton.setIconSize(QtCore.QSize(32, 32))
        self.exportToolButton.setObjectName(_fromUtf8("exportToolButton"))

        self.retranslateUi(reportsDialog)
        QtCore.QMetaObject.connectSlotsByName(reportsDialog)

    def retranslateUi(self, reportsDialog):
        reportsDialog.setWindowTitle(_translate("reportsDialog", "View Reports", None))
        self.configGroupBox.setTitle(_translate("reportsDialog", "Configure Report", None))
        self.goPushButton.setToolTip(_translate("reportsDialog", "Generate the report", None))
        self.goPushButton.setText(_translate("reportsDialog", "GO", None))
        self.endDateLabel.setText(_translate("reportsDialog", "End Date:", None))
        self.startDateEdit.setToolTip(_translate("reportsDialog", "Select the start date of the report date range", None))
        self.startDateLabel.setText(_translate("reportsDialog", "Start Date:", None))
        self.reportTypeLabel.setText(_translate("reportsDialog", "Report Type:", None))
        self.reportTypeComboBox.setToolTip(_translate("reportsDialog", "Select the report type", None))
        self.additionalDataLabel.setText(_translate("reportsDialog", "Additional Data:", None))
        self.endDateEdit.setToolTip(_translate("reportsDialog", "Select the end date of the report date range", None))
        self.resultGroupBox.setTitle(_translate("reportsDialog", "Report Result", None))
        self.totalLabel.setText(_translate("reportsDialog", "Total:", None))
        self.donePushButton.setToolTip(_translate("reportsDialog", "Close the reports dialog", None))
        self.donePushButton.setText(_translate("reportsDialog", "Done", None))
        self.clearToolButton.setToolTip(_translate("reportsDialog", "Reset report configuration to defaults", None))
        self.clearToolButton.setText(_translate("reportsDialog", "...", None))
        self.printToolButton.setToolTip(_translate("reportsDialog", "Print report", None))
        self.printToolButton.setText(_translate("reportsDialog", "...", None))
        self.exportToolButton.setToolTip(_translate("reportsDialog", "Export report to PDF file", None))
        self.exportToolButton.setText(_translate("reportsDialog", "...", None))

import resources_rc
