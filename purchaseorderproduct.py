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

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Numeric, Integer
from sqlabase import Base


class PurchaseOrderProduct(Base):
    '''SQLAlchemy class used to map to the purchase_order_product table in the 
    database.
    '''
    __tablename__ = "purchase_order_product"
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False)
    
    # Initially I had the primary_key property set to True for this column, and
    # with autoincrement set to False. I'm sure I got this from the docs. 
    # But it didn't work. SQLAlchemy ended up treating this column as the 
    # primary key, i.e., not including it when setting value in SQL statements.  
    purchase_order_id = Column(Integer, 
                               ForeignKey("purchase_order.id"),
                               nullable=False)
    
    # Initially I had the primary_key property set to True for this column, and
    # with autoincrement set to False. I'm sure I got this from the docs.
    product_id = Column(Integer, 
                        ForeignKey("product.id"),
                        nullable=False)
    
    unit_price = Column(Integer, nullable=False)
    
    discount = Column(Integer, nullable=False)
    
    quantity = Column(Integer, nullable=False)
    
    # Relationships
    # The cascade property is set to "save-update" instead of, e.g., "all, 
    # delete-orphan" because a delete of a purchase_order_product record must 
    # not result in a delete of the relevant purchase_order records.
    purchase_order = relationship("PurchaseOrder", 
                                  back_populates="products",
                                  cascade="save-update", 
                                  single_parent=True)
    
    # The cascade property is set to "save-update" because a delete of a 
    # purchase_order_product record must not result in a delete of the relevant 
    # product records.
    product = relationship("Product", 
                           back_populates="purchase_orders",
                           cascade="save-update")
    
    def __repr__(self):
        return ("<PurchaseOrderProduct(id='%s',"
                "purchase_order_id='%s',"
                "product_id='%s',"
                "unit_price='%s',"
                "discount='%s',"
                "quantity='%s')>") % (str(self.id),
                                      str(self.purchase_order_id), 
                                      str(self.product_id), 
                                      str(self.unit_price), 
                                      str(self.discount), 
                                      str(self.quantity))
                