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

from messagebox import (execute_critical_msg_box, execute_warning_msg_box, 
                        execute_info_msg_box)


DATA_VAL_ERROR_MSG_BOX_TITLE = "Data Validation Error"


def warn_about_changing_used_data(item_name):
    '''Warn the user about changing data that is referenced in a purchase order.
    
    Shows a message box describing the consequences of changing data that is 
    referenced in a purchase order, and asks the user to confirm that she wants
    to do this.
    
    Args:
    :param item_name: The top-level data item that is being changed, e.g., 
        "project", "supplier", "product".
    :type item_name: String
        
    Returns:
    :return: The message box result, which is either "Yes" or "Cancel".
    :rtype: QMessageBox.Yes or QMessageBox.Cancel
    '''
    result = execute_warning_msg_box(
                    "Data Warning", 
                    ("You are changing the data of a {} that has been used in "
                     "one or more purchase orders. If you do this then those "
                     "purchase orders will reflect the new data. The old data "
                     "will be lost.\n\nAre you sure you want to change this "
                     "{}'s data?").format(item_name, item_name), 
                    QMessageBox.Yes | QMessageBox.Cancel)
    return result

def show_error_rows_with_default_values(field_name, row_numbers):
    '''Inform the user that there are rows with data set to default values.
    
    Shows a message box indicating the rows that have data set to default 
    values.
    
    Args:
    :param field_name: The name of the field that has default values, e.g.,
        "project description".
    :type field_name: String
    :param row_numbers: The row numbers where the error occurs. Note that these
        should correspond to row numbers that the user can see, i.e., the table
        row numbers as displayed in a QTableView. That means that the model row
        numbers should be incremented before passing to this function.
    :type row_numbers: List of integers 
    '''
    if len(row_numbers) == 0:
        raise ValueError("No row numbers were specified.")
    row_numbers_string = "Affected rows: " + str(row_numbers[0])
    for row_number in row_numbers[1:]:
        row_numbers_string += ", "
        row_numbers_string += str(row_number)
    execute_critical_msg_box(
                    DATA_VAL_ERROR_MSG_BOX_TITLE, 
                    ("The following rows contain the default {}. The {} must "
                     "not be left as the default value. This must be corrected "
                     "before the table can be saved.\n\n{}").format(
                                                            field_name,
                                                            field_name,
                                                            row_numbers_string),
                    QMessageBox.Ok)
    
def show_error_rows_with_zero_prices(field_name, row_numbers):
    '''Inform the user that there are rows with price data set to zero.
    
    Shows a message box indicating the rows that have price data set to zero.
    
    Args:
    :param field_name: The name of the field that has default values, e.g.,
        "current price".
    :type field_name: String
    :param row_numbers: The row numbers where the error occurs. Note that these
        should correspond to row numbers that the user can see, i.e., the table
        row numbers as displayed in a QTableView. That means that the model row
        numbers should be incremented before passing to this function.
    :type row_numbers: List of integers
    '''
    if len(row_numbers) == 0:
        raise ValueError("No row numbers were specified.")
    row_numbers_string = "Affected rows: " + str(row_numbers[0])
    for row_number in row_numbers[1:]:
        row_numbers_string += ", "
        row_numbers_string += str(row_number)
    execute_critical_msg_box(
                    DATA_VAL_ERROR_MSG_BOX_TITLE, 
                    ("The following rows contain {} fields set to zero. "
                     "The {} must not be zero. This must be corrected "
                     "before the table can be saved.\n\n{}").format(
                                                            field_name,
                                                            field_name,
                                                            row_numbers_string), 
                    QMessageBox.Ok)
    
def show_error_product_already_on_po(field_name, field_value):
    '''Inform the user via a message box that the selected product is already 
    on the purchase order.
    
    Args:
    :param field_name: The name of the field that was selected, e.g., 
        "part number" or "description".
    :type field_name: String
    :param field_value: The value of the selected field, e.g., "PARTXYZ".
    :type field_value: String
    '''
    execute_info_msg_box("Product Selection", 
                         ("The product with {} \"{}\" is already "
                          "listed on this purchase order.\n\n"
                          "A product can only appear once on a purchase "
                          "order.").format(field_name, field_value), 
                         QMessageBox.Ok)

