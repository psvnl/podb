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
import ui_purchaseordersdialog
from purchaseordermodel import PurchaseOrderModel

class PurchaseOrdersDialog(QDialog, 
                           ui_purchaseordersdialog.Ui_purchaseOrdersDialog):
    
    def __init__(self, app_config, session, parent=None):
        super(PurchaseOrdersDialog, self).__init__(parent)
        self.setupUi(self)
        self.session = session
        self.app_config = app_config
        self.model = PurchaseOrderModel(self.app_config, self.session)
        self.selected_row = self.model.rowCount() - 1
        self.buttonBox.connect(self.buttonBox, SIGNAL("accepted()"), 
                               self.accepted)
        self.buttonBox.connect(self.buttonBox, SIGNAL("rejected()"), 
                               self.rejected)
        # Allow the displayed purchase order data to be sorted as required to 
        # facilitate searching
        self.sort_proxy_model = QSortFilterProxyModel()
        self.sort_proxy_model.setDynamicSortFilter(True)
        self.sort_proxy_model.setSourceModel(self.model)
        self.tableView.setModel(self.sort_proxy_model)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.hideColumn(
                    PurchaseOrderModel.DELIVERY_ADDRESS_COLUMN)
        self.tableView.hideColumn(
                    PurchaseOrderModel.DELIVERY_ADDRESS_GPS_COORDINATES_COLUMN)
        self.tableView.hideColumn(
                    PurchaseOrderModel.DELIVERY_DATE_COLUMN)
        self.tableView.hideColumn(
                    PurchaseOrderModel.PAYMENT_TERMS_COLUMN)
        self.tableView.hideColumn(
                    PurchaseOrderModel.NOTES_COLUMN)
        self.tableView.hideColumn(
                    PurchaseOrderModel.TAX_RATE_COLUMN)
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setStretchLastSection(True)
        # Show the total columns at the end of the table.
        self.tableView.horizontalHeader().moveSection(
                                PurchaseOrderModel.TOTAL_INCLUDING_TAX_COLUMN, 
                                PurchaseOrderModel.SUPPLIER_COMPANY_NAME_COLUMN)
        self.tableView.horizontalHeader().moveSection(
                                PurchaseOrderModel.TOTAL_TAX_COLUMN, 
                                PurchaseOrderModel.PROJECT_CODE_COLUMN)
        self.tableView.horizontalHeader().moveSection(
                                PurchaseOrderModel.TOTAL_EXCLUDING_TAX_COLUMN, 
                                PurchaseOrderModel.TOTAL_INCLUDING_TAX_COLUMN)
        self.tableView.verticalHeader().setDefaultSectionSize(25)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setSortingEnabled(True)
        self.tableView.selectRow(0)
        self.updateUi()
    
    def updateUi(self):
        pass
    
    def accepted(self):
        po_model_index = self.sort_proxy_model.mapToSource(
                                                self.tableView.currentIndex())
        self.selected_row = po_model_index.row()
        self.close()
        
    def rejected(self):
        self.close()
    
if __name__ == '__main__':
#     create_database_if_required()
    app = QApplication(sys.argv)
    form = PurchaseOrdersDialog()
    form.show()
    app.exec_()
        
    