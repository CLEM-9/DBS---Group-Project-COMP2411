import sys
import mysql.connector

from source.connection import Connection

if __name__ == '__main__':
    database = "banquet_database"
    user = "test_user"
    password = input('Enter your password: ')
    accessStatus = True

    try:
        access1 = Connection(user, password, database)
    except mysql.connector.Error as err:
        print(f"ERROR CODE: {err}")
        accessStatus = False
    finally:
        if not accessStatus:
            print("Connection Failed")
            sys.exit()
        # noinspection PyUnboundLocalVariable
        if access1.connection.is_connected():
            print(f"Connected to {database}")
            while True:
                closeConnection = input("Close the connection? (y/n): ")
                if closeConnection == 'y':
                    access1.connection.close()
                    print(f"Disconnected from {database}")
                    sys.exit()

