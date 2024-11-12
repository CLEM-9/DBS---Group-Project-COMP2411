import mysql.connector
from mysql.connector import errorcode, Error

DB_NAME = 'banquet_database'

TABLES = {
    'attendees': (
        "CREATE TABLE IF NOT EXISTS attendees ("
        "  email VARCHAR(100) PRIMARY KEY,"
        "  password VARCHAR(50) NOT NULL,"
        "  address VARCHAR(100) NOT NULL,"
        "  lastName VARCHAR(50) NOT NULL,"
        "  firstName VARCHAR(50) NOT NULL,"
        "  phone CHAR(8),"
        "  attendeeType ENUM('Student', 'Alumni', 'Staff', 'Guest') NOT NULL,"
        "  affiliateOrganization CHAR(50),"
        "  CHECK (email LIKE '%_@_%._%')"
        ")"
    ),
    'Administrators': (
        "CREATE TABLE IF NOT EXISTS Administrators ("
        "  adminEmail VARCHAR(100) PRIMARY KEY,"
        "  adminName VARCHAR(50) NOT NULL,"
        "  adminLastName VARCHAR(50) NOT NULL,"
        "  adminPassword VARCHAR(50) NOT NULL"
        ")"
    ),
    'Banquet': (
        "CREATE TABLE IF NOT EXISTS Banquet ("
        "  BID INT AUTO_INCREMENT PRIMARY KEY,"
        "  banquetName VARCHAR(100) NOT NULL,"
        "  address VARCHAR(100) NOT NULL,"
        "  location VARCHAR(50) NOT NULL,"
        "  staffEmail VARCHAR(100) NOT NULL UNIQUE,"
        "  banquetDate DATE NOT NULL,"
        "  banquetTime TIME NOT NULL,"
        "  available CHAR(8) NOT NULL,"
        "  totalSeats INT NOT NULL,"
        "  FOREIGN KEY (staffEmail) REFERENCES Administrators(adminEmail)"
        "    ON UPDATE CASCADE ON DELETE RESTRICT,"
        "  CONSTRAINT unique_banquet UNIQUE (address, location, banquetDate)"
        ")"
    ),
    'Meal': (
        "CREATE TABLE IF NOT EXISTS Meal ("
        "  mealName VARCHAR(100) PRIMARY KEY,"
        "  special VARCHAR(100),"
        "  type VARCHAR(50)"
        ")"
    ),
    'Drink': (
        "CREATE TABLE IF NOT EXISTS Drink ("
        "  drinkName VARCHAR(100) PRIMARY KEY,"
        "  isAlcoholic ENUM('Yes', 'No')"
        ")"
    ),
    'UserBanquetRegistration' : (
    "CREATE TABLE IF NOT EXISTS UserBanquetRegistration ("
    "  BID INT,"
    "  email VARCHAR(100),"
    "  mealName VARCHAR(100) NOT NULL,"
    "  alcoholicDrink ENUM('Yes', 'No') NOT NULL,"
    "  seatAssignment INT,"
    "  specialNeeds VARCHAR(128),"
    "  regDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "  seatingPreference1 VARCHAR(100),"
    "  seatingPreference2 VARCHAR(100),"
    "  PRIMARY KEY (BID, email),"
    "  CHECK (seatingPreference1 LIKE '%_@_%._%'),"
    "  CHECK (seatingPreference2 LIKE '%_@_%._%'),"
    "  FOREIGN KEY (BID) REFERENCES Banquet(BID) ON DELETE CASCADE,"
    "  FOREIGN KEY (mealName) REFERENCES Meal(mealName) ON UPDATE CASCADE,"
    "  FOREIGN KEY (email) REFERENCES attendees(email) ON UPDATE CASCADE ON DELETE CASCADE"
    ")"
    )
}

# Function to create the database
def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    except Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

# Function to initialize the tables
def initialize_database():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password'
    )
    cursor = connection.cursor()

    try:
        create_database(cursor)
        cursor.execute(f"USE {DB_NAME}")
        
        for table_name, table_sql in TABLES.items():
            cursor.execute(table_sql)
            print(f"Created table {table_name}.")
        insert_test_data(cursor)
    except Error as err:
        print(f"Error: {err}")

    finally:
        connection.commit()
        cursor.close()
        connection.close()

def insert_test_data(cursor):
    try:
        cursor.execute(
            "INSERT INTO attendees (email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization) "
            "VALUES ('johndoe@example.com', 'password123', '123 Elm St', 'Doe', 'John', '12345678', 'Student', 'University'),"
            "       ('janedoe@example.com', 'securepass', '456 Oak St', 'Doe', 'Jane', '87654321', 'Alumni', 'TechCorp'),"
            "       ('b@gmail.com', 'b123', '789 Maple St', 'Doe', 'Bob', '12348765', 'Staff', 'University')"
        )

        cursor.execute(
            "INSERT INTO Administrators (adminEmail, adminName, adminLastName, adminPassword) "
            "VALUES ('buse@gmail.com' , 'Buse', 'Kaya', 'buse123')"
        )
        
        cursor.execute(
            "INSERT INTO Banquet (banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats) "
            "VALUES ('Graduation Banquet', '123 Elm St', 'Ballroom', 'buse@gmail.com' , '2022-06-30', '19:00:00', 'Y', 100)"
        )

        cursor.execute(
            "INSERT INTO Meal (mealName, special, type) "
            "VALUES ('Vegan Plate', 'Gluten-Free', 'Main Course'),"
            "       ('Chicken Dish', 'Spicy', 'Main Course')"
        )

        cursor.execute(
            "INSERT INTO Drink (drinkName, isAlcoholic) "
            "VALUES ('Red Wine', 'Yes'),"
            "       ('Sparkling Water', 'No')"
        )

        print("Test data inserted successfully.")

    except Error as e:
        print(f"Error inserting test data: {e}")