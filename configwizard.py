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

from copy import copy
from decimal import Decimal
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker
import ui_configwizard
import ui_configwizardp1
import ui_configwizardp2
import ui_configwizardp3
import ui_configwizardp4
import ui_configwizardp5
from appconfig import DatabaseSection, AppConfigError, LocaleSection
from dbaccess import (sqlite_connection_is_ok, mysql_database_exists, 
                      mysql_connection_is_ok)
from userconfigmodel import (UserConfigError, UserConfigEditor, CompanySettings, 
                             PurchaseOrderSettings, LocaleSettings)
from purchaseorder import PO_ORDER_STATUSUS, PO_PAYMENT_TERMS


class StartUpConfigWizard(QWizard, ui_configwizard.Ui_Wizard):
    '''Config wizard that is run on start-up.
    
    This wizard should be run on start-up if there is no application 
    configuration file (appconfig.ConfigFile._CONFIG_FILE_NAME), or if there 
    are errors in the application or user configuration. 
    '''
    
    # Wizard page IDs
    _INTRO_PAGE_ID = 0
    _APP_SETTINGS_PAGE_1_ID = 1
    _APP_SETTINGS_PAGE_2_ID = 2
    _USER_SETTINGS_PAGE_1_ID = 3
    _USER_SETTINGS_PAGE_2_ID = 4
    
    def __init__(self, app_config, parent=None):
        '''Initialiser for the StartUpConfigWizard object.
        
        Initialises internal data and adds the wizard pages to the wizard.
        
        Args:
        :param app_config: The application config in use.
        :type app_config: appconfig.ConfigFile
        :param parent: The wizard's parent.
        :type parent: QObject
        '''
        super().__init__(parent=parent)
        self.app_config = app_config
        self.session = None
        self.user_config = None
        self.setupUi(self)
        self.wizardPage1 = ConfigWizardPage1()
        self.wizardPage2 = ConfigWizardPage2(self.app_config, lock=False)
        self.wizardPage3 = ConfigWizardPage3(self.app_config, lock=False)
        self.wizardPage4 = ConfigWizardPage4(parent=self)
        self.wizardPage5 = ConfigWizardPage5(self.app_config, parent=self)
        self.addPage(self.wizardPage1)
        self.addPage(self.wizardPage2)
        self.addPage(self.wizardPage3)
        self.addPage(self.wizardPage4)
        self.addPage(self.wizardPage5)
        self.connect(self.button(QWizard.FinishButton), 
                     SIGNAL("clicked()"),
                     self._finish_button_clicked)
           
    def initializePage(self, id):
        ''' Refer to QWizard.initializePage.
        
        If the first user settings page is about to be initialised, and there
        is no SQLAlchemy session, and there is no user configuration object, 
        then the method creates the session and user configuration objects.
        This can only be done at this time because these objects are dependent
        upon the database configuration settings, which may have been changed 
        in page 2.  
        
        :param id: Page ID to initialise.
        :type id: Integer
        '''
        if id == self._USER_SETTINGS_PAGE_1_ID and \
            self.session is None and \
            self.user_config is None:
            # Import all the database class definitions so that SQL Alchemy
            # knows what they are. (Ignore the "unused import" warnings in the
            # following six lines.)
            from product import Product
            from project import Project
            from purchaseorder import PurchaseOrder
            from purchaseorderproduct import PurchaseOrderProduct
            from supplier import Supplier
            from userconfig import UserConfig
            # Create a session object, now that we know the database settings.
            from sqlaengine import engine
            from sqlabase import Base
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine, autoflush=True)
            self.session = Session()
            self.user_config = UserConfigEditor(self.session)
        super().initializePage(id)
        
    def get_user_config(self, caller):
        '''Provides the wizard's pages with access to the user configuration 
        object. 
        
        :param caller: The calling object, which is expected to be a wizard 
            page.
        :type caller: QWizardPage.
        '''
        assert (type(caller) == ConfigWizardPage4 or \
                type(caller) == ConfigWizardPage5) 
        if caller.parent is self:
            return self.user_config
        
    def set_user_config(self, caller, user_config):
        '''Allows the wizard's pages to write to the user configuration object.
        
        :param caller: The calling object, which is expected to be a wizard 
            page.
        :type caller: QWizardPage.
        :param user_config: The user configuration to be set. 
        :type user_config: userconfigmodel.UserConfigEditor
        '''
        assert (type(caller) == ConfigWizardPage4 or \
                type(caller) == ConfigWizardPage5)
        if caller.parent is self:
            self.user_config = copy(user_config)
        
    def save_user_config(self, caller):
        '''Allows the wizard's pages to save the user configuration object. 
        
        :param caller: The calling object, which is expected to be a wizard 
            page.
        :type caller: QWizardPage.
        '''
        assert type(caller) == ConfigWizardPage5
        if caller.parent is self:
            self.user_config.save(self.session)
            
    def _finish_button_clicked(self):
        '''Slot for when the Finish button is clicked. The local SQLAlchemy
        session is closed.
        '''
        self.session.close()
            
    def closeEvent(self, event):
        '''Refer to QWidget.closeEvent.
        
        Ensures that the local SQLAlchemy session is closed if the wizard is 
        closed. Then calls the parent's closeEvent method.
        
        :param event: The close event.
        :type event: QCloseEvent
        '''
        self.session.close()
        super().closeEvent(event)
        

