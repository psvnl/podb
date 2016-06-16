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
from product import Product
from datavalidation import MAX_ADDRESS_LINES

# The string that is added to the list of products to allow the user to request 
# to add a new product.
ADD_NEW_PRODUCT_COMBO_STRING = "Add new..."


class ProductPartNumberEditDelegate(QItemDelegate):
    
    def __init__(self, session, purchase_order, parent=None):
        QItemDelegate.__init__(self, parent)
        self.session = session
        self.purchase_order = purchase_order
        self.product_part_numbers = []
        
    def createEditor(self, parent, option, index):
        self.product_part_numbers.clear()
        with self.session.no_autoflush:
            products = self.session.query(Product).\
            filter(Product.supplier_id == self.purchase_order.supplier.id).all()
        self.product_part_numbers.append(ADD_NEW_PRODUCT_COMBO_STRING)
        for product in products:
            self.product_part_numbers.append(product.part_number)
        self.completer = QCompleter(self.product_part_numbers, parent)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        combobox = QComboBox(parent)
        combobox.setCompleter(self.completer)
        combobox.addItems(self.product_part_numbers)
        self.connect(combobox, SIGNAL("activated(const QString&)"), 
                     self.activated)
        self.connect(combobox, SIGNAL("editingFinished()"), self, 
                     SLOT("editingFinished()"))
        return combobox
    
    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        comboindex = editor.findText(index.model().data(index, 
                                                        role=Qt.EditRole))
        editor.setCurrentIndex(comboindex)
        editor.blockSignals(False)
        
    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText())
        
    def activated(self, value):
        self.emit(SIGNAL("commitData(QWidget*)"), self.sender())
        self.emit(SIGNAL("closeEditor(QWidget*,"
                         "QAbstractItemDelegate::EndEditHint)"), 
                  self.sender(), QAbstractItemDelegate.NoHint)
        
    @pyqtSlot()
    def editingFinished(self):
        self.commitData.emit(self.sender())
        
        
class ProductDescriptionEditDelegate(QItemDelegate):
    
    def __init__(self, session, purchase_order, parent=None):
        QItemDelegate.__init__(self, parent)
        self.session = session 
        self.purchase_order = purchase_order
        self.product_descriptions = []
        
    def createEditor(self, parent, option, index):
        self.product_descriptions.clear()
        with self.session.no_autoflush:
            products = self.session.query(Product).\
            filter(Product.supplier_id == self.purchase_order.supplier.id).all()
        self.product_descriptions.append(ADD_NEW_PRODUCT_COMBO_STRING)
        for product in products:
            self.product_descriptions.append(product.product_description)
        self.completer = QCompleter(self.product_descriptions, parent)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        combobox = QComboBox(parent)
        combobox.setCompleter(self.completer)
        combobox.addItems(self.product_descriptions)
        self.connect(combobox, SIGNAL("activated(const QString&)"), 
                     self.activated)
        self.connect(combobox, SIGNAL("editingFinished()"), self, 
                     SLOT("editingFinished()"))
        return combobox
    
    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        comboindex = editor.findText(index.model().data(index, 
                                                        role=Qt.EditRole))
        editor.setCurrentIndex(comboindex)
        editor.blockSignals(False)
        
    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText())
        
    def activated(self, value):
        self.emit(SIGNAL("commitData(QWidget*)"), self.sender())
        self.emit(SIGNAL("closeEditor(QWidget*,"
                         "QAbstractItemDelegate::EndEditHint)"), 
                  self.sender(), QAbstractItemDelegate.NoHint)
        
    @pyqtSlot()
    def editingFinished(self):
        self.commitData.emit(self.sender())
        
        
class PercentageEditDelegate(QItemDelegate):
    
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)
        
    def createEditor(self, parent, option, index):
        spinbox = QSpinBox(parent)
        spinbox.setRange(0, 99)
        spinbox.setSingleStep(1)
        self.connect(spinbox, SIGNAL("editingFinished()"), self, 
                     SLOT("editingFinished()"))
        return spinbox
    
    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setValue(int(index.model().data(index, role=Qt.EditRole) * 100))
        editor.blockSignals(False)
        
    def setModelData(self, editor, model, index):
        model.setData(index, Decimal(editor.text()) / Decimal("100.0"))
            
    @pyqtSlot()
    def editingFinished(self):
        self.commitData.emit(self.sender())
        
        
class LimitedLinePlainTextEdit(QPlainTextEdit):
    
    def __init__(self, line_limit, parent=None):
        super().__init__(parent=parent)
        self.line_limit = line_limit
        
    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            if self.blockCount() < self.line_limit:
                super().keyPressEvent(e)
        else:
            super().keyPressEvent(e)
        
        
class AddressEditDelegate(QItemDelegate):
    
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)
        
    def createEditor(self, parent, option, index):
        plaintextedit = LimitedLinePlainTextEdit(MAX_ADDRESS_LINES, 
                                                 parent=parent)
        return plaintextedit
    
    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.document().setPlainText(index.model().data(index, 
                                                          role=Qt.EditRole))
        editor.selectAll()
        editor.blockSignals(False)
        
    def setModelData(self, editor, model, index):
        model.setData(index, editor.document().toPlainText())
    
    
class ProjectCodeEditDelegate(QItemDelegate):
    
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)
        
    def createEditor(self, parent, option, index):
        lineedit = QLineEdit(parent)
        inputmask = ">AAA999"
        lineedit.setInputMask(inputmask)
        regexp = QRegExp(r"[A-Z]{3,3}\d{3,3}")
        validator = QRegExpValidator(regexp, parent)
        lineedit.setValidator(validator)
        self.connect(lineedit, SIGNAL("editingFinished()"), self, 
                     SLOT("editingFinished()"))
        return lineedit
    
    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setText(index.model().data(index, role=Qt.EditRole))
        editor.blockSignals(False)
        
    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())
            
    @pyqtSlot()
    def editingFinished(self):
        self.commitData.emit(self.sender())
