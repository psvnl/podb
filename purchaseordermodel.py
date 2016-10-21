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
import logging
from decimal import Decimal
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from conversions import (monetary_int_to_decimal, monetary_decimal_to_int,
                         percentage_int_to_decimal)
from project import Project
from purchaseorder import PurchaseOrder
from supplier import Supplier
from userconfigmodel import UserConfigReader


class PrerequisitesError(Exception):
    '''Exception raised if the prerequisites of the purchase order model are
    not met. 
    '''
    pass


class PurchaseOrderNumberError(Exception):
    '''Exception raised if the calculated order number has been used before. 
    '''
    pass


class PurchaseOrderModel(QAbstractTableModel):
    '''Data model for the purchase order table.
    '''

    PURCHASE_ORDER_NUM_COLUMNS = 14
    (ORDER_NUMBER_COLUMN,
     ORDER_DATE_COLUMN,
     DELIVERY_ADDRESS_COLUMN,
     DELIVERY_ADDRESS_GPS_COORDINATES_COLUMN,
     DELIVERY_DATE_COLUMN,
     PAYMENT_TERMS_COLUMN,
     ORDER_STATUS_COLUMN,
     NOTES_COLUMN,
     TAX_RATE_COLUMN,
     TOTAL_EXCLUDING_TAX_COLUMN,
     TOTAL_TAX_COLUMN,
     TOTAL_INCLUDING_TAX_COLUMN,
     PROJECT_CODE_COLUMN,
     SUPPLIER_COMPANY_NAME_COLUMN) = range(PURCHASE_ORDER_NUM_COLUMNS)

    def __init__(self, app_config, session, parent=None):
        '''Initialise the PurchaseOrderModel object.
        
        Loads a local purchase orders list (self.purchase_orders) with the 
        result of a query for all purchase orders.
        
        Args:
        :param session: The SQLAlchemny session in use. 
        :type session: Session object (the class created by the call to  
            :func:`sessionmaker` in :mod:`sqlasession`).
        :param parent: The model's parent.
        :type parent: QObject
        '''
        super().__init__(parent=parent)
        self.session = session
        self.app_config = app_config
        with self.session.no_autoflush:
            self.purchase_orders = self.session.query(PurchaseOrder).all()
        
    def do_pre_commit_processing(self):
        '''Perform any processing required before a commit.
        '''
        pass
        
    def rowCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.rowCount.
        '''
        return len(self.purchase_orders)

    def columnCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.columnCount.
        '''
        return self.PURCHASE_ORDER_NUM_COLUMNS
    
    def data(self, index, role=Qt.DisplayRole):
        '''Refer to QAbstractItemModel.data.
        '''
        if not index.isValid() or \
        not (0 <= index.row() < self.rowCount()):
            return None
        order = self.purchase_orders[index.row()]
        column = index.column()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if column == self.ORDER_NUMBER_COLUMN:
                return order.order_number
            elif column == self.ORDER_DATE_COLUMN:
                date = QDate(order.order_date.year,
                             order.order_date.month,
                             order.order_date.day)
                return date
            elif column == self.DELIVERY_ADDRESS_COLUMN:
                return order.delivery_address
            elif column == self.DELIVERY_ADDRESS_GPS_COORDINATES_COLUMN:
                return order.delivery_address_gps_coordinates
            elif column == self.DELIVERY_DATE_COLUMN:
                date = QDate(order.delivery_date.year,
                             order.delivery_date.month,
                             order.delivery_date.day)
                return datetime
            elif column == self.PAYMENT_TERMS_COLUMN:
                return order.payment_terms
            elif column == self.ORDER_STATUS_COLUMN:
                return order.order_status
            elif column == self.NOTES_COLUMN:
                return order.notes
            elif column == self.TAX_RATE_COLUMN:
                # Display tax rate as % with two digits and no decimal point.
                # The tax rate is in the referenced user config record. 
                return "{:2.0%}".format(percentage_int_to_decimal(
                                                order.user_config.tax_rate))
            elif column == self.TOTAL_EXCLUDING_TAX_COLUMN:
                # Display totals with two decimal places and comma separators.
                converted_value = monetary_int_to_decimal(
                                                    order.total_excluding_tax, 
                                                    self.app_config)
                return "R {:,.2f}".format(converted_value)
            elif column == self.TOTAL_TAX_COLUMN:
                converted_value = monetary_int_to_decimal(
                                                    order.total_tax, 
                                                    self.app_config)
                return "R {:,.2f}".format(converted_value)
            elif column == self.TOTAL_INCLUDING_TAX_COLUMN:
                converted_value = monetary_int_to_decimal(
                                                    order.total_including_tax, 
                                                    self.app_config)
                return "R {:,.2f}".format(converted_value)
            elif column == self.PROJECT_CODE_COLUMN:
                return order.project.code
            elif column == self.SUPPLIER_COMPANY_NAME_COLUMN:
                return order.supplier.company_name
            else:
                return None
        elif role == Qt.TextAlignmentRole:
            if column == self.TAX_RATE_COLUMN:
                return Qt.AlignHCenter | Qt.AlignVCenter
            elif column == self.TOTAL_EXCLUDING_TAX_COLUMN:
                return Qt.AlignRight | Qt.AlignVCenter
            elif column == self.TOTAL_TAX_COLUMN:
                return Qt.AlignRight | Qt.AlignVCenter
            elif column == self.TOTAL_INCLUDING_TAX_COLUMN:
                return Qt.AlignRight | Qt.AlignVCenter
        else:
            return None
        
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        '''Refer to QAbstractItemModel.headerData.
        '''
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignLeft | Qt.AlignVCenter)
            return int(Qt.AlignRight | Qt.AlignVCenter)
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == self.ORDER_NUMBER_COLUMN:
                return "Order Number"
            elif section == self.ORDER_DATE_COLUMN:
                return "Order Date"
            elif section == self.DELIVERY_ADDRESS_COLUMN:
                return "Delivery Address"
            elif section == self.DELIVERY_ADDRESS_GPS_COORDINATES_COLUMN:
                return "Delivery Address GPS Coordinates"
            elif section == self.DELIVERY_DATE_COLUMN:
                return "Delivery Date"
            elif section == self.PAYMENT_TERMS_COLUMN:
                return "Payment Terms"
            elif section == self.ORDER_STATUS_COLUMN:
                return "Order Status"
            elif section == self.NOTES_COLUMN:
                return "Notes"
            elif section == self.TAX_RATE_COLUMN:
                return "{} Rate".format(self.app_config.locale.tax_name)
            elif section == self.TOTAL_EXCLUDING_TAX_COLUMN:
                return "Total Excluding {}".format(
                                            self.app_config.locale.tax_name)
            elif section == self.TOTAL_TAX_COLUMN:
                return "Total {}".format(self.app_config.locale.tax_name)
            elif section == self.TOTAL_INCLUDING_TAX_COLUMN:
                return "Total Including {}".format(
                                            self.app_config.locale.tax_name)
            elif section == self.PROJECT_CODE_COLUMN:
                return "Project"
            elif section == self.SUPPLIER_COMPANY_NAME_COLUMN:
                return "Supplier"
        return int(section + 1)
    
    def flags(self, index):
        '''Refer to QAbstractItemModel.flags.
        '''
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | 
                            Qt.ItemIsEditable)
        
    def setData(self, index, value, role=Qt.EditRole):
        '''Refer to QAbstractItemModel.setData.
        '''
        if index.isValid() and \
        (0 <= index.row() < self.rowCount()):
            column = index.column()
            try:
                if column == self.ORDER_DATE_COLUMN or \
                   column == self.DELIVERY_DATE_COLUMN:
                    self._validate_and_set_date_data(index, value)
                elif column == self.TAX_RATE_COLUMN:
                    # The tax rate column is not editable.
                    return False
                elif column == self.TOTAL_EXCLUDING_TAX_COLUMN or \
                     column == self.TOTAL_TAX_COLUMN or \
                     column == self.TOTAL_INCLUDING_TAX_COLUMN:
                    self._validate_and_set_decimal_data(index, value)
                elif column == self.PROJECT_CODE_COLUMN:
                    self._validate_and_set_project(index, value)
                elif column == self.SUPPLIER_COMPANY_NAME_COLUMN:
                    self._validate_and_set_supplier(index, value)
                else:
                    self._validate_and_set_general_data(index, value)
            except ValueError:
                logging.debug("ValueError")
                # If the user types in something stupid then don't do anything.
                return False
            return True
        return False
    
    def _validate_and_set_date_data(self, index, requested_value):
        '''Validate and set date data, i.e., the order date and delivery date.
        
        The method checks that the requested value is different to the current
        value. If it is then the data is set.
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written.
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param requested_value: The requested value for the field.
        :type requested_value: String
        
        Raises:
        :raises: ValueError if the index parameter indicates a column that is
            not date data.
        '''
        row = index.row()
        column = index.column()
        if column == self.ORDER_DATE_COLUMN:
            current_date = self.purchase_orders[row].order_date
            requested_date = requested_value.toPyDateTime().date()
        elif column == self.DELIVERY_DATE_COLUMN:
            current_date = self.purchase_orders[row].delivery_date
            requested_date = requested_value.toPyDateTime()
        else:
            raise ValueError(("Invalid index. Column value {} is not "
                              "date data.").format(column))
        if current_date != requested_date:
            if column == self.ORDER_DATE_COLUMN:
                self.purchase_orders[row].order_date = requested_date
            elif column == self.DELIVERY_DATE_COLUMN:
                self.purchase_orders[row].delivery_date = requested_date
            # Emit the data changed signal.
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
        
    def _validate_and_set_decimal_data(self, index, requested_value):
        '''Validate and set decimal data, i.e., the tax rate and totals.
        
        The method checks that the requested value is different to the current
        value. If it is then the data is set.
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written.
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param requested_value: The requested value for the field.
        :type requested_value: String
        
        Raises:
        :raises: ValueError if the index parameter indicates a column that is
            not decimal data.
        '''
        row = index.row()
        column = index.column()
        if column == self.TOTAL_EXCLUDING_TAX_COLUMN:
            current_value = self.purchase_orders[row].total_excluding_tax
            # Ensure converted value is rounded to two decimal places so that 
            # the comparison is meaningful.
            converted_requested_value = monetary_decimal_to_int(requested_value, 
                                                                self.app_config) 
        elif column == self.TOTAL_TAX_COLUMN:
            current_value = self.purchase_orders[row].total_tax
            # Ensure converted value is rounded to two decimal places so that 
            # the comparison is meaningful.
            converted_requested_value = monetary_decimal_to_int(requested_value, 
                                                                self.app_config)
        elif column == self.TOTAL_INCLUDING_TAX_COLUMN:
            current_value = self.purchase_orders[row].total_including_tax
            # Ensure converted value is rounded to two decimal places so that 
            # the comparison is meaningful.
            converted_requested_value = monetary_decimal_to_int(requested_value, 
                                                                self.app_config)
        else:
            raise ValueError(("Invalid index. Column value {} is not "
                              "decimal data.").format(column))
        if current_value != converted_requested_value:
            if column == self.TOTAL_EXCLUDING_TAX_COLUMN:
                self.purchase_orders[row].total_excluding_tax = \
                                            converted_requested_value
            elif column == self.TOTAL_TAX_COLUMN:
                self.purchase_orders[row].total_tax = \
                                            converted_requested_value
            elif column == self.TOTAL_INCLUDING_TAX_COLUMN:
                self.purchase_orders[row].total_including_tax = \
                                            converted_requested_value
            # Emit the data changed signal.
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
            
    def _validate_and_set_project(self, index, project_code):
        '''Validate and set the project. 
        
        The method checks that the requested project is different to the 
        current project. If it is then the data is set.
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written.
        
        :param index: The model index being updated.
        :type index: QModelIndex
        :param project_code: The requested project code.
        :type project_code: String
        '''
        row = index.row()
        if project_code != \
                        self.purchase_orders[row].project.code:
            with self.session.no_autoflush:
                self.purchase_orders[row].project = \
                    self.session.query(Project).\
                    filter(Project.code == project_code).one()
                # Emit the data changed signal.
                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                          index, index)
                
    def _validate_and_set_supplier(self, index, company_name):
        '''Validate and set the supplier.
        
        The method checks that the requested supplier is different to the 
        current supplier. If it is then the data is set.
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written.
        
        :param index: The model index being updated.
        :type index: QModelIndex
        :param company_name: The requested supplier company name.
        :type company_name: String
        '''
        row = index.row()
        if company_name != self.purchase_orders[row].supplier.company_name:
            with self.session.no_autoflush:
                self.purchase_orders[row].supplier = \
                    self.session.query(Supplier).\
                    filter(Supplier.company_name == company_name).one()
                # Emit the data changed signal.
                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                          index, index)
            
    def _validate_and_set_general_data(self, index, requested_value):
        '''Validate and set data other than the dates, decimal data, project
        ID and supplier ID.
        
        The method checks that the requested value is different to the current
        value. If it is then the data is set.
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written.
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param requested_value: The requested value for the field.
        :type requested_value: String
        
        Raises:
        :raises: ValueError if the index parameter indicates a column that is
            not "general data".
        '''
        row = index.row()
        column = index.column()
        if column == self.ORDER_NUMBER_COLUMN:
            current_value = self.purchase_orders[row].order_number
        elif column == self.DELIVERY_ADDRESS_COLUMN:
            current_value = self.purchase_orders[row].delivery_address
        elif column == self.DELIVERY_ADDRESS_GPS_COORDINATES_COLUMN:
            current_value = self.purchase_orders[row].\
                                delivery_address_gps_coordinates
        elif column == self.PAYMENT_TERMS_COLUMN:
            current_value = self.purchase_orders[row].payment_terms
        elif column == self.ORDER_STATUS_COLUMN:
            current_value = self.purchase_orders[row].order_status
        elif column == self.NOTES_COLUMN:
            current_value = self.purchase_orders[row].notes
        else:
            raise ValueError(("Invalid index. Column value {} is not "
                              "considered to be \"general data\".").format(
                                                                        column))
        if current_value != requested_value:
            if column == self.ORDER_NUMBER_COLUMN:
                self.purchase_orders[row].order_number = requested_value
            elif column == self.DELIVERY_ADDRESS_COLUMN:
                self.purchase_orders[row].delivery_address = requested_value
            elif column == self.DELIVERY_ADDRESS_GPS_COORDINATES_COLUMN:
                self.purchase_orders[row].\
                    delivery_address_gps_coordinates = requested_value
            elif column == self.PAYMENT_TERMS_COLUMN:
                self.purchase_orders[row].payment_terms = requested_value
            elif column == self.ORDER_STATUS_COLUMN:
                self.purchase_orders[row].order_status = requested_value
            elif column == self.NOTES_COLUMN:
                self.purchase_orders[row].notes = requested_value
            # Emit the data changed signal.
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
        
    def _calculate_purchase_order_number(self):
        '''Create a new purchase order number.
        
        The purchase order number starts at <Prefix>00001 and is incremented
        each time a new purchase order is created. The purchase order number
        does not correlate to the purchase order primary key.
        
        The <Prefix> comes from the application settings file.
        
        Returns:
        :return: The order number in the form <Prefix>XXXXX.
        :rtype: String
        
        Raises:
        :raises: PurchaseOrderNumberError if it is found that the calculated
            purchase order number has been used before.
        '''
        with self.session.no_autoflush:
            result = self.session.query(PurchaseOrder).count()
        if result == 0:
            new_order_number_int = 1
        else:
            new_order_number_int = result + 1
        new_order_number = "{}{:05d}".format(
                                self.app_config.purchaseorder.number_prefix,
                                new_order_number_int)
        # Make sure that the purchase order number has not been used before.
        if self.session.query(PurchaseOrder).\
            filter(PurchaseOrder.order_number == new_order_number).\
            count() != 0:
            raise PurchaseOrderNumberError(
                            ("The calculated order number ({}) "
                             "has been used before.").format(new_order_number))
        return new_order_number
    
    def insertRows(self, position, rows=1, index=QModelIndex()):
        '''Refer to QAbstractItemModel.insertRows.
        '''
        # Insertion of a PO is not allowed, only addition of a PO.
        assert position == self.rowCount()
        # Only one PO can be inserted at a time.
        assert rows == 1
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        order_number = self._calculate_purchase_order_number() 
        # Initialise the order date and delivery date to the current date.
        order_date = datetime.date.today()
        delivery_date = datetime.datetime.now()
        # Create a reader to access the latest user config.
        user_config = UserConfigReader(self.session) 
        new_po = PurchaseOrder(
                    order_number=order_number,
                    order_date=order_date,
                    delivery_address=user_config.company.physical_address,
                    delivery_address_gps_coordinates=\
                        user_config.company.gps_coordinates,
                    delivery_date=delivery_date,
                    payment_terms=\
                        user_config.purchaseorder.default_payment_terms,
                    order_status=\
                        user_config.purchaseorder.default_order_status,
                    notes="",
                    total_excluding_tax=0,
                    total_tax=0,
                    total_including_tax=0,
                    user_config_id=user_config.db_record.id)
        with self.session.no_autoflush:
            if self.session.query(Supplier).count() != 0:
                new_po.supplier = self.session.query(Supplier).\
                                    order_by(Supplier.id).first()
                if new_po.supplier is None:
                    raise PrerequisitesError(
                                    "The purchase order model requires at "
                                    "least one supplier. But none were found.")
            if self.session.query(Project).count() != 0:
                new_po.project = self.session.query(Project).\
                                    order_by(Project.id).first()
                if new_po.project is None:
                    raise PrerequisitesError(
                                    "The purchase order model requires at "
                                    "least one project. But none were found.")
        self.session.add(new_po)
        self.purchase_orders.append(new_po)
        self.endInsertRows()
        return True
    
    def get_purchase_order(self, row):
        '''Retrieve a purchase order object.
        
        Args:
        :param row: The table row index for the purchase order that must be 
            returned.
        :type row: Integer
        
        Returns:
        :return: The requested purchase order object.
        :rtype: sqlasession.PurchaseOrder
        '''
        if (0 <= row < self.rowCount()):
            return self.purchase_orders[row]
    
    