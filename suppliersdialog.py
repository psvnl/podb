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
import ui_suppliersdialog
from sqlasession import session_scope
from suppliermodel import SupplierModel
from customdelegates import AddressEditDelegate

class SuppliersDialog(QDialog, ui_suppliersdialog.Ui_suppliersDialog):
    
    def __init__(self, config_file, session, parent=None):
        super(SuppliersDialog, self).__init__(parent)
        self.setupUi(self)
        self.app_config = config_file
        self.session = session
        self.model = SupplierModel(self.app_config, self.session)
        self.savePushButton.connect(self.savePushButton, 
                                    SIGNAL("clicked()"),
                                    self.handle_save_request)
        self.cancelPushButton.connect(self.cancelPushButton, 
                                       SIGNAL("clicked()"),
                                       self.reject)
        self.addRowPushButton.connect(self.addRowPushButton,
                                      SIGNAL("clicked()"),
                                      self.add_row)
        self.tableView.setModel(self.model)
        self.addressEditDelegate = AddressEditDelegate(self.tableView)
        self.tableView.setItemDelegateForColumn(
                                            SupplierModel.ADDRESS_COLUMN,
                                            self.addressEditDelegate)
        self.addressEditDelegate.connect(self.addressEditDelegate,
                                         SIGNAL("closeEditor(QWidget*,"
                                                "QAbstractItemDelegate::"
                                                "EndEditHint)"),
                                         self.handle_editor_close)
        self.tableView.hideColumn(SupplierModel.ID_COLUMN)
        table_width = self.tableView.width()
        self.tableView.setColumnWidth(SupplierModel.COMPANY_NAME_COLUMN, 
                                      0.12 * table_width)
        self.tableView.setColumnWidth(SupplierModel.CONTACT_PERSON_NAME_COLUMN, 
                                      0.12 * table_width)
        self.tableView.setColumnWidth(SupplierModel.ADDRESS_COLUMN, 
                                      0.15 * table_width)
        self.tableView.setColumnWidth(SupplierModel.PHONE_NUMBER_COLUMN, 
                                      0.08 * table_width)
        self.tableView.setColumnWidth(SupplierModel.FAX_NUMBER_COLUMN, 
                                      0.08 * table_width)
        self.tableView.setColumnWidth(SupplierModel.EMAIL_ADDRESS_COLUMN, 
                                      0.23 * table_width)
        self.tableView.setColumnWidth(SupplierModel.TAX_NUMBER_COLUMN, 
                                      0.12 * table_width)
        self.tableView.setColumnWidth(SupplierModel.ARCHIVED_COLUMN, 
                                      0.1 * table_width)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setDefaultSectionSize(60)
        self.updateUi()

    def updateUi(self):
        pass
        
    def add_row(self):
        insert_allowed = self.model.is_insert_allowed()
        if insert_allowed:
            row = self.model.rowCount()
            self.model.insertRows(row)
            self.tableView.selectRow(row)
        
    def handle_save_request(self):
        save_allowed = self.model.is_save_allowed()
        if save_allowed:
            self.accept()
           
    def closeEvent(self, event):
        super(SuppliersDialog, self).closeEvent(event)

    def handle_editor_close(self, widget, hint):
        # If the row width is small to begin with, and you want to resize it to
        # contents once the editor is closed, add a call here to
        # self.tableView.resizeRowsToContents()
        pass

if __name__ == '__main__':
    with session_scope() as session:
#         create_database_if_required()
        app = QApplication(sys.argv)
        form = SuppliersDialog(session)
        dialog_result = form.exec_()
        if dialog_result == QDialog.Accepted:
            session.commit()
        elif dialog_result == QDialog.Rejected:
            session.rollback()
        else:
            raise RuntimeError(("The projects dialog result was {}. Only "
                                "QDialog.Accepted (1) or QDialog.Rejected (0) "
                                "are valid.").format(str(dialog_result)))
        app.exec_()
        
