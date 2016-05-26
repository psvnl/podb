'''
Created on 17 May 2016

@author: Paulo Leal
'''

from copy import copy
import datetime
from decimal import Decimal
import os

from conversions import percentage_int_to_decimal, percentage_decimal_to_int
from purchaseorder import PO_ORDER_STATUSUS, PO_PAYMENT_TERMS
from userconfig import UserConfig


class UserConfigError(Exception):
    '''Raised when an error is found in the user config data.
    '''
    pass


def _verify_setting_is_not_value(setting_name, setting_var, value):
    if setting_var == value:
        _raise_config_setting_error(setting_name, value)

def _verify_setting_is_not_blank(setting_name, setting_var):
    _verify_setting_is_not_value(setting_name, setting_var, "")
    if setting_var.isspace():
        _raise_config_setting_error(setting_name, "blank")

def _raise_config_setting_error(setting_name, value, extra_info=""):
    raise UserConfigError(("Invalid config option: "
                           "{} was: {}.\n\n{}").format(setting_name, 
                                                       value,
                                                       extra_info))


class CompanySettings(object):
    '''A class representing the user settings related to the company.
    '''
    
    def __init__(self):
        '''Initialises the CompanySettings object.
        
        All attributes are set to empty strings.
        '''
        self.physical_address = ""
        self.gps_coordinates = ""
        self.postal_address = ""
        self.phone_number = ""
        self.fax_number = ""
        self.email_address = ""
        self.web_address = ""
        self.signatory_name = ""
        self.signature_filename = ""
        self.logo_filename = ""
        
    def load_from_db_record(self, db_record):
        '''Load the CompanySettings object with values from a database record 
        (UserConfig object).
        
        Copies each of the attributes of the UserConfig object to the 
        corresponding attributes in the CompanySettings object.
        
        Args:
        :param db_record: The user config database record.
        :type db_record: userconfig.UserConfig
        '''
        if db_record:
            self.physical_address = db_record.company_physical_address
            self.gps_coordinates = db_record.company_gps_coordinates
            self.postal_address = db_record.company_postal_address
            self.phone_number = db_record.company_phone_number
            self.fax_number = db_record.company_fax_number
            self.email_address = db_record.company_email_address
            self.web_address = db_record.company_web_address
            self.signatory_name = db_record.company_signatory_name
            self.signature_filename = db_record.company_signature_filename
            self.logo_filename = db_record.company_logo_filename
            
    def validate(self):
        _verify_setting_is_not_blank("company physical address", 
                                     self.physical_address)
        _verify_setting_is_not_blank("company postal address", 
                                     self.postal_address)
        _verify_setting_is_not_blank("company phone number", 
                                     self.phone_number)
        _verify_setting_is_not_blank("signatory name", 
                                     self.signatory_name)
        if self.signature_filename != "":
            if not os.path.exists(self.signature_filename):
                raise UserConfigError("Invalid config option: "
                                      "The signature file does not exist.")
        if self.logo_filename != "":
            if not os.path.exists(self.logo_filename):
                raise UserConfigError("Invalid config option: "
                                      "The company logo file does not exist.")
        
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __ne__(self, other):
        return not self.__dict__ == other.__dict__
    
    def __str__(self):
        return str(self.__dict__)


class PurchaseOrderSettings(object):
    '''A class representing the user settings related to the purchase orders.
    '''
    
    def __init__(self):
        '''Initialises the PurchaseOrderSettings object.
        
        All attributes are set to default values.
        '''
        self.default_payment_terms = PO_PAYMENT_TERMS[2]    # Pay in 30 days
        self.default_order_status = PO_ORDER_STATUSUS[0]    # Draft

    def load_from_db_record(self, db_record):
        '''Load the PurchaseOrderSettings object with values from a database 
        record (UserConfig object).
        
        Copies each of the attributes of the UserConfig object to the 
        corresponding attributes in the PurchaseOrderSettings object.
        
        Args:
        :param db_record: The user config database record.
        :type db_record: userconfig.UserConfig
        '''
        if db_record:
            self.default_payment_terms = db_record.default_payment_terms
            self.default_order_status = db_record.default_order_status
            
    def validate(self):
        if self.default_payment_terms not in PO_PAYMENT_TERMS:
            _raise_config_setting_error("default payment terms", 
                                        self.default_payment_terms)
        if self.default_order_status not in PO_ORDER_STATUSUS:
            _raise_config_setting_error("default order status", 
                                        self.default_order_status)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__dict__ == other.__dict__
    
    def __str__(self):
        return str(self.__dict__)
    

