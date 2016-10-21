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

from sqlalchemy import create_engine
from appconfig import app_config, DatabaseSection
from dbaccess import create_mysql_database_if_required


def _get_engine_string():
    engine_string = ""
    if app_config.database.type == DatabaseSection.TYPE_SQLITE:
        engine_string = r"{}:///{}".format(app_config.database.type, 
                                           app_config.database.filename)
    elif app_config.database.type == DatabaseSection.TYPE_MYSQL:
        engine_string = "{}+{}://{}:{}@{}/{}".format(
                                           app_config.database.type,
                                           app_config.database.driver,
                                           app_config.database.username,
                                           app_config.database.password,
                                           app_config.database.host,
                                           app_config.database.name)
    else:
        pass
    return engine_string


if app_config.database.type == DatabaseSection.TYPE_SQLITE:
    engine = create_engine(_get_engine_string(), 
                           echo=False)
    # Set echo=True in the line above to enable SQLAlchemy logging.
elif app_config.database.type == DatabaseSection.TYPE_MYSQL:
    # Including the creation of the MySQL database here, opportunistically!
    create_mysql_database_if_required(app_config.database.username, 
                                      app_config.database.password, 
                                      app_config.database.host, 
                                      app_config.database.name)
    # The isolation_level setting is set to READ COMMITTED to ensure that 
    # committed changes are read by transactions without having to restart 
    # the transaction.
    engine = create_engine(_get_engine_string(),
                           isolation_level="READ COMMITTED",
                           echo=False)
    # Set echo=True in the line above to enable SQLAlchemy logging.
else:
    # No other database types catered for.
    pass