MAX_ADDRESS_LINES = 4

def validate_num_address_lines(address):
    '''
    Checks that the supplied address does not have more than four lines. Raises
    a ValueError exception if it does.
    :param address: An address string.
    '''
    address_lines = address.split('\n')
    if len(address_lines) > MAX_ADDRESS_LINES:
        raise ValueError("Address is longer than four lines.")
    return address_lines


class TextFieldValidator(object):
    '''A class used to validate text data that is being added to the database.    
    '''
    
    def __init__(self, field_name, field_value, column_data, default_text,
                 check_unique=True, check_not_blank=True, 
                 check_not_default=True):
        '''Initialise the TextFieldValidator object with local copies of the 
        parameters.
        
        Args:
        :param field_name: The name of the field that is being validated, as it
            would be referred to in a sentence, e.g., "project description" or 
            "supplier company name".
        :type field_name: String
        :param field_value: The value to be validated. 
        :type field_value: String 
        :param column_data: The list of values for this field for the entire 
            column.
        :type column_data: List of strings
        :param default_text: The default text that is used to initialise the 
            field when a new table record is created, e.g., when a new project
            record is created, the project_description field is initialised 
            with "Describe the project".
        :type default_text: String
        :param check_unique: Enable check that the value is unique in the 
            column.
        :type check_unique: Boolean
        :param check_not_blank: Enable check that the value is not blank, i.e., 
            composed of just white space.
        :type check_not_blank: Boolean
        :param check_not_default: Enable check that the value is not equal to 
            the default text.
        :type check_not_default: Boolean
        
        Raises:
        :raises: ValueError if all of the check enabling parameters are False.
        '''
        self.field_name = field_name
        self.field_value = field_value
        self.column_data = column_data
        self.default_text = default_text
        if check_unique is False and \
        check_not_blank is False and \
        check_not_default is False:
            raise ValueError("None of the available validation checks have "
                             "been requested.")
        self.check_unique = check_unique
        self.check_not_blank = check_not_blank
        self.check_not_default = check_not_default
       
    def field_is_valid(self):
        '''Carry out the requested validation on the field.
        
        Note that if a validation check fails, the error is displayed to the
        user using a message box.
        
        Returns:
        :return: True if the field is valid. False if the field is invalid.
        :rtype: Boolean
        '''
        is_valid = True
        if self.check_unique:
            is_valid = self._field_unique()
        if is_valid:
            if self.check_not_blank:
                is_valid = self._field_not_blank()
        if is_valid:
            if self.check_not_default:
                is_valid = self._field_not_default()
        return is_valid
        
    def _field_unique(self):
        '''Verify that the field is unique.
        
        Compares the field value to the values in the list of column data. If a
        duplicate value is found then a message box is used to display the 
        error.
        
        Returns:
        :return: True if the field value is unique. False if the field value is
            not unique.
        :rtype: Boolean
        '''
        is_unique = True
        for text_item in self.column_data:
            if text_item != self.default_text:
                if self.field_value == text_item:
                    is_unique = False
        if not is_unique:
            execute_critical_msg_box(
                            DATA_VAL_ERROR_MSG_BOX_TITLE, 
                            ("The {} you entered already exists. "
                             "The {} field must be unique.").format(
                                                            self.field_name, 
                                                            self.field_name), 
                            QMessageBox.Ok)
        return is_unique
    
    def _field_not_blank(self):
        '''Verify that the field is not blank.

        Checks if the field is composed only of white space. If it is then a
        message box is used to display the error.
        
        Returns:
        :return: True if the field is not blank. False if the field is blank.
        :rtype: Boolean
        '''
        if self.field_value.isspace():
            execute_critical_msg_box(
                            DATA_VAL_ERROR_MSG_BOX_TITLE, 
                            "The {} must not be blank.".format(self.field_name), 
                            QMessageBox.Ok)
            return False
        return True
    
    def _field_not_default(self):
        '''Verify that the field is not equal to the default value.
        
        Compares the field to the default value. If the field equals the 
        default value then a message box is used to display the error.
        
        Returns:
        :return: True if the field is not equal to the default value. False if 
            the field is equal to the default value.
        :rtype: Boolean
        '''
        if self.field_value == self.default_text:
            execute_critical_msg_box(
                            DATA_VAL_ERROR_MSG_BOX_TITLE, 
                            ("The {} must not be left as the default text "
                             "\"{}\".").format(self.field_name, 
                                               self.default_text), 
                            QMessageBox.Ok)
            return False
        return True
                    

