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
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from datavalidation import DATA_VAL_ERROR_MSG_BOX_TITLE
from messagebox import execute_critical_msg_box
from pdfreports import ReportPdf, ReportPdfLineItemDetails
from project import Project
from purchaseorder import PurchaseOrder
from reportmodel import ReportModel
from sqlasession import session_scope
from supplier import Supplier
import ui_reportsdialog


class ReportsDialog(QDialog, ui_reportsdialog.Ui_reportsDialog):
    
    _report_types = ["Items by Project", "Items by Supplier"]
    
    def __init__(self, app_config, session, company_name, parent=None):
        super(ReportsDialog, self).__init__(parent)
        self.setupUi(self)
        self.session = session
        self.app_config = app_config
        self.company_name = company_name
        self.model = None
        self.donePushButton.connect(self.donePushButton, 
                                    SIGNAL("clicked()"),
                                    self.reject)
        self.on_clearToolButton_clicked()
        
    @pyqtSignature("")
    def on_clearToolButton_clicked(self):
        self._current_report = ReportModel.REPORT_TYPE_NONE
        self._project_description = ""
        self._supplier_company_name = ""
        self.additionalDataComboBox.setEnabled(False)
        self.clearToolButton.setEnabled(False)
        self.exportToolButton.setEnabled(False)
        self.printToolButton.setEnabled(False)
        self.totalLabel.setEnabled(False)
        self.totalResultLabel.setEnabled(False)
        self.totalResultLabel.setText("R 0.00")
        self._populate_report_type_combo_box()
        self._initialise_start_date()
        self._initialise_end_date()
        if self.model:
            selection_model = self.tableView.selectionModel()
            del(selection_model)
            self.model = None
        self.tableView.setEnabled(False)
        self.tableView.setModel(None)
            
    def _populate_report_type_combo_box(self):
        self.reportTypeComboBox.clear()
        for report_type in self._report_types:
            self.reportTypeComboBox.addItem(report_type)
        self.reportTypeComboBox.setCurrentIndex(0)
            
    def _initialise_start_date(self):
        # Get the date of the first ever purchase order.
        first_po = self.session.query(PurchaseOrder).first()
        if first_po is None:
            # There are no purchase orders. Why are we even here?
            self.startDateEdit.setDate(datetime.date.today())
            self._start_date = datetime.date.today()
        else:
            self.startDateEdit.setDate(first_po.order_date)
            self._start_date = first_po.order_date
        self.startDateEdit.setCalendarPopup(True)
        self.startDateEdit.connect(self.startDateEdit, 
                                   SIGNAL("dateChanged(const QDate&)"),
                                   self._start_date_changed)
    
    def _initialise_end_date(self):
        self.endDateEdit.setDate(datetime.date.today())
        self._end_date = datetime.date.today()
        self.endDateEdit.setCalendarPopup(True)
        self.endDateEdit.connect(self.endDateEdit, 
                                 SIGNAL("dateChanged(const QDate&)"),
                                 self._end_date_changed)
        
    @pyqtSignature("const QString&")
    def on_reportTypeComboBox_currentIndexChanged(self, text):
        if text == self._report_types[
                                    ReportModel.REPORT_TYPE_ITEMS_BY_PROJECT]:
            self.additionalDataLabel.setText("Project:")
            self.additionalDataComboBox.setToolTip("Select the project")
            self._current_report = ReportModel.REPORT_TYPE_ITEMS_BY_PROJECT
            self._populate_projects_combo_box()
        elif text == self._report_types[
                                    ReportModel.REPORT_TYPE_ITEMS_BY_SUPPLIER]:
            self.additionalDataLabel.setText("Supplier:")
            self.additionalDataComboBox.setToolTip("Select the supplier")
            self._current_report = ReportModel.REPORT_TYPE_ITEMS_BY_SUPPLIER
            self._populate_suppliers_combo_box()
            
    def _populate_projects_combo_box(self):
        self.additionalDataComboBox.clear()
        self.projects = self.session.query(Project).all()
        for project in self.projects:
            self.additionalDataComboBox.addItem(project.code)
        self.additionalDataComboBox.setCurrentIndex(0)
        self.additionalDataComboBox.setEnabled(True)
    
    def _populate_suppliers_combo_box(self):
        self.additionalDataComboBox.clear()
        self.suppliers = self.session.query(Supplier).all()
        for supplier in self.suppliers:
            self.additionalDataComboBox.addItem(supplier.company_name)
        self.additionalDataComboBox.setCurrentIndex(0)
        self.additionalDataComboBox.setEnabled(True)
    
    @pyqtSignature("const QString&")
    def on_additionalDataComboBox_currentIndexChanged(self, text):
        if self._current_report == ReportModel.REPORT_TYPE_ITEMS_BY_PROJECT:
            self._project_description = text
        elif self._current_report == ReportModel.REPORT_TYPE_ITEMS_BY_SUPPLIER:
            self._supplier_company_name = text
    
    def _start_date_changed(self, start_date):
        self._start_date = start_date.toPyDate()
    
    def _end_date_changed(self, end_date):
        self._end_date = end_date.toPyDate()
        
    @pyqtSignature("")
    def on_goPushButton_clicked(self):
        if self._start_date > self._end_date:
            execute_critical_msg_box(
                            DATA_VAL_ERROR_MSG_BOX_TITLE, 
                            "The start date cannot be after the end date.", 
                            QMessageBox.Ok)
            return
        if self.model:
            selection_model = self.tableView.selectionModel()
            del(selection_model)
            del(self.model)
        # Request to view the result of the configured report.
        if self._current_report == ReportModel.REPORT_TYPE_ITEMS_BY_PROJECT:
            self.model = ReportModel(self.app_config, 
                                     self.session,
                                     self._current_report,
                                     self._project_description,
                                     self._start_date,
                                     self._end_date,
                                     parent=self)
        elif self._current_report == ReportModel.REPORT_TYPE_ITEMS_BY_SUPPLIER:
            self.model = ReportModel(self.app_config, 
                                     self.session,
                                     self._current_report,
                                     self._supplier_company_name,
                                     self._start_date,
                                     self._end_date,
                                     parent=self)
        else:
            return
        if self.model:
            self.tableView.setModel(self.model)
            self.tableView.setEnabled(True)
            self.tableView.resizeColumnsToContents()
            self.tableView.horizontalHeader().setStretchLastSection(True)
            self.tableView.verticalHeader().setDefaultSectionSize(25)
            self.tableView.verticalHeader().setVisible(False)
            self.totalLabel.setEnabled(True)
            self.totalResultLabel.setEnabled(True)
            self.totalResultLabel.setText(
                                    "R {:,.2f}".format(
                                            self.model.calculate_total_value()))
            self.clearToolButton.setEnabled(True)
            self.exportToolButton.setEnabled(True)
            
    @pyqtSignature("")
    def on_exportToolButton_clicked(self):
        if self.model:
            pdf_filename = QFileDialog.getSaveFileName(
                                        self, 
                                        caption="Save Report to PDF", 
                                        filter="*.pdf")
            if pdf_filename == "":
                # The file name is empty, which probably means that the user 
                # pressed Cancel in the file dialog. Just return.
                return
            line_items = []
            for row in range(self.model.rowCount()):
                line_items.append(self.model.get_row(row))
            total_value = self.model.calculate_total_value()
            line_item_details = ReportPdfLineItemDetails(
                                            line_items,
                                            "R {:,.2f}".format(total_value))
            
            pdf_report = ReportPdf(pdf_filename,
                                   self._report_types[self._current_report],
                                   self.additionalDataComboBox.currentText(),
                                   str(self._start_date),
                                   str(self._end_date),
                                   line_item_details,
                                   self.company_name)
            pdf_report.build()
            
    def closeEvent(self, event):
        super(ReportsDialog, self).closeEvent(event)

if __name__ == '__main__':
    with session_scope() as session:
#         create_database_if_required()
        app = QApplication(sys.argv)
        form = ReportsDialog(session, "Acme Explosives (Pty) Ltd")
        dialog_result = form.exec_()
        if dialog_result == QDialog.Accepted:
            session.commit()
        elif dialog_result == QDialog.Rejected:
            session.rollback()
        else:
            raise RuntimeError(("The reports dialog result was {}. Only "
                                "QDialog.Accepted (1) or QDialog.Rejected (0) "
                                "are valid.").format(str(dialog_result)))
        app.exec_()