class LocaleSettings(object):
    '''A class representing the user settings related to the locale.
    '''
    
    def __init__(self):
        '''Initialises the PurchaseOrderSettings object.
        
        The tax rate attribute is set to zero.
        '''
        self.tax_rate = Decimal("0.0") 

    def load_from_db_record(self, db_record):
        '''Load the LocaleSettings object with values from a database 
        record (UserConfig object).
        
        Copies each of the attributes of the UserConfig object to the 
        corresponding attributes in the LocaleSettings object.
        
        Args:
        :param db_record: The user config database record.
        :type db_record: userconfig.UserConfig
        '''
        if db_record:
            self.tax_rate = percentage_int_to_decimal(db_record.tax_rate)

    def validate(self):
        try:
            percentage_decimal_to_int(self.tax_rate)
        except ValueError as e:
            _raise_config_setting_error("tax rate", self.tax_rate, str(e))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.__dict__)
        

class UserConfigReader(object):
    '''A class that provides read-only access to the latest user settings 
    loaded from the database.
    
    The class should not be instantiated for long, to avoid recent changes from 
    being missed. Instantiate it just before it is used, i.e., just before the 
    user config is read.  
    '''
    
    def __init__(self, session):
        '''Initialises the UserConfigReader object.
        
        The config date and time is initialised to None, and empty instances of
        CompanySettings, PurchaseOrderSettings and LocaleSettings are created.
        Then the latest UserConfig record is queried from the database, and is
        used to initialise the config date and time, and the CompanySettings, 
        PurchaseOrderSettings and LocaleSettings objects.
        
        If all of the above works, then the config_valid attribute is set to 
        True. Otherwise it is set to False.
        
        Args:
        :param session: The SQLAlchemy session in use. 
        :type session: Session object (the class created by the call to  
            :func:`sessionmaker` in :mod:`sqlasession`).
        '''
        self.config_date_time = None
        self.company = CompanySettings()
        self.purchaseorder = PurchaseOrderSettings()
        self.locale = LocaleSettings()
        self.config_valid = False
        self.db_record = None
        user_configs = session.query(UserConfig).all()
        if user_configs:
            self.db_record = user_configs[-1]
            self.config_date_time = self.db_record.created_date_time
            self.company.load_from_db_record(self.db_record)
            self.purchaseorder.load_from_db_record(self.db_record)
            self.locale.load_from_db_record(self.db_record)
            self.config_valid = True
            
    
