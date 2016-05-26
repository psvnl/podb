# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'suppliersdialog.ui'
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

class Ui_suppliersDialog(object):
    def setupUi(self, suppliersDialog):
        suppliersDialog.setObjectName(_fromUtf8("suppliersDialog"))
        suppliersDialog.resize(900, 498)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/podbicon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        suppliersDialog.setWindowIcon(icon)
        self.suppliersGroupBox = QtGui.QGroupBox(suppliersDialog)
        self.suppliersGroupBox.setGeometry(QtCore.QRect(-1, 9, 901, 441))
        self.suppliersGroupBox.setObjectName(_fromUtf8("suppliersGroupBox"))
        self.tableView = QtGui.QTableView(self.suppliersGroupBox)
        self.tableView.setGeometry(QtCore.QRect(10, 20, 881, 381))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.addRowPushButton = QtGui.QPushButton(self.suppliersGroupBox)
        self.addRowPushButton.setGeometry(QtCore.QRect(10, 410, 75, 23))
        self.addRowPushButton.setObjectName(_fromUtf8("addRowPushButton"))
        self.savePushButton = QtGui.QPushButton(suppliersDialog)
        self.savePushButton.setGeometry(QtCore.QRect(680, 460, 100, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.savePushButton.sizePolicy().hasHeightForWidth())
        self.savePushButton.setSizePolicy(sizePolicy)
        self.savePushButton.setObjectName(_fromUtf8("savePushButton"))
        self.cancelPushButton = QtGui.QPushButton(suppliersDialog)
        self.cancelPushButton.setGeometry(QtCore.QRect(790, 460, 100, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelPushButton.sizePolicy().hasHeightForWidth())
        self.cancelPushButton.setSizePolicy(sizePolicy)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))

        self.retranslateUi(suppliersDialog)
        QtCore.QMetaObject.connectSlotsByName(suppliersDialog)

    def retranslateUi(self, suppliersDialog):
        suppliersDialog.setWindowTitle(_translate("suppliersDialog", "Edit Suppliers", None))
        self.suppliersGroupBox.setTitle(_translate("suppliersDialog", "Suppliers", None))
        self.addRowPushButton.setToolTip(_translate("suppliersDialog", "Add a new supplier to the table", None))
        self.addRowPushButton.setText(_translate("suppliersDialog", "Add Supplier", None))
        self.savePushButton.setToolTip(_translate("suppliersDialog", "Save changes and close the dialog", None))
        self.savePushButton.setText(_translate("suppliersDialog", "Save Changes", None))
        self.cancelPushButton.setToolTip(_translate("suppliersDialog", "Close the dialog, discarding any changes", None))
        self.cancelPushButton.setText(_translate("suppliersDialog", "Cancel", None))

import resources_rc