class InAppConfigWizard(QWizard, ui_configwizard.Ui_Wizard):
    '''Config wizard that is run when the application is running.
    
    This wizard should be run when the user selects "Configuration Wizard..." 
    in the Edit menu.
    
    A different wizard is used to the one used on start-up because this one 
    need not show the introduction page, and it must not allow edits of the 
    application config settings. 
    '''
    
    _APP_SETTINGS_PAGE_1_ID = 0
    _APP_SETTINGS_PAGE_2_ID = 1
    _USER_SETTINGS_PAGE_1_ID = 2
    _USER_SETTINGS_PAGE_2_ID = 3
    
    def __init__(self, app_config, parent=None):
        super().__init__(parent=parent)
        self.app_config = app_config
        self.session = None
        self.user_config = None
        self.setupUi(self)
        self.wizardPage2 = ConfigWizardPage2(self.app_config, lock=True)
        self.wizardPage3 = ConfigWizardPage3(self.app_config, lock=True)
        self.wizardPage4 = ConfigWizardPage4(parent=self)
        self.wizardPage5 = ConfigWizardPage5(self.app_config, parent=self)
        self.addPage(self.wizardPage2)
        self.addPage(self.wizardPage3)
        self.addPage(self.wizardPage4)
        self.addPage(self.wizardPage5)
        self.connect(self.button(QWizard.FinishButton), 
                     SIGNAL("clicked()"),
                     self._finish_button_clicked)
           
    def initializePage(self, id):
        if id == self._USER_SETTINGS_PAGE_1_ID and \
            self.session is None and \
            self.user_config is None:
            # Create a session object, now that we know the database settings.
            from sqlaengine import engine
            from sqlabase import Base
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine, autoflush=True)
            self.session = Session()
            self.user_config = UserConfigEditor(self.session)
        super().initializePage(id)
        
    def get_user_config(self, caller):
        if caller.parent is self:
            return self.user_config
        
    def set_user_config(self, caller, user_config):
        if caller.parent is self:
            self.user_config = copy(user_config)
        
    def save_user_config(self, caller):
        if caller.parent is self:
            self.user_config.save(self.session)
            
    def _finish_button_clicked(self):
        self.session.close()
            
    def closeEvent(self, event):
        self.session.close()
        super().closeEvent(event)


class ConfigWizardPage1(QWizardPage, ui_configwizardp1.Ui_WizardPage):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        