class UserConfigEditor(UserConfigReader):
    '''A class that provides read access to the latest user settings loaded 
    from the database, and the ability to write new settings to the database.
    '''
    
    def __init__(self, session):
        '''Initialises the UserConfigEditor object.
        
        Copies of the CompanySettings, PurchaseOrderSettings and LocaleSettings
        objects are created ("new" objects), which are later used to determine 
        if the settings have changed. 
        
        Args:
        :param session: The SQLAlchemy session in use. 
        :type session: Session object (the class created by the call to  
            :func:`sessionmaker` in :mod:`sqlasession`).
        '''
        super().__init__(session)
        self.new_company = copy(self.company)
        self.new_purchaseorder = copy(self.purchaseorder)
        self.new_locale = copy(self.locale)
        self._dirty = False
        
    def update_company_settings(self, settings):
        '''Update the company settings.
        
        Copies the attributes in the supplied CompanySettings object to the 
        internal "new" CompanySettings object if there is a difference between 
        the two objects. 
        
        Args:
        :param settings: The updated company settings.
        :type settings: CompanySettings
        '''
        if settings != self.new_company:
            self.new_company.physical_address = settings.physical_address
            self.new_company.gps_coordinates = settings.gps_coordinates
            self.new_company.postal_address = settings.postal_address
            self.new_company.phone_number = settings.phone_number
            self.new_company.fax_number = settings.fax_number
            self.new_company.email_address = settings.email_address
            self.new_company.web_address = settings.web_address
            self.new_company.signatory_name = settings.signatory_name
            self.new_company.signature_filename = settings.signature_filename
            self.new_company.logo_filename = settings.logo_filename
            self._dirty = True
            
    def update_purchaseorder_settings(self, settings):
        '''Update the purchase order settings.
        
        Copies the attributes in the supplied PurchaseOrderSettings object to 
        the internal "new" PurchaseOrderSettings object if there is a difference 
        between the two objects. 
        
        :param settings: The updated purchase order settings.
        :type settings: PurchaseOrderSettings
        '''
        if settings != self.new_purchaseorder:
            self.new_purchaseorder.default_payment_terms = \
                settings.default_payment_terms
            self.new_purchaseorder.default_order_status = \
                settings.default_order_status
            self._dirty = True
            
    def update_locale_settings(self, settings):
        '''Update the locale settings.
        
        Copies the attributes in the supplied LocaleSettings object to 
        the internal "new" LocaleSettings object if there is a difference 
        between the two objects. 
        
        :param settings: The updated purchase order settings.
        :type settings: LocaleSettings
        '''
        if settings != self.new_locale:
            self.new_locale.tax_rate = settings.tax_rate
            self._dirty = True
        
    def validate(self):
        self.new_company.validate()
        self.new_purchaseorder.validate()
        self.new_locale.validate()
            
    def save(self, session):
        '''Save the updated user settings to a new record in the database if
        the settings have changed.
        '''
        if self._dirty:
            user_config = UserConfig()
            # Timestamp
            user_config.created_date_time = datetime.datetime.now()
            # Company settings
            user_config.company_physical_address = \
                self.new_company.physical_address
            user_config.company_gps_coordinates = \
                self.new_company.gps_coordinates
            user_config.company_postal_address = \
                self.new_company.postal_address
            user_config.company_phone_number = self.new_company.phone_number
            user_config.company_fax_number = self.new_company.fax_number
            user_config.company_email_address = self.new_company.email_address
            user_config.company_web_address = self.new_company.web_address
            user_config.company_signatory_name = \
                self.new_company.signatory_name
            user_config.company_signature_filename = \
                self.new_company.signature_filename
            user_config.company_logo_filename = self.new_company.logo_filename
            # Purchase order settings
            user_config.default_payment_terms = \
                self.new_purchaseorder.default_payment_terms
            user_config.default_order_status = \
                self.new_purchaseorder.default_order_status
            # Locale settings. Assumes that the validate method has been called.
            user_config.tax_rate = percentage_decimal_to_int(
                                                    self.new_locale.tax_rate)
            # Commit
            session.add(user_config)
            session.commit()
            self._dirty = False
            
            
