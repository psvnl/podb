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
from conversions import (monetary_int_to_decimal, monetary_decimal_to_int,
                         monetary_float_to_int, percentage_int_to_decimal, 
                         percentage_decimal_to_int)
from customdelegates import ADD_NEW_PRODUCT_COMBO_STRING
from datavalidation import show_error_product_already_on_po
from product import Product
from purchaseorderproduct import PurchaseOrderProduct
from userconfigmodel import UserConfigReader


class ValidPurchaseOrderProduct(object):
    '''Groups a PurchaseOrderProduct object with a validity.
    '''
    
    def __init__(self, po_product, valid):
        self.po_product = po_product
        self.valid = valid
        
    def __repr__(self):
        return ("<ValidPurchaseOrderProduct(valid=%s,"
                "po_product=%s)>") % (str(self.valid), 
                                      str(self.po_product))


class LineItemModel(QAbstractTableModel):
    '''Data model for the line items on a purchase order.
    '''

    LINE_ITEM_NUM_COLUMNS = 6
    (PART_NUMBER_COLUMN, 
     DESCRIPTION_COLUMN, 
     UNIT_PRICE_COLUMN,
     DISCOUNT_COLUMN, 
     QUANTITY_COLUMN, 
     LINE_PRICE_COLUMN) = range(LINE_ITEM_NUM_COLUMNS)

    def __init__(self, app_config, session, purchase_order, parent=None):
        '''Initialises the LineItemModel object.
        
        In particular, initialises a local list of products from those in the 
        specified purchase order object.    
        
        Args:
        :param session: The SQLAlchemny session in use. 
        :type session: Session object (the class created by the call to  
            :func:`sessionmaker` in :mod:`sqlasession`).
        :param purchase_order: The active purchase order object.
        :type purchase_order: purchaseorder.PurchaseOrder
        :param parent: The model's parent.
        :type parent: QObject
        '''
        super().__init__(parent=parent)
        self.session = session
        self.app_config = app_config
        self._po = None
        self._po_prod_buffer = []
        self.reset_model(purchase_order)
        self.add_new_product_requested = pyqtSignal()
            
    def reset_model(self, purchase_order):
        '''Resets the line item model.
        
        The line item model is an interface to a purchase order's associated 
        products collection. Changing the purchase order requires a reset
        of the line item model.
        
        This method is the interface to use when the active purchase order 
        changes. It clears the local list of products and reloads the list from
        the new purchase order object.
        
        Args:
        :param purchase_order: The active purchase order object.
        :type purchase_order: purchaseorder.PurchaseOrder
        '''
        self.beginResetModel()
        # Assumes that the empty row has not been added, or has already been 
        # removed before a session save. 
        self._po = purchase_order
        # Initialise list of PurchaseOrderProduct objects. The ones provided in 
        # the purchase order must be valid since they have come from the 
        # database.
        self._po_prod_buffer.clear()
        for entry in self._po.products:
            self._po_prod_buffer.append(ValidPurchaseOrderProduct(entry,
                                                                  True))
        # Always have one (empty) line item at the end.
        self.restore_empty_row()
        self.endResetModel()
        
    def do_pre_commit_processing(self):
        '''Perform all processing required before a session commit.
        
        The method clears the active purchase order's list of products, and 
        then loops through the local list of products and adds each of the 
        valid products to the purchase order's list of products.
        '''
        if self._po:
            self._po.products.clear()
            for entry in self._po_prod_buffer:
                if entry.valid is True:
                    self._po.products.append(entry.po_product)
    
    def prepare_for_supplier_change(self):
        pass
            
    def rowCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.rowCount.
        '''
        return len(self._po_prod_buffer)
    
    def columnCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.columnCount.
        '''
        return self.LINE_ITEM_NUM_COLUMNS
    
    def data(self, index, role=Qt.DisplayRole):
        '''Refer to QAbstractItemModel.data.
        '''
        if not index.isValid() or \
        not (0 <= index.row() < self.rowCount()):
            return None
        po_product = self._po_prod_buffer[index.row()].po_product
        column = index.column()
        if role == Qt.DisplayRole:
            if column == self.PART_NUMBER_COLUMN:
                if po_product.product:
                    return po_product.product.part_number
                else:
                    return None
            elif column == self.DESCRIPTION_COLUMN:
                if po_product.product:
                    return po_product.product.product_description
                else:
                    return None
            elif column == self.UNIT_PRICE_COLUMN:
                converted_value = monetary_int_to_decimal(po_product.unit_price, 
                                                          self.app_config)
                return "R {:,.2f}".format(converted_value)
            elif column == self.DISCOUNT_COLUMN:
                converted_value = percentage_int_to_decimal(po_product.discount)
                return "{:2.0%}".format(converted_value)
            elif column == self.QUANTITY_COLUMN:
                return po_product.quantity
            elif column == self.LINE_PRICE_COLUMN:
                converted_unit_price = monetary_int_to_decimal(
                                                        po_product.unit_price,
                                                        self.app_config)
                converted_discount = percentage_int_to_decimal(
                                                        po_product.discount)
                line_price = self._calculate_line_price(converted_unit_price, 
                                                        converted_discount, 
                                                        po_product.quantity)
                return "R {:,.2f}".format(line_price)
            else:
                return None
        elif role == Qt.EditRole:
            if column == self.PART_NUMBER_COLUMN:
                if po_product.product:
                    return po_product.product.part_number
                else:
                    return None
            elif column == self.DESCRIPTION_COLUMN:
                if po_product.product:
                    return po_product.product.product_description
                else:
                    return None
            elif column == self.UNIT_PRICE_COLUMN:
                converted_value = monetary_int_to_decimal(po_product.unit_price, 
                                                          self.app_config)
                return float(converted_value)
            elif column == self.DISCOUNT_COLUMN:
                converted_value = percentage_int_to_decimal(po_product.discount)
                return converted_value
            elif column == self.QUANTITY_COLUMN:
                return po_product.quantity
            elif column == self.LINE_PRICE_COLUMN:
                converted_unit_price = monetary_int_to_decimal(
                                                        po_product.unit_price,
                                                        self.app_config)
                converted_discount = percentage_int_to_decimal(
                                                        po_product.discount)
                line_price = self._calculate_line_price(converted_unit_price, 
                                                        converted_discount, 
                                                        po_product.quantity)
                return line_price
            else:
                return None
        elif role == Qt.TextAlignmentRole:
            if column == self.UNIT_PRICE_COLUMN:
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
            if section == self.PART_NUMBER_COLUMN:
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
                if column == self.PART_NUMBER_COLUMN:
                    print("--------->setData: {}".format(str(index.row())))
                    print("---------> 1")
                    if self._request_to_add_new_product(value) is True:
                        print("---------> 2")
                        # The user has requested to add a new product. 
                        # Therefore, emit the signal to notify the main form. 
                        self.emit(SIGNAL("add_new_product_requested()"))
                        return True
                    print("---------> 3")
                    self._validate_and_set_part_number(index, value)
                elif column == self.DESCRIPTION_COLUMN:
                    if self._request_to_add_new_product(value) is True:
                        # The user has requested to add a new product. 
                        # Therefore, emit the signal to notify the main form.
                        self.emit(SIGNAL("add_new_product_requested()"))
                        return True
                    self._validate_and_set_description(index, value)
                elif column == self.LINE_PRICE_COLUMN:
                    # The line price column is not editable.
                    return False
                else:
                    self._validate_and_set_general_data(index, value)
            except ValueError:
                print("ValueError")
                # If the user types in something stupid then don't do anything.
                return False
            return True
        return False

    def _request_to_add_new_product(self, requested_value):
        '''Determines if there has been a request to add a new product.
        
        The list of available products, whether displayed as the product part
        numbers or product descriptions, includes an item defined by 
        ADD_NEW_PRODUCT_COMBO_STRING, e.g., "Add new...". This method checks
        if this item has been selected. 
        
        Args:
        :param requested_value: The part number or product description value
            that was requested.
        :type requested_value: String
        
        Returns: 
        :return: True if requested_value is equal to 
            ADD_NEW_PRODUCT_COMBO_STRING. Otherwise False.
        :rtype: Boolean
        '''
        if requested_value == ADD_NEW_PRODUCT_COMBO_STRING:
            return True
        return False
    
    def _validate_and_set_part_number(self, index, part_number):
        '''Validate and set the line item's part number.
        
        The method first validates the specified part number. Then it retrieves 
        the Product object matching the specified (unique) part number and 
        adds it to the local products list as a valid entry. In doing so it
        also initialises the line item's unit price and discount fields based
        on the product's current price and current discount fields.  
        
        Selection of the part number is equivalent to linking that product to
        the active purchase order. The actual "linking" happens only when the 
        :meth:`do_pre_commit_processing` method is called, when all valid 
        entries in the local product list are added to the active purchase 
        order's product list.
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written. 
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param part_number: The requested part number.
        :type part_number: String
        '''
        row = index.row()
        if self._selected_part_number_is_valid(row, part_number):
            product = self._get_product_with_part_number(part_number)
            self._po_prod_buffer[row].po_product.product = product
            self._po_prod_buffer[row].po_product.unit_price = \
                product.current_price
            self._po_prod_buffer[row].po_product.discount = \
                product.current_discount
            self._po_prod_buffer[row].valid = True
            # If a valid part  number has been selected in the last row then 
            # add another row.
            if row == self.rowCount() - 1:
                self.insertRows(self.rowCount())
            # Emit the data changed signal.
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
        else:
            # Do nothing. No change to current status.
            pass

    def _selected_part_number_is_valid(self, row, selected_part_number):
        '''Determines if a selected part number is valid.
        
        A part number is considered valid if:
        - It is not already the value set at this index.
        - It is on the active purchase order's supplier's list of products.
        - It is not already listed on the active purchase order.
        
        Note that if the selected part number is found to already be listed on 
        the purchase order, this method will use a message box to inform the 
        user of this.  
        
        Args:
        :param row: The model row being updated.
        :type row: Integer
        :param selected_part_number: The requested part number. 
        :type selected_part_number: String
        
        Returns:
        :return: True if the requested part number is valid. Otherwise False.
        :rtype: Boolean
        '''
        # The part number must be new.
        if self._po_prod_buffer[row].po_product.product:
            if self._po_prod_buffer[row].po_product.product.part_number == \
            selected_part_number:
                return False
        # The part number must exist in the list of products of the applicable
        # supplier.
        if self._part_number_in_supplier_list(selected_part_number) \
        is not True:
            return False
        # The part number must not already be on this purchase order.
        if self._part_number_on_purchase_order(selected_part_number) \
        is not False:
            show_error_product_already_on_po("part number", 
                                             selected_part_number)
            return False
        return True
    
    def _part_number_in_supplier_list(self, part_number):
        '''Determine if a part number is on the active purchase order's 
        supplier's list of products. 
        
        Args:
        :param part_number: The requested part number.
        :type part_number: String
        
        Returns:
        :return: True if the part number is on the supplier's list of products.
            Otherwise False.
        :rtype: Boolean
        '''
        with self.session.no_autoflush:
            valid_products = self.session.query(Product).\
                                filter(Product.supplier_id == \
                                       self._po.supplier.id).all()
        for product in valid_products:
            if part_number == product.part_number:
                return True
        return False
    
    def _part_number_on_purchase_order(self, part_number):
        '''Determine if a part number is already listed on the active purchase 
        order.
        
        Args:
        :param part_number: The requested part number.
        :type part_number: String
        
        Returns:
        :return: True if the part number is already on the purchase order.
            Otherwise False.
        :rtype: Boolean
        '''
        for entry in self._po_prod_buffer:
            if entry.po_product.product:
                if part_number == entry.po_product.product.part_number:
                    return True
        return False

    def _get_product_with_part_number(self, part_number):
        '''Retrieve the Product object matching the specified (unique) part 
        number.
        
        Args:
        :param part_number: The requested part number.
        :type part_number: String
        
        Returns:
        :return: The Product object with the specified part number.
        :rtype: purchaseorder.Product
        '''
        with self.session.no_autoflush:
            product = self.session.query(Product).\
                        filter(Product.supplier_id == \
                               self._po.supplier.id).\
                        filter(Product.part_number == \
                               part_number).one()
        return product
    
    def _validate_and_set_description(self, index, description):
        '''Validate and set the line item's product description.
        
        The method first validates the specified description. Then it retrieves 
        the Product object matching the specified (unique) description and 
        adds it to the local products list as a valid entry. In doing so it
        also initialises the line item's unit price and discount fields based
        on the product's current price and current discount fields.  
        
        Selection of the description is equivalent to linking that product to
        the active purchase order. The actual "linking" happens only when the 
        :meth:`do_pre_commit_processing` method is called, when all valid 
        entries in the local product list are added to the active purchase 
        order's product list.
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written. 
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param description: The requested product description.
        :type description: String
        '''
        row = index.row()
        if self._selected_description_is_valid(row, description) is True:
            product = self._get_product_with_description(description)
            self._po_prod_buffer[row].po_product.product = product
            self._po_prod_buffer[row].po_product.unit_price = \
                product.current_price
            self._po_prod_buffer[row].po_product.discount = \
                product.current_discount
            self._po_prod_buffer[row].valid = True
            # If a valid part number has been selected in the last 
            # row then add another row.
            if row == self.rowCount() - 1:
                self.insertRows(self.rowCount())
            # Emit the data changed signal.
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
        else:
            # Do nothing. No change to current status.
            pass

    def _selected_description_is_valid(self, row, selected_description):
        '''Determines if a selected product description is valid.
        
        A product description is considered valid if:
        - It is not already the value set at this index.
        - It is on the active purchase order's supplier's list of products.
        - It is not already listed on the active purchase order.
        
        Note that if the selected product description is found to already be 
        listed on the purchase order, this method will use a message box to 
        inform the user of this.  
        
        Args:
        :param row: The model row being updated.
        :type row: Integer
        :param selected_description: The requested product description. 
        :type selected_description: String
        
        Returns:
        :return: True if the requested product description is valid. Otherwise 
            False.
        :rtype: Boolean
        '''
        # The description must be new.
        if self._po_prod_buffer[row].po_product.product:
            if self._po_prod_buffer[row].po_product.product.\
            product_description == selected_description:
                return False
        # The description must exist in the list of products of the applicable
        # supplier.
        if self._description_in_supplier_list(selected_description) \
        is not True:
            return False
        # The description must not already be on this purchase order.
        if self._description_on_purchase_order(selected_description) \
        is not False:
            show_error_product_already_on_po("description", 
                                             selected_description)
            return False
        return True
    
    def _description_in_supplier_list(self, description):
        '''Determine if a product description is on the active purchase order's 
        supplier's list of products. 
        
        Args:
        :param description: The requested product description.
        :type description: String
        
        Returns:
        :return: True if the description is on the supplier's list of products.
            Otherwise False.
        :rtype: Boolean
        '''
        with self.session.no_autoflush:
            valid_products = self.session.query(Product).\
                                filter(Product.supplier_id == \
                                       self._po.supplier.id).all()
        for product in valid_products:
            if description == product.product_description:
                return True
        return False
    
    def _description_on_purchase_order(self, description):
        '''Determine if a product description is already listed on the active 
        purchase order.
        
        Args:
        :param description: The requested product description.
        :type description: String
        
        Returns:
        :return: True if the description is already on the purchase order.
            Otherwise False.
        :rtype: Boolean
        '''
        for entry in self._po_prod_buffer:
            if entry.po_product.product:
                if description == entry.po_product.product.product_description:
                    return True
        return False
    
    def _get_product_with_description(self, description):
        '''Retrieve the Product object matching the specified (unique) product 
        description.
        
        Args:
        :param description: The requested product description.
        :type description: String
        
        Returns:
        :return: The Product object with the specified description.
        :rtype: purchaseorder.Product
        '''
        with self.session.no_autoflush:
            product = self.session.query(Product).\
                        filter(Product.supplier_id == \
                               self._po.supplier.id).\
                        filter(Product.product_description == \
                               description).one()
        return product
    
    def _validate_and_set_general_data(self, index, requested_value):
        '''Validate and set data other than the product part number and 
        description.
        
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
        if column == self.UNIT_PRICE_COLUMN:
            current_value = self._po_prod_buffer[row].po_product.unit_price
            converted_requested_value = monetary_float_to_int(requested_value, 
                                                              self.app_config)
        elif column == self.DISCOUNT_COLUMN:
            current_value = self._po_prod_buffer[row].po_product.discount
            # No need to convert to decimal here because the 
            # PercentageEditDelegate passes a decimal.
            converted_requested_value = monetary_decimal_to_int(requested_value, 
                                                                self.app_config)
        elif column == self.QUANTITY_COLUMN:
            current_value = self._po_prod_buffer[row].po_product.quantity
            converted_requested_value = int(requested_value)
        else:
            raise ValueError(("Invalid index. Column value {} is not "
                              "considered to be \"general data\".").format(
                                                                        column))
        if current_value != converted_requested_value:
            if column == self.UNIT_PRICE_COLUMN:
                self._po_prod_buffer[row].po_product.unit_price = \
                                                    converted_requested_value
            elif column == self.DISCOUNT_COLUMN:
                self._po_prod_buffer[row].po_product.discount = \
                                                    converted_requested_value
            elif column == self.QUANTITY_COLUMN:
                self._po_prod_buffer[row].po_product.quantity = \
                                                    converted_requested_value
            # Emit the data changed signal.
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
         
    def insertRows(self, position, rows=1, index=QModelIndex()):
        '''Refer to QAbstractItemModel.insertRows.
        '''
        # Insertion of a line item is not allowed, only addition of a line item.
        assert position == self.rowCount()
        # Only one line item can be inserted at a time.
        assert rows == 1
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        # The purchase order is known, therefore its id can be set. However,
        # the product is not known yet; it hasn't been chosen yet. The product
        # ID will be set when the product is chosen.
        # Setting of purchase_order_id=self._po.id added 26 Apr 2016 20:56
        po_prod = PurchaseOrderProduct(purchase_order_id=self._po.id,
                                       unit_price=0,
                                       discount=0,
                                       quantity=1)
        # Inserted purchase order product starts out invalid.
        self._po_prod_buffer.append(ValidPurchaseOrderProduct(po_prod, False))
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        '''Refer to QAbstractItemModel.removeRows.
        '''
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self._po_prod_buffer = self._po_prod_buffer[:position] + \
                                self._po_prod_buffer[position + rows:]
        self.endRemoveRows()
        return True
    
    def remove_all_rows(self):
        '''Remove all line items.
        
        This is required, e.g., when the supplier is changed on a purchase
        order that has line items listed on it.
        
        The active purchase order's list of products is cleared. The local list
        of products is cleared.
        '''
        if self.rowCount() > 0:
            self.beginRemoveRows(QModelIndex(), 0, self.rowCount() - 1)
            self._po_prod_buffer.clear()
            self._po.products.clear()
            self.endRemoveRows()
    
    def remove_empty_row(self):
        '''Remove the empty line item at the end of the table.
        '''
        if self.rowCount() != 0:
            self.removeRows(self.rowCount() - 1)
    
    def restore_empty_row(self):
        '''Insert an empty line item row at the end of the table.
        '''
        self.insertRows(self.rowCount())
    
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

    def calculate_total_excluding_tax(self):
        '''Calculate the total price of the active purchase order's line items
        excluding tax. 
        
        Returns:
        :return: Total price of the active purchase order's line items 
            excluding tax
        :rtype: Decimal
        '''
        total_price = Decimal("0.0")
        for entry in self._po_prod_buffer:
            converted_unit_price = monetary_int_to_decimal(
                                                entry.po_product.unit_price,
                                                self.app_config)
            converted_discount = percentage_int_to_decimal(
                                                entry.po_product.discount)
            total_price += self._calculate_line_price(
                                                converted_unit_price, 
                                                converted_discount, 
                                                entry.po_product.quantity)
        return total_price
    
    def calculate_total_tax(self):
        '''Calculate the total tax of the active purchase order's line items.
        
        Returns:
        :return: Total tax of the active purchase order's line items.
        :rtype: Decimal
        '''
        total_price = self.calculate_total_excluding_tax()
        # Create a reader to access the latest user config.
        user_config = UserConfigReader(self.session)
        total_tax = total_price * user_config.locale.tax_rate
        return total_tax
    
    def get_row(self, row):
        '''Retrieve a single row of the line item model.

        The list contains: part number, description, unit price, discount, 
        quantity, and line price.
        
        Args:
        :param row: The row to retrieve.
        :type row: Integer
        
        Returns:
        :return: A list containing the data for the specified row of the line
            item model. 
        :rtype: The list contains: 
            [String, String, Decimal, Decimal, Integer, Decimal]
            
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
