# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configwizardp2.ui'
#
# Created: Wed May 25 13:43:28 2016
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

class Ui_wizardPage2(object):
    def setupUi(self, wizardPage2):
        wizardPage2.setObjectName(_fromUtf8("wizardPage2"))
        wizardPage2.resize(545, 310)
        self.connectionTestInstructionLabel = QtGui.QLabel(wizardPage2)
        self.connectionTestInstructionLabel.setGeometry(QtCore.QRect(10, 225, 521, 20))
        self.connectionTestInstructionLabel.setObjectName(_fromUtf8("connectionTestInstructionLabel"))
        self.testResultLabel = QtGui.QLabel(wizardPage2)
        self.testResultLabel.setGeometry(QtCore.QRect(120, 260, 411, 20))
        self.testResultLabel.setText(_fromUtf8(""))
        self.testResultLabel.setObjectName(_fromUtf8("testResultLabel"))
        self.testConnectionPushButton = QtGui.QPushButton(wizardPage2)
        self.testConnectionPushButton.setGeometry(QtCore.QRect(10, 260, 91, 23))
        self.testConnectionPushButton.setObjectName(_fromUtf8("testConnectionPushButton"))
        self.layoutWidget = QtGui.QWidget(wizardPage2)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 521, 171))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dbTypeLabel = QtGui.QLabel(self.layoutWidget)
        self.dbTypeLabel.setObjectName(_fromUtf8("dbTypeLabel"))
        self.gridLayout.addWidget(self.dbTypeLabel, 0, 0, 1, 1)
        self.dbTypeComboBox = QtGui.QComboBox(self.layoutWidget)
        self.dbTypeComboBox.setObjectName(_fromUtf8("dbTypeComboBox"))
        self.gridLayout.addWidget(self.dbTypeComboBox, 0, 1, 1, 1)
        self.dbFileNameLabel = QtGui.QLabel(self.layoutWidget)
        self.dbFileNameLabel.setObjectName(_fromUtf8("dbFileNameLabel"))
        self.gridLayout.addWidget(self.dbFileNameLabel, 1, 0, 1, 1)
        self.dbFileNameLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.dbFileNameLineEdit.setObjectName(_fromUtf8("dbFileNameLineEdit"))
        self.gridLayout.addWidget(self.dbFileNameLineEdit, 1, 1, 1, 1)
        self.dbNameLabel = QtGui.QLabel(self.layoutWidget)
        self.dbNameLabel.setObjectName(_fromUtf8("dbNameLabel"))
        self.gridLayout.addWidget(self.dbNameLabel, 2, 0, 1, 1)
        self.dbNameLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.dbNameLineEdit.setObjectName(_fromUtf8("dbNameLineEdit"))
        self.gridLayout.addWidget(self.dbNameLineEdit, 2, 1, 1, 1)
        self.dbUserNameLabel = QtGui.QLabel(self.layoutWidget)
        self.dbUserNameLabel.setObjectName(_fromUtf8("dbUserNameLabel"))
        self.gridLayout.addWidget(self.dbUserNameLabel, 3, 0, 1, 1)
        self.dbUserNameLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.dbUserNameLineEdit.setObjectName(_fromUtf8("dbUserNameLineEdit"))
        self.gridLayout.addWidget(self.dbUserNameLineEdit, 3, 1, 1, 1)
        self.dbPasswordLabel = QtGui.QLabel(self.layoutWidget)
        self.dbPasswordLabel.setObjectName(_fromUtf8("dbPasswordLabel"))
        self.gridLayout.addWidget(self.dbPasswordLabel, 3, 2, 1, 1)
        self.dbPasswordLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.dbPasswordLineEdit.setObjectName(_fromUtf8("dbPasswordLineEdit"))
        self.gridLayout.addWidget(self.dbPasswordLineEdit, 3, 3, 1, 1)
        self.dbHostLabel = QtGui.QLabel(self.layoutWidget)
        self.dbHostLabel.setObjectName(_fromUtf8("dbHostLabel"))
        self.gridLayout.addWidget(self.dbHostLabel, 4, 0, 1, 1)
        self.dbHostLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.dbHostLineEdit.setObjectName(_fromUtf8("dbHostLineEdit"))
        self.gridLayout.addWidget(self.dbHostLineEdit, 4, 1, 1, 1)
        self.dbPortLabel = QtGui.QLabel(self.layoutWidget)
        self.dbPortLabel.setObjectName(_fromUtf8("dbPortLabel"))
        self.gridLayout.addWidget(self.dbPortLabel, 4, 2, 1, 1)
        self.dbPortLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.dbPortLineEdit.setObjectName(_fromUtf8("dbPortLineEdit"))
        self.gridLayout.addWidget(self.dbPortLineEdit, 4, 3, 1, 1)
        self.label = QtGui.QLabel(wizardPage2)
        self.label.setGeometry(QtCore.QRect(10, 201, 121, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(wizardPage2)
        QtCore.QMetaObject.connectSlotsByName(wizardPage2)

    def retranslateUi(self, wizardPage2):
        wizardPage2.setWindowTitle(_translate("wizardPage2", "WizardPage", None))
        wizardPage2.setTitle(_translate("wizardPage2", "Database Parameters", None))
        wizardPage2.setSubTitle(_translate("wizardPage2", "Select the database type that you want to use and the parameters required for that database type. You will be able to change some of these settings later by selecting \"Configuration Wizard...\" in the Edit menu.", None))
        self.connectionTestInstructionLabel.setText(_translate("wizardPage2", "Click Test Connection when done. The connection test must pass before continuing.", None))
        self.testConnectionPushButton.setText(_translate("wizardPage2", "Test Connection", None))
        self.dbTypeLabel.setText(_translate("wizardPage2", "Database Type:", None))
        self.dbTypeComboBox.setToolTip(_translate("wizardPage2", "Select the database type to use", None))
        self.dbFileNameLabel.setText(_translate("wizardPage2", "Database File Name: *", None))
        self.dbFileNameLineEdit.setToolTip(_translate("wizardPage2", "Enter the full path to the database file and the database file name", None))
        self.dbNameLabel.setText(_translate("wizardPage2", "Database Name: *", None))
        self.dbNameLineEdit.setToolTip(_translate("wizardPage2", "Enter the name of the database", None))
        self.dbUserNameLabel.setText(_translate("wizardPage2", "User Name: *", None))
        self.dbUserNameLineEdit.setToolTip(_translate("wizardPage2", "Enter the database user name", None))
        self.dbPasswordLabel.setText(_translate("wizardPage2", "Password: *", None))
        self.dbPasswordLineEdit.setToolTip(_translate("wizardPage2", "Enter the database password", None))
        self.dbHostLabel.setText(_translate("wizardPage2", "Host: *", None))
        self.dbHostLineEdit.setToolTip(_translate("wizardPage2", "Enter the database host", None))
        self.dbPortLabel.setText(_translate("wizardPage2", "Port:", None))
        self.dbPortLineEdit.setToolTip(_translate("wizardPage2", "Enter the database port", None))
        self.label.setText(_translate("wizardPage2", "* indicates required fields", None))

