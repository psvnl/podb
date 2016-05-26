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

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from configparser import ConfigParser
from messagebox import execute_critical_msg_box 


class AppConfigStructureError(Exception):
    '''Raised when an error is found in the config file structure.
    '''
    pass

class AppConfigError(Exception):
    '''Raised when an error is found in the application config file data.
    '''
    pass


def _verify_setting_is_value(section_name, setting_name, setting_var, value):
    if setting_var != value:
        _raise_config_setting_error(section_name, setting_name, value)
        
def _verify_setting_is_not_value(section_name, setting_name, setting_var, value):
    if setting_var == value:
        _raise_config_setting_error(section_name, setting_name, value)
        
def _verify_setting_is_not_blank(section_name, setting_name, setting_var):
    _verify_setting_is_not_value(section_name, setting_name, setting_var, "")
    if setting_var.isspace():
        _raise_config_setting_error(section_name, setting_name, "blank")

def _raise_config_setting_error(section_name, setting_name, value):
    raise AppConfigError(("Invalid config setting: "
                           "{} {} was: {}.").format(section_name, 
                                                    setting_name, 
                                                    value))


class DatabaseSection(object):
    '''A class containing the data in the Database section of the application 
    config file.
    '''
    
    NAME_IN_FILE = "Database"
    
    NUM_OPTIONS = 8
    (   TYPE, 
        DRIVER, 
        FILENAME, 
        NAME, 
        USERNAME, 
        PASSWORD, 
        HOST, 
        PORT
        ) = range(NUM_OPTIONS)
    
    OPTION_NAMES_IN_FILE = {
        TYPE: "type",
        DRIVER: "driver",
        FILENAME: "filename",
        NAME: "name",
        USERNAME: "username",
        PASSWORD: "password",
        HOST: "host",
        PORT: "port"
        }
    
    TYPE_MYSQL = "mysql"
    TYPE_SQLITE = "sqlite"
    DRIVER_MYSQL = "mysqlconnector"
    
    DEFAULT = {
        OPTION_NAMES_IN_FILE[TYPE]: TYPE_MYSQL,
        OPTION_NAMES_IN_FILE[DRIVER]: DRIVER_MYSQL,
        OPTION_NAMES_IN_FILE[FILENAME]: "",
        OPTION_NAMES_IN_FILE[NAME]: "",
        OPTION_NAMES_IN_FILE[USERNAME]: "",
        OPTION_NAMES_IN_FILE[PASSWORD]: "",
        OPTION_NAMES_IN_FILE[HOST]: "127.0.0.1",
        OPTION_NAMES_IN_FILE[PORT]: ""
        }
    
    def __init__(self, section_dict):
        self.type = section_dict[self.OPTION_NAMES_IN_FILE[self.TYPE]]
        self.driver = section_dict[self.OPTION_NAMES_IN_FILE[self.DRIVER]]
        self.filename = section_dict[self.OPTION_NAMES_IN_FILE[self.FILENAME]]
        self.name = section_dict[self.OPTION_NAMES_IN_FILE[self.NAME]]
        self.username = section_dict[self.OPTION_NAMES_IN_FILE[self.USERNAME]]
        self.password = section_dict[self.OPTION_NAMES_IN_FILE[self.PASSWORD]]
        self.host = section_dict[self.OPTION_NAMES_IN_FILE[self.HOST]]
        self.port = section_dict[self.OPTION_NAMES_IN_FILE[self.PORT]]
        
    def validate(self):
        if self.type == self.TYPE_MYSQL:
            _verify_setting_is_value(self.NAME_IN_FILE, 
                                   self.OPTION_NAMES_IN_FILE[self.DRIVER],
                                   self.driver, self.DRIVER_MYSQL)
            _verify_setting_is_value(self.NAME_IN_FILE, self.FILENAME, 
                                   self.filename, "")
            _verify_setting_is_not_blank(self.NAME_IN_FILE, 
                                       self.OPTION_NAMES_IN_FILE[self.NAME], 
                                       self.name)
            _verify_setting_is_not_blank(self.NAME_IN_FILE, 
                                       self.OPTION_NAMES_IN_FILE[self.USERNAME], 
                                       self.username)
            _verify_setting_is_not_blank(self.NAME_IN_FILE, 
                                       self.OPTION_NAMES_IN_FILE[self.PASSWORD], 
                                       self.password)
            _verify_setting_is_not_blank(self.NAME_IN_FILE, 
                                       self.OPTION_NAMES_IN_FILE[self.HOST], 
                                       self.host)
        elif self.type == self.TYPE_SQLITE:
            _verify_setting_is_value(self.NAME_IN_FILE, 
                                   self.OPTION_NAMES_IN_FILE[self.DRIVER], 
                                   self.driver, "")
            _verify_setting_is_not_blank(self.NAME_IN_FILE, 
                                       self.OPTION_NAMES_IN_FILE[self.FILENAME], 
                                       self.filename)
            _verify_setting_is_value(self.NAME_IN_FILE, 
                                   self.OPTION_NAMES_IN_FILE[self.NAME], 
                                   self.name, "")
            _verify_setting_is_value(self.NAME_IN_FILE, 
                                   self.OPTION_NAMES_IN_FILE[self.PASSWORD], 
                                   self.password, "")
            _verify_setting_is_value(self.NAME_IN_FILE, 
                                   self.OPTION_NAMES_IN_FILE[self.HOST], 
                                   self.host, "")
            _verify_setting_is_value(self.NAME_IN_FILE, 
                                   self.OPTION_NAMES_IN_FILE[self.PORT], 
                                   self.port, "")
        else:
            _raise_config_setting_error(self.NAME_IN_FILE, self.TYPE, self.type)

    def get_dict(self):
        return {
            self.OPTION_NAMES_IN_FILE[self.TYPE]: self.type,
            self.OPTION_NAMES_IN_FILE[self.DRIVER]: self.driver,
            self.OPTION_NAMES_IN_FILE[self.FILENAME]: self.filename,
            self.OPTION_NAMES_IN_FILE[self.NAME]: self.name,
            self.OPTION_NAMES_IN_FILE[self.USERNAME]: self.username,
            self.OPTION_NAMES_IN_FILE[self.PASSWORD]: self.password,
            self.OPTION_NAMES_IN_FILE[self.HOST]: self.host,
            self.OPTION_NAMES_IN_FILE[self.PORT]: self.port
            }


