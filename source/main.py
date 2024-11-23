from db_connection import get_db_connection
from WelcomePage import WelcomePage
from db_setup import BanquetDatabase

DB_NAME = "banquet_database"

if __name__ == "__main__":
    connection, cursor = get_db_connection(DB_NAME)
    BMS_database = BanquetDatabase(cursor, connection, DB_NAME)
    # TODO drop database, delete before submitting
    BMS_database.drop_database()

    # sets up the database and tables
    BMS_database.setup_database_and_tables()
    BMS_database.load_testing_data()

    if connection and cursor:
        welcome_page = WelcomePage(cursor, connection, BMS_database)
        welcome_page.display()
    else:
        print("Failed to establish database connection, please try again.")
        