class ConfigWizardPage2(QWizardPage, ui_configwizardp2.Ui_wizardPage2):
    
    _DB_TYPE_SQLITE_TEXT = "SQLite"
    _DB_TYPE_MYSQL_TEXT = "MySQL"
    
    def __init__(self, app_config, lock=True, parent=None):
        super().__init__(parent=parent)
        self.app_config = app_config
        self.lock = lock
        self.db_connection_ok = False
        self.emit(SIGNAL("completeChanged()"))
        self.setupUi(self)
        
    def initializePage(self):
        # Initialise widgets using config file data.
        self._populate_db_type_combo_box()
        self._initialise_widgets_using_config()

    def _populate_db_type_combo_box(self):
        self.dbTypeComboBox.blockSignals(True)
        self.dbTypeComboBox.addItem(self._DB_TYPE_SQLITE_TEXT)
        self.dbTypeComboBox.addItem(self._DB_TYPE_MYSQL_TEXT)
        self.dbTypeComboBox.blockSignals(False)
        
    def _initialise_widgets_using_config(self):
        if self.app_config.database.type == DatabaseSection.TYPE_SQLITE:
            self.dbTypeComboBox.setCurrentIndex(
                        self.dbTypeComboBox.findText(self._DB_TYPE_SQLITE_TEXT))
        elif self.app_config.database.type == DatabaseSection.TYPE_MYSQL:
            self.dbTypeComboBox.setCurrentIndex(
                        self.dbTypeComboBox.findText(self._DB_TYPE_MYSQL_TEXT))
        else:
            self.dbTypeComboBox.setCurrentIndex(0)
        self.on_dbTypeComboBox_currentIndexChanged(
                                            self.dbTypeComboBox.currentText())
        self.dbFileNameLineEdit.setText(self.app_config.database.filename)
        self.dbNameLineEdit.setText(self.app_config.database.name)
        self.dbUserNameLineEdit.setText(self.app_config.database.username)
        self.dbPasswordLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.dbPasswordLineEdit.setText(self.app_config.database.password)
        self.dbHostLineEdit.setText(self.app_config.database.host)
        self.dbPortLineEdit.setText(self.app_config.database.port)
        if self.lock:
            self.dbTypeComboBox.setEnabled(False)
            self.dbFileNameLineEdit.setEnabled(False)
            self.dbNameLineEdit.setEnabled(False)
            
    def cleanupPage(self):
        # Do nothing.
        pass
    
    def validatePage(self):
        # Save the config file.
        self.app_config.write()
        return True
    
    def isComplete(self):
        # The user can move on to the next page once the database connection 
        # test has passed. 
        return self.db_connection_ok
    
    @pyqtSignature("const QString&")
    def on_dbTypeComboBox_currentIndexChanged(self, text):
        self.db_connection_ok = False
        self.emit(SIGNAL("completeChanged()"))
        if text == self._DB_TYPE_SQLITE_TEXT:
            self.dbFileNameLabel.setEnabled(True)
            self.dbFileNameLineEdit.setEnabled(True)
            self.dbNameLabel.setEnabled(False)
            self.dbNameLineEdit.setEnabled(False)
            self.dbUserNameLabel.setEnabled(False)
            self.dbUserNameLineEdit.setEnabled(False)
            self.dbPasswordLabel.setEnabled(False)
            self.dbPasswordLineEdit.setEnabled(False)
            self.dbHostLabel.setEnabled(False)
            self.dbHostLineEdit.setEnabled(False)
            self.dbPortLabel.setEnabled(False)
            self.dbPortLineEdit.setEnabled(False)
            self.app_config.database.type = DatabaseSection.TYPE_SQLITE
            # Blank the MySQL settings.
            # TODO: Do this via the ConfigFile class.
            self.app_config.database.driver = ""
            self.app_config.database.name = ""
            self.app_config.database.username = ""
            self.app_config.database.password = ""
            self.app_config.database.host = ""
            self.app_config.database.port = ""
            self.dbNameLineEdit.setText(self.app_config.database.name)
            self.dbUserNameLineEdit.setText(self.app_config.database.username)
            self.dbPasswordLineEdit.setText(self.app_config.database.password)
            self.dbHostLineEdit.setText(self.app_config.database.host)
            self.dbPortLineEdit.setText(self.app_config.database.port)
        if text == self._DB_TYPE_MYSQL_TEXT:
            self.dbFileNameLabel.setEnabled(False)
            self.dbFileNameLineEdit.setEnabled(False)
            self.dbNameLabel.setEnabled(True)
            self.dbNameLineEdit.setEnabled(True)
            self.dbUserNameLabel.setEnabled(True)
            self.dbUserNameLineEdit.setEnabled(True)
            self.dbPasswordLabel.setEnabled(True)
            self.dbPasswordLineEdit.setEnabled(True)
            self.dbHostLabel.setEnabled(True)
            self.dbHostLineEdit.setEnabled(True)
            self.dbPortLabel.setEnabled(True)
            self.dbPortLineEdit.setEnabled(True)
            self.app_config.database.type = DatabaseSection.TYPE_MYSQL
            self.app_config.database.driver = DatabaseSection.DRIVER_MYSQL
            # Blank the SQLite settings.
            self.app_config.database.filename = ""
            self.dbFileNameLineEdit.setText(self.app_config.database.filename)
            
    @pyqtSignature("")
    def on_dbFileNameLineEdit_editingFinished(self):
        self.app_config.database.filename = self.dbFileNameLineEdit.text()
    
    @pyqtSignature("")
    def on_dbNameLineEdit_editingFinished(self):
        self.app_config.database.name = self.dbNameLineEdit.text()
    
    @pyqtSignature("")
    def on_dbUserNameLineEdit_editingFinished(self):
        self.app_config.database.username = self.dbUserNameLineEdit.text()
    
    @pyqtSignature("")
    def on_dbPasswordLineEdit_editingFinished(self):
        self.app_config.database.password = self.dbPasswordLineEdit.text()
    
    @pyqtSignature("")
    def on_dbHostLineEdit_editingFinished(self):
        self.app_config.database.host = self.dbHostLineEdit.text()
    
    @pyqtSignature("")
    def on_dbPortLineEdit_editingFinished(self):
        self.app_config.database.port = self.dbPortLineEdit.text()
        
    @pyqtSignature("")
    def on_testConnectionPushButton_clicked(self):
        self.db_connection_ok = False
        # Validate the database configuration.
        try:
            self.app_config.database.validate()
        except AppConfigError as e:
            self.testResultLabel.setText(str(e))
            return
        if self.app_config.database.type == DatabaseSection.TYPE_SQLITE:
            # No need to check that database exists before testing connection
            # for SQLite.
            db_exists = True
            self.db_connection_ok = sqlite_connection_is_ok(
                                            self.app_config.database.filename)
        elif self.app_config.database.type == DatabaseSection.TYPE_MYSQL:
            db_exists = mysql_database_exists(
                                          self.app_config.database.username, 
                                          self.app_config.database.password, 
                                          self.app_config.database.host, 
                                          self.app_config.database.name)
            if db_exists:
                self.db_connection_ok = mysql_connection_is_ok(
                                          self.app_config.database.username, 
                                          self.app_config.database.password, 
                                          self.app_config.database.host, 
                                          self.app_config.database.name)
        result = []
        if db_exists and self.db_connection_ok:
            result.append("Database connection test passed.")
        if not db_exists:
            result.append("Database '{}' does not exist.".format(
                                                self.app_config.database.name))
        if not self.db_connection_ok:
            result.append("Could not connect to database '{}'.".format(
                                                self.app_config.database.name))
        self.testResultLabel.setText(" ".join(result))
        self.emit(SIGNAL("completeChanged()"))
    
    