class CompanySection(object):
    '''A class containing the data in the Company section of the application 
    config file.
    '''
    
    NAME_IN_FILE = "Company"
    
    NUM_OPTIONS = 1
    (   NAME
        ) = range(NUM_OPTIONS)
    
    OPTION_NAMES_IN_FILE = {
        NAME: "name"
        }
    
    DEFAULT = {
        OPTION_NAMES_IN_FILE[NAME]: ""
        }
    
    def __init__(self, section_dict):
        self.name = section_dict[self.OPTION_NAMES_IN_FILE[self.NAME]]
        
    def validate(self):
        _verify_setting_is_not_blank(self.NAME_IN_FILE, 
                                   self.OPTION_NAMES_IN_FILE[self.NAME], 
                                   self.name)
        
    def get_dict(self):
        return {
            self.OPTION_NAMES_IN_FILE[self.NAME]: self.name
            }


class PurchaseOrderSection(object):
    '''A class containing the data in the Purchase Order section of the 
    application config file.
    '''
    
    NAME_IN_FILE = "Purchase Order"
    
    NUM_OPTIONS = 1
    (   PREFIX
        ) = range(NUM_OPTIONS)
    
    OPTION_NAMES_IN_FILE = {
        PREFIX: "number_prefix"
        }
    
    DEFAULT = {
        OPTION_NAMES_IN_FILE[PREFIX]: "PO"
        }
    
    def __init__(self, section_dict):
        self.number_prefix = section_dict[self.OPTION_NAMES_IN_FILE[
                                                                self.PREFIX]]
        
    def validate(self):
        pass
        
    def get_dict(self):
        return {
            self.OPTION_NAMES_IN_FILE[self.PREFIX]: self.number_prefix
            } 
        
        
