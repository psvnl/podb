# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configwizard.ui'
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

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        Wizard.setObjectName(_fromUtf8("Wizard"))
        Wizard.resize(563, 406)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/podbicon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Wizard.setWindowIcon(icon)
        Wizard.setWizardStyle(QtGui.QWizard.ModernStyle)

        self.retranslateUi(Wizard)
        QtCore.QMetaObject.connectSlotsByName(Wizard)

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(_translate("Wizard", "POdB Configuration Wizard", None))

import resources_rc
