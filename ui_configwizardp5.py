# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configwizardp5.ui'
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

class Ui_wizardPage5(object):
    def setupUi(self, wizardPage5):
        wizardPage5.setObjectName(_fromUtf8("wizardPage5"))
        wizardPage5.resize(545, 310)
        self.layoutWidget = QtGui.QWidget(wizardPage5)
        self.layoutWidget.setGeometry(QtCore.QRect(140, 80, 256, 121))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_4 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.poDefaultPaymentTermsLabel = QtGui.QLabel(self.layoutWidget)
        self.poDefaultPaymentTermsLabel.setObjectName(_fromUtf8("poDefaultPaymentTermsLabel"))
        self.gridLayout_4.addWidget(self.poDefaultPaymentTermsLabel, 0, 0, 1, 1)
        self.poDefaultPaymentTermsComboBox = QtGui.QComboBox(self.layoutWidget)
        self.poDefaultPaymentTermsComboBox.setObjectName(_fromUtf8("poDefaultPaymentTermsComboBox"))
        self.gridLayout_4.addWidget(self.poDefaultPaymentTermsComboBox, 0, 1, 1, 1)
        self.poDefaultOrderStatusLabel = QtGui.QLabel(self.layoutWidget)
        self.poDefaultOrderStatusLabel.setObjectName(_fromUtf8("poDefaultOrderStatusLabel"))
        self.gridLayout_4.addWidget(self.poDefaultOrderStatusLabel, 1, 0, 1, 1)
        self.poDefaultOrderStatusComboBox = QtGui.QComboBox(self.layoutWidget)
        self.poDefaultOrderStatusComboBox.setObjectName(_fromUtf8("poDefaultOrderStatusComboBox"))
        self.gridLayout_4.addWidget(self.poDefaultOrderStatusComboBox, 1, 1, 1, 1)
        self.locTaxRateLabel = QtGui.QLabel(self.layoutWidget)
        self.locTaxRateLabel.setObjectName(_fromUtf8("locTaxRateLabel"))
        self.gridLayout_4.addWidget(self.locTaxRateLabel, 2, 0, 1, 1)
        self.locTaxRateLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.locTaxRateLineEdit.setObjectName(_fromUtf8("locTaxRateLineEdit"))
        self.gridLayout_4.addWidget(self.locTaxRateLineEdit, 2, 1, 1, 1)
        self.label = QtGui.QLabel(wizardPage5)
        self.label.setGeometry(QtCore.QRect(140, 200, 121, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(wizardPage5)
        QtCore.QMetaObject.connectSlotsByName(wizardPage5)

    def retranslateUi(self, wizardPage5):
        wizardPage5.setWindowTitle(_translate("wizardPage5", "WizardPage", None))
        wizardPage5.setTitle(_translate("wizardPage5", "Miscellaneous Settings", None))
        wizardPage5.setSubTitle(_translate("wizardPage5", "Select the default payment terms, order status and the tax rate. You will be able to change these settings later by selecting \"Configuration Wizard...\" in the Edit menu.", None))
        self.poDefaultPaymentTermsLabel.setText(_translate("wizardPage5", "Default Payment Terms:", None))
        self.poDefaultPaymentTermsComboBox.setToolTip(_translate("wizardPage5", "Select the default payment terms", None))
        self.poDefaultOrderStatusLabel.setText(_translate("wizardPage5", "Default Order Status:", None))
        self.poDefaultOrderStatusComboBox.setToolTip(_translate("wizardPage5", "Select the default order status", None))
        self.locTaxRateLabel.setText(_translate("wizardPage5", "Tax Rate: *", None))
        self.locTaxRateLineEdit.setToolTip(_translate("wizardPage5", "Enter the tax rate as a decimal, e.g., 0.14 for 14%", None))
        self.label.setText(_translate("wizardPage5", "* indicates required fields", None))

