# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'purchaseordersdialog.ui'
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

class Ui_purchaseOrdersDialog(object):
    def setupUi(self, purchaseOrdersDialog):
        purchaseOrdersDialog.setObjectName(_fromUtf8("purchaseOrdersDialog"))
        purchaseOrdersDialog.resize(800, 498)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/podbicon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        purchaseOrdersDialog.setWindowIcon(icon)
        self.buttonBox = QtGui.QDialogButtonBox(purchaseOrdersDialog)
        self.buttonBox.setGeometry(QtCore.QRect(450, 455, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.purchaseOrdersGroupBox = QtGui.QGroupBox(purchaseOrdersDialog)
        self.purchaseOrdersGroupBox.setGeometry(QtCore.QRect(-1, 9, 801, 441))
        self.purchaseOrdersGroupBox.setObjectName(_fromUtf8("purchaseOrdersGroupBox"))
        self.tableView = QtGui.QTableView(self.purchaseOrdersGroupBox)
        self.tableView.setGeometry(QtCore.QRect(10, 20, 781, 401))
        self.tableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableView.setObjectName(_fromUtf8("tableView"))

        self.retranslateUi(purchaseOrdersDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), purchaseOrdersDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), purchaseOrdersDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(purchaseOrdersDialog)

    def retranslateUi(self, purchaseOrdersDialog):
        purchaseOrdersDialog.setWindowTitle(_translate("purchaseOrdersDialog", "Open Purchase Order", None))
        self.purchaseOrdersGroupBox.setTitle(_translate("purchaseOrdersDialog", "Purchase Orders", None))

import resources_rc
