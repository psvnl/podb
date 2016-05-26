'''
POdB: A purchase order management system for small businesses 
Copyright (C) 2016  Paulo S. V. N. Leal

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT 
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program. If not, see <http://www.gnu.org/licenses/>.

Contact: paulosvnleal@gmail.com
'''

import datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui_mainwindow
from customdelegates import (LimitedLinePlainTextEdit, 
                             ProductPartNumberEditDelegate, 
                             ProductDescriptionEditDelegate,
                             PercentageEditDelegate)

from activepurchaseordermodel import ActivePurchaseOrderModel
from lineitemmodel import LineItemModel
from projectmodel import ProjectModel
from purchaseorder import PO_ORDER_STATUSUS, PO_PAYMENT_TERMS
from purchaseordermodel import PurchaseOrderModel
from suppliermodel import SupplierModel

from configwizard import InAppConfigWizard
from messagebox import (execute_info_msg_box, execute_warning_msg_box, 
                        execute_critical_msg_box)
from productsdialog import ProductsDialog
from projectsdialog import ProjectsDialog
from purchaseordersdialog import PurchaseOrdersDialog
from reportsdialog import ReportsDialog
from suppliersdialog import SuppliersDialog

from pdfreports import (PoPdf, PoPdfCompanyDetails, PoPdfOrderDetails, 
                        PoPdfSupplierDetails, PoPdfLineItemDetails, 
                        PoPdfDeliveryDetails, PoPdfSignatureDetails)
from userconfigmodel import UserConfigReader


class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
    
    def __init__(self, app_config, session, parent=None):
        super(MainWindow, self).__init__(parent)
        # TODO: Call check_ui_types in the next line.
