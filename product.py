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

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Boolean
from sqlabase import Base
from dbfieldsizes import PART_NUMBER_STRING_LENGTH, DESCRIPTION_STRING_LENGTH


class Product(Base):
    '''SQLAlchemy class used to map to the product table in the database.
    '''
    __tablename__ = "product"
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False)
    
    part_number = Column(String(PART_NUMBER_STRING_LENGTH), nullable=False)
    
    product_description = Column(String(DESCRIPTION_STRING_LENGTH))
    
    current_price = Column(Integer, nullable=False)
    
    current_discount = Column(Integer, nullable=False)
    
    supplier_id = Column(Integer, ForeignKey("supplier.id"), 
                         nullable=False)
    
    archived = Column(Boolean, nullable=False)
    
    # Relationships
    supplier = relationship("Supplier", 
                            back_populates="product")
    
    # The cascade property is set to "all, delete-orphan" because a delete of a 
    # product record must result in a delete of the relevant 
    # purchase_order_product records. 
    purchase_orders = relationship("PurchaseOrderProduct", 
                                   back_populates="product",
                                   cascade="all, delete-orphan")
    
    def __repr__(self):
        return ("<Product(id='%s',"
                "part_number='%s',"
                "product_description='%s',"
                "current_price='%s',"
                "current_discount='%s',"
                "supplier_id='%s')>") % (str(self.id), 
                                         self.part_number, 
                                         self.product_description, 
                                         self.current_price, 
                                         self.current_discount, 
                                         str(self.supplier_id))
