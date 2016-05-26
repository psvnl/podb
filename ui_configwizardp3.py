# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configwizardp3.ui'
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

class Ui_wizardPage3(object):
    def setupUi(self, wizardPage3):
        wizardPage3.setObjectName(_fromUtf8("wizardPage3"))
        wizardPage3.resize(545, 310)
        self.layoutWidget = QtGui.QWidget(wizardPage3)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 50, 521, 171))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.coNameLabel = QtGui.QLabel(self.layoutWidget)
        self.coNameLabel.setObjectName(_fromUtf8("coNameLabel"))
        self.gridLayout_2.addWidget(self.coNameLabel, 0, 0, 1, 1)
        self.coNameLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.coNameLineEdit.setObjectName(_fromUtf8("coNameLineEdit"))
        self.gridLayout_2.addWidget(self.coNameLineEdit, 0, 1, 1, 1)
        self.poPrefixLabel = QtGui.QLabel(self.layoutWidget)
        self.poPrefixLabel.setObjectName(_fromUtf8("poPrefixLabel"))
        self.gridLayout_2.addWidget(self.poPrefixLabel, 1, 0, 1, 1)
        self.poPrefixLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.poPrefixLineEdit.setObjectName(_fromUtf8("poPrefixLineEdit"))
        self.gridLayout_2.addWidget(self.poPrefixLineEdit, 1, 1, 1, 1)
        self.locCurrencySymbolLabel = QtGui.QLabel(self.layoutWidget)
        self.locCurrencySymbolLabel.setObjectName(_fromUtf8("locCurrencySymbolLabel"))
        self.gridLayout_2.addWidget(self.locCurrencySymbolLabel, 2, 0, 1, 1)
        self.locCurrencySymbolLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.locCurrencySymbolLineEdit.setObjectName(_fromUtf8("locCurrencySymbolLineEdit"))
        self.gridLayout_2.addWidget(self.locCurrencySymbolLineEdit, 2, 1, 1, 1)
        self.locCurrencyDecPlacesLabel = QtGui.QLabel(self.layoutWidget)
        self.locCurrencyDecPlacesLabel.setObjectName(_fromUtf8("locCurrencyDecPlacesLabel"))
        self.gridLayout_2.addWidget(self.locCurrencyDecPlacesLabel, 3, 0, 1, 1)
        self.locTaxNameLabel = QtGui.QLabel(self.layoutWidget)
        self.locTaxNameLabel.setObjectName(_fromUtf8("locTaxNameLabel"))
        self.gridLayout_2.addWidget(self.locTaxNameLabel, 4, 0, 1, 1)
        self.locTaxNameLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.locTaxNameLineEdit.setObjectName(_fromUtf8("locTaxNameLineEdit"))
        self.gridLayout_2.addWidget(self.locTaxNameLineEdit, 4, 1, 1, 1)
        self.locCurrencyDecPlacesComboBox = QtGui.QComboBox(self.layoutWidget)
        self.locCurrencyDecPlacesComboBox.setObjectName(_fromUtf8("locCurrencyDecPlacesComboBox"))
        self.gridLayout_2.addWidget(self.locCurrencyDecPlacesComboBox, 3, 1, 1, 1)
        self.label = QtGui.QLabel(wizardPage3)
        self.label.setGeometry(QtCore.QRect(10, 221, 121, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(wizardPage3)
        QtCore.QMetaObject.connectSlotsByName(wizardPage3)

    def retranslateUi(self, wizardPage3):
        wizardPage3.setWindowTitle(_translate("wizardPage3", "WizardPage", None))
        wizardPage3.setTitle(_translate("wizardPage3", "Essential Settings", None))
        wizardPage3.setSubTitle(_translate("wizardPage3", "Set up essential settings that are required by the application. You will not be able to change these settings later.", None))
        self.coNameLabel.setText(_translate("wizardPage3", "Company Name: *", None))
        self.coNameLineEdit.setToolTip(_translate("wizardPage3", "Enter the name of the company whose application this is", None))
        self.poPrefixLabel.setText(_translate("wizardPage3", "Order Number Prefix:", None))
        self.poPrefixLineEdit.setToolTip(_translate("wizardPage3", "Enter the prefix that appears before the five-digit purchase order number", None))
        self.locCurrencySymbolLabel.setText(_translate("wizardPage3", "Currency Symbol: *", None))
        self.locCurrencySymbolLineEdit.setToolTip(_translate("wizardPage3", "Enter the symbol of the local currency", None))
        self.locCurrencyDecPlacesLabel.setText(_translate("wizardPage3", "Currency Decimal Places:", None))
        self.locTaxNameLabel.setText(_translate("wizardPage3", "Tax Name: *", None))
        self.locTaxNameLineEdit.setToolTip(_translate("wizardPage3", "Enter the name of the tax applicable to the purchase order", None))
        self.label.setText(_translate("wizardPage3", "* indicates required fields", None))

