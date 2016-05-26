# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configwizardp4.ui'
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

class Ui_wizardPage4(object):
    def setupUi(self, wizardPage4):
        wizardPage4.setObjectName(_fromUtf8("wizardPage4"))
        wizardPage4.resize(545, 310)
        self.coPostalAddressLabel = QtGui.QLabel(wizardPage4)
        self.coPostalAddressLabel.setGeometry(QtCore.QRect(279, 10, 95, 20))
        self.coPostalAddressLabel.setObjectName(_fromUtf8("coPostalAddressLabel"))
        self.coPostalAddressPlainTextEdit = QtGui.QPlainTextEdit(wizardPage4)
        self.coPostalAddressPlainTextEdit.setGeometry(QtCore.QRect(380, 10, 150, 62))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coPostalAddressPlainTextEdit.sizePolicy().hasHeightForWidth())
        self.coPostalAddressPlainTextEdit.setSizePolicy(sizePolicy)
        self.coPostalAddressPlainTextEdit.setObjectName(_fromUtf8("coPostalAddressPlainTextEdit"))
        self.coPhysicalAddressPlainTextEdit = QtGui.QPlainTextEdit(wizardPage4)
        self.coPhysicalAddressPlainTextEdit.setGeometry(QtCore.QRect(111, 10, 150, 62))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coPhysicalAddressPlainTextEdit.sizePolicy().hasHeightForWidth())
        self.coPhysicalAddressPlainTextEdit.setSizePolicy(sizePolicy)
        self.coPhysicalAddressPlainTextEdit.setObjectName(_fromUtf8("coPhysicalAddressPlainTextEdit"))
        self.layoutWidget_2 = QtGui.QWidget(wizardPage4)
        self.layoutWidget_2.setGeometry(QtCore.QRect(9, 77, 523, 191))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.layoutWidget_2)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.coGpsCoordsLabel = QtGui.QLabel(self.layoutWidget_2)
        self.coGpsCoordsLabel.setObjectName(_fromUtf8("coGpsCoordsLabel"))
        self.gridLayout_4.addWidget(self.coGpsCoordsLabel, 0, 0, 1, 1)
        self.coGpsCoordsLineEdit = QtGui.QLineEdit(self.layoutWidget_2)
        self.coGpsCoordsLineEdit.setObjectName(_fromUtf8("coGpsCoordsLineEdit"))
        self.gridLayout_4.addWidget(self.coGpsCoordsLineEdit, 0, 1, 1, 1)
        self.coTelephoneLabel = QtGui.QLabel(self.layoutWidget_2)
        self.coTelephoneLabel.setObjectName(_fromUtf8("coTelephoneLabel"))
        self.gridLayout_4.addWidget(self.coTelephoneLabel, 1, 0, 1, 1)
        self.coTelephoneLineEdit = QtGui.QLineEdit(self.layoutWidget_2)
        self.coTelephoneLineEdit.setObjectName(_fromUtf8("coTelephoneLineEdit"))
        self.gridLayout_4.addWidget(self.coTelephoneLineEdit, 1, 1, 1, 1)
        self.coFaxLabel = QtGui.QLabel(self.layoutWidget_2)
        self.coFaxLabel.setObjectName(_fromUtf8("coFaxLabel"))
        self.gridLayout_4.addWidget(self.coFaxLabel, 1, 2, 1, 1)
        self.coFaxLineEdit = QtGui.QLineEdit(self.layoutWidget_2)
        self.coFaxLineEdit.setObjectName(_fromUtf8("coFaxLineEdit"))
        self.gridLayout_4.addWidget(self.coFaxLineEdit, 1, 3, 1, 1)
        self.coEmailLabel = QtGui.QLabel(self.layoutWidget_2)
        self.coEmailLabel.setObjectName(_fromUtf8("coEmailLabel"))
        self.gridLayout_4.addWidget(self.coEmailLabel, 2, 0, 1, 1)
        self.coEmailLineEdit = QtGui.QLineEdit(self.layoutWidget_2)
        self.coEmailLineEdit.setObjectName(_fromUtf8("coEmailLineEdit"))
        self.gridLayout_4.addWidget(self.coEmailLineEdit, 2, 1, 1, 2)
        self.coWebLabel = QtGui.QLabel(self.layoutWidget_2)
        self.coWebLabel.setObjectName(_fromUtf8("coWebLabel"))
        self.gridLayout_4.addWidget(self.coWebLabel, 3, 0, 1, 1)
        self.coWebLineEdit = QtGui.QLineEdit(self.layoutWidget_2)
        self.coWebLineEdit.setObjectName(_fromUtf8("coWebLineEdit"))
        self.gridLayout_4.addWidget(self.coWebLineEdit, 3, 1, 1, 2)
        self.coSignatoryLabel = QtGui.QLabel(self.layoutWidget_2)
        self.coSignatoryLabel.setObjectName(_fromUtf8("coSignatoryLabel"))
        self.gridLayout_4.addWidget(self.coSignatoryLabel, 4, 0, 1, 1)
        self.coSignatureFileLabel = QtGui.QLabel(self.layoutWidget_2)
        self.coSignatureFileLabel.setObjectName(_fromUtf8("coSignatureFileLabel"))
        self.gridLayout_4.addWidget(self.coSignatureFileLabel, 5, 0, 1, 1)
        self.coSignatureFileLineEdit = QtGui.QLineEdit(self.layoutWidget_2)
        self.coSignatureFileLineEdit.setObjectName(_fromUtf8("coSignatureFileLineEdit"))
        self.gridLayout_4.addWidget(self.coSignatureFileLineEdit, 5, 1, 1, 3)
        self.coSignatureFilePushButton = QtGui.QPushButton(self.layoutWidget_2)
        self.coSignatureFilePushButton.setObjectName(_fromUtf8("coSignatureFilePushButton"))
        self.gridLayout_4.addWidget(self.coSignatureFilePushButton, 5, 4, 1, 1)
        self.coLogoFileLabel = QtGui.QLabel(self.layoutWidget_2)
        self.coLogoFileLabel.setObjectName(_fromUtf8("coLogoFileLabel"))
        self.gridLayout_4.addWidget(self.coLogoFileLabel, 6, 0, 1, 1)
        self.coLogoFileLineEdit = QtGui.QLineEdit(self.layoutWidget_2)
        self.coLogoFileLineEdit.setObjectName(_fromUtf8("coLogoFileLineEdit"))
        self.gridLayout_4.addWidget(self.coLogoFileLineEdit, 6, 1, 1, 3)
        self.coLogoFilePushButton = QtGui.QPushButton(self.layoutWidget_2)
        self.coLogoFilePushButton.setObjectName(_fromUtf8("coLogoFilePushButton"))
        self.gridLayout_4.addWidget(self.coLogoFilePushButton, 6, 4, 1, 1)
        self.coSignatoryLineEdit = QtGui.QLineEdit(self.layoutWidget_2)
        self.coSignatoryLineEdit.setObjectName(_fromUtf8("coSignatoryLineEdit"))
        self.gridLayout_4.addWidget(self.coSignatoryLineEdit, 4, 1, 1, 2)
        self.coPhysicalAddressLabel = QtGui.QLabel(wizardPage4)
        self.coPhysicalAddressLabel.setGeometry(QtCore.QRect(10, 10, 95, 20))
        self.coPhysicalAddressLabel.setObjectName(_fromUtf8("coPhysicalAddressLabel"))
        self.label = QtGui.QLabel(wizardPage4)
        self.label.setGeometry(QtCore.QRect(10, 268, 121, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(wizardPage4)
        QtCore.QMetaObject.connectSlotsByName(wizardPage4)

    def retranslateUi(self, wizardPage4):
        wizardPage4.setWindowTitle(_translate("wizardPage4", "WizardPage", None))
        wizardPage4.setTitle(_translate("wizardPage4", "Company Details", None))
        wizardPage4.setSubTitle(_translate("wizardPage4", "Fill in the details of your company. You will be able to change these settings later by selecting \"Configuration Wizard...\" in the Edit menu.", None))
        self.coPostalAddressLabel.setText(_translate("wizardPage4", "Postal Address: *", None))
        self.coPostalAddressPlainTextEdit.setToolTip(_translate("wizardPage4", "Enter the company postal address", None))
        self.coPhysicalAddressPlainTextEdit.setToolTip(_translate("wizardPage4", "Enter the company physical address", None))
        self.coGpsCoordsLabel.setText(_translate("wizardPage4", "GPS Coordinates:", None))
        self.coGpsCoordsLineEdit.setToolTip(_translate("wizardPage4", "Enter the company\'s GPS coordinates", None))
        self.coTelephoneLabel.setText(_translate("wizardPage4", "Telephone Number: *", None))
        self.coTelephoneLineEdit.setToolTip(_translate("wizardPage4", "Enter the company\'s telephone number", None))
        self.coFaxLabel.setText(_translate("wizardPage4", "Fax Number:", None))
        self.coFaxLineEdit.setToolTip(_translate("wizardPage4", "Enter the company\'s fax number", None))
        self.coEmailLabel.setText(_translate("wizardPage4", "Email Address:", None))
        self.coEmailLineEdit.setToolTip(_translate("wizardPage4", "Enter the company\'s email address", None))
        self.coWebLabel.setText(_translate("wizardPage4", "Web Address:", None))
        self.coWebLineEdit.setToolTip(_translate("wizardPage4", "Enter the company\'s web address", None))
        self.coSignatoryLabel.setText(_translate("wizardPage4", "Signatory Name: *", None))
        self.coSignatureFileLabel.setText(_translate("wizardPage4", "Signature Filename:", None))
        self.coSignatureFileLineEdit.setToolTip(_translate("wizardPage4", "Enter or browse for the signature image file that should appear on the PDF of the purchase order.", None))
        self.coSignatureFilePushButton.setText(_translate("wizardPage4", "Browse...", None))
        self.coLogoFileLabel.setText(_translate("wizardPage4", "Logo Filename:", None))
        self.coLogoFileLineEdit.setToolTip(_translate("wizardPage4", "Enter or browse for the company logo image file that should appear on the letterhead of the PDF of the purchase order.", None))
        self.coLogoFilePushButton.setText(_translate("wizardPage4", "Browse...", None))
        self.coSignatoryLineEdit.setToolTip(_translate("wizardPage4", "Enter the name of the person that signs the purchase orders", None))
        self.coPhysicalAddressLabel.setText(_translate("wizardPage4", "Physical Address: *", None))
        self.label.setText(_translate("wizardPage4", "* indicates required fields", None))

