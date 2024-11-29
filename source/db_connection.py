import mysql.connector
from mysql.connector import Error
from db_setup import BanquetDatabase
from getpass import getpass

def get_db_connection(DB_NAME):
    """
    Establishes a connection to the MySQL database and initializes the required database and tables.

    Returns:
        tuple: (connection, cursor) if successful, otherwise (None, None).
    """
    try:
        print("\n" + "=" * 50)
        print("🔑 Welcome to the Banquet Database Connection Setup")
        print("💡 If you need to change the MySQL username or host, edit 'db_connection.py'.")
        print("=" * 50)

        #TODO switch to getpass for final version, getpass doesn't work on PYCHARM IDE
        #password = getpass("👉 Enter your MySQL password: ")
        password = input("👉 Enter your MySQL password: ")
        print("\nTrying to connect to database...")

        # Attempt to establish a connection
        connection = mysql.connector.connect(
            host='localhost',
            user='test_user',
            password=password
        )
        cursor = connection.cursor()

        if connection.is_connected():
            print("✅ Successfully connected to the MySQL database.\n")
            return connection, cursor
        else:
            print("\n❌ Failed to connect to the MySQL database. Please check your credentials.")
            return None, None

    except Error as e:
        print(f"\n❌ Error connecting to the database: {e}")
        return None, None