class LocaleSection(object):
    '''A class containing the data in the Locale section of the application 
    config file.
    '''
    
    NAME_IN_FILE = "Locale"
    
    NUM_OPTIONS = 3
    (   CURRENCY_SYMBOL,
        CURRENCY_DECIMAL_PLACES, 
        TAX_NAME 
        ) = range(NUM_OPTIONS)
    
    OPTION_NAMES_IN_FILE = {
        CURRENCY_SYMBOL: "currency_symbol",
        CURRENCY_DECIMAL_PLACES: "currency_decimal_places",
        TAX_NAME: "tax_name" 
        }
    
    DEFAULT = {
        OPTION_NAMES_IN_FILE[CURRENCY_SYMBOL]: "R",
        OPTION_NAMES_IN_FILE[CURRENCY_DECIMAL_PLACES]: "2",
        OPTION_NAMES_IN_FILE[TAX_NAME]: "VAT"
        }
    
    VALID_CURRENCY_DECIMAL_PLACES = ["0", "1", "2", "3", "4"]
    
    def __init__(self, section_dict):
        self.currency_symbol = section_dict[self.OPTION_NAMES_IN_FILE[
                                                        self.CURRENCY_SYMBOL]]
        self.currency_decimal_places = section_dict[
                                            self.OPTION_NAMES_IN_FILE[
                                                self.CURRENCY_DECIMAL_PLACES]]
        self.tax_name = section_dict[self.OPTION_NAMES_IN_FILE[self.TAX_NAME]]
        
    def validate(self):
        _verify_setting_is_not_blank(
                                self.NAME_IN_FILE, 
                                self.OPTION_NAMES_IN_FILE[self.CURRENCY_SYMBOL], 
                                self.currency_symbol)
        _verify_setting_is_not_blank(
                                self.NAME_IN_FILE, 
                                self.OPTION_NAMES_IN_FILE[
                                                self.CURRENCY_DECIMAL_PLACES], 
                                self.currency_decimal_places)
        if self.currency_decimal_places not in \
            self.VALID_CURRENCY_DECIMAL_PLACES:
            _raise_config_setting_error(self.NAME_IN_FILE, 
                                      self.OPTION_NAMES_IN_FILE[
                                                self.CURRENCY_DECIMAL_PLACES], 
                                      self.currency_decimal_places)
        _verify_setting_is_not_blank(
                                self.NAME_IN_FILE, 
                                self.OPTION_NAMES_IN_FILE[self.TAX_NAME], 
                                self.tax_name)
            
    def get_dict(self):
        return {
            self.OPTION_NAMES_IN_FILE[self.CURRENCY_SYMBOL]: \
                                                      self.currency_symbol,
            self.OPTION_NAMES_IN_FILE[self.CURRENCY_DECIMAL_PLACES]: \
                                                self.currency_decimal_places,                                                      
            self.OPTION_NAMES_IN_FILE[self.TAX_NAME]: self.tax_name,
            } 
   

