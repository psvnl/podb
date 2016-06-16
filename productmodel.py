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
from datavalidation import (TextFieldValidator, warn_about_changing_used_data, 
                            show_error_rows_with_default_values,
                            DecimalFieldValidator, 
                            show_error_rows_with_zero_prices)
from product import Product
from purchaseorderproduct import PurchaseOrderProduct


class ProductModel(QAbstractTableModel):
    '''Data model for the product table.
    '''

    PRODUCT_MODEL_NUM_COLUMNS = 6
    (ID_COLUMN,
     PART_NUMBER_COLUMN,
     PRODUCT_DESCRIPTION_COLUMN,
     CURRENT_PRICE_COLUMN,
     CURRENT_DISCOUNT_COLUMN,
     ARCHIVED_COLUMN) = range(PRODUCT_MODEL_NUM_COLUMNS)
     
    # String used to initialise the part number field of a new product.
    _PART_NUMBER_DEFAULT = "Enter part number"
    # String used to initialise the description field of a new product.
    _PRODUCT_DESCRIPTON_DEFAULT = "Describe the product"

    def __init__(self, app_config, session, supplier_id, parent=None):
        '''Initialise the ProductModel object.
        
        Loads a local products list (self.products) with the result of a query
        for all products with the specified supplier ID.
        
        Args:
        :param session: The SQLAlchemny session in use. 
        :type session: Session object (the class created by the call to  
            :func:`sessionmaker` in :mod:`sqlasession`).
        :param supplier_id: The primary key of the supplier in question 
            (supplier.id).
        :type supplier_id: Integer
        :param parent: The model's parent.
        :type parent: QObject
        '''
        super().__init__(parent=parent)
        self.session = session
        self.app_config = app_config
        self.supplier_id = supplier_id
        with self.session.no_autoflush:
            self.products = self.session.query(Product).\
                            filter(Product.supplier_id == self.supplier_id).\
                            all()
     
    def rowCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.rowCount.
        '''
        return len(self.products) 

    def columnCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.columnCount.
        '''
        return self.PRODUCT_MODEL_NUM_COLUMNS
    
    def data(self, index, role=Qt.DisplayRole):
        '''Refer to QAbstractItemModel.data.
        '''
        if not index.isValid() or \
        not (0 <= index.row() < self.rowCount()):
            return None
        product = self.products[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == self.PART_NUMBER_COLUMN:
                return product.part_number
            elif column == self.PRODUCT_DESCRIPTION_COLUMN:
                return product.product_description
            elif column == self.CURRENT_PRICE_COLUMN:
                converted_value = monetary_int_to_decimal(
                                                    product.current_price, 
                                                    self.app_config)
                return "R {:,.2f}".format(converted_value)
            elif column == self.CURRENT_DISCOUNT_COLUMN:
                converted_value = percentage_int_to_decimal(
                                                    product.current_discount)
                return "{:2.0%}".format(converted_value)
            elif column == self.ARCHIVED_COLUMN:
                return "Archived"
            else:
                return None
        elif role == Qt.EditRole:
            if column == self.PART_NUMBER_COLUMN:
                return product.part_number
            elif column == self.PRODUCT_DESCRIPTION_COLUMN:
                return product.product_description
            elif column == self.CURRENT_PRICE_COLUMN:
                converted_value = monetary_int_to_decimal(
                                                    product.current_price, 
                                                    self.app_config)
                return str(converted_value)
            elif column == self.CURRENT_DISCOUNT_COLUMN:
                converted_value = percentage_int_to_decimal(
                                                    product.current_discount)
                return converted_value
            elif column == self.ARCHIVED_COLUMN:
                return "Archived"
            else:
                return None
        elif role == Qt.TextAlignmentRole:
            if column == self.CURRENT_PRICE_COLUMN:
                return Qt.AlignRight | Qt.AlignVCenter
            elif column == self.CURRENT_DISCOUNT_COLUMN:
                return Qt.AlignHCenter | Qt.AlignVCenter
            else:
                return None
        elif role == Qt.CheckStateRole:
            if column == self.ARCHIVED_COLUMN:
                if product.archived:
                    return Qt.Checked
                else:
                    return Qt.Unchecked
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
                return "Part Number"
            elif section == self.PRODUCT_DESCRIPTION_COLUMN:
                return "Product Description"
            elif section == self.CURRENT_PRICE_COLUMN:
                return "Current Price"
            elif section == self.CURRENT_DISCOUNT_COLUMN:
                return "Current Discount"
            elif section == self.ARCHIVED_COLUMN:
                return "Status"
        return int(section + 1)
    
    def flags(self, index):
        '''Refer to QAbstractItemModel.flags.
        '''
        if not index.isValid():
            return Qt.ItemIsEnabled
        column = index.column()
        if column == self.ARCHIVED_COLUMN:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | 
                                Qt.ItemIsEditable | Qt.ItemIsUserCheckable)
        else:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | 
                                Qt.ItemIsEditable)
        
    def setData(self, index, value, role=Qt.EditRole):
        '''Refer to QAbstractItemModel.setData.
        '''
        if index.isValid() and \
        (0 <= index.row() < self.rowCount()):
            column = index.column()
            if role == Qt.CheckStateRole and column == self.ARCHIVED_COLUMN:
                self._validate_and_set_archived(index, value)
            else:
                try:
                    if column == self.PART_NUMBER_COLUMN:
                        if value:
                            self._validate_and_set_part_number(index, value)
                    elif column == self.PRODUCT_DESCRIPTION_COLUMN:
                        if value:
                            self._validate_and_set_product_description(index, 
                                                                       value)
                    elif column == self.CURRENT_PRICE_COLUMN:
                        self._validate_and_set_current_price(index, 
                                                             Decimal(value))
                    elif column == self.CURRENT_DISCOUNT_COLUMN:
                        # No need to convert to decimal here because the 
                        # PercentageEditDelegate passes a decimal.
                        self._validate_and_set_current_discount(index, 
                                                                value)
                    elif column == self.ARCHIVED_COLUMN:
                        pass
                except ValueError:
                    # If the user types in something stupid then don't do 
                    # anything.
                    return False
            return True
        return False
    
    def _validate_and_set_archived(self, index, checked_state):
        '''Validate the requested product archived state and set the table 
        field data if validation passes.
        
        The method verifies that the requested state is either "checked" or 
        "not checked", mapping to "archived" or "not archived", before 
        setting the field.
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written.
        
        Args:
        :param index:  The model index being updated.
        :type index: QModelIndex
        :param checked_state: The requested checkbox state.
        :type checked_state: Qt.CheckState
        '''
        row = index.row()
        if checked_state == Qt.Checked:
            self.products[row].archived = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
        elif checked_state == Qt.Unchecked:
            self.products[row].archived = False
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
    
    def _validate_and_set_part_number(self, index, part_number):
        '''Validate the requested part number and set the table field
        data if validation passes.
        
        The method checks if the specified row corresponds to a product that is 
        referenced in a purchase order. If this is the case, the method warns 
        the user of the consequences of changing the data using a message box.
        
        The method calls :meth:`_is_part_number_valid` to validate the
        company name. 
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written. 
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param part_number: The requested part number. 
        :type part_number: String
        '''
        result = QMessageBox.Yes
        row = index.row()
        if self._is_product_used(self.products[row].id):
            # The product is used, i.e., referenced in a purchase order.
            if self.products[row].part_number != part_number:
                # Warn about changing a used product only if a different value
                # is requested
                result = warn_about_changing_used_data("product")
        if result == QMessageBox.Yes:
            valid = False
            if part_number == self._PART_NUMBER_DEFAULT:
                # The requested value is the default value. In this case the
                # validation must be run, regardless of whether the value is 
                # the same as the current value, so that the user is told that 
                # the field must not be left as the default value.
                valid = self._is_part_number_valid(part_number)
            else:
                # The requested value is not the default value. In this case 
                # the validation must be run only if the requested value is 
                # different from the current value. 
                if self.products[row].part_number != part_number:
                    valid = self._is_part_number_valid(part_number)
            if valid is True:
                # The requested value is valid. Set the data.
                self.products[row].part_number = part_number
                # Emit the data changed signal.
                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                          index, index)
    
    def _is_product_used(self, product_id):
        '''Determines if the product is referenced in a purchase order.
        
        Args:
        :param product_id: The primary key (product.id) of the product to be
            checked.
        :type product_id: Integer
        
        Returns: 
        :return: True if the product is referenced in a purchase order. False
            otherwise.
        :rtype: Boolean 
        '''
        with self.session.no_autoflush:
            if self.session.query(PurchaseOrderProduct).\
                filter(PurchaseOrderProduct.product_id == product_id).\
                count() > 0:
                return True
            return False
    
    def _is_part_number_valid(self, part_number, check_unique=True):
        '''Determines if a product part number is valid.
        
        A product part number is considered valid if:
        - It is unique, i.e., is not already in the table for this supplier.
        - It is not blank, i.e., made up only of white space.
        - It is not the default text that is used to initalise a newly inserted
          supplier.
        A TextFieldValidator object is used to perform the actual validation.
        
        Note that if a validation check fails, TextFieldValidator will use
        message boxes to inform the user of the failed check. 
        
        Args:
        :param part_number: The pratnumber to validate.
        :type part_number: String
        :param check_unique: Enable check that the value is unique in the 
            column.
        :type check_unique: Boolean
        
        Returns:
        :return: True if the part number is valid. False otherwise.
        :rtype: Boolean 
        '''
        validator = TextFieldValidator(
                                    "product part number",
                                    part_number,
                                    [p.part_number for p in self.products],
                                    self._PART_NUMBER_DEFAULT,
                                    check_unique=check_unique)
        return validator.field_is_valid()
    
    def _validate_and_set_product_description(self, index, product_description):
        '''Validate the requested product description and set the table field
        data if validation passes.
        
        The method checks if the specified row corresponds to a product that is 
        referenced in a purchase order. If this is the case, the method warns 
        the user of the consequences of changing the data using a message box.
        
        The method calls :meth:`_is_product_description_valid` to validate the 
        product description. 
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written. 
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param product_description: The requested product description/
        :type product_description: String
        '''
        result = QMessageBox.Yes
        row = index.row()
        if self._is_product_used(self.products[row].id):
            # The product is used, i.e., referenced in a purchase order.
            if self.products[row].product_description != product_description:
                # Warn about changing a used product only if a different value
                # is requested
                result = warn_about_changing_used_data("product")
        if result == QMessageBox.Yes:
            valid = False
            if product_description == self._PRODUCT_DESCRIPTON_DEFAULT:
                # The requested value is the default value. In this case the
                # validation must be run, regardless of whether the value is 
                # the same as the current value, so that the user is told that 
                # the field must not be left as the default value.
                valid = self._is_product_description_valid(product_description)
            else:
                # The requested value is not the default value. In this case 
                # the validation must be run only if the requested value is 
                # different from the current value. 
                #
                # This block is not really necessary since the validation 
                # performed is only to check against the default value. But the
                # same processing structure as used in other methods has been 
                # maintained in case the validation changes later. 
                if self.products[row].product_description != \
                product_description:
                    valid = self._is_product_description_valid(
                                                        product_description)
            if valid is True:
                # The requested value is valid. Set the data.
                self.products[row].product_description = product_description
                # Emit the data changed signal.
                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                          index, index)
                    
    def _is_product_description_valid(self, product_description, 
                                      check_unique=True):
        '''Determines if the product description is valid.
        
        A product description is considered valid if:
        - It is unique, i.e., is not already in the table for this supplier.
        - It is not blank, i.e., made up only of white space.
        - It is not the default text that is used to initalise a newly inserted
          supplier.
        A TextFieldValidator object is used to perform the actual validation.
        
        Note that if a validation check fails, TextFieldValidator will use
        message boxes to inform the user of the failed check.
        
        Args:
        :param product_description: The product description to validate.
        :type product_description: string
        :param check_unique: Enable check that the value is unique in the 
            column.
        :type check_unique: Boolean
        
        Returns:
        :return: True if the product description is valid. False otherwise.
        :rtype: Boolean
        '''
        validator = TextFieldValidator(
                                "product description",
                                product_description,
                                [p.product_description for p in self.products],
                                self._PRODUCT_DESCRIPTON_DEFAULT,
                                check_unique=check_unique)
        return validator.field_is_valid()
    
    def _validate_and_set_current_price(self, index, current_price):
        '''Validate the requested price and set the table field data if
        validation passes.
        
        The current price field may be set regardless of whether the product
        is referenced in a purchase order or not. This is because the actual 
        price at the time of the purchase order is stored in the 
        purchase_order_product table.
        
        This method just checks that the price value is not zero. The 
        DecimalFieldValidator is used to perform the actual validation.
        
        Note that if a validation check fails, DecimalFieldValidator will use
        message boxes to inform the user of the failed check.
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written. 
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param current_price: The requested price. 
        :type current_price: Decimal
        '''
        validator = DecimalFieldValidator("product current price",
                                          current_price,
                                          None,
                                          None,
                                          check_within_limits=False)
        if validator.field_is_valid():
            row = index.row()
            converted_requested_value = monetary_decimal_to_int(current_price, 
                                                                self.app_config)
            if self.products[row].current_price != converted_requested_value:
                # The requested value is valid. Set the data.
                self.products[row].current_price = converted_requested_value
                # Emit the data changed signal.
                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                          index, index)
    
    def _validate_and_set_current_discount(self, index, current_discount):
        '''Validate the requested discount and set the table field data if
        validation passes.
        
        The current discount field may be set regardless of whether the product
        is referenced in a purchase order or not. This is because the actual 
        discount at the time of the purchase order is stored in the 
        purchase_order_product table.
        
        This method just checks that the discount value is greater than or 
        equal to 0.0, and less than 1.0. The DecimalFieldValidator is used to
        perform the actual validation.
        
        Note that if a validation check fails, DecimalFieldValidator will use
        message boxes to inform the user of the failed check.
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written. 
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param current_discount: The requested discount. 
        :type current_discount: Decimal
        '''
        validator = DecimalFieldValidator("product current discount",
                                          current_discount,
                                          Decimal("0.0"),
                                          Decimal("1.0"),
                                          check_not_zero=False)
        if validator.field_is_valid():
            row = index.row()
            converted_requested_value = percentage_decimal_to_int(
                                                            current_discount)
            if self.products[row].current_discount != converted_requested_value:
                # The requested value is valid. Set the data.
                self.products[row].current_discount = converted_requested_value
                # Emit the data changed signal.
                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                          index, index)
    
    def insertRows(self, position, rows=1, index=QModelIndex()):
        '''Refer to QAbstractItemModel.insertRows.
        '''
        # Insertion of a product is not allowed, only addition of a product.
        assert position == self.rowCount()
        # Only one product can be inserted at a time.
        assert rows == 1
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        new_product = Product(
                        part_number=self._PART_NUMBER_DEFAULT,
                        product_description=self._PRODUCT_DESCRIPTON_DEFAULT,
                        current_price=0,
                        current_discount=0,
                        supplier_id=self.supplier_id,
                        archived=False)
        self.session.add(new_product)
        self.products.append(new_product)
        self.endInsertRows()
        return True
    
    def is_save_allowed(self):
        '''Perform any necessary validation before saving the data.
        
        The method checks if there are any part numbers or descriptions still 
        set to the default value. This can happen. If it does then the user 
        will be told about the errors through a message box.
        
        Returns:
        :return: True if the validation passed and the data may be saved. False
            if the validation failed.
        :rtype: Boolean
        '''
        ok, affected_rows = self._part_numbers_not_default()
        if not ok:
            show_error_rows_with_default_values("part number", 
                                                affected_rows)
        else:
            ok, affected_rows = self._product_descriptions_not_default()
            if not ok:
                show_error_rows_with_default_values("product description", 
                                                    affected_rows)
            else:
                ok, affected_rows = self._current_prices_not_zero()
                if not ok:
                    show_error_rows_with_zero_prices("current price", 
                                                     affected_rows)
        return ok
            
    def _part_numbers_not_default(self):
        '''Checks if any of the part numbers are set to the default value.
        
        Returns:
        :return: Two items are returned: 
            - A boolean indication of whether or not there are default values. 
              True means that none of the part numbers are default. 
              False means some of the part numbers are default.
            - A list of the affected rows, i.e., rows that have default part
              numbers.
        :rtype: Boolean
        :rtype: List of integers
        '''
        ok = True
        affected_rows = []
        row = 1
        for product in self.products:
            if product.part_number == self._PART_NUMBER_DEFAULT:
                ok = False
                affected_rows.append(row)
            row += 1
        return ok, affected_rows
    
    def _product_descriptions_not_default(self):
        '''Checks if any of the product descriptions are set to the default 
        value.
        
        Returns:
        :return: Two items are returned: 
            - A boolean indication of whether or not there are default values. 
              True means that none of the descriptions are default. 
              False means some of the descriptions are default.
            - A list of the affected rows, i.e., rows that have default 
              descriptions.
        :rtype: Boolean
        :rtype: List of integers
        '''
        ok = True
        affected_rows = []
        row = 1
        for product in self.products:
            if product.product_description == self._PRODUCT_DESCRIPTON_DEFAULT:
                ok = False
                affected_rows.append(row)
            row += 1
        return ok, affected_rows
    
    def _current_prices_not_zero(self):
        '''Checks if any of the current prices are zero.
        
        Returns:
        :return: Two items are returned: 
            - A boolean indication of whether or not there are prices set to 
              zero. 
              True means that none of the prices are zero. 
              False means some of the prices are zero.
            - A list of the affected rows, i.e., rows that have prices set to 
              zero.
        :rtype: Boolean
        :rtype: List of integers
        '''
        ok = True
        affected_rows = []
        row = 1
        for product in self.products:
            if product.current_price == 0:
                ok = False
                affected_rows.append(row)
            row += 1
        return ok, affected_rows
        
    def is_insert_allowed(self):
        '''Perform any necessary validation before inserting a new product.
        
        The method validates the last row in the model. If the row is invalid 
        then the user will be told about the errors through a message box.
        
        By using this method, the GUI can control the insertion of new rows, 
        ensuring that a row is valid before a new one is inserted.
        
        Returns:
        :return: True if the validation passed and a new row may be inserted. 
            False if the validation failed.
        :rtype: Boolean
        '''
        allowed = True
        if self.rowCount() == 0:
            return allowed
        row = self.rowCount() - 1
        part_number_index = self.createIndex(row, self.PART_NUMBER_COLUMN)
        allowed = self._is_part_number_valid(self.data(part_number_index), 
                                             check_unique=False)
        if allowed:
            description_index = self.createIndex(
                                            row, 
                                            self.PRODUCT_DESCRIPTION_COLUMN)
            allowed = self._is_product_description_valid(
                                                self.data(description_index), 
                                                check_unique=False)
        return allowed
    