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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from purchaseordermodel import PurchaseOrderModel
from lineitemmodel import LineItemModel


class ModelWriteError(Exception):
    '''Exception raised when a write to the purchase order model fails.  
    '''
    pass


class ActivePurchaseOrderModel(QAbstractTableModel):
    '''Data model for the active purchase order record of the purchase order 
    model.
    '''

    def __init__(self, app_config, session, new_po=True, 
                 po_row=-1, parent=None):
        '''Initialise the ActivePurchaseOrderModel object.
        
        Args:
        :param app_config: The application configuration in use. 
        :type app_config: appconfig.ConfigFile
        :param session: The SQLAlchemy session in use. 
        :type session: Session object (the class created by the call to  
            :func:`sessionmaker` in :mod:`sqlasession`).
        :param new_po: Indicator of whether a new purchase order should be
            created. A value of False means that a purchase order should be 
            opened, in which case the po_row parameter specifies which purchase
            order should be opened.
        :type new_po: Boolean
        :param po_row: The purchase order model row of the purchase order that 
            should be opened. This parameter must be set if the new_po 
            parameter is set to False.
        :type po_row: Integer
        :param parent: The model's parent.
        :type parent: QObject
        
        Raises:
        :raises: ValueError under the following conditions:
                 - new_po is True and po_row is not -1
                 - new_po is False and po_row is -1
                 - new_po is False and po_row is less than 0
                 - new_po is not True and new_po is not False
        '''
        super().__init__(parent=parent)
        if new_po is True and po_row != -1:
            raise ValueError("The new_po parameter was True and a non-default "
                             "value was provided for the po_row parameter. The "
                             "po_row parameter should not be specified when "
                             "creating a new purchase order, which is what "
                             "new_po=True requests.")
        if new_po is False and po_row == -1:
            raise ValueError("The new_po parameter was False but the po_row "
                             "parameter was set to its default value of -1. "
                             "The po_row parameter must be specified when "
                             "opening an existing purchase order, which is "
                             "what new_po=False requests.")
        if new_po is False and po_row < 0:
            raise ValueError("The po_row parameter cannot be negative.")
        if new_po is not True and new_po is not False:
            raise ValueError("Parameter new_po was neither True nor False.")
        self.new_po = new_po
        self._po_model = PurchaseOrderModel(app_config, session, parent)
        self._po_model.connect(self._po_model, 
                               SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                               self._handle_change_in_po_data)
        self._active_po_model_row = -1
        self.valid = False
        if self.new_po is True:
            self._active_po_model_row = self._po_model.rowCount()
            self._po_model.insertRows(self._active_po_model_row)
            # A new purchase order has been created, therefore dirty  
            # starts out as True. 
            self.dirty = True
        else:
            self._active_po_model_row = po_row
            self._validate_active_row()
            # An existing purchase order has been opened, therefore dirty  
            # starts out as False.
            self.dirty = False
        # Active row is now valid.
        
        # Flush the session so that if a new purchase order was created, the 
        # purchase order ID is assigned. It'll be required by the line item
        # model.
        session.flush()
        
        self._active_po = self._po_model.get_purchase_order(
                                                    self._active_po_model_row)
        self.line_item_model = LineItemModel(app_config, session, 
                                             self._active_po)
        self.line_item_model.connect(
                                self.line_item_model, 
                                SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                                self._handle_change_in_line_item_data)
        self.line_item_model.connect(
                                self.line_item_model, 
                                SIGNAL("rowsInserted(QModelIndex,int,int)"),
                                self._handle_line_item_rows_inserted)
        self.line_item_model.connect(
                                self.line_item_model, 
                                SIGNAL("rowsRemoved(QModelIndex,int,int)"),
                                self._handle_line_item_rows_removed)
        self.line_item_model.connect(
                                self.line_item_model,
                                SIGNAL("add_new_product_requested()"),
                                self._handle_add_new_product_request)
        self.add_new_product_requested = pyqtSignal()
        self.totals_calculated = pyqtSignal()
        self._calculate_totals()
        # All initialisation is complete
        self.valid = True
        
    # TODO: Is this method really required? 
    def reset_model(self):
        self.beginResetModel()
        # Make sure active row is still valid
        self._validate_active_row()
        self._active_po = self._po_model.get_purchase_order(
                                                    self._active_po_model_row)
        self.line_item_model.reset_model(self._active_po)
        self._calculate_totals()
        self.dirty = False
        self.endResetModel()
        
    def _validate_active_row(self):
        '''Validates the active purchase order model row.
        
        Ensures that the active purchase order model row (index) is within the
        limits of the purchase order model.
        
        Raises:
        :raises: IndexError if the active purchase order model row indicates a
            row outside the limits of the purchase order model.
        '''
        if self._active_po_model_row >= self._po_model.rowCount():
            raise IndexError(("The self._active_po_model_row parameter was "
                              "out of bounds. "
                              "There are only %s purchase orders, but "
                              "self._active_po_model_row was %s.") % 
                             (str(self._po_model.rowCount()), 
                              str(self._active_po_model_row)))
        
    def rowCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.rowCount.
        
        Returns:
        :returns: 1 because only one purchase order can be the active purchase 
            order.
        '''
        return 1

    def columnCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.columnCount.
        '''
        return PurchaseOrderModel.PURCHASE_ORDER_NUM_COLUMNS
    
    def data(self, index, role=Qt.DisplayRole):
        '''Refer to QAbstractItemModel.data.
        
        The method uses the active purchase order model row variable to create
        an index that is used in a call to the purchase order model's data()
        method.
        '''
        if not index.isValid() or index.row() != 0:
            return None
        po_model_index = self._po_model.createIndex(
                                                self._active_po_model_row,
                                                index.column())
        return self._po_model.data(po_model_index, role)
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        '''Refer to QAbstractItemModel.headerData.
        '''
        return self._po_model.headerData(section, orientation, role)
    
    def flags(self, index):
        '''Refer to QAbstractItemModel.flags.
        '''
        return self._po_model.flags(index)
    
    def setData(self, index, value, role=Qt.EditRole):
        '''Refer to QAbstractItemModel.setData.
        
        The method uses the active purchase order model row variable to create
        an index that is used in a call to the purchase order model's setData()
        method.
        '''
        if index.isValid() and index.row() == 0:
            po_model_index = self._po_model.createIndex(
                                                    self._active_po_model_row,
                                                    index.column())
            result = self._po_model.setData(po_model_index, value, role)
            return result 
        return False

    def do_pre_commit_processing(self):
        '''Perform any processing required before a commit.
        '''
        self._po_model.do_pre_commit_processing()
        self.line_item_model.do_pre_commit_processing()

    def do_post_commit_processing(self):
        '''Perform any processing required after a commit.
        '''
        self.dirty = False
        
    def do_post_rollback_processing(self):
        '''Perform any processing required after a rollback.
        '''
        self.dirty = False
    
    def set_project(self, project_code):
        '''Set the project of the active purchase order. 
        
        The method calls the setData method of the purchase order model.
        
        The purchase order model uses the specified project description to 
        work out the project ID, which is what is actually written to the 
        record.
        
        Args:
        :param project_code: The project description. 
        :type project_code: String
        
        Raises:
        :raises: ModelWriteError if the result of the call to the purchase
            order model's setData method is False. 
        '''
        index = self.createIndex(0, 
                                 PurchaseOrderModel.PROJECT_CODE_COLUMN)
        result = self.setData(index, project_code)
        if result is not True:
            raise ModelWriteError(("There was an error writing project "
                                   "description %s to the model.") % \
                                  project_code)
            
    def get_project(self):
        '''Get the project of the active purchase order.
        
        Returns:
        :return: The project code.
        :rtype: String
        '''
        index = self.createIndex(0, 
                                 PurchaseOrderModel.PROJECT_CODE_COLUMN)
        return self.data(index)
            
    def set_supplier(self, session, supplier_company_name):
        '''Set the supplier of the active purchase order. 
        
        Setting the supplier of the active purchase order means that the 
        current line items must be removed. This method does this.
        
        The method calls the setData method of the purchase order model.
        
        The purchase order model uses the specified supplier company name to 
        work out the supplier ID, which is what is actually written to the 
        record.
        
        Args:
        :param session: The SQLAlchemy session in use. 
        :type session: Session object (the class created by the call to  
            :func:`sessionmaker` in :mod:`sqlasession`).
        :param supplier_company_name: The supplier company name.
        :type supplier_company_name: String
        
        Raises:
        :raises: ModelWriteError if the result of the call to the purchase
            order model's setData method is False.
        '''
        if self.has_line_items() is True:
            self.line_item_model.remove_all_rows()
            # Flush the session to ensure that all removed line item objects are
            # marked for deletion.
            session.flush()
        index = self.createIndex(
                            0, 
                            PurchaseOrderModel.SUPPLIER_COMPANY_NAME_COLUMN)
        result = self.setData(index, supplier_company_name)
        if result is not True:
            raise ModelWriteError(("There was an error writing supplier "
                                   "company name %s to the model.") % \
                                  supplier_company_name)
        # Changing the purchase order supplier must reset the line item model.
        self.line_item_model.prepare_for_supplier_change()
        self.line_item_model.reset_model(self._active_po)
        
    def get_supplier(self):
        '''Get the supplier of the active purchase order.
        
        Returns:
        :return: The supplier company name.
        :rtype: String
        '''
        index = self.createIndex(
                            0, 
                            PurchaseOrderModel.SUPPLIER_COMPANY_NAME_COLUMN)
        return self.data(index)
        
    def set_order_status(self, order_status):
        '''Set the order status of the active purchase order.
        
        The method calls the setData method of the purchase order model.
        
        :param order_status: The order status.
        :type order_status: String
        
        Raises:
        :raises: ModelWriteError if the result of the call to the purchase
            order model's setData method is False.
        '''
        index = self.createIndex(0, 
                                 PurchaseOrderModel.ORDER_STATUS_COLUMN)
        result = self.setData(index, order_status)
        if result is not True:
            raise ModelWriteError(("There was an error writing order status %s "
                                   "to the model.") % order_status)
            
    def get_order_status(self):
        '''Get the order status of the active purchase order.
        
        Returns:
        :return: The order status.
        :rtype: String
        '''
        index = self.createIndex(0, 
                                 PurchaseOrderModel.ORDER_STATUS_COLUMN)
        return self.data(index)
            
    def set_payment_terms(self, payment_terms):
        '''Set the payment terms of the active purchase order.
        
        The method calls the setData method of the purchase order model.
        
        :param payment_terms: The payment terms.
        :type payment_terms: String
        
        Raises:
        :raises: ModelWriteError if the result of the call to the purchase
            order model's setData method is False.
        '''
        index = self.createIndex(0, 
                                 PurchaseOrderModel.PAYMENT_TERMS_COLUMN)
        result = self.setData(index, payment_terms)
        if result is not True:
            raise ModelWriteError(("There was an error writing payment terms "
                                   "%s to the model.") % payment_terms)
    
    def get_payment_terms(self):
        '''Get the payment terms of the active purchase order.
        
        Returns:
        :return: The payment terms.
        :rtype: String
        '''
        index = self.createIndex(0, 
                                 PurchaseOrderModel.PAYMENT_TERMS_COLUMN)
        return self.data(index)
    
    def get_active_purchase_order(self):
        '''Retrieve the active purchase order object.
        
        Returns:
        :return: The active purchase order object.
        :rtype: purchaseorder.PurchaseOrder or None
        '''
        if self._active_po:
            return self._active_po
        else:
            return None

    def has_line_items(self):
        '''Determine if the active purchase order has line items.
        
        Returns:
        :return: True if the active purchase order has line items. 
            Otherwise False.
        :rtype: Boolean
        '''
        if self.line_item_model.rowCount() > 1:
            return True
        return False
    
    def remove_all_line_items(self):
        '''Remove all of the line items of the active purchase order.
        
        Calls the :meth:`LineItemModel.remove_all_rows` to achieve this.
        '''
        self.line_item_model.remove_all_rows()

    def _calculate_totals(self):
        '''Calculate the total values of the active purchase order.
        
        The totals that are calculated are the total excluding tax, the total
        tax, and the total including tax.
        
        Emits the totals_calculated signal to allow the main form to update its
        widgets.
        '''
        # Total excluding tax
        self.total_price = self.line_item_model.calculate_total_excluding_tax()
        index = self.createIndex(0,
                                 PurchaseOrderModel.TOTAL_EXCLUDING_TAX_COLUMN)
        self.setData(index, self.total_price, Qt.EditRole)
        # Total tax
        self.total_tax = self.line_item_model.calculate_total_tax()
        index = self.createIndex(0, 
                                 PurchaseOrderModel.TOTAL_TAX_COLUMN)
        self.setData(index, self.total_tax, Qt.EditRole)
        # Total including tax
        self.total = self.total_price + self.total_tax
        index = self.createIndex(0, 
                                 PurchaseOrderModel.TOTAL_INCLUDING_TAX_COLUMN)
        self.setData(index, self.total, Qt.EditRole)
        self.emit(SIGNAL("totals_calculated()"))

    def _handle_change_in_po_data(self, top_left_index, 
                                  bottom_right_index):
        '''Slot for the dataChanged signal of the purchase order model.
        
        Sets the dirty indicator to True and re-calculates the total values 
        of the active purchase order.
        
        Args:
            Refer to QAbstractItemModel.dataChanged.
        '''
        print("_handle_change_in_po_data")
        self.dirty = True
        self._calculate_totals()
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                  top_left_index, bottom_right_index)
            
    def _handle_change_in_line_item_data(self, top_left_index, 
                                         bottom_right_index):
        '''Slot for the dataChanged signal of the line item model.
        
        Sets the dirty indicator to True and re-calculates the total values 
        of the active purchase order.
        
        Args:
            Refer to QAbstractItemModel.dataChanged.
        '''
        print("_handle_change_in_line_item_data")
        self.dirty = True
        self._calculate_totals()
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                  top_left_index, bottom_right_index)
        
    def _handle_line_item_rows_removed(self, parent_index, start_item, 
                                       end_item):
        '''Slot for the rowsRemoved signal of the line item model.
        
        Sets the dirty indicator to True and re-calculates the total values 
        of the active purchase order.
        
        Args:
            Refer to QAbstractItemModel.rowsRemoved.
        '''
        print("_handle_line_item_rows_removed")
        self.dirty = True
        self._calculate_totals()
        
    def _handle_line_item_rows_inserted(self, parent_index, start_item, 
                                        end_item):
        '''Slot for the rowsInserted signal of the line item model.
        
        Sets the dirty indicator to True and re-calculates the total values 
        of the active purchase order.
        
        Args:
            Refer to QAbstractItemModel.rowsInserted.
        '''
        print("_handle_line_item_rows_inserted")
        self.dirty = True
        self._calculate_totals()
        
    def _handle_add_new_product_request(self):
        '''Slot for the add_new_product_requested signal of the line item model.
        
        Emits the add_new_product_requested signal of the active purchase order 
        model, allowing the main form to bring up the products dialog. 
        '''
        self.emit(SIGNAL("add_new_product_requested()"))