class ConfigWizardPage3(QWizardPage, ui_configwizardp3.Ui_wizardPage3):
    
    def __init__(self, app_config, lock=True, parent=None):
        super().__init__(parent=parent)
        self.app_config = app_config
        self.lock = lock
        self.valid = False
        self._update_data_validity()
        self.setupUi(self)
        
    def initializePage(self):
        self._populate_decimal_places_combo_box()
        self._initialise_widgets_using_config()
    
    def _populate_decimal_places_combo_box(self):
        self.locCurrencyDecPlacesComboBox.blockSignals(True)
        for decimal_places in LocaleSection.VALID_CURRENCY_DECIMAL_PLACES:
            self.locCurrencyDecPlacesComboBox.addItem(decimal_places)
        self.locCurrencyDecPlacesComboBox.blockSignals(False)
    
    def _initialise_widgets_using_config(self):
        self.coNameLineEdit.setText(
                                self.app_config.company.name)
        self.poPrefixLineEdit.setText(
                                self.app_config.purchaseorder.number_prefix)
        self.locCurrencySymbolLineEdit.setText(
                                self.app_config.locale.currency_symbol)
        if self.app_config.locale.currency_decimal_places in \
            LocaleSection.VALID_CURRENCY_DECIMAL_PLACES:
            self.locCurrencyDecPlacesComboBox.setCurrentIndex(
                    self.locCurrencyDecPlacesComboBox.findText(
                        str(self.app_config.locale.currency_decimal_places)))
        else:
            self.locCurrencyDecPlacesComboBox.setCurrentIndex(0)
        self.locTaxNameLineEdit.setText(
                                self.app_config.locale.tax_name)
        if self.lock:
            self.coNameLineEdit.setEnabled(False)
            self.poPrefixLineEdit.setEnabled(False)
            self.locCurrencySymbolLineEdit.setEnabled(False)
            self.locCurrencyDecPlacesComboBox.setEnabled(False)
            self.locTaxNameLineEdit.setEnabled(False)
    
    def cleanupPage(self):
        pass
    
    def validatePage(self):
        # Save the config file.
        self.app_config.write()
        return True
    
    def isComplete(self):
        return self.valid
    
    @pyqtSignature("")        
    def on_coNameLineEdit_editingFinished(self):
        self.app_config.company.name = self.coNameLineEdit.text()
        self._update_data_validity()
        
    def _update_data_validity(self):
        try:
            self.app_config.company.validate()
            self.app_config.purchaseorder.validate()
            self.app_config.locale.validate()
            self.valid = True
            self.emit(SIGNAL("completeChanged()"))
        except  AppConfigError:
            self.valid = False
            self.emit(SIGNAL("completeChanged()"))
            
    @pyqtSignature("")        
    def on_poPrefixLineEdit_editingFinished(self):
        self.app_config.purchaseorder.number_prefix = \
                                    self.poPrefixLineEdit.text()
        self._update_data_validity()
                                            
    @pyqtSignature("")
    def on_locCurrencySymbolLineEdit_editingFinished(self):
        self.app_config.locale.currency_symbol = \
                                    self.locCurrencySymbolLineEdit.text()
        self._update_data_validity()
                                             
    @pyqtSignature("const QString&")
    def on_locCurrencyDecPlacesComboBox_currentIndexChanged(self, text):
        self.app_config.locale.currency_decimal_places = \
                            self.locCurrencyDecPlacesComboBox.currentText()
        self._update_data_validity()
                                    
    @pyqtSignature("")
    def on_locTaxNameLineEdit_editingFinished(self):
        self.app_config.locale.tax_name = self.locTaxNameLineEdit.text()
        self._update_data_validity()
    
    
