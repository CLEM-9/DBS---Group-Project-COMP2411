from db_connection import get_db_connection
from WelcomePage import WelcomePage

if __name__ == "__main__":
    connection, cursor = get_db_connection()
    if connection and cursor:
        welcome_page = WelcomePage(cursor, connection)
        welcome_page.display()
    else:
        print("Failed to establish database connection, please try again.")
        