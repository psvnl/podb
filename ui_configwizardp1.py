# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configwizardp1.ui'
#
# Created: Wed May 25 13:43:27 2016
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

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName(_fromUtf8("WizardPage"))
        WizardPage.resize(545, 310)
        self.paragraph3Label = QtGui.QLabel(WizardPage)
        self.paragraph3Label.setGeometry(QtCore.QRect(70, 240, 411, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.paragraph3Label.setFont(font)
        self.paragraph3Label.setWordWrap(True)
        self.paragraph3Label.setObjectName(_fromUtf8("paragraph3Label"))
        self.paragraph2Label = QtGui.QLabel(WizardPage)
        self.paragraph2Label.setGeometry(QtCore.QRect(70, 190, 411, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.paragraph2Label.setFont(font)
        self.paragraph2Label.setWordWrap(True)
        self.paragraph2Label.setObjectName(_fromUtf8("paragraph2Label"))
        self.paragraph1Label = QtGui.QLabel(WizardPage)
        self.paragraph1Label.setGeometry(QtCore.QRect(70, 140, 411, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.paragraph1Label.setFont(font)
        self.paragraph1Label.setWordWrap(True)
        self.paragraph1Label.setObjectName(_fromUtf8("paragraph1Label"))
        self.label = QtGui.QLabel(WizardPage)
        self.label.setGeometry(QtCore.QRect(70, 50, 411, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.paragraph3Label.setText(_translate("WizardPage", "Click Next to get started...", None))
        self.paragraph2Label.setText(_translate("WizardPage", "This wizard runs when the configuration file is not found at start-up, or when there are errors in the configuration.", None))
        self.paragraph1Label.setText(_translate("WizardPage", "The POdB application stores application settings in a configuration file, and user settings in the database itself.", None))
        self.label.setText(_translate("WizardPage", "POdB Application Configuration Wizard", None))

