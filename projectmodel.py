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
from project import Project
from purchaseorder import PurchaseOrder
from datavalidation import (TextFieldValidator, warn_about_changing_used_data,
                            show_error_rows_with_default_values)


class ProjectModel(QAbstractTableModel):
    '''Data model for the project table.
    '''

    PROJECT_MODEL_NUM_COLUMNS = 4
    (ID_COLUMN,
     CODE_COLUMN, 
     DESCRIPTION_COLUMN,
     COMPLETED_COLUMN) = range(PROJECT_MODEL_NUM_COLUMNS)
     
    # String used to initialise the project code field of a new project.
    _CODE_DEFAULT = "ABC123"
    # String used to initialise the project description field of a new project.
    _DESCRIPTION_DEFAULT = "Describe the project"

    def __init__(self, session, parent=None):
        '''Initialise the ProjectModel object.
        
        Loads a local projects list (self.projects) with the result of a query
        for all projects in the database.
        
        Args:
        :param session: The SQLAlchemny session in use. 
        :type session: Session object (the class created by the call to  
            :func:`sessionmaker` in :mod:`sqlasession`).
        :param parent: The model's parent.
        :type parent: QObject
        '''
        super().__init__(parent=parent)
        self.session = session
        with self.session.no_autoflush:
            self.projects = self.session.query(Project).all()
        
    def rowCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.rowCount.
        '''
        return len(self.projects) 

    def columnCount(self, index=QModelIndex()):
        '''Refer to QAbstractItemModel.columnCount.
        '''
        return self.PROJECT_MODEL_NUM_COLUMNS
    
    def data(self, index, role=Qt.DisplayRole):
        '''Refer to QAbstractItemModel.data.
        '''
        if not index.isValid() or \
        not (0 <= index.row() < self.rowCount()):
            return None
        project = self.projects[index.row()]
        column = index.column()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if column == self.CODE_COLUMN:
                return project.code
            elif column == self.DESCRIPTION_COLUMN:
                return project.description
            elif column == self.COMPLETED_COLUMN:
                return "Completed"
            else:
                return None
        elif role == Qt.CheckStateRole:
            if column == self.COMPLETED_COLUMN:
                if project.completed:
                    return Qt.Checked
                else:
                    return Qt.Unchecked
            else:
                return None
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
            if section == self.CODE_COLUMN:
                return "Code"
            elif section == self.DESCRIPTION_COLUMN:
                return "Description"
            elif section == self.COMPLETED_COLUMN:
                return "Status"
        return int(section + 1)
    
    def flags(self, index):
        '''Refer to QAbstractItemModel.flags.
        '''
        if not index.isValid():
            return Qt.ItemIsEnabled
        column = index.column()
        if column == self.COMPLETED_COLUMN:
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
            if role == Qt.CheckStateRole and column == self.COMPLETED_COLUMN:
                self._validate_and_set_completed(index, value)
            else:
                if value:
                    if column == self.CODE_COLUMN:
                        self._validate_and_set_code(index, value)
                    elif column == self.DESCRIPTION_COLUMN:
                        self._validate_and_set_description(index, value)
            return True
        return False
    
    def _validate_and_set_completed(self, index, checked_state):
        '''Validate the requested project completed state and set the table 
        field data if validation passes.
        
        The method verifies that the requested state is either "checked" or 
        "not checked", mapping to "completed" or "not completed", before 
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
            self.projects[row].completed = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
        elif checked_state == Qt.Unchecked:
            self.projects[row].completed = False
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
        
    def _validate_and_set_code(self, index, code):
        '''Validate the requested project code and set the table field data 
        if validation passes.
        
        The method checks if the specified row corresponds to a project that is 
        referenced in a purchase order. If this is the case, the method warns 
        the user of the consequences of changing the data using a message box.
        
        The method calls :meth:`_is_project_description_valid` to validate the
        project description.
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written. 
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param code: The requested project code.
        :type code: String
        '''
        result = QMessageBox.Yes
        row = index.row()
        if self._is_project_used(self.projects[row].id):
            # The project is used, i.e., referenced in a purchase order.
            if self.projects[row].code != code:
                # Warn about changing a used project only if a different value
                # is requested
                result = warn_about_changing_used_data("project")
        if result == QMessageBox.Yes:
            valid = False
            if code == self._CODE_DEFAULT:
                # The requested value is the default value. In this case the
                # validation must be run, regardless of whether the value is 
                # the same as the current value, so that the user is told that 
                # the field must not be left as the default value.
                valid = self._is_project_code_valid(code)
            else:
                # The requested value is not the default value. In this case 
                # the validation must be run only if the requested value is 
                # different from the current value. 
                if self.projects[row].code != code:
                    valid = self._is_project_code_valid(code)
            if valid is True:
                # The requested value is valid. Set the data.
                self.projects[row].code = code
                # Emit the data changed signal.
                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                          index, index)
    
    def _is_project_used(self, project_id):
        '''Determines if a project is referenced in a purchase order.
        
        Args:
        :param project_id: The primary key (project.id) of the project to be 
            checked.
        :type project_id: Integer
            
        Returns:
        :return: True if the project is referenced in a purchase order. False
            otherwise.
        :rtype: Boolean
        '''
        with self.session.no_autoflush:
            if self.session.query(PurchaseOrder).\
                filter(PurchaseOrder.project_id == project_id).count() > 0:
                return True
            return False
                
    def _is_project_code_valid(self, code, check_unique=True):
        '''Determines if a project code is valid.
        
        A project code is considered valid if:
        - It is unique, i.e., is not already in the table.
        - It is not blank, i.e., made up only of white space.
        - It is not the default text that is used to initialise a newly 
          inserted project.
        A TextFieldValidator object is used to perform the actual validation.
        
        Note that if a validation check fails, TextFieldValidator will use
        message boxes to inform the user of the failed check. 
        
        Args:
        :param code: The project code to validate.
        :type code: String
        :param check_unique: Enable check that the value is unique in the 
            column.
        :type check_unique: Boolean
        
        Returns:
        :return: True if the code is valid. False otherwise.
        :rtype: Boolean 
        '''
        validator = TextFieldValidator(
                                "project code",
                                code,
                                [p.code for p in self.projects],
                                self._CODE_DEFAULT,
                                check_unique=check_unique)
        return validator.field_is_valid()
        
    def _validate_and_set_description(self, index, description):
        '''Validate the requested project description and set the table field
        data if validation passes.
        
        The method checks if the specified row corresponds to a project that is 
        referenced in a purchase order. If this is the case, the method warns 
        the user of the consequences of changing the data using a message box.
        
        The method calls :meth:`_is_project_description_valid` to validate the
        project description.
        
        Emits the QAbstractTableModel.dataChanged signal if a new, different
        value was written. 
        
        Args:
        :param index: The model index being updated.
        :type index: QModelIndex
        :param description: The requested project description.
        :type description: String
        '''
        result = QMessageBox.Yes
        row = index.row()
        if self._is_project_used(self.projects[row].id):
            # The project is used, i.e., referenced in a purchase order.
            if self.projects[row].description != description:
                # Warn about changing a used project only if a different value
                # is requested
                result = warn_about_changing_used_data("project")
        if result == QMessageBox.Yes:
            valid = False
            if description == self._DESCRIPTION_DEFAULT:
                # The requested value is the default value. In this case the
                # validation must be run, regardless of whether the value is 
                # the same as the current value, so that the user is told that 
                # the field must not be left as the default value.
                valid = self._is_project_description_valid(description)
            else:
                # The requested value is not the default value. In this case 
                # the validation must be run only if the requested value is 
                # different from the current value. 
                if self.projects[row].description != description:
                    valid = self._is_project_description_valid(description)
            if valid is True:
                # The requested value is valid. Set the data.
                self.projects[row].description = description
                # Emit the data changed signal.
                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                          index, index)
    
    def _is_project_description_valid(self, description, check_unique=True):
        '''Determines if a project description is valid.
        
        A project description is considered valid if:
        - It is unique, i.e., is not already in the table.
        - It is not blank, i.e., made up only of white space.
        - It is not the default text that is used to initialise a newly 
          inserted project.
        A TextFieldValidator object is used to perform the actual validation.
        
        Note that if a validation check fails, TextFieldValidator will use
        message boxes to inform the user of the failed check. 
        
        Args:
        :param description: The project description to validate.
        :type description: String
        :param check_unique: Enable check that the value is unique in the 
            column.
        :type check_unique: Boolean
        
        Returns:
        :return: True if the description is valid. False otherwise.
        :rtype: Boolean 
        '''
        validator = TextFieldValidator(
                                "project description",
                                description,
                                [p.description for p in self.projects],
                                self._DESCRIPTION_DEFAULT,
                                check_unique=check_unique)
        return validator.field_is_valid()
        
    def insertRows(self, position, rows=1, index=QModelIndex()):
        '''Refer to QAbstractItemModel.insertRows.
        '''
        # Insertion of a project is not allowed, only addition of a project.
        assert position == self.rowCount()
        # Only one project can be inserted at a time.
        assert rows == 1
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        new_project = Project(code=self._CODE_DEFAULT,
                              description=self._DESCRIPTION_DEFAULT,
                              completed=False)
        self.session.add(new_project)
        self.projects.append(new_project)
        self.endInsertRows()
        return True
        
    def get_project_list(self):
        '''Retrieve a list of all project codes.
        
        Returns:
        :return: A list of the project codes for all projects in the 
            database.
        :rtype: List of strings
        '''
        project_code_list = []
        for project in self.projects:
            project_code_list.append(project.code)
        return project_code_list

    def is_save_allowed(self):
        '''Perform any necessary validation before saving the data.
        
        The method checks if there are any project descriptions still set to 
        the default value. This can happen. If it does then the user will be
        told about the errors through a message box.
        
        Returns:
        :return: True if the validation passed and the data may be saved. False
            if the validation failed.
        :rtype: Boolean
        '''
        allowed, affected_rows = self._project_codes_not_default()
        if not allowed:
            show_error_rows_with_default_values("project code", 
                                                affected_rows)
        else:
            allowed, affected_rows = self._project_descriptions_not_default()
            if not allowed:
                show_error_rows_with_default_values("project description", 
                                                    affected_rows)
        return allowed
        
    def _project_codes_not_default(self):
        '''Checks ifany of the project codes are set to the default value.
        
        Returns:
        :return: Two items are returned: 
            - A boolean indication of whether or not there are default values. 
              True means that none of the project codes are default. 
              False means some of the project codes are default.
            - A list of the affected rows, i.e., rows that have default project
              codes.
        :rtype: Boolean
        :rtype: List of integers
        '''
        ok = True
        affected_rows = []
        row = 1
        for project in self.projects:
            if project.code == self._CODE_DEFAULT:
                ok = False
                affected_rows.append(row)
            row += 1
        return ok, affected_rows
        
    def _project_descriptions_not_default(self):
        '''Checks if any of the project descriptions are set to the default 
        value.
        
        Returns:
        :return: Two items are returned: 
            - A boolean indication of whether or not there are default values. 
              True means that none of the project descriptions are default. 
              False means some of the project descriptions are default.
            - A list of the affected rows, i.e., rows that have default project
              descriptions.
        :rtype: Boolean
        :rtype: List of integers 
        '''
        ok = True
        affected_rows = []
        row = 1
        for project in self.projects:
            if project.description == self._DESCRIPTION_DEFAULT:
                ok = False
                affected_rows.append(row)
            row += 1
        return ok, affected_rows
    
    def is_insert_allowed(self):
        '''Perform any necessary validation before inserting a new project.
        
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
        code_index = self.createIndex(row, self.CODE_COLUMN)
        allowed = self._is_project_code_valid(self.data(code_index), 
                                              check_unique=False)
        if allowed:
            description_index = self.createIndex(row, self.DESCRIPTION_COLUMN)
            allowed = self._is_project_description_valid(
                                                self.data(description_index), 
                                                check_unique=False)
        return allowed
        