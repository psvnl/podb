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

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_productsdialog
from sqlasession import session_scope
from productmodel import ProductModel
from suppliermodel import SupplierModel
from customdelegates import PercentageEditDelegate


class ProductsDialog(QDialog, ui_productsdialog.Ui_productsDialog):
    
    def __init__(self, app_config, session, init_supplier_name, parent=None):
        super(ProductsDialog, self).__init__(parent)
        self.setupUi(self)
        self.app_config = app_config
        self.session = session
        self.model = None
        self.savePushButton.connect(self.savePushButton, 
                                    SIGNAL("clicked()"),
                                    self.handle_save_request)
        self.cancelPushButton.connect(self.cancelPushButton, 
                                       SIGNAL("clicked()"),
                                       self.reject)
        self.addRowPushButton.connect(self.addRowPushButton, 
                                      SIGNAL("clicked()"), 
                                      self.add_row)
        self.addRowPushButton.setEnabled(False)
        self.populate_supplier_combo_box()
        start_index = self.supplierComboBox.findText(init_supplier_name)
        if start_index == -1: 
            self.supplierComboBox.setCurrentIndex(0)
        else:
            self.supplierComboBox.setCurrentIndex(start_index)
        self.update_supplier_info()
        self.updateUi()
        
    def updateUi(self):
        pass   
    
    def add_row(self):
        if self.model:
            insert_allowed = self.model.is_insert_allowed()
            if insert_allowed:
                row = self.model.rowCount()
                self.model.insertRows(row)
                self.tableView.selectRow(row)
            
    def handle_save_request(self):
        if self.model:
            save_allowed = self.model.is_save_allowed()
            if save_allowed:
                self.accept()
        
    def populate_supplier_combo_box(self):
        # Note that the call to the clear function will result in a call to the  
        # on_supplierComboBox_currentIndexChanged function.
        self.supplierComboBox.clear()
        supplier_model = SupplierModel(self.app_config, self.session)
        supplier_list = supplier_model.get_supplier_list()
        if len(supplier_list) > 0:
            for supplier in supplier_list:
                self.supplierComboBox.addItem(supplier)
        # Set the current index of the combo box after calling this function.

    def update_supplier_info(self):
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
        self.supplierEmailLabel.setText(supplier_model.data(
                                                        supplier_model_index))

    @pyqtSignature("const QString&")
    def on_supplierComboBox_currentIndexChanged(self, text):
        if self.model:
            del self.model
        supplier_model = SupplierModel(self.app_config, self.session)
        self.supplier_id = supplier_model.\
            get_supplier_id_from_company_name(text)
        self.model = ProductModel(self.app_config, self.session, 
                                  self.supplier_id)
        self.tableView.setModel(self.model)
        self.tableView.setItemDelegateForColumn(
                                        ProductModel.CURRENT_DISCOUNT_COLUMN,
                                        PercentageEditDelegate(self.tableView))
        self.tableView.hideColumn(ProductModel.ID_COLUMN)
        self.tableView.setColumnWidth(ProductModel.PART_NUMBER_COLUMN,
                                      117)
        self.tableView.setColumnWidth(ProductModel.PRODUCT_DESCRIPTION_COLUMN,
                                      265)
        self.tableView.setColumnWidth(ProductModel.CURRENT_PRICE_COLUMN,
                                      117)
        self.tableView.setColumnWidth(ProductModel.CURRENT_DISCOUNT_COLUMN,
                                      110)
        self.tableView.verticalHeader().setDefaultSectionSize(25)
        self.addRowPushButton.setEnabled(True)
        self.update_supplier_info()
        
    def closeEvent(self, event):
        super(ProductsDialog, self).closeEvent(event)

if __name__ == '__main__':
    with session_scope() as session:
#         create_database_if_required()
        app = QApplication(sys.argv)
        form = ProductsDialog(session, "")
        dialog_result = form.exec_()
        if dialog_result == QDialog.Accepted:
            session.commit()
        elif dialog_result == QDialog.Rejected:
            session.rollback()
        else:
            raise RuntimeError(("The products dialog result was {}. Only "
                                "QDialog.Accepted (1) or QDialog.Rejected (0) "
                                "are valid.").format(str(dialog_result)))
        app.exec_()