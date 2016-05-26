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
from sqlalchemy.types import Integer, Boolean
from sqlabase import Base
from dbfieldsizes import PROJECT_CODE_STRING_LENGTH, DESCRIPTION_STRING_LENGTH


class Project(Base):
    '''SQLAlchemy class used to map to the project table in the database.
    '''
    __tablename__ = "project"
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False)
    
    code = Column(String(PROJECT_CODE_STRING_LENGTH), nullable=False)
    
    description = Column(String(DESCRIPTION_STRING_LENGTH), nullable=False)
    
    completed = Column(Boolean, nullable=False)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", 
                                  back_populates="project")
    
    def __repr__(self):
        return ("<Project(id='%s',"
                "description='%s')>") % (str(self.id), 
                                                 self.description)
                