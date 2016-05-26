# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'projectsdialog.ui'
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

class Ui_projectsDialog(object):
    def setupUi(self, projectsDialog):
        projectsDialog.setObjectName(_fromUtf8("projectsDialog"))
        projectsDialog.resize(520, 289)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/podbicon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        projectsDialog.setWindowIcon(icon)
        self.projectsGroupBox = QtGui.QGroupBox(projectsDialog)
        self.projectsGroupBox.setGeometry(QtCore.QRect(0, 10, 521, 231))
        self.projectsGroupBox.setObjectName(_fromUtf8("projectsGroupBox"))
        self.tableView = QtGui.QTableView(self.projectsGroupBox)
        self.tableView.setGeometry(QtCore.QRect(10, 20, 501, 171))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.addRowPushButton = QtGui.QPushButton(self.projectsGroupBox)
        self.addRowPushButton.setGeometry(QtCore.QRect(10, 200, 75, 23))
        self.addRowPushButton.setObjectName(_fromUtf8("addRowPushButton"))
        self.savePushButton = QtGui.QPushButton(projectsDialog)
        self.savePushButton.setGeometry(QtCore.QRect(300, 250, 100, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.savePushButton.sizePolicy().hasHeightForWidth())
        self.savePushButton.setSizePolicy(sizePolicy)
        self.savePushButton.setObjectName(_fromUtf8("savePushButton"))
        self.cancelPushButton = QtGui.QPushButton(projectsDialog)
        self.cancelPushButton.setGeometry(QtCore.QRect(410, 250, 100, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelPushButton.sizePolicy().hasHeightForWidth())
        self.cancelPushButton.setSizePolicy(sizePolicy)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))

        self.retranslateUi(projectsDialog)
        QtCore.QMetaObject.connectSlotsByName(projectsDialog)

    def retranslateUi(self, projectsDialog):
        projectsDialog.setWindowTitle(_translate("projectsDialog", "Edit Projects", None))
        self.projectsGroupBox.setTitle(_translate("projectsDialog", "Projects", None))
        self.addRowPushButton.setToolTip(_translate("projectsDialog", "Add a new project to the table", None))
        self.addRowPushButton.setText(_translate("projectsDialog", "Add Project", None))
        self.savePushButton.setToolTip(_translate("projectsDialog", "Save changes and close the dialog", None))
        self.savePushButton.setText(_translate("projectsDialog", "Save Changes", None))
        self.cancelPushButton.setToolTip(_translate("projectsDialog", "Close the dialog, discarding any changes", None))
        self.cancelPushButton.setText(_translate("projectsDialog", "Cancel", None))

import resources_rc