class DecimalFieldValidator(object):
    '''A class used to validate decimal data that is being added to the 
    database.    
    '''
    
    def __init__(self, field_name, field_value, low_limit, high_limit,
                 check_within_limits=True, check_not_zero=True):
        '''Initialise the DecimalFieldValidator object with local copies of the 
        parameters.
        
        Args:
        :param field_name: The name of the field that is being validated, as it
            would be referred to in a sentence, e.g., "project description" or 
            "supplier company name".
        :type field_name: String
        :param field_value: The value to be validated.
        :type field_value: Decimal
        :param low_limit: The lower limit against which to check the field
            value. The comparison is "greater than or equal to". The parameter 
            cannot be None if the check_within_limits parameter is True.
        :type low_limit: Decimal or None
        :param high_limit: The upper limit against which to check the field
            value. The comparison is "less than". The parameter cannot be None 
            if the check_within_limits parameter is True.
        :type high_limit: Decimal or None
        :param check_within_limits: Enable check that the value is within 
            specified limits.
        :type check_within_limits: Boolean
        :param check_not_zero: Enable check that the value is not zero.
        :type check_not_zero: Boolean
        
        :raises: ValueError if:
            - All of the check enabling parameters are False.
            - check_within_limits is True and either low_limit or high_limit 
                are None.
        '''
        self.field_name = field_name
        self.field_value = field_value
        if check_within_limits is True and low_limit is None:
            raise ValueError("The check within limits validation was requested "
                             "but low_limit is None.")
        if check_within_limits is True and high_limit is None:
            raise ValueError("The check within limits validation was requested "
                             "but high_limit is None.")
        self.low_limit = low_limit
        self.high_limit = high_limit
        if check_within_limits is False and check_not_zero is False:
            raise ValueError("None of the available validation checks have "
                             "been requested.")
        self.check_within_limits = check_within_limits
        self.check_not_zero = check_not_zero
        
    def field_is_valid(self):
        '''Carry out the requested validation on the field.
        
        Note that if a validation check fails, the error is displayed to the
        user using a message box.
        
        Returns:
        :return: True if the field is valid. False if the field is invalid.
        :rtype: Boolean
        '''
        is_valid = True
        if self.check_within_limits:
            is_valid = self._field_within_limits()
        if is_valid is True:
            if self.check_not_zero:
                is_valid = self._field_not_zero()
        return is_valid
    
    def _field_within_limits(self):
        '''Verify that the field is within the specified range.

        Checks if the field value is greater than or equal to self.low_limit 
        and less than self.high_limit.
        
        Returns:
        :return: True if the field is within the specified limits. False if the 
            field is outside the specified limits.
        :rtype: Boolean
        '''
        if self.field_value >= self.low_limit and \
        self.field_value < self.high_limit:
            return True
        else:
            execute_critical_msg_box(
                            DATA_VAL_ERROR_MSG_BOX_TITLE, 
                            ("The {} must be greater than or equal to {} "
                             "and less than {}.").format(self.field_name, 
                                                         self.low_limit,
                                                         self.high_limit), 
                            QMessageBox.Ok)
            return False
    
    def _field_not_zero(self):
        '''Verify that the field is not equal to zero.
        
        Returns:
        :return: True if the field is not equal to zero. False if the field is
            equal to zero.
        :rtype: Boolean
        '''
        if self.field_value == Decimal("0.0"):
            execute_critical_msg_box(
                            DATA_VAL_ERROR_MSG_BOX_TITLE, 
                            "The {} must not be zero.".format(self.field_name), 
                            QMessageBox.Ok)
            return False
        return True

if __name__ == '__main__':
    pass