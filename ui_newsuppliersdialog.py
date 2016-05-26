# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newsuppliersdialog.ui'
#
# Created: Sat Apr 30 20:53:28 2016
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
        suppliersDialog.resize(900, 503)
        self.buttonBox = QtGui.QDialogButtonBox(suppliersDialog)
        self.buttonBox.setGeometry(QtCore.QRect(550, 460, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Discard|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.suppliersGroupBox = QtGui.QGroupBox(suppliersDialog)
        self.suppliersGroupBox.setGeometry(QtCore.QRect(-1, 9, 901, 441))
        self.suppliersGroupBox.setObjectName(_fromUtf8("suppliersGroupBox"))
        self.tableView = QtGui.QTableView(self.suppliersGroupBox)
        self.tableView.setGeometry(QtCore.QRect(10, 20, 881, 381))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.addRowPushButton = QtGui.QPushButton(self.suppliersGroupBox)
        self.addRowPushButton.setGeometry(QtCore.QRect(10, 410, 75, 23))
        self.addRowPushButton.setObjectName(_fromUtf8("addRowPushButton"))

        self.retranslateUi(suppliersDialog)
        QtCore.QMetaObject.connectSlotsByName(suppliersDialog)

    def retranslateUi(self, suppliersDialog):
        suppliersDialog.setWindowTitle(_translate("suppliersDialog", "Edit Suppliers", None))
        self.suppliersGroupBox.setTitle(_translate("suppliersDialog", "Suppliers", None))
        self.addRowPushButton.setText(_translate("suppliersDialog", "Add Row", None))

