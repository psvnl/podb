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

import os
import logging
import sqlite3
import mysql.connector


_TEST_TABLE_NAME = "test_table"
_TEST_CREATE_TABLE = "CREATE TABLE test_table (test_column VARCHAR(20))"
_TEST_DROP_TABLE = "DROP TABLE test_table"


def sqlite_database_exists(filename):
    '''Determine if a SQLite database exists.
    
    Args:
    :param filename: The SQLite database filename.
    :type filename: String
    
    Returns:
    :return: True if the database file exists. False otherwise.
    '''
    return os.path.exists(filename)

def sqlite_connection_is_ok(filename):
    '''Test the "connection" to the SQLite database.
    
    The test steps are as follows: 
    1. Connect to the database. 
    2. Create a test table and confirm that it has been created.
    3. Drop the test table and confirm that it has been deleted.
    
    Args:
    :param filename: The SQLite database filename.
    :type filename: String
    
    Returns:
    :return: True if the connection test passes. False otherwise. 
    '''
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    try:
        # Create a table.
        cursor.execute(_TEST_CREATE_TABLE)
        # Confirm table created.
        if _table_is_in_sqlite_database(cursor, _TEST_TABLE_NAME):
            # Drop the table.
            cursor.execute(_TEST_DROP_TABLE)
            # Confirm table deleted.
            if not _table_is_in_sqlite_database(cursor, _TEST_TABLE_NAME):
                conn.close()
                return True
        conn.close()
        return False
    except Exception:
        conn.close()
        return False
        
def _table_is_in_sqlite_database(cursor, table_name):
    '''Determine if a table is in the SQLite database.
    
    Args:
    :param cursor: The database cursor in use.
    :type cursor: sqlite3.Cursor
    :param table_name: The name of the table to check. 
    :type table_name: String
    
    Returns:
    :return: True if the table exists. False otherwise.
    '''
    cursor.execute(("SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name='{}'").format(table_name))
    result = cursor.fetchone()
    if result:
        if table_name in result:
            return True
    return False
    
def mysql_database_exists(username, password, host, db_name):
    '''Determine if a MySQL database exists.
    
    Args:
    :param username: The MySQL database user name.
    :type username: String
    :param password: The MySQL database password.
    :type password: String
    :param host: The MySQL database host.
    :type host: String
    :param db_name: The name of the MySQL database.
    :type db_name: String
    
    Returns:
    :return: True if the database file exists. False otherwise.
    '''
    try:
        conn = mysql.connector.connect(user=username, 
                                       password=password, 
                                       host=host)
        cursor = conn.cursor()
    except mysql.connector.Error as e:
        _print_mysql_connection_error(db_name, e.msg)
        return False
    try:
        cursor.execute("USE {}".format(db_name))
    except mysql.connector.Error as e:
        logging.debug("Error executing 'USE {}': {}".format(db_name, e.msg))
        cursor.close()
        conn.close()
        return False
    cursor.close()
    conn.close()
    return True

def _print_mysql_connection_error(db_name, error_message):
    logging.debug("Error connecting to MySQL database {}: {}".format(db_name, 
                                                             error_message))

def mysql_connection_is_ok(username, password, host, db_name):
    '''Test the connection to the MySQL database.
    
    The test steps are as follows: 
    1. Connect to the database. 
    2. Create a test table and confirm that it has been created.
    3. Drop the test table and confirm that it has been deleted.
    
    Args:
    :param username: The MySQL database user name.
    :type username: String
    :param password: The MySQL database password.
    :type password: String
    :param host: The MySQL database host.
    :type host: String
    :param db_name: The name of the MySQL database.
    :type db_name: String
    
    Returns:
    :return: True if the connection test passes. False otherwise.
    '''
    try:
        conn = mysql.connector.connect(user=username, 
                                       password=password, 
                                       host=host)
        cursor = conn.cursor()
    except mysql.connector.Error as e:
        _print_mysql_connection_error(db_name, e.msg)
        return False
    try:
        cursor.execute("USE {}".format(db_name))
        # Create a table.
        cursor.execute(_TEST_CREATE_TABLE)
        # Confirm table created.
        if _table_is_in_mysql_database(cursor, _TEST_TABLE_NAME):
            # Drop the table.
            cursor.execute(_TEST_DROP_TABLE)
            # Confirm table deleted.
            if not _table_is_in_mysql_database(cursor, _TEST_TABLE_NAME):
                cursor.close()
                conn.close()
                return True
        cursor.close()
        conn.close()
        return False
    except Exception:
        cursor.close()
        conn.close()
        return False

def _table_is_in_mysql_database(cursor, table_name):
    '''Determine if a table is in the MySQL database.
    
    Args:
    :param cursor: The database cursor in use.
    :type cursor: mysql.connector.cursor.MySQLCursor
    :param table_name: The name of the table to check. 
    :type table_name: String
    
    Returns:
    :return: True if the table exists. False otherwise.
    '''
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    for item in result:
        if table_name in item:
            return True
    return False

def create_mysql_database_if_required(username, password, host, db_name):
    '''Create a MySQL database if it does not yet exist.
    
    Args:
    :param username: The MySQL database user name.
    :type username: String
    :param password: The MySQL database password.
    :type password: String
    :param host: The MySQL database host.
    :type host: String
    :param db_name: The name of the MySQL database.
    :type db_name: String
    
    Returns:
    :return: True if processing successful. False if an error occurs. 
    '''
    try:
        conn = mysql.connector.connect(user=username, 
                                       password=password, 
                                       host=host)
        cursor = conn.cursor()
    except mysql.connector.Error as e:
        _print_mysql_connection_error(db_name, e.msg)
        return False
    try:
        cursor.execute(("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER "
                        "SET 'utf8'").format(db_name))
    except mysql.connector.Error as err:
        logging.debug("Error: " + err.msg)
        cursor.close()
        conn.close()
        return False
    conn.commit()
    cursor.close()
    conn.close()
    return True


if __name__ == '__main__':
    if sqlite_connection_is_ok("new_leal_eng_orders.db"):
        print("SQLite Connection OK")
    else:
        print("SQLite Connection NOT OK")
    if mysql_connection_is_ok("root", "26Cihad&", "127.0.0.1", "new_leal_eng_orders"):
        print("MySQL Connection OK")
    else:
        print("MySQL Connection NOT OK")