if __name__ == '__main__':
    from sqlalchemy import Column, String, create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.types import Numeric, Text, Integer, DateTime, Enum
    
    engine = create_engine("sqlite:///test_userconfigmodel.db", echo=True)
    
    Base = declarative_base()
    
    _COMPANY_NAME_STRING_LENGTH = 50
    _DESCRIPTION_STRING_LENGTH = 255
    _EMAIL_ADDRESS_STRING_LENGTH = 100
    _FILENAME_STRING_LENGTH = 255
    _GPS_COORDINATES_STRING_LENGTH = 100
    _ORDER_NUMBER_STRING_LENGTH = 8
    _PART_NUMBER_STRING_LENGTH = 100
    _PERSON_NAME_STRING_LENGTH = 100
    _PHONE_NUMBER_STRING_LENGTH = 20
    _PROJECT_CODE_STRING_LENGTH = 6
    _TAX_NUMBER_STRING_LENGTH = 50
    _WEB_ADDRESS_STRING_LENGTH = 100
    # The statuses that an order may be in. The enum used in the database 
    # should be composed of this dictionary's keys.
    _ORDER_STATUSUS = {
                       "Draft": "Order still to be placed",
                       "Placed": "Order has been placed",
                       "Received": "Order has been completed",
                       "Partial": "Some goods have been received, but not all",
                       "Cancelled": "Order has been cancelled"
                       }
    
    # The payment terms that are allowed. The enum used in the database should 
    # be composed of this tuple.
    _PAYMENT_TERMS = [
                      "Pay in advance",
                      "Pay in 7 days",
                      "Pay in 30 days",
                      "Pay in 60 days",
                      "Cash on delivery"
                      ]
    payment_terms = _PAYMENT_TERMS
    payment_terms.sort()
    order_statuses = []
    for order_status in _ORDER_STATUSUS.keys():
        order_statuses.append(order_status)
    order_statuses.sort()
    
    class UserConfig(Base):
        '''SQLAlchemy class used to map to the configuration table in the database.
        '''
        __tablename__ = "user_config"
        
        # Columns
        id = Column(Integer, primary_key=True, autoincrement=True,
                    nullable=False)
        
        created_date_time = Column(DateTime, nullable=False)
        
        company_physical_address = Column(Text, nullable=False)
        
        company_gps_coordinates = Column(String(_GPS_COORDINATES_STRING_LENGTH))
        
        company_postal_address = Column(Text, nullable=False)
        
        company_phone_number = Column(String(_PHONE_NUMBER_STRING_LENGTH), 
                                      nullable=False)
        
        company_fax_number = Column(String(_PHONE_NUMBER_STRING_LENGTH))
        
        company_email_address = Column(String(_EMAIL_ADDRESS_STRING_LENGTH))
        
        company_web_address = Column(String(_WEB_ADDRESS_STRING_LENGTH))
        
        company_signatory_name = Column(String(_PERSON_NAME_STRING_LENGTH), 
                                        nullable=False)
        
        company_signature_filename = Column(String(_FILENAME_STRING_LENGTH))
        
        company_logo_filename = Column(String(_FILENAME_STRING_LENGTH))
        
        default_payment_terms = Column(Enum(
                                        *payment_terms), 
                                       nullable=False)
        
        default_order_status = Column(Enum(
                                        *order_statuses), 
                                      nullable=False)
        
        tax_rate = Column(Integer, nullable=False)
        
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=True)
    
    session = Session()
    
    reader = UserConfigReader(session)
    print("User Config Validity: " + str(reader.config_valid))
    if reader.config_valid:
        print(str(reader.config_date_time))
        print(str(reader.company))
        print(str(reader.purchaseorder))
        print(str(reader.locale))
    else:
        co_settings = CompanySettings()
        co_settings.physical_address = "123 Fourth Rd\nAlberton\n2009"
        co_settings.postal_address = "PO Box 123\nAlberton\2109"
        co_settings.phone_number = "011 876 6554"
        co_settings.fax_number = "011 876 6555"
        co_settings.email_address = "albert.marais@foxtrot.co.za"
        co_settings.signatory_name = "Albert E. Marais"
        co_settings.signature_filename = r"C:\POdB\images\signature.png"
        po_settings = PurchaseOrderSettings()
        po_settings.default_payment_terms = "Pay in 30 days"
        po_settings.default_order_status = "Draft"
        loc_settings = LocaleSettings()
        loc_settings.tax_rate = 14
        editor = UserConfigEditor(session)
        editor.update_company_settings(co_settings)
        editor.update_purchaseorder_settings(po_settings)
        editor.update_locale_settings(loc_settings)
        editor.save(session)
        session.close()