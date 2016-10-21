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
import datetime
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_projectsdialog
from sqlasession import session_scope
from projectmodel import ProjectModel
from customdelegates import ProjectCodeEditDelegate


class ProjectsDialog(QDialog, ui_projectsdialog.Ui_projectsDialog):
            
    def __init__(self, session, parent=None):
        super(ProjectsDialog, self).__init__(parent)
        self.setupUi(self)
        self.session = session
        self.model = ProjectModel(self.session, parent=self)
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
        self.tableView.setItemDelegateForColumn(
                                    ProjectModel.CODE_COLUMN,
                                    ProjectCodeEditDelegate(self.tableView))
        self.tableView.hideColumn(ProjectModel.ID_COLUMN)
        self.tableView.setColumnWidth(ProjectModel.CODE_COLUMN, 
                                      self.tableView.width() * 0.13)
        self.tableView.setColumnWidth(ProjectModel.DESCRIPTION_COLUMN, 
                                      self.tableView.width() * 0.65)
        self.tableView.setColumnWidth(ProjectModel.COMPLETED_COLUMN, 
                                      self.tableView.width() * 0.22)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setDefaultSectionSize(25)
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
            
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F12:
            p = QPixmap.grabWindow(self.winId())
            date = datetime.datetime.now()
            filename = date.strftime("screenshot-%Y-%m-%d_%H-%M-%S.jpg")
            p.save(filename, "jpg")
            logging.debug("{} screenshot done".format(type(self).__name__))
        
    def closeEvent(self, event):
        super(ProjectsDialog, self).closeEvent(event)
        
if __name__ == '__main__':
    with session_scope() as session:
#         create_database_if_required()
        app = QApplication(sys.argv)
        form = ProjectsDialog(session)
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
         