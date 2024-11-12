# db_connection.py
import mysql.connector
from mysql.connector import Error

DB_NAME = 'banquet_database'

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='test_user',
            password='password',
            database=DB_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None