class ConfigWizardPage4(QWizardPage, ui_configwizardp4.Ui_wizardPage4):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.user_config = None
        self.company = None
        self.valid = False
        self.setupUi(self)
        
    def initializePage(self):
        self.user_config = self.parent.get_user_config(self)
        self.company = CompanySettings()
        self.company.load_from_db_record(self.user_config.db_record)
        self._update_data_validity()
        self._initialise_widgets_using_config()
    
    def _initialise_widgets_using_config(self):
        self.coPhysicalAddressPlainTextEdit.setPlainText(
                                self.user_config.company.physical_address)
        self.coGpsCoordsLineEdit.setText(
                                self.user_config.company.gps_coordinates)
        self.coPostalAddressPlainTextEdit.setPlainText(
                                self.user_config.company.postal_address)
        self.coTelephoneLineEdit.setText(
                                self.user_config.company.phone_number)
        self.coFaxLineEdit.setText(
                                self.user_config.company.fax_number)
        self.coEmailLineEdit.setText(
                                self.user_config.company.email_address)
        self.coWebLineEdit.setText(
                                self.user_config.company.web_address)
        self.coSignatoryLineEdit.setText(
                                self.user_config.company.signatory_name)
        self.coSignatureFileLineEdit.setText(
                                self.user_config.company.signature_filename)
        self.coLogoFileLineEdit.setText(
                                self.user_config.company.logo_filename)
    
    def cleanupPage(self):
        pass
    
    def validatePage(self):
        self.user_config.update_company_settings(self.company)
        self.parent.set_user_config(self, self.user_config)
        return True
    
    def isComplete(self):
        return self.valid
    
    def _update_data_validity(self):
        self.user_config.update_company_settings(self.company)
        try:
            self.user_config.new_company.validate()
            self.valid = True
            self.emit(SIGNAL("completeChanged()"))
        except  UserConfigError:
            self.valid = False
            self.emit(SIGNAL("completeChanged()"))
    
    @pyqtSignature("")
    def on_coPhysicalAddressPlainTextEdit_textChanged(self):
        self.company.physical_address = self.coPhysicalAddressPlainTextEdit.\
                                                toPlainText()
        self._update_data_validity()
    
    @pyqtSignature("")
    def on_coGpsCoordsLineEdit_editingFinished(self):
        self.company.gps_coordinates = self.coGpsCoordsLineEdit.text()
        self._update_data_validity()
    
    @pyqtSignature("")
    def on_coPostalAddressPlainTextEdit_textChanged(self):
        self.company.postal_address = self.coPostalAddressPlainTextEdit.\
                                                toPlainText()
        self._update_data_validity()
    
    @pyqtSignature("")
    def on_coTelephoneLineEdit_editingFinished(self):
        self.company.phone_number = self.coTelephoneLineEdit.text()
        self._update_data_validity()
    
    @pyqtSignature("")
    def on_coFaxLineEdit_editingFinished(self):
        self.company.fax_number = self.coFaxLineEdit.text()
        self._update_data_validity()
    
    @pyqtSignature("")
    def on_coEmailLineEdit_editingFinished(self):
        self.company.email_address = self.coEmailLineEdit.text()
        self._update_data_validity()
    
    @pyqtSignature("")
    def on_coWebLineEdit_editingFinished(self):
        self.company.web_address = self.coWebLineEdit.text()
        self._update_data_validity()
    
    @pyqtSignature("")
    def on_coSignatoryLineEdit_editingFinished(self):
        self.company.signatory_name = self.coSignatoryLineEdit.text()
        self._update_data_validity()
                      
    @pyqtSignature("")                                            
    def on_coSignatureFileLineEdit_editingFinished(self):
        self.company.signature_filename = self.coSignatureFileLineEdit.text()
        self._update_data_validity()
                                            
    @pyqtSignature("")                                            
    def on_coLogoFileLineEdit_editingFinished(self):
        self.company.logo_filename = self.coLogoFileLineEdit.text()
        self._update_data_validity()
    
    @pyqtSignature("")
    def on_coSignatureFilePushButton_clicked(self):
        self.company.signature_filename = QFileDialog.getOpenFileName(
                                                self, 
                                                caption="Signature Image File", 
                                                filter="Images (*.png *.jpg)")
        self.coSignatureFileLineEdit.setText(self.company.signature_filename)
        self._update_data_validity()
    
    @pyqtSignature("")
    def on_coLogoFilePushButton_clicked(self):
        self.company.logo_filename = QFileDialog.getOpenFileName(
                                            self, 
                                            caption="Company Logo Image File", 
                                            filter="Images (*.png *.jpg)")
        self.coLogoFileLineEdit.setText(self.company.logo_filename)
        self._update_data_validity()
                                            
    
