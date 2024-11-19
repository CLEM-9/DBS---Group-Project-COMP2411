import mysql.connector
from mysql.connector import Error
from db_setup import initialize_database
from getpass import getpass

DB_NAME = 'banquet_database'

def get_db_connection():
    try:
        password = getpass("Enter your MySQL password: ")
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password
        )
        cursor = connection.cursor()
        initialize_database(connection, cursor)
        if connection.is_connected():
            connection.database = DB_NAME  # Switch to the correct database
            return connection, connection.cursor()
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None, None