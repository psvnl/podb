'''
Created on 18 May 2016

@author: Paulo Leal
'''

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Text, DateTime, Enum, Numeric
from sqlabase import Base
from dbfieldsizes import (PERSON_NAME_STRING_LENGTH, FILENAME_STRING_LENGTH,
                          PHONE_NUMBER_STRING_LENGTH, WEB_ADDRESS_STRING_LENGTH,
                          EMAIL_ADDRESS_STRING_LENGTH,
                          GPS_COORDINATES_STRING_LENGTH)
from purchaseorder import PO_PAYMENT_TERMS, PO_ORDER_STATUSUS


class UserConfig(Base):
    '''SQLAlchemy class used to map to the configuration table in the database.
    '''
    __tablename__ = "user_config"
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False)
    
    created_date_time = Column(DateTime, nullable=False)
    
    company_physical_address = Column(Text, nullable=False)
    
    company_gps_coordinates = Column(String(GPS_COORDINATES_STRING_LENGTH))
    
    company_postal_address = Column(Text, nullable=False)
    
    company_phone_number = Column(String(PHONE_NUMBER_STRING_LENGTH), 
                                  nullable=False)
    
    company_fax_number = Column(String(PHONE_NUMBER_STRING_LENGTH))
    
    company_email_address = Column(String(EMAIL_ADDRESS_STRING_LENGTH))
    
    company_web_address = Column(String(WEB_ADDRESS_STRING_LENGTH))
    
    company_signatory_name = Column(String(PERSON_NAME_STRING_LENGTH), 
                                    nullable=False)
    
    company_signature_filename = Column(String(FILENAME_STRING_LENGTH))
    
    company_logo_filename = Column(String(FILENAME_STRING_LENGTH))
    
    default_payment_terms = Column(Enum(*PO_PAYMENT_TERMS), nullable=False)
    
    default_order_status = Column(Enum(*PO_ORDER_STATUSUS), nullable=False)
    
    tax_rate = Column(Integer, nullable=False)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder",
                                  back_populates="user_config")
    
    