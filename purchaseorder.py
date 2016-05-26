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
from sqlalchemy.types import Integer, Date, Text, Enum
from sqlabase import Base
from dbfieldsizes import (GPS_COORDINATES_STRING_LENGTH, 
                          ORDER_NUMBER_STRING_LENGTH)

# The payment terms that are allowed.
PO_PAYMENT_TERMS = [
                    "Pay in advance",
                    "Pay in 7 days",
                    "Pay in 30 days",
                    "Pay in 60 days",
                    "Cash on delivery"
                    ]

# The statuses that an order may be in. 
PO_ORDER_STATUSUS = [
                     "Draft",       # Order still to be placed
                     "Placed",      # Order has been placed
                     "Received",    # Order has been completed
                     "Partial",     # Some goods received, but not all
                     "Cancelled"    # Order has been cancelled
                     ]


class PurchaseOrder(Base):
    '''SQLAlchemy class used to map to the purchase_order table in the database.
    '''
    __tablename__ = "purchase_order"
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False)
    
    order_number = Column(String(ORDER_NUMBER_STRING_LENGTH), nullable=False)
    
    order_date = Column(Date, nullable=False)
    
    delivery_address = Column(Text, nullable=False)
    
    delivery_address_gps_coordinates = Column(String(
                                                GPS_COORDINATES_STRING_LENGTH))
    
    delivery_date = Column(Date, nullable=False)
    
    # The asterisk unpacks the strings in the list into arguments for the Enum
    # initialiser. 
    payment_terms = Column(Enum(*PO_PAYMENT_TERMS), nullable=False)
    
    # The asterisk unpacks the strings in the list into arguments for the Enum
    # initialiser.
    order_status = Column(Enum(*PO_ORDER_STATUSUS), nullable=False)
    
    notes = Column(Text)
    
    total_excluding_tax = Column(Integer, nullable=False)
    
    total_tax = Column(Integer, nullable=False)
    
    total_including_tax = Column(Integer, nullable=False)
    
    project_id = Column(Integer, ForeignKey("project.id"))
    
    supplier_id = Column(Integer, ForeignKey("supplier.id"), 
                         nullable=False)
    
    user_config_id = Column(Integer, ForeignKey("user_config.id"), 
                            nullable=False)
    
    # Relationships
    project = relationship("Project", 
                           back_populates="purchase_order")
    
    supplier = relationship("Supplier", 
                            back_populates="purchase_order")
        
    # The cascade property is set to "all, delete-orphan" because a delete of a 
    # purchase_order record must result in a delete of the relevant 
    # purchase_order_product records.
    products = relationship("PurchaseOrderProduct", 
                            back_populates="purchase_order",
                            cascade="all, delete-orphan")
    
    user_config = relationship("UserConfig",
                               back_populates="purchase_order")
    
    def __repr__(self):
        return ("<PurchaseOrder(id='%s',"
                "order_number='%s',"
                "total_excluding_tax='%s',"
                "total_tax='%s',"
                "total_including_tax='%s',"
                "project_id='%s',"
                "supplier_id='%s')>") % (str(self.id), 
                                         self.order_number, 
                                         str(self.total_excluding_tax), 
                                         str(self.total_tax), 
                                         str(self.total_including_tax), 
                                         str(self.project_id), 
                                         str(self.supplier_id))
                