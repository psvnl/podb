# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 752)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/podbicon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.statusBarLabel = QtGui.QLabel(self.centralwidget)
        self.statusBarLabel.setGeometry(QtCore.QRect(0, 690, 801, 20))
        self.statusBarLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.statusBarLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.statusBarLabel.setText(_fromUtf8(""))
        self.statusBarLabel.setObjectName(_fromUtf8("statusBarLabel"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 801, 31))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.clearToolButton = QtGui.QToolButton(self.frame)
        self.clearToolButton.setGeometry(QtCore.QRect(90, 0, 32, 32))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/clear.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearToolButton.setIcon(icon1)
        self.clearToolButton.setIconSize(QtCore.QSize(32, 32))
        self.clearToolButton.setObjectName(_fromUtf8("clearToolButton"))
        self.saveToolButton = QtGui.QToolButton(self.frame)
        self.saveToolButton.setGeometry(QtCore.QRect(60, 0, 32, 32))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveToolButton.setIcon(icon2)
        self.saveToolButton.setIconSize(QtCore.QSize(32, 32))
        self.saveToolButton.setObjectName(_fromUtf8("saveToolButton"))
        self.openToolButton = QtGui.QToolButton(self.frame)
        self.openToolButton.setGeometry(QtCore.QRect(30, 0, 32, 32))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openToolButton.setIcon(icon3)
        self.openToolButton.setIconSize(QtCore.QSize(32, 32))
        self.openToolButton.setObjectName(_fromUtf8("openToolButton"))
        self.newToolButton = QtGui.QToolButton(self.frame)
        self.newToolButton.setGeometry(QtCore.QRect(0, 0, 32, 32))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newToolButton.setIcon(icon4)
        self.newToolButton.setIconSize(QtCore.QSize(32, 32))
        self.newToolButton.setObjectName(_fromUtf8("newToolButton"))
        self.printToolButton = QtGui.QToolButton(self.frame)
        self.printToolButton.setGeometry(QtCore.QRect(770, 0, 32, 32))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/print.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.printToolButton.setIcon(icon5)
        self.printToolButton.setIconSize(QtCore.QSize(32, 32))
        self.printToolButton.setObjectName(_fromUtf8("printToolButton"))
        self.exportToolButton = QtGui.QToolButton(self.frame)
        self.exportToolButton.setGeometry(QtCore.QRect(740, 0, 32, 32))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/exportpdf.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportToolButton.setIcon(icon6)
        self.exportToolButton.setIconSize(QtCore.QSize(32, 32))
        self.exportToolButton.setObjectName(_fromUtf8("exportToolButton"))
        self.orderDetailsGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.orderDetailsGroupBox.setGeometry(QtCore.QRect(0, 40, 801, 71))
        self.orderDetailsGroupBox.setObjectName(_fromUtf8("orderDetailsGroupBox"))
        self.layoutWidget = QtGui.QWidget(self.orderDetailsGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 781, 48))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.orderNumberLabel = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.orderNumberLabel.setFont(font)
        self.orderNumberLabel.setText(_fromUtf8(""))
        self.orderNumberLabel.setObjectName(_fromUtf8("orderNumberLabel"))
        self.gridLayout.addWidget(self.orderNumberLabel, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.orderDateEdit = QtGui.QDateEdit(self.layoutWidget)
        self.orderDateEdit.setObjectName(_fromUtf8("orderDateEdit"))
        self.gridLayout.addWidget(self.orderDateEdit, 0, 3, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 4, 1, 1)
        self.paymentTermsComboBox = QtGui.QComboBox(self.layoutWidget)
        self.paymentTermsComboBox.setObjectName(_fromUtf8("paymentTermsComboBox"))
        self.gridLayout.addWidget(self.paymentTermsComboBox, 0, 5, 1, 1)
        self.label_18 = QtGui.QLabel(self.layoutWidget)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout.addWidget(self.label_18, 1, 0, 1, 1)
        self.projectComboBox = QtGui.QComboBox(self.layoutWidget)
        self.projectComboBox.setObjectName(_fromUtf8("projectComboBox"))
        self.gridLayout.addWidget(self.projectComboBox, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.orderStatusComboBox = QtGui.QComboBox(self.layoutWidget)
        self.orderStatusComboBox.setObjectName(_fromUtf8("orderStatusComboBox"))
        self.gridLayout.addWidget(self.orderStatusComboBox, 1, 3, 1, 1)
        self.taxRateLabel = QtGui.QLabel(self.layoutWidget)
        self.taxRateLabel.setObjectName(_fromUtf8("taxRateLabel"))
        self.gridLayout.addWidget(self.taxRateLabel, 1, 4, 1, 1)
        self.taxRateValueLabel = QtGui.QLabel(self.layoutWidget)
        self.taxRateValueLabel.setText(_fromUtf8(""))
        self.taxRateValueLabel.setObjectName(_fromUtf8("taxRateValueLabel"))
        self.gridLayout.addWidget(self.taxRateValueLabel, 1, 5, 1, 1)
        self.supplierGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.supplierGroupBox.setGeometry(QtCore.QRect(0, 120, 801, 80))
        self.supplierGroupBox.setObjectName(_fromUtf8("supplierGroupBox"))
        self.layoutWidget1 = QtGui.QWidget(self.supplierGroupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(280, 12, 512, 62))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_11 = QtGui.QLabel(self.layoutWidget1)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 0, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.layoutWidget1)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 0, 2, 1, 1)
        self.supplierPhoneLabel = QtGui.QLabel(self.layoutWidget1)
        self.supplierPhoneLabel.setText(_fromUtf8(""))
        self.supplierPhoneLabel.setObjectName(_fromUtf8("supplierPhoneLabel"))
        self.gridLayout_2.addWidget(self.supplierPhoneLabel, 0, 3, 1, 1)
        self.label_9 = QtGui.QLabel(self.layoutWidget1)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 1, 2, 1, 1)
        self.supplierFaxLabel = QtGui.QLabel(self.layoutWidget1)
        self.supplierFaxLabel.setText(_fromUtf8(""))
        self.supplierFaxLabel.setObjectName(_fromUtf8("supplierFaxLabel"))
        self.gridLayout_2.addWidget(self.supplierFaxLabel, 1, 3, 1, 1)
        self.label_7 = QtGui.QLabel(self.layoutWidget1)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)
        self.supplierContactLabel = QtGui.QLabel(self.layoutWidget1)
        self.supplierContactLabel.setText(_fromUtf8(""))
        self.supplierContactLabel.setObjectName(_fromUtf8("supplierContactLabel"))
        self.gridLayout_2.addWidget(self.supplierContactLabel, 2, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.layoutWidget1)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 2, 2, 1, 1)
        self.supplierEmailLabel = QtGui.QLabel(self.layoutWidget1)
        self.supplierEmailLabel.setText(_fromUtf8(""))
        self.supplierEmailLabel.setObjectName(_fromUtf8("supplierEmailLabel"))
        self.gridLayout_2.addWidget(self.supplierEmailLabel, 2, 3, 1, 1)
        self.supplierAddressLabel = QtGui.QLabel(self.layoutWidget1)
        self.supplierAddressLabel.setText(_fromUtf8(""))
        self.supplierAddressLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.supplierAddressLabel.setWordWrap(True)
        self.supplierAddressLabel.setObjectName(_fromUtf8("supplierAddressLabel"))
        self.gridLayout_2.addWidget(self.supplierAddressLabel, 0, 1, 2, 1)
        self.gridLayout_2.setColumnMinimumWidth(0, 80)
        self.gridLayout_2.setColumnMinimumWidth(1, 166)
        self.gridLayout_2.setColumnMinimumWidth(2, 80)
        self.gridLayout_2.setColumnMinimumWidth(3, 166)
        self.gridLayout_2.setRowMinimumHeight(0, 16)
        self.gridLayout_2.setRowMinimumHeight(1, 16)
        self.gridLayout_2.setRowMinimumHeight(2, 16)
        self.supplierComboBox = QtGui.QComboBox(self.supplierGroupBox)
        self.supplierComboBox.setGeometry(QtCore.QRect(11, 18, 256, 20))
        self.supplierComboBox.setObjectName(_fromUtf8("supplierComboBox"))
        self.productsGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.productsGroupBox.setGeometry(QtCore.QRect(0, 210, 801, 331))
        self.productsGroupBox.setObjectName(_fromUtf8("productsGroupBox"))
        self.productsTableView = QtGui.QTableView(self.productsGroupBox)
        self.productsTableView.setGeometry(QtCore.QRect(10, 20, 781, 241))
        self.productsTableView.setObjectName(_fromUtf8("productsTableView"))
        self.layoutWidget2 = QtGui.QWidget(self.productsGroupBox)
        self.layoutWidget2.setGeometry(QtCore.QRect(590, 270, 201, 53))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.layoutWidget2)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.totalExcludingTaxLabel = QtGui.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.totalExcludingTaxLabel.setFont(font)
        self.totalExcludingTaxLabel.setObjectName(_fromUtf8("totalExcludingTaxLabel"))
        self.gridLayout_3.addWidget(self.totalExcludingTaxLabel, 0, 0, 1, 1)
        self.totalExcludingTaxResultLabel = QtGui.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.totalExcludingTaxResultLabel.setFont(font)
        self.totalExcludingTaxResultLabel.setText(_fromUtf8(""))
        self.totalExcludingTaxResultLabel.setObjectName(_fromUtf8("totalExcludingTaxResultLabel"))
        self.gridLayout_3.addWidget(self.totalExcludingTaxResultLabel, 0, 1, 1, 1)
        self.totalTaxLabel = QtGui.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.totalTaxLabel.setFont(font)
        self.totalTaxLabel.setObjectName(_fromUtf8("totalTaxLabel"))
        self.gridLayout_3.addWidget(self.totalTaxLabel, 1, 0, 1, 1)
        self.totalTaxResultLabel = QtGui.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.totalTaxResultLabel.setFont(font)
        self.totalTaxResultLabel.setText(_fromUtf8(""))
        self.totalTaxResultLabel.setObjectName(_fromUtf8("totalTaxResultLabel"))
        self.gridLayout_3.addWidget(self.totalTaxResultLabel, 1, 1, 1, 1)
        self.totalLabel = QtGui.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.totalLabel.setFont(font)
        self.totalLabel.setObjectName(_fromUtf8("totalLabel"))
        self.gridLayout_3.addWidget(self.totalLabel, 2, 0, 1, 1)
        self.totalResultLabel = QtGui.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.totalResultLabel.setFont(font)
        self.totalResultLabel.setText(_fromUtf8(""))
        self.totalResultLabel.setObjectName(_fromUtf8("totalResultLabel"))
        self.gridLayout_3.addWidget(self.totalResultLabel, 2, 1, 1, 1)
        self.deliveryGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.deliveryGroupBox.setGeometry(QtCore.QRect(0, 550, 801, 131))
        self.deliveryGroupBox.setObjectName(_fromUtf8("deliveryGroupBox"))
        self.layoutWidget3 = QtGui.QWidget(self.deliveryGroupBox)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 20, 781, 99))
        self.layoutWidget3.setObjectName(_fromUtf8("layoutWidget3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.layoutWidget3)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_16 = QtGui.QLabel(self.layoutWidget3)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_4.addWidget(self.label_16, 0, 3, 1, 1)
        self.label_14 = QtGui.QLabel(self.layoutWidget3)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_4.addWidget(self.label_14, 0, 1, 1, 1)
        self.gpsCoordinatesLineEdit = QtGui.QLineEdit(self.layoutWidget3)
        self.gpsCoordinatesLineEdit.setObjectName(_fromUtf8("gpsCoordinatesLineEdit"))
        self.gridLayout_4.addWidget(self.gpsCoordinatesLineEdit, 3, 2, 1, 1)
        self.notesPlainTextEdit = QtGui.QPlainTextEdit(self.layoutWidget3)
        self.notesPlainTextEdit.setPlainText(_fromUtf8(""))
        self.notesPlainTextEdit.setObjectName(_fromUtf8("notesPlainTextEdit"))
        self.gridLayout_4.addWidget(self.notesPlainTextEdit, 0, 4, 4, 1)
        self.deliveryAddressPlainTextEdit = QtGui.QPlainTextEdit(self.layoutWidget3)
        self.deliveryAddressPlainTextEdit.setObjectName(_fromUtf8("deliveryAddressPlainTextEdit"))
        self.gridLayout_4.addWidget(self.deliveryAddressPlainTextEdit, 0, 2, 3, 1)
        self.label_17 = QtGui.QLabel(self.layoutWidget3)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_4.addWidget(self.label_17, 3, 1, 1, 1)
        self.label_15 = QtGui.QLabel(self.layoutWidget3)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_4.addWidget(self.label_15, 0, 0, 1, 1)
        self.deliveryDateEdit = QtGui.QDateEdit(self.layoutWidget3)
        self.deliveryDateEdit.setObjectName(_fromUtf8("deliveryDateEdit"))
        self.gridLayout_4.addWidget(self.deliveryDateEdit, 1, 0, 1, 1)
        self.gridLayout_4.setColumnMinimumWidth(0, 125)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionNewPurchaseOrder = QtGui.QAction(MainWindow)
        self.actionNewPurchaseOrder.setObjectName(_fromUtf8("actionNewPurchaseOrder"))
        self.actionView_Purchase_Order = QtGui.QAction(MainWindow)
        self.actionView_Purchase_Order.setObjectName(_fromUtf8("actionView_Purchase_Order"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionExit_2 = QtGui.QAction(MainWindow)
        self.actionExit_2.setObjectName(_fromUtf8("actionExit_2"))
        self.actionPurchase_Order = QtGui.QAction(MainWindow)
        self.actionPurchase_Order.setObjectName(_fromUtf8("actionPurchase_Order"))
        self.actionViewReports = QtGui.QAction(MainWindow)
        self.actionViewReports.setObjectName(_fromUtf8("actionViewReports"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionOpenPurchaseOrder = QtGui.QAction(MainWindow)
        self.actionOpenPurchaseOrder.setObjectName(_fromUtf8("actionOpenPurchaseOrder"))
        self.actionCopyPurchaseOrder = QtGui.QAction(MainWindow)
        self.actionCopyPurchaseOrder.setObjectName(_fromUtf8("actionCopyPurchaseOrder"))
        self.actionClearPurchaseOrder = QtGui.QAction(MainWindow)
        self.actionClearPurchaseOrder.setObjectName(_fromUtf8("actionClearPurchaseOrder"))
        self.actionPrintPurchaseOrder = QtGui.QAction(MainWindow)
        self.actionPrintPurchaseOrder.setObjectName(_fromUtf8("actionPrintPurchaseOrder"))
        self.actionEditProjects = QtGui.QAction(MainWindow)
        self.actionEditProjects.setObjectName(_fromUtf8("actionEditProjects"))
        self.actionEditSuppliers = QtGui.QAction(MainWindow)
        self.actionEditSuppliers.setObjectName(_fromUtf8("actionEditSuppliers"))
        self.actionEditProducts = QtGui.QAction(MainWindow)
        self.actionEditProducts.setObjectName(_fromUtf8("actionEditProducts"))
        self.actionSavePurchaseOrder = QtGui.QAction(MainWindow)
        self.actionSavePurchaseOrder.setObjectName(_fromUtf8("actionSavePurchaseOrder"))
        self.actionExportPurchaseOrder = QtGui.QAction(MainWindow)
        self.actionExportPurchaseOrder.setObjectName(_fromUtf8("actionExportPurchaseOrder"))
        self.actionEditConfiguration = QtGui.QAction(MainWindow)
        self.actionEditConfiguration.setObjectName(_fromUtf8("actionEditConfiguration"))
        self.menuFile.addAction(self.actionNewPurchaseOrder)
        self.menuFile.addAction(self.actionOpenPurchaseOrder)
        self.menuFile.addAction(self.actionSavePurchaseOrder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExportPurchaseOrder)
        self.menuFile.addAction(self.actionPrintPurchaseOrder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit_2)
        self.menuView.addAction(self.actionViewReports)
        self.menuHelp.addAction(self.actionAbout)
        self.menuEdit.addAction(self.actionClearPurchaseOrder)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionEditProjects)
        self.menuEdit.addAction(self.actionEditSuppliers)
        self.menuEdit.addAction(self.actionEditProducts)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionEditConfiguration)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.label_3.setBuddy(self.orderDateEdit)
        self.label_5.setBuddy(self.paymentTermsComboBox)
        self.label_18.setBuddy(self.orderStatusComboBox)
        self.label_4.setBuddy(self.orderStatusComboBox)
        self.label_16.setBuddy(self.notesPlainTextEdit)
        self.label_14.setBuddy(self.deliveryAddressPlainTextEdit)
        self.label_17.setBuddy(self.gpsCoordinatesLineEdit)
        self.label_15.setBuddy(self.deliveryDateEdit)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.newToolButton, self.projectComboBox)
        MainWindow.setTabOrder(self.projectComboBox, self.orderDateEdit)
        MainWindow.setTabOrder(self.orderDateEdit, self.orderStatusComboBox)
        MainWindow.setTabOrder(self.orderStatusComboBox, self.paymentTermsComboBox)
        MainWindow.setTabOrder(self.paymentTermsComboBox, self.supplierComboBox)
        MainWindow.setTabOrder(self.supplierComboBox, self.productsTableView)
        MainWindow.setTabOrder(self.productsTableView, self.deliveryDateEdit)
        MainWindow.setTabOrder(self.deliveryDateEdit, self.deliveryAddressPlainTextEdit)
        MainWindow.setTabOrder(self.deliveryAddressPlainTextEdit, self.gpsCoordinatesLineEdit)
        MainWindow.setTabOrder(self.gpsCoordinatesLineEdit, self.notesPlainTextEdit)
        MainWindow.setTabOrder(self.notesPlainTextEdit, self.saveToolButton)
        MainWindow.setTabOrder(self.saveToolButton, self.printToolButton)
        MainWindow.setTabOrder(self.printToolButton, self.openToolButton)
        MainWindow.setTabOrder(self.openToolButton, self.clearToolButton)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.clearToolButton.setToolTip(_translate("MainWindow", "Clear data", None))
        self.clearToolButton.setText(_translate("MainWindow", "...", None))
        self.saveToolButton.setToolTip(_translate("MainWindow", "Save purchase order", None))
        self.saveToolButton.setText(_translate("MainWindow", "...", None))
        self.openToolButton.setToolTip(_translate("MainWindow", "Open an existing purchase order", None))
        self.openToolButton.setText(_translate("MainWindow", "...", None))
        self.newToolButton.setToolTip(_translate("MainWindow", "Create a new purchase order", None))
        self.newToolButton.setText(_translate("MainWindow", "...", None))
        self.printToolButton.setToolTip(_translate("MainWindow", "Print purchase order", None))
        self.printToolButton.setText(_translate("MainWindow", "...", None))
        self.exportToolButton.setToolTip(_translate("MainWindow", "Export purchase order to PDF file", None))
        self.exportToolButton.setText(_translate("MainWindow", "...", None))
        self.orderDetailsGroupBox.setTitle(_translate("MainWindow", "Order Details", None))
        self.label_2.setText(_translate("MainWindow", "Order Number:", None))
        self.label_3.setText(_translate("MainWindow", "Order Date:", None))
        self.label_5.setText(_translate("MainWindow", "Payment Terms:", None))
        self.label_18.setText(_translate("MainWindow", "Project:", None))
        self.label_4.setText(_translate("MainWindow", "Order Status:", None))
        self.taxRateLabel.setText(_translate("MainWindow", "Tax Rate:", None))
        self.supplierGroupBox.setTitle(_translate("MainWindow", "Supplier", None))
        self.label_11.setText(_translate("MainWindow", "Address:", None))
        self.label_8.setText(_translate("MainWindow", "Phone Number:", None))
        self.label_9.setText(_translate("MainWindow", "Fax Number:", None))
        self.label_7.setText(_translate("MainWindow", "Contact Person:", None))
        self.label_10.setText(_translate("MainWindow", "Email:", None))
        self.productsGroupBox.setTitle(_translate("MainWindow", "Products", None))
        self.totalExcludingTaxLabel.setText(_translate("MainWindow", "Total Excluding Tax:", None))
        self.totalTaxLabel.setText(_translate("MainWindow", "Total Tax:", None))
        self.totalLabel.setText(_translate("MainWindow", "Total:", None))
        self.deliveryGroupBox.setTitle(_translate("MainWindow", "Delivery", None))
        self.label_16.setText(_translate("MainWindow", "Notes:", None))
        self.label_14.setText(_translate("MainWindow", "Delivery Address:", None))
        self.label_17.setText(_translate("MainWindow", "GPS Coordinates:", None))
        self.label_15.setText(_translate("MainWindow", "Delivery Date:", None))
        self.menuFile.setTitle(_translate("MainWindow", "&File", None))
        self.menuView.setTitle(_translate("MainWindow", "&View", None))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help", None))
        self.menuEdit.setTitle(_translate("MainWindow", "&Edit", None))
        self.actionNewPurchaseOrder.setText(_translate("MainWindow", "Create &New Purchase Order", None))
        self.actionView_Purchase_Order.setText(_translate("MainWindow", "View Purchase Order...", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionExit_2.setText(_translate("MainWindow", "E&xit", None))
        self.actionPurchase_Order.setText(_translate("MainWindow", "Purchase Order...", None))
        self.actionViewReports.setText(_translate("MainWindow", "View &Reports...", None))
        self.actionAbout.setText(_translate("MainWindow", "&About", None))
        self.actionOpenPurchaseOrder.setText(_translate("MainWindow", "&Open Purchase Order...", None))
        self.actionCopyPurchaseOrder.setText(_translate("MainWindow", "&Copy Purchase Order", None))
        self.actionClearPurchaseOrder.setText(_translate("MainWindow", "C&lear Purchase Order", None))
        self.actionPrintPurchaseOrder.setText(_translate("MainWindow", "&Print Purchase Order...", None))
        self.actionEditProjects.setText(_translate("MainWindow", "Edit Projects...", None))
        self.actionEditSuppliers.setText(_translate("MainWindow", "Edit Suppliers...", None))
        self.actionEditProducts.setText(_translate("MainWindow", "Edit Products...", None))
        self.actionSavePurchaseOrder.setText(_translate("MainWindow", "Save Purchase Order", None))
        self.actionExportPurchaseOrder.setText(_translate("MainWindow", "Export Purchase Order...", None))
        self.actionEditConfiguration.setText(_translate("MainWindow", "Configuration Wizard...", None))

import resources_rc