#         self.check_ui_types()
        self.session = session
        self.app_config = app_config
        self.active_po_model = None     
        self.po_mapper = None
        self.setupUi(self)
        self.additional_ui_setup()
        assert type(self.deliveryAddressPlainTextEdit) is QPlainTextEdit  

    def check_ui_types(self):
        assert type(self.deliveryAddressPlainTextEdit) is \
            LimitedLinePlainTextEdit

    def additional_ui_setup(self):
        '''
        
        '''
        # Prevent main window from being resized.
        self.setFixedWidth(self.width())
        self.setFixedHeight(self.height())
        # The company name in the main window title comes from the application 
        # settings file.
        window_title = "{}: {}".format("POdB", self.app_config.company.name)
        self.setWindowTitle(window_title)
        # TODO: Set the window icon to the configured file if available.
        # If we have reached this point then we are connected to the database.
        status_text = []
        status_text.append("Connected to ")
        status_text.append(self.app_config.database.type)
        status_text.append(" database ")
        status_text.append(self.app_config.database.name)
        if self.app_config.database.driver:
            status_text.append(" through ")
            status_text.append(self.app_config.database.driver)
        self.statusBarLabel.setText("".join(status_text))
        # Use the calendar pop ups.
        self.orderDateEdit.setCalendarPopup(True)
        self.deliveryDateEdit.setCalendarPopup(True)
        self.blank_all_widgets()
        self.populate_order_status_combo_box()
        self.populate_payment_terms_combo_box()
        self.populate_supplier_combo_box()
        self.supplierComboBox.setCurrentIndex(0)
        self.populate_project_combo_box()
        self.projectComboBox.setCurrentIndex(0)
        # Overwrite the default labels that mention tax, to use the tax name, 
        # which comes from the application settings file.
        tax_rate_label = "{} Rate:".format(
                                        self.app_config.locale.tax_name)
        self.taxRateLabel.setText(tax_rate_label)
        total_excl_label = "Total Excluding {}:".format(
                                        self.app_config.locale.tax_name)
        self.totalExcludingTaxLabel.setText(total_excl_label) 
        total_tax_label = "Total {}:".format(self.app_config.locale.tax_name)
        self.totalTaxLabel.setText(total_tax_label)
        self.totalExcludingTaxResultLabel.setAlignment(
                                                Qt.AlignRight|Qt.AlignVCenter)
        self.totalTaxResultLabel.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.totalResultLabel.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        # File menu handlers
        self.connect(self.actionNewPurchaseOrder, SIGNAL("triggered()"),
                     self.on_newToolButton_clicked)
        self.connect(self.actionOpenPurchaseOrder, SIGNAL("triggered()"),
                     self.on_openToolButton_clicked)
        self.connect(self.actionSavePurchaseOrder, SIGNAL("triggered()"),
                     self.on_saveToolButton_clicked)
        self.connect(self.actionExportPurchaseOrder, SIGNAL("triggered()"),
                     self.on_exportToolButton_clicked)
        self.connect(self.actionPrintPurchaseOrder, SIGNAL("triggered()"),
                     self.on_printToolButton_clicked)
        self.connect(self.actionExit_2, SIGNAL("triggered()"),
                     self.on_exitAction_triggered)
        # Edit menu handlers 
        self.connect(self.actionClearPurchaseOrder, SIGNAL("triggered()"),
                     self.on_clearPurchaseOrderAction_triggered)
        self.connect(self.actionEditProjects, SIGNAL("triggered()"), 
                     self.on_editProjectsAction_triggered)
        self.connect(self.actionEditSuppliers, SIGNAL("triggered()"), 
                     self.on_editSuppliersAction_triggered)
        self.connect(self.actionEditProducts, SIGNAL("triggered()"), 
                     self.on_editProductsAction_triggered)
        self.connect(self.actionEditConfiguration, SIGNAL("triggered()"), 
                     self.on_editConfigAction_triggered)
        # View menu handlers
        self.connect(self.actionViewReports, SIGNAL("triggered()"),
                     self.on_viewReportsAction_triggered)
                                
    def populate_order_status_combo_box(self):
        for order_status in PO_ORDER_STATUSUS:
            self.orderStatusComboBox.addItem(str(order_status))
            
    def populate_payment_terms_combo_box(self):
        for payment_term in PO_PAYMENT_TERMS:
            self.paymentTermsComboBox.addItem(payment_term)
                        
    def populate_supplier_combo_box(self):
        # Note that the call to the clear function will result in a call to the  
        # on_supplierComboBox_currentIndexChanged function. Therefore, block
        # signals.
        self.supplierComboBox.blockSignals(True)
        self.supplierComboBox.clear()
        supplier_model = SupplierModel(self.app_config, self.session)
        supplier_list = supplier_model.get_supplier_list()
        if len(supplier_list) > 0:
            for supplier in supplier_list:
                self.supplierComboBox.addItem(supplier)
        self.supplierComboBox.blockSignals(False)
        # Set the current index of the combo box after calling this function.
        
    def populate_project_combo_box(self):
        # Note that the call to the clear function will result in a call to the  
        # on_projectComboBox_currentIndexChanged function. Therefore, block
        # signals.
        self.projectComboBox.blockSignals(True)
        self.projectComboBox.clear()
        project_model = ProjectModel(self.session)
        project_list = project_model.get_project_list()
        if len(project_list) > 0:
            for project in project_list:
                self.projectComboBox.addItem(project)
        self.projectComboBox.blockSignals(False)
        # Set the current index of the combo box after calling this function.
        
    def blank_all_widgets(self):
        self.orderNumberLabel.setText("")
        self.projectComboBox.setCurrentIndex(0)
        self.orderDateEdit.setDate(datetime.date.today())
        self.orderStatusComboBox.setCurrentIndex(0)
        self.paymentTermsComboBox.setCurrentIndex(0)
        self.taxRateValueLabel.setText("")
        self.supplierAddressLabel.setText("")
        self.supplierContactLabel.setText("")
        self.supplierPhoneLabel.setText("")
        self.supplierFaxLabel.setText("")
        self.supplierEmailLabel.setText("")
        self.totalExcludingTaxResultLabel.setText("")
        self.totalTaxResultLabel.setText("")
        self.totalResultLabel.setText("")
        self.deliveryDateEdit.setDateTime(datetime.datetime.now())
        self.deliveryAddressPlainTextEdit.setPlainText("")
        self.gpsCoordinatesLineEdit.setText("")
        self.notesPlainTextEdit.setPlainText("")
        # Disable the contents of all group boxes until a purchase order is 
        # created or opened. 
        self.orderDetailsGroupBox.setEnabled(False)
        self.supplierGroupBox.setEnabled(False)
        self.productsGroupBox.setEnabled(False)
        self.deliveryGroupBox.setEnabled(False)
        # Tool buttons
        self.newToolButton.setEnabled(True)
        self.openToolButton.setEnabled(True)
        self.saveToolButton.setEnabled(False)
        self.clearToolButton.setEnabled(False)
        self.exportToolButton.setEnabled(False)
        self.printToolButton.setEnabled(False)
        # Menu items
        self.actionNewPurchaseOrder.setEnabled(True)
        self.actionOpenPurchaseOrder.setEnabled(True)
        self.actionSavePurchaseOrder.setEnabled(False)
        self.actionClearPurchaseOrder.setEnabled(False)
        self.actionExportPurchaseOrder.setEnabled(False)
        self.actionPrintPurchaseOrder.setEnabled(False)
                                
    def create_po_mapper(self):
        # Note how the combo boxes are not mapped below. Mapping them is tricky.
        self.po_mapper = QDataWidgetMapper(parent=self)
        self.po_mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.po_mapper.setModel(self.active_po_model)
        self.po_mapper.addMapping(self.orderNumberLabel,
                    PurchaseOrderModel.ORDER_NUMBER_COLUMN,
                    "text")
        self.po_mapper.addMapping(self.orderDateEdit,
                    PurchaseOrderModel.ORDER_DATE_COLUMN)
        self.po_mapper.addMapping(self.deliveryAddressPlainTextEdit,
                    PurchaseOrderModel.DELIVERY_ADDRESS_COLUMN)
        self.po_mapper.addMapping(self.gpsCoordinatesLineEdit,
                    PurchaseOrderModel.DELIVERY_ADDRESS_GPS_COORDINATES_COLUMN)
        self.po_mapper.addMapping(self.deliveryDateEdit,
                    PurchaseOrderModel.DELIVERY_DATE_COLUMN)
        self.po_mapper.addMapping(self.notesPlainTextEdit,
                    PurchaseOrderModel.NOTES_COLUMN)
        self.po_mapper.addMapping(self.taxRateValueLabel,
                    PurchaseOrderModel.TAX_RATE_COLUMN,
                    "text")
        # The total labels are not mapped because they require special 
        # formatting.
        self.po_mapper.toLast()
        
    def update_supplier_info(self):
        # TODO: Move access to this stuff to inside the supplier model.
        supplier_model = SupplierModel(self.app_config, self.session)
        supplier_row = self.supplierComboBox.currentIndex()
        supplier_model_index = supplier_model.createIndex(
                                    supplier_row,
                                    SupplierModel.ADDRESS_COLUMN)
        self.supplierAddressLabel.setText(
                                    supplier_model.data(supplier_model_index))
        supplier_model_index = supplier_model.createIndex(
                                    supplier_row,
                                    SupplierModel.CONTACT_PERSON_NAME_COLUMN)
        self.supplierContactLabel.setText(
                                    supplier_model.data(supplier_model_index))
        supplier_model_index = supplier_model.createIndex(
                                    supplier_row,
                                    SupplierModel.PHONE_NUMBER_COLUMN)
        self.supplierPhoneLabel.setText(
                                    supplier_model.data(supplier_model_index))
        supplier_model_index = supplier_model.createIndex(
                                    supplier_row,
                                    SupplierModel.FAX_NUMBER_COLUMN)
        self.supplierFaxLabel.setText(
                                    supplier_model.data(supplier_model_index))
        supplier_model_index = supplier_model.createIndex(
                                    supplier_row,
                                    SupplierModel.EMAIL_ADDRESS_COLUMN)
        self.supplierEmailLabel.setText(
                                    supplier_model.data(supplier_model_index))
        
    # How the columns divide up the product table view.
    _PART_NUMBER_COLUMN_SHARE = 0.15
    _DESCRIPTION_COLUMN_SHARE = 0.34
    _UNIT_PRICE_COLUMN_SHARE  = 0.15
    _DISCOUNT_COLUMN_SHARE    = 0.08
    _QUANTITY_COLUMN_SHARE    = 0.08
    # The share of the total column is not specified because it'll be stretched
    # to use the remaining, available space.
        
    def initialise_product_table(self):
        active_purchase_order = self.active_po_model.get_active_purchase_order()
        self.productsTableView.setItemDelegateForColumn(
                                    0, 
                                    ProductPartNumberEditDelegate(
                                                    self.session, 
                                                    active_purchase_order, 
                                                    self.productsTableView))
        self.productsTableView.setItemDelegateForColumn(
                                    1, 
                                    ProductDescriptionEditDelegate(
                                                    self.session, 
                                                    active_purchase_order, 
                                                    self.productsTableView))
        self.productsTableView.setItemDelegateForColumn(
                                    3, 
                                    PercentageEditDelegate(
                                                    self.productsTableView))
        self.productsTableView.setModel(self.active_po_model.line_item_model)
        self.productsTableView.setEditTriggers(
                                        QAbstractItemView.CurrentChanged | \
                                        QAbstractItemView.SelectedClicked)
        table_width = self.productsTableView.width()
        self.productsTableView.setColumnWidth(
                            LineItemModel.PART_NUMBER_COLUMN, 
                            int(self._PART_NUMBER_COLUMN_SHARE * table_width))
        self.productsTableView.setColumnWidth(
                            LineItemModel.DESCRIPTION_COLUMN, 
                            int(self._DESCRIPTION_COLUMN_SHARE * table_width))
        self.productsTableView.setColumnWidth(
                            LineItemModel.UNIT_PRICE_COLUMN, 
                            int(self._UNIT_PRICE_COLUMN_SHARE * table_width))
        self.productsTableView.setColumnWidth(
                            LineItemModel.DISCOUNT_COLUMN, 
                            int(self._DISCOUNT_COLUMN_SHARE * table_width))
        self.productsTableView.setColumnWidth(
                            LineItemModel.QUANTITY_COLUMN, 
                            int(self._QUANTITY_COLUMN_SHARE * table_width))
        self.productsTableView.horizontalHeader().setStretchLastSection(True)
        self.productsTableView.verticalHeader().setDefaultSectionSize(25) 
        # Set up the context menu that allows rows to be deleted.
        self.productsTableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.productsTableView.connect(
                        self.productsTableView, 
                        SIGNAL("customContextMenuRequested(const QPoint&)"),
                        self.productsTableViewContextMenuRequested)
        self.active_po_model.connect(
                        self.active_po_model,
                        SIGNAL("totals_calculated()"),
                        self.update_totals)
        self.active_po_model.connect(
                        self.active_po_model,
                        SIGNAL("add_new_product_requested()"),
                        self.on_editProductsAction_triggered)
        self.update_totals()
        # Assumes that the product group box has been enabled elsewhere.
        
    def productsTableViewContextMenuRequested(self, pos):
        index = self.productsTableView.indexAt(pos)
        if index.isValid():
            menu = QMenu(self)
            delete_row_action = menu.addAction("Delete row") 
            action = menu.exec_(self.productsTableView.mapToGlobal(pos))
            if action == delete_row_action:
                self.active_po_model.line_item_model.removeRows(index.row(), 1)
            
    def update_totals(self):
        self.totalExcludingTaxResultLabel.setText(
                                    "R {:,.2f}".format(
                                            self.active_po_model.total_price))
        self.totalTaxResultLabel.setText(
                                    "R {:,.2f}".format(
                                            self.active_po_model.total_tax))
        self.totalResultLabel.setText(
                                    "R {:,.2f}".format(
                                            self.active_po_model.total))
        
    def at_least_one_supplier(self):
        supplier_model = SupplierModel(self.app_config, self.session)
        if supplier_model.rowCount() > 0:
            return True
        return False
    
    def at_least_one_project(self):
        project_model = ProjectModel(self.session)
        if project_model.rowCount() > 0:
            return True
        return False
    
    def at_least_one_purchase_order(self):
        po_model = PurchaseOrderModel(self.app_config, self.session)
        if po_model.rowCount() > 0:
            return True
        return False
    
    PREREQUISITE_STRING_SUPPLIER = "supplier"
    PREREQUISITE_STRING_PROJECT = "project"
    PREREQUISITE_STRING_PURCHASE_ORDER = "purchase order"
    
    def show_failed_prerequisite_message_box(self, prerequisite):
        execute_info_msg_box(
                        "Failed Prerequisite", 
                        ("There are no {}s in the database. You need at least "
                         "one to continue.").format(prerequisite), 
                        QMessageBox.Ok)
        
    def prerequisites_for_new_met(self):
        if self.at_least_one_supplier() is not True:
            self.show_failed_prerequisite_message_box(
                                        self.PREREQUISITE_STRING_SUPPLIER)
            return False
        if self.at_least_one_project() is not True:
            self.show_failed_prerequisite_message_box(
                                        self.PREREQUISITE_STRING_PROJECT)
            return False
        return True
    
    def prerequisites_for_open_met(self):
        if self.at_least_one_purchase_order() is not True:
            self.show_failed_prerequisite_message_box(
                                        self.PREREQUISITE_STRING_PURCHASE_ORDER)
            return False
        return self.prerequisites_for_new_met()
    
    def prerequisites_for_reports_met(self):
        return self.prerequisites_for_open_met()
        
    EDITABLE_STRING_SUPPLIERS = "suppliers"
    EDITABLE_STRING_PROJECTS = "projects"
    EDITABLE_STRING_PRODUCTS = "products"
    EDITABLE_STRING_CONFIG = "configuration"
    
    MSG_BOX_TITLE_UNSAVED_CHANGES = "Unsaved Changes"
    
    def show_save_before_editing_message_box(self, editable):
        if self.active_po_model and self.active_po_model.dirty:
            result = execute_warning_msg_box(
                            self.MSG_BOX_TITLE_UNSAVED_CHANGES, 
                            ("There are some unsaved changes. These must be "
                             "either saved or discarded before editing the "
                             "{}.").format(editable), 
                            QMessageBox.Save | QMessageBox.Discard)
            if result == QMessageBox.Save:
                self.save_all()
            else:
                self.session.rollback()
                self.active_po_model.do_post_rollback_processing()
    
    def show_save_before_po_access(self):
        if self.active_po_model and self.active_po_model.dirty:
            result = execute_warning_msg_box(
                            self.MSG_BOX_TITLE_UNSAVED_CHANGES, 
                            ("There are some unsaved changes. These must be "
                             "either saved or discarded before accessing a "
                             "new purchase order."), 
                            QMessageBox.Save | QMessageBox.Discard)
            if result == QMessageBox.Save:
                self.save_all()
            else:
                self.session.rollback()
                self.active_po_model.do_post_rollback_processing()
                
    def show_save_before_report_access(self):
        if self.active_po_model and self.active_po_model.dirty:
            result = execute_warning_msg_box(
                            self.MSG_BOX_TITLE_UNSAVED_CHANGES, 
                            ("There are some unsaved changes. These must be "
                             "either saved or discarded before accessing the "
                             "reports."), 
                            QMessageBox.Save | QMessageBox.Discard)
            if result == QMessageBox.Save:
                self.save_all()
            else:
                self.session.rollback()
                self.active_po_model.do_post_rollback_processing()
                
    def show_save_before_close(self):
        if self.active_po_model and self.active_po_model.dirty:
            result = execute_warning_msg_box(
                            self.MSG_BOX_TITLE_UNSAVED_CHANGES, 
                            ("There are some unsaved changes. These must be "
                             "either saved or discarded before closing the "
                             "application."), 
                            QMessageBox.Save | QMessageBox.Discard)
            if result == QMessageBox.Save:
                self.save_all()
            else:
                self.session.rollback()
                self.active_po_model.do_post_rollback_processing()
                
    @pyqtSignature("")
    def on_newToolButton_clicked(self):
        '''Handles the request to create a new purchase order. 
        
        Does the following:
        - Verify that prerequisites are met:
            - At least one supplier
            - At least one project
        - Create a new ActivePurchaseOrderModel with new_po=True
        - Create a new QDataWidgetMapper to map widgets to model
        - Enable all group boxes
        - Update all combo boxes
        - Setup the product line item table, mapping it to the active PO
          model's line item model
        '''
        if self.prerequisites_for_new_met() is True:
            print("---> New")
            self.show_save_before_po_access()
            if self.active_po_model:
                del self.active_po_model
            self.active_po_model = ActivePurchaseOrderModel(self.app_config,
                                                            self.session)
            self.create_po_mapper()
            # Enable the order details, supplier and delivery group boxes.
            self.orderDetailsGroupBox.setEnabled(True)
            self.supplierGroupBox.setEnabled(True)
            self.deliveryGroupBox.setEnabled(True)
            self.productsGroupBox.setEnabled(True)
            # Tool buttons
            self.newToolButton.setEnabled(True)
            self.openToolButton.setEnabled(True)
            self.saveToolButton.setEnabled(True)
            # TODO: Clear tool button functionality.
            self.clearToolButton.setEnabled(False)
            self.exportToolButton.setEnabled(True)
            # TODO: Print tool button functionality.
            self.printToolButton.setEnabled(False)
            # Menu items
            # Menu items
            self.actionNewPurchaseOrder.setEnabled(True)
            self.actionOpenPurchaseOrder.setEnabled(True)
            self.actionSavePurchaseOrder.setEnabled(True)
            self.actionClearPurchaseOrder.setEnabled(False)
            self.actionExportPurchaseOrder.setEnabled(True)
            self.actionPrintPurchaseOrder.setEnabled(False)
            # Update all combo boxes to reflect the data in the new purchase 
            # order.
            self.update_all_combo_boxes()
            # Set up the product line item table view.
            self.initialise_product_table()

    @pyqtSignature("")
    def on_openToolButton_clicked(self):
        '''Handles the request to open an existing purchase order. 
        
        Does the following:
        - Verify that prerequisites are met:
            - At least one supplier
            - At least one project
            - At least one purchase order
        - Create a new ActivePurchaseOrderModel with new_po=True
        - Create a new QDataWidgetMapper to map widgets to model
        - Enable all group boxes
        - Update all combo boxes
        - Setup the product line item table, mapping it to the active PO
          model's line item model
        '''
        if self.prerequisites_for_open_met() is True:
            print("---> Open")
            self.show_save_before_po_access()
            purchase_orders_dialog = PurchaseOrdersDialog(self.app_config,
                                                          self.session, 
                                                          parent=self)
            if purchase_orders_dialog.exec_() == QDialog.Accepted:
                po_model_row = purchase_orders_dialog.selected_row
                if self.active_po_model:
                    del self.active_po_model
                self.active_po_model = ActivePurchaseOrderModel(
                                                            self.app_config,
                                                            self.session,
                                                            new_po=False,
                                                            po_row=po_model_row)
                self.create_po_mapper()
                # Enable the order details, supplier and delivery group boxes.
                self.orderDetailsGroupBox.setEnabled(True)
                self.supplierGroupBox.setEnabled(True)
                self.deliveryGroupBox.setEnabled(True)
                self.productsGroupBox.setEnabled(True)
                # Tool buttons
                self.newToolButton.setEnabled(True)
                self.openToolButton.setEnabled(True)
                self.saveToolButton.setEnabled(True)
                # TODO: Clear tool button functionality.
                self.clearToolButton.setEnabled(False)
                self.exportToolButton.setEnabled(True)
                # TODO: Print tool button functionality.
                self.printToolButton.setEnabled(False)
                # Menu items
                self.actionNewPurchaseOrder.setEnabled(True)
                self.actionOpenPurchaseOrder.setEnabled(True)
                self.actionSavePurchaseOrder.setEnabled(True)
                self.actionClearPurchaseOrder.setEnabled(False)
                self.actionExportPurchaseOrder.setEnabled(True)
                self.actionPrintPurchaseOrder.setEnabled(False)
                # Update all combo boxes to reflect the data in the opened 
                # purchase order.
                self.update_all_combo_boxes()
                # Set up the product line item table view.
                self.initialise_product_table()
        
    def update_orderStatusComboBox(self):
        self.orderStatusComboBox.blockSignals(True)
        order_status = self.active_po_model.get_order_status()
        combo_index = self.orderStatusComboBox.findText(order_status)
        self.orderStatusComboBox.setCurrentIndex(combo_index)
        self.orderStatusComboBox.blockSignals(False)
    
    def update_paymentTermsComboBox(self):
        self.paymentTermsComboBox.blockSignals(True)
        payment_terms = self.active_po_model.get_payment_terms()
        combo_index = self.paymentTermsComboBox.findText(payment_terms)
        self.paymentTermsComboBox.setCurrentIndex(combo_index)
        self.paymentTermsComboBox.blockSignals(False)
    
    def update_supplierComboBox(self):
        self.supplierComboBox.blockSignals(True)
        supplier = self.active_po_model.get_supplier()
        combo_index = self.supplierComboBox.findText(supplier)
        self.supplierComboBox.setCurrentIndex(combo_index)
        self.supplierComboBox.blockSignals(False)
        # Update_supplier information labels. 
        self.update_supplier_info()
    
    def update_projectComboBox(self):
        self.projectComboBox.blockSignals(True)
        project = self.active_po_model.get_project()
        combo_index = self.projectComboBox.findText(project)
        self.projectComboBox.setCurrentIndex(combo_index)
        self.projectComboBox.blockSignals(False)
    
    def update_all_combo_boxes(self):
        self.update_orderStatusComboBox()
        self.update_paymentTermsComboBox()
        self.update_supplierComboBox()
        self.update_projectComboBox()
    
    def save_all(self):
        # The dialogs may be accessed without a purchase order being open. 
        # Therefore, the check to see if an active purchase order exists is 
        # necessary.
        print("---> Save all")
        if self.po_mapper:
            self.po_mapper.submit()
        if self.active_po_model:
            self.active_po_model.do_pre_commit_processing()
        self.session.commit()
        if self.active_po_model:
            self.active_po_model.do_post_commit_processing()
        
    @pyqtSignature("")
    def on_saveToolButton_clicked(self):
        self.save_all()
    
    def process_dialog_result(self, result):
        if result == QDialog.Accepted:
            self.save_all()
        else:
            self.session.rollback()
    
    @pyqtSignature("")
    def on_clearPurchaseOrderAction_triggered(self):
        pass
    
    @pyqtSignature("")
    def on_editProjectsAction_triggered(self):
        self.show_save_before_editing_message_box(
                                            self.EDITABLE_STRING_PROJECTS)
        # Save the combo box index of the current project.
        current_project_combo_index= self.projectComboBox.currentIndex()
        # Run the dialog that allows project data to be edited.
        projects_dialog = ProjectsDialog(self.session, parent=self)
        result = projects_dialog.exec_()
        self.process_dialog_result(result)
        self.populate_project_combo_box()
        # Restore the project to what it was.
        self.projectComboBox.blockSignals(True)
        self.projectComboBox.setCurrentIndex(current_project_combo_index)
        self.projectComboBox.blockSignals(False)
        
    @pyqtSignature("")
    def on_editSuppliersAction_triggered(self):
        # BUG: Have a PO open. Edit suppliers. Click cancel on the edit 
        # suppliers dialog. The message box saying that you are trying to 
        # change the supplier of a PO with items on it is shown. This should 
        # not happen. Editing the suppliers should never result in an attempt 
        # to change the current PO's supplier.
        self.show_save_before_editing_message_box(
                                            self.EDITABLE_STRING_SUPPLIERS)
        # Save the combo box index of the current supplier.
        current_supplier_combo_index = self.supplierComboBox.currentIndex()
        # Run the dialog that allows supplier data to be edited.
        suppliers_dialog = SuppliersDialog(self.app_config, self.session, 
                                           parent=self)
        result = suppliers_dialog.exec_()
        self.process_dialog_result(result)
        self.populate_supplier_combo_box()
        # Restore the supplier to what it was.
        self.supplierComboBox.blockSignals(True)
        self.supplierComboBox.setCurrentIndex(current_supplier_combo_index)
        self.supplierComboBox.blockSignals(False)
        self.update_supplier_info()
        
    @pyqtSignature("")
    def on_editProductsAction_triggered(self):
        self.show_save_before_editing_message_box(
                                            self.EDITABLE_STRING_PRODUCTS)
        products_dialog = ProductsDialog(self.app_config, self.session, 
                                         self.supplierComboBox.currentText(), 
                                         parent=self)
        result = products_dialog.exec_()
        self.process_dialog_result(result)
        
    @pyqtSignature("")
    def on_editConfigAction_triggered(self):
        self.show_save_before_editing_message_box(
                                            self.EDITABLE_STRING_CONFIG)
        # The InAppConfigWizard does not allow editing the application settings.
        config_wizard = InAppConfigWizard(self.app_config)
        result = config_wizard.exec_()
        
    @pyqtSignature("const QString&")
    def on_orderStatusComboBox_currentIndexChanged(self, text):
        if self.active_po_model:
            self.active_po_model.set_order_status(text)
    
    @pyqtSignature("const QString&")
    def on_paymentTermsComboBox_currentIndexChanged(self, text):
        if self.active_po_model:
            self.active_po_model.set_payment_terms(text)
        
    @pyqtSignature("const QString&")
    def on_supplierComboBox_currentIndexChanged(self, text):
        if self.active_po_model:
            if self.active_po_model.has_line_items() is True:
                result = execute_warning_msg_box(
                                "Supplier Change Warning",
                                ("You are trying to change the supplier of a "
                                 "purchase order with items on it."), 
                                QMessageBox.Ok | QMessageBox.Cancel, 
                                info_text=("If you do this then all of the "
                                           "current line items on this "
                                           "purchase order will be removed. " 
                                           "Click OK to continue."))
                if result == QMessageBox.Ok:
                    self.active_po_model.set_supplier(self.session, text)
                else:
                    return
            else:
                self.active_po_model.set_supplier(self.session, text)
            self.update_supplier_info() 
            self.initialise_product_table()
            
    @pyqtSignature("const QString&")
    def on_projectComboBox_currentIndexChanged(self, text):
        if self.active_po_model:
            self.active_po_model.set_project(text)

    @pyqtSignature("")
    def on_clearToolButton_clicked(self):
        pass

    @pyqtSignature("")
    def on_printToolButton_clicked(self):
        pass
         
    @pyqtSignature("")
    def on_exportToolButton_clicked(self):
        if self.active_po_model:
            pdf_filename = QFileDialog.getSaveFileName(
                                        self, 
                                        caption="Save Purchase Order to PDF", 
                                        filter="*.pdf")
            if pdf_filename == "":
                # The file name is empty, which probably means that the user 
                # pressed Cancel in the file dialog. Just return.
                return
            # The file name is valid.
            # Create a reader to access the latest user config.
            user_config = UserConfigReader(self.session)
            company_details = PoPdfCompanyDetails(
                        self.app_config.company.name,
                        user_config.company.postal_address,
                        user_config.company.phone_number,
                        fax=user_config.company.fax_number,
                        email=user_config.company.email_address,
                        web=user_config.company.web_address,
                        logo_filename=user_config.company.logo_filename)
                                    
            order_details = PoPdfOrderDetails(
                                    self.orderNumberLabel.text(),
                                    self.orderDateEdit.text(),
                                    self.paymentTermsComboBox.currentText())
            
            supplier_details = PoPdfSupplierDetails(
                                    self.supplierComboBox.currentText(),
                                    self.supplierAddressLabel.text(),
                                    self.supplierPhoneLabel.text(),
                                    self.supplierFaxLabel.text(),
                                    self.supplierEmailLabel.text(),
                                    self.supplierContactLabel.text())
            
            delivery_details = PoPdfDeliveryDetails(
                                    self.deliveryDateEdit.text(),
                                    self.deliveryAddressPlainTextEdit.\
                                        document().toPlainText(),
                                    self.gpsCoordinatesLineEdit.text()) 
             
             
            line_items = []
            for row in range(self.active_po_model.line_item_model.\
                             rowCount() - 1):
                line_items.append(self.active_po_model.line_item_model.\
                                  get_row(row))
            line_item_details = PoPdfLineItemDetails(
                                    line_items, 
                                    self.totalExcludingTaxResultLabel.text(),
                                    self.totalTaxResultLabel.text(),
                                    self.totalResultLabel.text(),
                                    self.app_config.locale.tax_name)
            
            signature_details = PoPdfSignatureDetails(
                                    user_config.company.signatory_name,
                                    user_config.company.signature_filename,
                                    draft=True)
            
            pdf_report = PoPdf(pdf_filename, 
                               company_details,
                               order_details,
                               supplier_details,
                               delivery_details,
                               line_item_details,
                               self.notesPlainTextEdit.document().\
                                    toPlainText(),
                               signature_details,
                               show_all_grids=False)
            # TODO: Wrap with try except, since will raise, e.g., 
            # FileNotFoundError.
            try:
                pdf_report.build()
            except PermissionError as e:
                execute_critical_msg_box("Permission Error", 
                                         ("Could not open the PDF file. Make "
                                          "sure that it is not open and the "
                                          "try again."), 
                                          QMessageBox.Ok,
                                          info_text=str(e))
            
    @pyqtSignature("")
    def on_viewReportsAction_triggered(self):
        if self.prerequisites_for_reports_met() is True:
            self.show_save_before_report_access()
            reports_dialog = ReportsDialog(self.app_config, self.session, 
                                           self.app_config.company.name,
                                           parent=self)
            reports_dialog.exec_()

    @pyqtSignature("")
    def on_exitAction_triggered(self):
        self.close()

    def closeEvent(self, event):
        self.show_save_before_close()
