# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'productsdialog.ui'
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

class Ui_productsDialog(object):
    def setupUi(self, productsDialog):
        productsDialog.setObjectName(_fromUtf8("productsDialog"))
        productsDialog.resize(800, 498)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/podbicon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        productsDialog.setWindowIcon(icon)
        self.supplierGroupBox = QtGui.QGroupBox(productsDialog)
        self.supplierGroupBox.setGeometry(QtCore.QRect(0, 10, 801, 80))
        self.supplierGroupBox.setObjectName(_fromUtf8("supplierGroupBox"))
        self.supplierComboBox = QtGui.QComboBox(self.supplierGroupBox)
        self.supplierComboBox.setGeometry(QtCore.QRect(11, 23, 251, 20))
        self.supplierComboBox.setObjectName(_fromUtf8("supplierComboBox"))
        self.layoutWidget = QtGui.QWidget(self.supplierGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(280, 14, 512, 40))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_11 = QtGui.QLabel(self.layoutWidget)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.layoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 0, 2, 1, 1)
        self.supplierPhoneLabel = QtGui.QLabel(self.layoutWidget)
        self.supplierPhoneLabel.setText(_fromUtf8(""))
        self.supplierPhoneLabel.setObjectName(_fromUtf8("supplierPhoneLabel"))
        self.gridLayout.addWidget(self.supplierPhoneLabel, 0, 3, 1, 1)
        self.label_9 = QtGui.QLabel(self.layoutWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 1, 2, 1, 1)
        self.supplierFaxLabel = QtGui.QLabel(self.layoutWidget)
        self.supplierFaxLabel.setText(_fromUtf8(""))
        self.supplierFaxLabel.setObjectName(_fromUtf8("supplierFaxLabel"))
        self.gridLayout.addWidget(self.supplierFaxLabel, 1, 3, 1, 1)
        self.supplierAddressLabel = QtGui.QLabel(self.layoutWidget)
        self.supplierAddressLabel.setText(_fromUtf8(""))
        self.supplierAddressLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.supplierAddressLabel.setWordWrap(True)
        self.supplierAddressLabel.setObjectName(_fromUtf8("supplierAddressLabel"))
        self.gridLayout.addWidget(self.supplierAddressLabel, 0, 1, 2, 1)
        self.gridLayout.setColumnMinimumWidth(0, 80)
        self.gridLayout.setColumnMinimumWidth(1, 166)
        self.gridLayout.setColumnMinimumWidth(2, 80)
        self.gridLayout.setColumnMinimumWidth(3, 166)
        self.gridLayout.setRowMinimumHeight(0, 16)
        self.gridLayout.setRowMinimumHeight(1, 16)
        self.label_7 = QtGui.QLabel(self.supplierGroupBox)
        self.label_7.setGeometry(QtCore.QRect(11, 58, 78, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_10 = QtGui.QLabel(self.supplierGroupBox)
        self.label_10.setGeometry(QtCore.QRect(280, 58, 28, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.supplierEmailLabel = QtGui.QLabel(self.supplierGroupBox)
        self.supplierEmailLabel.setGeometry(QtCore.QRect(365, 58, 421, 16))
        self.supplierEmailLabel.setText(_fromUtf8(""))
        self.supplierEmailLabel.setObjectName(_fromUtf8("supplierEmailLabel"))
        self.supplierContactLabel = QtGui.QLabel(self.supplierGroupBox)
        self.supplierContactLabel.setGeometry(QtCore.QRect(102, 58, 151, 16))
        self.supplierContactLabel.setText(_fromUtf8(""))
        self.supplierContactLabel.setObjectName(_fromUtf8("supplierContactLabel"))
        self.productsGroupBox = QtGui.QGroupBox(productsDialog)
        self.productsGroupBox.setGeometry(QtCore.QRect(-1, 99, 801, 351))
        self.productsGroupBox.setObjectName(_fromUtf8("productsGroupBox"))
        self.tableView = QtGui.QTableView(self.productsGroupBox)
        self.tableView.setGeometry(QtCore.QRect(10, 20, 781, 291))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.addRowPushButton = QtGui.QPushButton(self.productsGroupBox)
        self.addRowPushButton.setGeometry(QtCore.QRect(10, 320, 75, 23))
        self.addRowPushButton.setObjectName(_fromUtf8("addRowPushButton"))
        self.cancelPushButton = QtGui.QPushButton(productsDialog)
        self.cancelPushButton.setGeometry(QtCore.QRect(690, 460, 100, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelPushButton.sizePolicy().hasHeightForWidth())
        self.cancelPushButton.setSizePolicy(sizePolicy)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.savePushButton = QtGui.QPushButton(productsDialog)
        self.savePushButton.setGeometry(QtCore.QRect(580, 460, 100, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.savePushButton.sizePolicy().hasHeightForWidth())
        self.savePushButton.setSizePolicy(sizePolicy)
        self.savePushButton.setObjectName(_fromUtf8("savePushButton"))

        self.retranslateUi(productsDialog)
        QtCore.QMetaObject.connectSlotsByName(productsDialog)

    def retranslateUi(self, productsDialog):
        productsDialog.setWindowTitle(_translate("productsDialog", "Edit Products", None))
        self.supplierGroupBox.setTitle(_translate("productsDialog", "Supplier", None))
        self.label_11.setText(_translate("productsDialog", "Address:", None))
        self.label_8.setText(_translate("productsDialog", "Phone Number:", None))
        self.label_9.setText(_translate("productsDialog", "Fax Number:", None))
        self.label_7.setText(_translate("productsDialog", "Contact Person:", None))
        self.label_10.setText(_translate("productsDialog", "Email:", None))
        self.productsGroupBox.setTitle(_translate("productsDialog", "Products", None))
        self.addRowPushButton.setToolTip(_translate("productsDialog", "Add a new product to the table", None))
        self.addRowPushButton.setText(_translate("productsDialog", "Add Product", None))
        self.cancelPushButton.setToolTip(_translate("productsDialog", "Close the dialog, discarding any changes", None))
        self.cancelPushButton.setText(_translate("productsDialog", "Cancel", None))
        self.savePushButton.setToolTip(_translate("productsDialog", "Save changes and close the dialog", None))
        self.savePushButton.setText(_translate("productsDialog", "Save Changes", None))

import resources_rc
