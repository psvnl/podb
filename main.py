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

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from dbaccess import (sqlite_database_exists, sqlite_connection_is_ok, 
                      mysql_database_exists, mysql_connection_is_ok)


RETURN_CODE_UNDEFINED = -1
RETURN_CODE_INVALID_APP_CONFIG = 1
RETURN_CODE_INVALID_USER_CONFIG = 2


if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_main_window = False
    from appconfig import app_config, app_config_ok, DatabaseSection
    # Note that importing the appconfig module in the previous line created  
    # global variables called app_config and app_config_ok.
    if app_config_ok:
        # Test the connection to the database.
        if app_config.database.type == DatabaseSection.TYPE_SQLITE:
            db_exists = sqlite_database_exists(
                                            app_config.database.filename)
            if db_exists:
                db_connection_ok = sqlite_connection_is_ok(
                                            app_config.database.filename) 
        elif app_config.database.type == DatabaseSection.TYPE_MYSQL:
            db_exists = mysql_database_exists(
                                            app_config.database.username,
                                            app_config.database.password,
                                            app_config.database.host,
                                            app_config.database.name)
            if db_exists:
                db_connection_ok = mysql_connection_is_ok(
                                            app_config.database.username,
                                            app_config.database.password,
                                            app_config.database.host,
                                            app_config.database.name)
        # Validate the configuration record in the database.
        if db_exists and db_connection_ok:
            # Import all the database class definitions so that SQL Alchemy
            # knows what they are. (Ignore the "unused import" warnings in the
            # following six lines.)
            from product import Product
            from project import Project
            from purchaseorder import PurchaseOrder
            from purchaseorderproduct import PurchaseOrderProduct
            from supplier import Supplier
            from userconfig import UserConfig
            
            from userconfigmodel import UserConfigReader
            from sqlaengine import engine
            from sqlabase import Base
            Base.metadata.create_all(engine)
            from sqlasession import session_scope
            with session_scope() as session:
                user_config = UserConfigReader(session)
                if user_config.config_valid:
                    start_main_window = True
    # In case of errors, run the configuration wizard (which will include 
    # testing the connection to the database and validating the configuration 
    # record in the database).
    return_code = RETURN_CODE_UNDEFINED
    from configwizard import StartUpConfigWizard
    if not app_config_ok or not db_exists or not db_connection_ok \
    or not user_config.config_valid:
        config_wizard = StartUpConfigWizard(app_config)
        result = config_wizard.exec_()
        if result == QWizard.Accepted:
            start_main_window = True
        else:
            if not app_config_ok:
                return_code = RETURN_CODE_INVALID_APP_CONFIG
            else:
                return_code = RETURN_CODE_INVALID_USER_CONFIG
    else:
        start_main_window = True
    if start_main_window:
        import ctypes
        from mainwindow import MainWindow, __version__
        myappid = u"POdB.{}".format(__version__)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        from sqlaengine import engine
        from sqlabase import Base
        Base.metadata.create_all(engine)
        from sqlasession import session_scope
        with session_scope() as session:
            form = MainWindow(app_config, session)
            form.show()
            return_code = app.exec_()
    sys.exit(return_code)