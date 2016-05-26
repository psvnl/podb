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
from purchaseorder import PurchaseOrder
from supplier import Supplier
from datavalidation import (TextFieldValidator, warn_about_changing_used_data,
                            show_error_rows_with_default_values)


class SupplierModel(QAbstractTableModel):
    '''Data model for the supplier table.
    '''

    SUPPLIER_MODEL_NUM_COLUMNS = 9
    (ID_COLUMN, 
     COMPANY_NAME_COLUMN, 
     CONTACT_PERSON_NAME_COLUMN,
     ADDRESS_COLUMN,
     PHONE_NUMBER_COLUMN,
     FAX_NUMBER_COLUMN,
     EMAIL_ADDRESS_COLUMN,
     TAX_NUMBER_COLUMN,
     ARCHIVED_COLUMN) = range(SUPPLIER_MODEL_NUM_COLUMNS)
     
    # String used to initialise the company name field of a new supplier.
    _COMPANY_NAME_DEFAULT = "Enter company name"
    # String used to initialise the company address field of a new supplier.
    _COMPANY_ADDRESS_DEFAULT = "Enter address"
    
    def __init__(self, config_file, session, parent=None):
        '''Initialise the SupplierModel object.
        
        Loads a local suppliers list (self.suppliers) with the result of a 
        query for all suppliers in the database.
        
        Args:
        :param app_config: The application configuration settings file object.
        :type app_config: appconfig.ConfigFile
        :param session: The SQLAlchemny session in use. 
        :type session: Session object (the class created by the call to  
            :func:`sessionmaker` in :mod:`sqlasession`).
        :param parent: The model's parent.
        :type parent: QObject
        '''
        super().__init__(parent=parent)
        self.app_config = config_file
        self.session = session
        with self.session.no_autoflush:
            self.suppliers = self.session.query(Supplier).all()
        
    def rowCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.rowCount.
        '''
        return len(self.suppliers) 

    def columnCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.columnCount.
        '''
        return self.SUPPLIER_MODEL_NUM_COLUMNS
    
    def data(self, index, role=Qt.DisplayRole):
        '''Refer to QAbstractItemModel.data.
        '''
        if not index.isValid() or \
        not (0 <= index.row() < self.rowCount()):
            return None
        supplier = self.suppliers[index.row()]
        column = index.column()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if column == self.COMPANY_NAME_COLUMN:
                return supplier.company_name
            elif column == self.CONTACT_PERSON_NAME_COLUMN:
                return supplier.contact_person_name
            elif column == self.ADDRESS_COLUMN:
                return supplier.address
            elif column == self.PHONE_NUMBER_COLUMN:
                return supplier.phone_number
            elif column == self.FAX_NUMBER_COLUMN:
                return supplier.fax_number
            elif column == self.EMAIL_ADDRESS_COLUMN:
                return supplier.email_address
            elif column == self.TAX_NUMBER_COLUMN:
                return supplier.tax_number
            elif column == self.ARCHIVED_COLUMN:
                return "Archived"
            else:
                return None
        elif role == Qt.CheckStateRole:
            if column == self.ARCHIVED_COLUMN:
                if supplier.archived:
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
            if section == self.COMPANY_NAME_COLUMN:
                return "Company Name"
            elif section == self.CONTACT_PERSON_NAME_COLUMN:
                return "Contact Person"
            elif section == self.ADDRESS_COLUMN:
                return "Address"
            elif section == self.PHONE_NUMBER_COLUMN:
                return "Phone No."
            elif section == self.FAX_NUMBER_COLUMN:
                return "Fax No."
            elif section == self.EMAIL_ADDRESS_COLUMN:
                return "Email Address"
            elif section == self.TAX_NUMBER_COLUMN:
                return "{} Number".format(self.app_config.locale.tax_name) 
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
                if value:
                    if column == self.COMPANY_NAME_COLUMN:
                        self._validate_and_set_company_name(index, value)
                    elif column == self.ADDRESS_COLUMN:
                        self._validate_and_set_address(index, value)
                    elif column == self.ARCHIVED_COLUMN:
                        pass
                    else:
                        self._validate_and_set_general_data(index, value)
            return True
        return False
    
    def _validate_and_set_archived(self, index, checked_state):
        '''Validate the requested supplier archived state and set the table 
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
            self.suppliers[row].archived = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
        elif checked_state == Qt.Unchecked:
            self.suppliers[row].archived = False
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
    
    def _validate_and_set_company_name(self, index, company_name):
        '''Validate the requested company name and set the table field
        data if validation passes.
        
        The method checks if the specified row corresponds to a supplier that is 
        referenced in a purchase order. If this is the case, the method warns 
        the user of the consequences of changing the data using a message box.
        
        The method calls :meth:`_is_company_name_valid` to validate the
        company name. 
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written.
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param company_name: The requested company name.
        :type company_name: String
        '''
        result = QMessageBox.Yes
        row = index.row()
        if self._is_supplier_used(self.suppliers[row].id):
            # The supplier is used, i.e., referenced in a purchase order.
            if self.suppliers[row].company_name != company_name:
                # Warn about changing a used supplier only if a different value
                # is requested
                result = warn_about_changing_used_data("supplier")
        if result == QMessageBox.Yes:
            valid = False
            if company_name == self._COMPANY_NAME_DEFAULT:
                # The requested value is the default value. In this case the
                # validation must be run, regardless of whether the value is 
                # the same as the current value, so that the user is told that 
                # the field must not be left as the default value.
                valid = self._is_company_name_valid(company_name)
            else:
                # The requested value is not the default value. In this case 
                # the validation must be run only if the requested value is 
                # different from the current value. 
                if self.suppliers[row].company_name != company_name:
                    valid = self._is_company_name_valid(company_name)
            if valid is True:
                # The requested value is valid. Set the data.
                self.suppliers[row].company_name = company_name
                # Emit the data changed signal.
                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                          index, index)
    
    def _is_supplier_used(self, supplier_id):
        '''Determines if a supplier is referenced in a purchase order.
        
        Args:
        :param supplier_id: The primary key (supplier.id) of the supplier to be 
            checked.
        :type supplier_id: Integer
            
        Returns:
        :return: True if the supplier is referenced in a purchase order. False
            otherwise.
        :rtype: Boolean
        '''
        with self.session.no_autoflush:
            if self.session.query(PurchaseOrder).\
                filter(PurchaseOrder.supplier_id == supplier_id).count() > 0:
                return True
            return False
    
    def _is_company_name_valid(self, company_name, check_unique=True):
        '''Determines if a supplier company name is valid.
        
        A supplier company name is considered valid if:
        - It is unique, i.e., is not already in the table.
        - It is not blank, i.e., made up only of white space.
        - It is not the default text that is used to initialise a newly inserted
          supplier.
        A TextFieldValidator object is used to perform the actual validation.
        
        Note that if a validation check fails, TextFieldValidator will use
        message boxes to inform the user of the failed check. 
        
        Args:
        :param company_name: The company name to validate.
        :type company_name: String
        :param check_unique: Enable check that the value is unique in the 
            column.
        :type check_unique: Boolean
        
        Returns:
        :return: True if the company name is valid. False otherwise.
        :rtype: Boolean
        '''
        validator = TextFieldValidator(
                                    "supplier company name",
                                    company_name,
                                    [s.company_name for s in self.suppliers],
                                    self._COMPANY_NAME_DEFAULT,
                                    check_unique=check_unique)
        return validator.field_is_valid()
    
    def _validate_and_set_address(self, index, address):
        '''Validate the requested company address and set the table field
        data if validation passes.
        
        The method checks if the specified row corresponds to a supplier that is 
        referenced in a purchase order. If this is the case, the method warns 
        the user of the consequences of changing the data using a message box.
        
        The method calls :meth:`_is_address_valid` to validate the company 
        address. 
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written. 
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param address: The requested company address.
        :type address: String
        '''
        result = QMessageBox.Yes
        row = index.row()
        if self._is_supplier_used(self.suppliers[row].id):
            # The supplier is used, i.e., referenced in a purchase order.
            if self.suppliers[row].address != address:
                # Warn about changing a used supplier only if a different value
                # is requested
                result = warn_about_changing_used_data("supplier")
        if result == QMessageBox.Yes:
            valid = False
            if address == self._COMPANY_ADDRESS_DEFAULT:
                # The requested value is the default value. In this case the
                # validation must be run, regardless of whether the value is 
                # the same as the current value, so that the user is told that 
                # the field must not be left as the default value.
                valid = self._is_address_valid(address)
            else:
                # The requested value is not the default value. In this case 
                # the validation must be run only if the requested value is 
                # different from the current value. 
                if self.suppliers[row].address != address:
                    valid = self._is_address_valid(address)
            if valid is True:
                # The requested value is valid. Set the data.
                self.suppliers[row].address = address
                # Emit the data changed signal.
                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                          index, index)
                
    def _is_address_valid(self, address):
        '''Determines if a supplier address is valid.
        
        A supplier address is considered valid if:
        - It is not the default text that is used to initialise a newly inserted
          supplier.
        A TextFieldValidator object is used to perform the actual validation.
        
        Note that if a validation check fails, TextFieldValidator will use
        message boxes to inform the user of the failed check. 
        
        Args:
        :param address: The company address to validate.
        :type address: String
        
        Returns:
        :return: True if the company address is valid. False otherwise.
        :rtype: Boolean
        '''
        validator = TextFieldValidator(
                                    "company address",
                                    address,
                                    [s.address for s in self.suppliers],
                                    self._COMPANY_ADDRESS_DEFAULT,
                                    check_unique=False,
                                    check_not_blank=False)
        return validator.field_is_valid()
    
    def _validate_and_set_general_data(self, index, requested_value):
        '''Validate and set data other than the company name and address.
        
        The method checks if the specified row corresponds to a supplier that is 
        referenced in a purchase order. If this is the case, the method warns 
        the user of the consequences of changing the data using a message box.
        
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
        if column == self.CONTACT_PERSON_NAME_COLUMN:
            current_value = self.suppliers[row].contact_person_name
        elif column == self.PHONE_NUMBER_COLUMN:
            current_value = self.suppliers[row].phone_number
        elif column == self.FAX_NUMBER_COLUMN:
            current_value = self.suppliers[row].fax_number
        elif column == self.EMAIL_ADDRESS_COLUMN:
            current_value = self.suppliers[row].email_address
        elif column == self.TAX_NUMBER_COLUMN:
            current_value = self.suppliers[row].tax_number
        else:
            raise ValueError(("Invalid index. Column value {} is not "
                              "considered to be \"general data\".").format(
                                                                        column))
        result = QMessageBox.Yes
        if self._is_supplier_used(self.suppliers[row].id):
            # The supplier is used, i.e., referenced in a purchase order.
            if current_value != requested_value:
                # Warn about changing a used supplier only if a different value
                # is requested
                result = warn_about_changing_used_data("supplier")
        if result == QMessageBox.Yes:
            if current_value != requested_value:
                if column == self.CONTACT_PERSON_NAME_COLUMN:
                    self.suppliers[row].contact_person_name = requested_value
                elif column == self.PHONE_NUMBER_COLUMN:
                    self.suppliers[row].phone_number = requested_value
                elif column == self.FAX_NUMBER_COLUMN:
                    self.suppliers[row].fax_number = requested_value
                elif column == self.EMAIL_ADDRESS_COLUMN:
                    self.suppliers[row].email_address = requested_value
                elif column == self.TAX_NUMBER_COLUMN:
                    self.suppliers[row].tax_number = requested_value
                # Emit the data changed signal.
                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                          index, index)
    
    def insertRows(self, position, rows=1, index=QModelIndex()):
        '''Refer to QAbstractItemModel.insertRows.
        '''
        # Insertion of a supplier is not allowed, only addition of a supplier.
        assert position == self.rowCount()
        # Only one supplier can be inserted at a time.
        assert rows == 1
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        new_supplier = Supplier(company_name=self._COMPANY_NAME_DEFAULT,
                                contact_person_name="None",
                                phone_number="None",
                                fax_number="None",
                                email_address="None",
                                tax_number="None",
                                address=self._COMPANY_ADDRESS_DEFAULT,
                                archived=False)
        self.session.add(new_supplier)
        self.suppliers.append(new_supplier)
        self.endInsertRows()
        return True
        
    def get_supplier_list(self):
        '''Retrieve a list of all supplier company names.
        
        Returns:
        :return: A list of the supplier company names for all suppliers in the
            database.
        :rtype: List of strings
        '''
        supplier_company_name_list = []
        for supplier in self.suppliers:
            supplier_company_name_list.append(supplier.company_name)
        return supplier_company_name_list
    
    def get_supplier_id_from_company_name(self, company_name):
        '''Get the supplier primary key given the company name.
        
        This method is intended to be used when it is known that the specified 
        company name is valid, i.e., is in the database. 
        
        Args:
        :param company_name: A company name.
        :type company_name: String
        
        Returns:
        :return: The primary key (supplier.id) of the supplier with the 
            specified company name.
        :rtype: Integer
        
        Raises:
        :raises: sqlalchemy.orm.exc.MultipleResultsFound if the query does not
            find exactly one result.
        '''
        with self.session.no_autoflush:
            supplier = self.session.query(Supplier).\
                filter(Supplier.company_name == company_name).one()
        return supplier.id
    
    def is_save_allowed(self):
        '''Perform any necessary validation before saving the data.
        
        The method checks if there are any company names or addresses still set 
        to the default value. This can happen. If it does then the user will be
        told about the errors through a message box.
        
        Returns:
        :return: True if the validation passed and the data may be saved. False
            if the validation failed.
        :rtype: Boolean
        '''
        allowed, affected_rows = self._company_names_not_default()
        if not allowed:
            show_error_rows_with_default_values("company name", 
                                                affected_rows)
        else:
            allowed, affected_rows = self._addresses_not_default()
            if not allowed:
                show_error_rows_with_default_values("company address", 
                                                    affected_rows)
        return allowed
    
    def _company_names_not_default(self):
        '''Checks if any of the company names are set to the default value.
        
        Returns:
        :return: Two items are returned: 
            - A boolean indication of whether or not there are default values. 
              True means that none of the company names are default. 
              False means some of the company names are default.
            - A list of the affected rows, i.e., rows that have default company
              names.
        :rtype: Boolean
        :rtype: List of integers
        '''
        ok = True
        affected_rows = []
        row = 1
        for supplier in self.suppliers:
            if supplier.company_name == self._COMPANY_NAME_DEFAULT:
                ok = False
                affected_rows.append(row)
            row += 1
        return ok, affected_rows
    
    def _addresses_not_default(self):
        '''Checks if any of the company addresses are set to the default value.
        
        Returns:
        :return: Two items are returned: 
            - A boolean indication of whether or not there are default values. 
              True means that none of the company addresses are default. 
              False means some of the company addresses are default.
            - A list of the affected rows, i.e., rows that have default company
              addresses.
        :rtype: Boolean
        :rtype: List of integers
        '''
        ok = True
        affected_rows = []
        row = 1
        for supplier in self.suppliers:
            if supplier.address == self._COMPANY_ADDRESS_DEFAULT:
                ok = False
                affected_rows.append(row)
            row += 1
        return ok, affected_rows
    
    def is_insert_allowed(self):
        '''Perform any necessary validation before inserting a new supplier.
        
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
        company_name_index = self.createIndex(row, self.COMPANY_NAME_COLUMN)
        allowed = self._is_company_name_valid(self.data(company_name_index),
                                               check_unique=False)
        if allowed:
            address_index = self.createIndex(row, self.ADDRESS_COLUMN)
            allowed = self._is_address_valid(self.data(address_index))
        return allowed
        