class ConfigWizardPage5(QWizardPage, ui_configwizardp5.Ui_wizardPage5):
    
    def __init__(self, app_config, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.app_config = app_config
        self.user_config = None
        self.purchaseorder = None
        self.locale = None
        self.valid = False
        self.setupUi(self)
        
    def initializePage(self):
        self.user_config = self.parent.get_user_config(self)
        self.purchaseorder = PurchaseOrderSettings()
        self.purchaseorder.load_from_db_record(self.user_config.db_record)
        self.locale = LocaleSettings()
        self.locale.load_from_db_record(self.user_config.db_record)
        self._update_data_validity()
        self._populate_combo_boxes()
        self._initialise_widgets_using_config()
    
    def _populate_combo_boxes(self):
        self.poDefaultPaymentTermsComboBox.blockSignals(True)
        self.poDefaultOrderStatusComboBox.blockSignals(True)
        for payment_terms in PO_PAYMENT_TERMS:
            self.poDefaultPaymentTermsComboBox.addItem(payment_terms)
        for order_status in PO_ORDER_STATUSUS:
            self.poDefaultOrderStatusComboBox.addItem(order_status)
        self.poDefaultPaymentTermsComboBox.blockSignals(False)
        self.poDefaultOrderStatusComboBox.blockSignals(False)
    
    def _initialise_widgets_using_config(self):
        self.poDefaultPaymentTermsComboBox.setCurrentIndex(
                    self.poDefaultPaymentTermsComboBox.findText(
                        self.user_config.purchaseorder.default_payment_terms))
        self.poDefaultOrderStatusComboBox.setCurrentIndex(
                    self.poDefaultOrderStatusComboBox.findText(
                        self.user_config.purchaseorder.default_order_status))
        self.locTaxRateLineEdit.setText(
                                    str(self.user_config.locale.tax_rate))
    
    def cleanupPage(self):
        pass
    
    def validatePage(self):
        self.user_config.update_purchaseorder_settings(self.purchaseorder)
        self.user_config.update_locale_settings(self.locale)
        self.parent.set_user_config(self, self.user_config)
        self.parent.save_user_config(self)
        return True
    
    def isComplete(self):
        return self.valid
    
    def _update_data_validity(self):
        self.user_config.update_purchaseorder_settings(self.purchaseorder)
        self.user_config.update_locale_settings(self.locale)
        try:
            self.user_config.new_purchaseorder.validate()
            self.user_config.new_locale.validate()
            self.valid = True
            self.emit(SIGNAL("completeChanged()"))
        except  UserConfigError:
            self.valid = False
            self.emit(SIGNAL("completeChanged()"))
    
    @pyqtSignature("const QString&")
    def on_poDefaultPaymentTermsComboBox_currentIndexChanged(self, text):
        self.purchaseorder.default_payment_terms = text
        self._update_data_validity()
        
    @pyqtSignature("const QString&")
    def on_poDefaultOrderStatusComboBox_currentIndexChanged(self, text):
        self.purchaseorder.default_order_status = text
        self._update_data_validity()
        
    @pyqtSignature("")
    def on_locTaxRateLineEdit_editingFinished(self):
        try:
            decimal_rate = Decimal(self.locTaxRateLineEdit.text())
            self.locale.tax_rate = decimal_rate
        except ValueError:
            self.locale.tax_rate = Decimal("0.0")
            self.locTaxRateLineEdit.setText(
                                    str(self.locale.tax_rate))
        self._update_data_validity()
        