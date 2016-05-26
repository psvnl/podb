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

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlaengine import engine

        
# This is the ONLY place where the Session class is created for the application.
Session = sessionmaker(bind=engine, autoflush=True)

@contextmanager
def session_scope():
    '''Provide a transactional scope around a series of operations.
    
    Refer to: 
    http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-
    frequently-asked-questions.
    '''
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        