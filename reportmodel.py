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

from decimal import Decimal
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from conversions import monetary_int_to_decimal, percentage_int_to_decimal
from project import Project
from purchaseorderproduct import PurchaseOrderProduct
from supplier import Supplier


class ReportModel(QAbstractTableModel):
    '''Data model for the report result table.
    '''
    
    # Only two reports supported for now.
    REPORT_TYPE_NONE = -1
    REPORT_TYPE_ITEMS_BY_PROJECT = 0
    REPORT_TYPE_ITEMS_BY_SUPPLIER = 1
    
    REPORT_NUM_COLUMNS = 11
    (ORDER_NUMBER_COLUMN,
     ORDER_DATE_COLUMN,
     ORDER_STATUS_COLUMN,
     PROJECT_CODE_COLUMN,
     SUPPLIER_COMPANY_NAME_COLUMN,
     PART_NUMBER_COLUMN,
     DESCRIPTION_COLUMN,
     UNIT_PRICE_COLUMN,
     DISCOUNT_COLUMN,
     QUANTITY_COLUMN,
     LINE_PRICE_COLUMN) = range(REPORT_NUM_COLUMNS)

    def __init__(self, app_config, session, report_type, additional_data, 
                 start_date, end_date, parent=None):
        '''Initialise the ReportModel object.
        
        Uses the supplied parameters to load a local list of line items 
        (self.line_items) by querying the database.
        
        Args:
        :param session: The SQLAlchemny session in use. 
        :type session: Session object (the class created by the call to  
            :func:`sessionmaker` in :mod:`sqlasession`).
        :param report_type: The type of report. One of 
            REPORT_TYPE_ITEMS_BY_PROJECT or REPORT_TYPE_ITEMS_BY_SUPPLIER.  
        :type report_type: Integer
        :param additional_data: The project description if report type is
            REPORT_TYPE_ITEMS_BY_PROJECT, or the supplier company name is 
            REPORT_TYPE_ITEMS_BY_SUPPLIER.
        :type additional_data: String
        :param start_date: The start date of the date range.
        :type start_date: datetime.date
        :param end_date: The end date of the date range.
        :type end_date: datetime.date
        :param parent: The model's parent.
        :type parent: QObject
        
        Raises:
        :raises: ValueError if the report type is not one of the recognised
            report types.
        '''
        super().__init__(parent=parent)
        self.session = session
        self.app_config = app_config
        if report_type != self.REPORT_TYPE_ITEMS_BY_PROJECT and \
           report_type != self.REPORT_TYPE_ITEMS_BY_SUPPLIER:
            raise ValueError("The report_type parameter is invalid.")
        self.line_items = []
        self.report_type = report_type
        if self.report_type == self.REPORT_TYPE_ITEMS_BY_PROJECT:
            self._load_line_items_by_project(additional_data, 
                                             start_date,
                                             end_date)
        elif self.report_type == self.REPORT_TYPE_ITEMS_BY_SUPPLIER:
            self._load_line_items_by_supplier(additional_data, 
                                              start_date, 
                                              end_date)

    def _load_line_items_by_project(self, project_code, start_date, 
                                    end_date):
        '''Load the local list of line items for the "items by project" report.
        
        Args:
        :param project_code: The project description.
        :type project_code: String
        :param start_date: The start date of the date range.
        :type start_date: datetime.date
        :param end_date: The end date of the date range.
        :type end_date: datetime.date
        '''
        project = self.session.query(Project).\
                        filter(Project.code == project_code).one()
        po_products = self.session.query(PurchaseOrderProduct).all()
        for po_product in po_products:
            if po_product.purchase_order.project_id == project.id:
                if po_product.purchase_order.order_date >= start_date and \
                   po_product.purchase_order.order_date <= end_date:
                    self.line_items.append(po_product)
        self.line_items.sort(key=lambda x: x.purchase_order_id, reverse=False)
    
    def _load_line_items_by_supplier(self, company_name, start_date, 
                                     end_date):
        '''Load the local list of line items for the "items by supplier" report.
        
        Args:
        :param company_name: The supplier company name.
        :type company_name: String
        :param start_date: The start date of the date range.
        :type start_date: datetime.date
        :param end_date: The end date of the date range.
        :type end_date: datetime.date
        '''
        supplier = self.session.query(Supplier).\
                        filter(Supplier.company_name == \
                               company_name).one()
        po_products = self.session.query(PurchaseOrderProduct).all()
        for po_product in po_products:
            if po_product.purchase_order.supplier_id == supplier.id:
                if po_product.purchase_order.order_date >= start_date and \
                   po_product.purchase_order.order_date <= end_date:
                    self.line_items.append(po_product)
        self.line_items.sort(key=lambda x: x.purchase_order_id, reverse=False)

    def rowCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.rowCount.
        '''
        return len(self.line_items)
    
    def columnCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.columnCount.
        '''
        return self.REPORT_NUM_COLUMNS
    
    def data(self, index, role=Qt.DisplayRole):
        '''Refer to QAbstractItemModel.data.
        '''
        if not index.isValid() or \
        not (0 <= index.row() < self.rowCount()):
            return None
        line_item = self.line_items[index.row()]
        column = index.column()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if column == self.ORDER_NUMBER_COLUMN:
                return line_item.purchase_order.order_number
            elif column == self.ORDER_DATE_COLUMN:
                return line_item.purchase_order.order_date.strftime("%Y-%m-%d")
            elif column == self.ORDER_STATUS_COLUMN:
                return line_item.purchase_order.order_status
            elif column == self.PROJECT_CODE_COLUMN:
                return line_item.purchase_order.project.code
            elif column == self.SUPPLIER_COMPANY_NAME_COLUMN:
                return line_item.purchase_order.supplier.company_name
            elif column == self.PART_NUMBER_COLUMN:
                return line_item.product.part_number
            elif column == self.DESCRIPTION_COLUMN:
                return line_item.product.product_description
            elif column == self.UNIT_PRICE_COLUMN:
                converted_value = monetary_int_to_decimal(line_item.unit_price, 
                                                          self.app_config)
                return "R {:,.2f}".format(converted_value)
            elif column == self.DISCOUNT_COLUMN:
                converted_value = percentage_int_to_decimal(line_item.discount)
                return "{:2.0%}".format(converted_value)
            elif column == self.QUANTITY_COLUMN:
                return str(line_item.quantity)
            elif column == self.LINE_PRICE_COLUMN:
                converted_unit_price = monetary_int_to_decimal(
                                                        line_item.unit_price,
                                                        self.app_config)
                converted_discount = percentage_int_to_decimal(
                                                        line_item.discount)
                line_price = self._calculate_line_price(converted_unit_price,
                                                        converted_discount,
                                                        line_item.quantity)
                return "R {:,.2f}".format(line_price)
        elif role == Qt.TextAlignmentRole:
            if column == self.ORDER_DATE_COLUMN:
                return Qt.AlignHCenter | Qt.AlignVCenter
            elif column == self.UNIT_PRICE_COLUMN:
                return Qt.AlignRight | Qt.AlignVCenter
            elif column == self.DISCOUNT_COLUMN:
                return Qt.AlignHCenter | Qt.AlignVCenter
            elif column == self.QUANTITY_COLUMN:
                return Qt.AlignHCenter | Qt.AlignVCenter
            elif column == self.LINE_PRICE_COLUMN:
                return Qt.AlignRight | Qt.AlignVCenter
            else:
                return Qt.AlignLeft | Qt.AlignVCenter
        else:
            return None
    
    def _calculate_line_price(self, unit_price, discount, quantity):
        '''Calculate the line total of a line item.
        
        Args:
        :param unit_price: Line item product's unit price.
        :type unit_price: Decimal
        :param discount: Line item product's discount.
        :type discount: Decimal 
        :param quantity: Line item quantity.
        :type quantity: Integer
        
        Returns:
        :return: The line total value.
        :rtype: Decimal
        '''
        line_price = (unit_price - (unit_price * discount)) * Decimal(quantity)
        return line_price
        
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
                return "Order No."
            elif section == self.ORDER_DATE_COLUMN:
                return "Order Date"
            elif section == self.ORDER_STATUS_COLUMN:
                return "Status"
            elif section == self.PROJECT_CODE_COLUMN:
                return "Project"
            elif section == self.SUPPLIER_COMPANY_NAME_COLUMN:
                return "Supplier"
            elif section == self.PART_NUMBER_COLUMN:
                return "Part No."
            elif section == self.DESCRIPTION_COLUMN:
                return "Description"
            elif section == self.UNIT_PRICE_COLUMN:
                return "Unit Price"
            elif section == self.DISCOUNT_COLUMN:
                return "Discount"
            elif section == self.QUANTITY_COLUMN:
                return "Quantity"
            elif section == self.LINE_PRICE_COLUMN:
                return "Total Price"
        return int(section + 1)
    
    def calculate_total_value(self):
        '''Calculate the total value of the report line items (excluding tax).
        '''
        total_value = Decimal("0.0")
        for line_item in self.line_items:
            converted_unit_price = monetary_int_to_decimal(
                                                        line_item.unit_price,
                                                        self.app_config)
            converted_discount = percentage_int_to_decimal(
                                                    line_item.discount)
            total_value += self._calculate_line_price(converted_unit_price,
                                                      converted_discount,
                                                      line_item.quantity)
        return total_value
    
    def get_row(self, row):
        '''Retrieve a single row of the report model.

        The list contains: order number, order date, order status, project
        description, supplier company name, part number, description, 
        unit price, discount, quantity, and line price.
        
        Args:
        :param row: The row to retrieve.
        :type row: Integer
        
        Returns:
        :return: A list containing the data for the specified row of the line
            item model. 
        :rtype: List containing eleven Strings 
            
        Raises:
        :raises: ValueError if the row parameter is out of bounds.  
        '''
        row_data = []
        if (0 <= row < self.rowCount()):
            for col in range(self.columnCount()):
                index = self.createIndex(row, col)
                row_data.append(self.data(index, Qt.DisplayRole))
            return row_data
        raise ValueError("Invalid row parameter.")
    