from db_connection import get_db_connection
from db_setup import initialize_database
from WelcomePage import WelcomePage

if __name__ == "__main__":
    connection = get_db_connection()
    if connection is None:
        initialize_database()
        connection = get_db_connection()
    cursor = connection.cursor()
    welcome_page = WelcomePage(cursor, connection)
    welcome_page.display()