class ConfigFile(object):
    '''A class that provides access to the application config file, including 
    functionality for validating and writing to the config file.
    '''

    _CONFIG_FILE_NAME = "settings.cfg"
    
    _DEFAULT_CONFIG = {
        DatabaseSection.NAME_IN_FILE: DatabaseSection.DEFAULT,
        CompanySection.NAME_IN_FILE: CompanySection.DEFAULT,
        PurchaseOrderSection.NAME_IN_FILE: PurchaseOrderSection.DEFAULT,
        LocaleSection.NAME_IN_FILE: LocaleSection.DEFAULT
        }
    
    def __init__(self):
        self._config_parser = ConfigParser()
        
    def load(self):
        if self.exists():
            # File exists. Load config parser with its contents.
            self._config_parser.read(self._CONFIG_FILE_NAME)
            self._validate_file_structure()
            self._load_sections()
        else:
            # File does not exist. Load config parser with defaults.
            self.set_to_defaults()
        
    def set_to_defaults(self):
        self._config_parser.clear()
        for section in self._DEFAULT_CONFIG.keys():
            self._config_parser[section] = self._DEFAULT_CONFIG[section]
        self._validate_file_structure()
        self._load_sections()
        
    def exists(self):
        return os.path.exists(self._CONFIG_FILE_NAME)
    
    def _validate_file_structure(self):
        for section in self._DEFAULT_CONFIG.keys():
            if not self._config_parser.has_section(section):
                raise AppConfigStructureError(
                            ("The config file does not have "
                             "section {}.").format(section))
            section_dict = self._DEFAULT_CONFIG[section]
            for option in section_dict.keys():
                if not self._config_parser.has_option(section, option):
                    raise AppConfigStructureError(
                            ("The config file does not have "
                             "option {} in section {}.").format(option,
                                                                section))

    def _load_sections(self):
        self.database = DatabaseSection(self._config_parser[
                                            DatabaseSection.NAME_IN_FILE])
        self.company = CompanySection(self._config_parser[
                                            CompanySection.NAME_IN_FILE])
        self.purchaseorder = PurchaseOrderSection(self._config_parser[
                                            PurchaseOrderSection.NAME_IN_FILE])
        self.locale = LocaleSection(self._config_parser[
                                            LocaleSection.NAME_IN_FILE])
        
    def validate(self):
        self.database.validate()
        self.company.validate()
        self.purchaseorder.validate()
        self.locale.validate()
        
    def write(self):
        self._config_parser[DatabaseSection.NAME_IN_FILE] = \
                                                self.database.get_dict()
        self._config_parser[CompanySection.NAME_IN_FILE] = \
                                                self.company.get_dict()
        self._config_parser[PurchaseOrderSection.NAME_IN_FILE] = \
                                                self.purchaseorder.get_dict()
        self._config_parser[LocaleSection.NAME_IN_FILE] = \
                                                self.locale.get_dict()
        with open(self._CONFIG_FILE_NAME, "w") as app_config:
            self._config_parser.write(app_config)
        
        
def show_error_config_file_structure(exception):
    execute_critical_msg_box("Config Validation Error", 
                             ("There were errors in the structure of the "
                              "config file. The file has been reset to "
                              "defaults. The configuration wizard must now "
                              "be run.\n\n{}").format(str(exception)), 
                             QMessageBox.Ok)
    
def show_error_config_file_setting():
    execute_critical_msg_box("Config Validation Error", 
                             ("There are errors in the config file. "
                              "The configuration wizard must now be run."), 
                             QMessageBox.Ok)

def show_error_no_config_file():
    execute_critical_msg_box("Config Validation Error", 
                             ("A config file was not found. "
                              "The configuration wizard must now be run."), 
                             QMessageBox.Ok)
    
# Read and validate the configuration file.
app_config = ConfigFile()
app_config_ok = False
if app_config.exists():
    try:
        app_config.load()
        app_config.validate()
        # The config file is valid. The main window may be started.
        app_config_ok = True
    except AppConfigStructureError as e:
        show_error_config_file_structure(e)
        app_config.set_to_defaults()
        # The config file structure was invalid and was set to defaults.
        # The config dialog must be run.
    except AppConfigError as e:
        show_error_config_file_setting()
        # The config file had an invalid setting.
        # The config dialog must be run. 
else:
    show_error_no_config_file()
    app_config.set_to_defaults()
    # The config file was not found. A default config file has been created.
    # The config dialog must be run.