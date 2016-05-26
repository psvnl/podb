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

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, Integer, Text
from sqlabase import Base
from dbfieldsizes import (COMPANY_NAME_STRING_LENGTH, PERSON_NAME_STRING_LENGTH,
                          EMAIL_ADDRESS_STRING_LENGTH, TAX_NUMBER_STRING_LENGTH,
                          PHONE_NUMBER_STRING_LENGTH)


class Supplier(Base):
    '''SQLAlchemy class used to map to the supplier table in the database.
    '''
    __tablename__ = "supplier"
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False)
    
    company_name = Column(String(COMPANY_NAME_STRING_LENGTH), nullable=False)
    
    contact_person_name = Column(String(PERSON_NAME_STRING_LENGTH))
    
    phone_number = Column(String(PHONE_NUMBER_STRING_LENGTH))
    
    fax_number = Column(String(PHONE_NUMBER_STRING_LENGTH))
    
    email_address = Column(String(EMAIL_ADDRESS_STRING_LENGTH))
    
    tax_number = Column(String(TAX_NUMBER_STRING_LENGTH))
    
    address = Column(Text, nullable=False)
    
    archived = Column(Boolean, nullable=False)
    
    # Relationships
    product = relationship("Product", back_populates="supplier")
    
    purchase_order = relationship("PurchaseOrder", back_populates="supplier")
    
    def __repr__(self):
        return ("<Supplier(id='%s',"
                "company_name='%s',"
                "contact_person_name='%s',"
                "phone_number='%s',"
                "fax_number='%s',"
                "email_address='%s',"
                "tax_number='%s',"
                "address='%s')>") % (str(self.id), 
                                     self.company_name, 
                                     self.contact_person_name, 
                                     self.phone_number, 
                                     self.fax_number, 
                                     self.email_address, 
                                     self.tax_number, 
                                     self.address)
