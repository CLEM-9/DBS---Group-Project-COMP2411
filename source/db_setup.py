import mysql.connector
from mysql.connector import Error
import pandas as pd
import os

DB_NAME = 'banquet_database'

TABLES = {
    'attendees': (
        "CREATE TABLE IF NOT EXISTS Attendees("
        "  email VARCHAR(100) PRIMARY KEY,"
        "  password VARCHAR(50) NOT NULL,"
        "  address VARCHAR(100) NOT NULL,"
        "  lastName VARCHAR(50) NOT NULL,"
        "  firstName VARCHAR(50) NOT NULL,"
        "  phone CHAR(8),"
        "  attendeeType ENUM('Student', 'Alumni', 'Staff', 'Guest') NOT NULL,"
        "  affiliateOrganization CHAR(50),"
        "  CHECK (email LIKE '%@%.__%')"
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
        "  staffEmail VARCHAR(100) NOT NULL,"
        "  banquetDate DATE NOT NULL,"
        "  banquetTime TIME NOT NULL,"
        "  available ENUM('Yes', 'No'),"
        "  totalSeats INT NOT NULL,"
        "  FOREIGN KEY (staffEmail) REFERENCES Attendees(email)"
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
        "  isAlcoholic BIT"
        ")"
    ),
    'UserBanquetRegistration': (
        "CREATE TABLE IF NOT EXISTS UserBanquetRegistration ("
        "  BID INT,"
        "  email VARCHAR(100),"
        "  mealName VARCHAR(100) NOT NULL,"
        "  alcoholicDrink BIT NOT NULL,"
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
        "  FOREIGN KEY (email) REFERENCES Attendees(email) ON UPDATE CASCADE ON DELETE CASCADE"
        ")"
    ),
    'BanquetMeals': (
        "CREATE TABLE IF NOT EXISTS BanquetMeals ("
        "  BID INT,"
        "  mealName VARCHAR(100),"
        "  price INT,"
        "  PRIMARY KEY (BID, mealName),"
        "  FOREIGN KEY (BID) REFERENCES Banquet(BID) ON DELETE CASCADE ON UPDATE CASCADE,"
        "  FOREIGN KEY (mealName) REFERENCES Meal(mealName) ON UPDATE CASCADE ON DELETE CASCADE"
        ")"
    ),
    'BanquetDrinks': (
        "CREATE TABLE IF NOT EXISTS BanquetDrinks ("
        "  BID INT,"
        "  drinkName VARCHAR(100),"
        "  price INT,"
        "  PRIMARY KEY (BID, drinkName),"
        "  FOREIGN KEY (BID) REFERENCES Banquet(BID) ON DELETE CASCADE ON UPDATE CASCADE,"
        "  FOREIGN KEY (drinkName) REFERENCES Drink(drinkName) ON UPDATE CASCADE ON DELETE CASCADE"
        ")"
    )
    
}

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    except Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def initialize_database(connection, cursor):
    if connection is None:
        print("Error: No connection to the database.")
        exit(1)
    try:
        create_database(cursor)
        cursor.execute(f"USE {DB_NAME}")
        
        for table_name, table_sql in TABLES.items():
            cursor.execute(table_sql)
        insert_data_from_excel(cursor, connection, 'Attendees')
        insert_data_from_excel(cursor, connection, 'Administrators')
        insert_data_from_excel(cursor, connection, 'Banquet')
        insert_data_from_excel(cursor, connection, 'Meal')
        insert_data_from_excel(cursor, connection, 'Drink')
        #insert_data_from_excel(cursor, connection, 'BanquetMeals')
        #insert_data_from_excel(cursor, connection, 'BanquetDrinks')
        #insert_data_from_excel(cursor, connection, 'UserBanquetRegistration')
        #insert_test_data(cursor)
    except Error as err:
        print(f"Error: {err}")
    finally:
        connection.commit()

def insert_test_data(cursor):
    try:
        # Check if test data already exists
        cursor.execute("SELECT COUNT(*) FROM Attendees")
        attendee_count = cursor.fetchone()[0]
        if attendee_count == 0:
            cursor.execute(
                "INSERT INTO Attendees (email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization) "
                "VALUES ('johndoe@example.com', 'password123', '123 Elm St', 'Doe', 'John', '12345678', 'Student', 'University'),"
                "       ('janedoe@example.hk', 'securepass', '456 Oak St', 'Doe', 'Jane', '87654321', 'Alumni', 'TechCorp'),"
                "       ('b@gmail.com', 'b123', '789 Maple St', 'Doe', 'Bob', '12348765', 'Staff', 'University')"
            )
        
        cursor.execute("SELECT COUNT(*) FROM Administrators")
        admin_count = cursor.fetchone()[0]
        if admin_count == 0:
            cursor.execute(
                "INSERT INTO Administrators (adminEmail, adminName, adminLastName, adminPassword) "
                "VALUES ('buse@gmail.com', 'Buse', 'Kaya', 'buse123')"
            )
        
        cursor.execute("SELECT COUNT(*) FROM Banquet")
        banquet_count = cursor.fetchone()[0]
        if banquet_count == 0:
            cursor.execute(
            "INSERT INTO Banquet (banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats) "
            "VALUES ('Graduation Banquet', '123 Elm St', 'Ballroom', 'buse@gmail.com' , 'Buse', 'Kaya', '2022-06-30', '18:00:00', 'Yes', 100)"
            )
            
        cursor.execute("SELECT COUNT(*) FROM Meal")
        meal_count = cursor.fetchone()[0]
        if meal_count == 0:
            cursor.execute(
                "INSERT INTO Meal (mealName, special, type) "
                "VALUES ('Vegan Plate', 'Gluten-Free', 'Main Course'),"
                "       ('Chicken Dish', 'Spicy', 'Main Course'),"
                "       ('Cheesecake', 'None', 'Dessert'),"
                "       ('Fruit Salad', 'Vegan', 'Appetizer'),"
                "       ('Beef Stew', 'None', 'Main Course')"
                
            )
        
        cursor.execute("SELECT COUNT(*) FROM Drink")
        drink_count = cursor.fetchone()[0]
        if drink_count == 0:
            cursor.execute(
                "INSERT INTO Drink (drinkName, isAlcoholic) "
                "VALUES ('Red Wine', 'Yes'),"
                "       ('Sparkling Water', 'No')"
            )
            
        cursor.execute("SELECT COUNT(*) FROM UserBanquetRegistration")
        reg_count = cursor.fetchone()[0]
        if reg_count == 0:
            cursor.execute(
                "INSERT INTO UserBanquetRegistration (BID, email, mealName, alcoholicDrink, seatAssignment, specialNeeds, seatingPreference1, seatingPreference2) "
                "VALUES (1, 'johndoe@example.com', 'Vegan Plate', 'No', 1, 'None', 'Front', 'Back')"
            )
        
        cursor.execute("SELECT COUNT(*) FROM BanquetMeals")
        meal_count = cursor.fetchone()[0]
        if meal_count == 0:
            cursor.execute(
                "INSERT INTO BanquetMeals (BID, mealName, price) "
                "VALUES (1, 'Vegan Plate', 10),"
                "       (1, 'Chicken Dish', 10),"
                "       (1, 'Cheesecake', 10),"
                "       (1, 'Fruit Salad', 10)"
            )
        
        cursor.execute("SELECT COUNT(*) FROM BanquetDrinks")
        drink_count = cursor.fetchone()[0]
        if drink_count == 0:
            cursor.execute(
                "INSERT INTO BanquetDrinks (BID, drinkName, price) "
                "VALUES (1, 'Red Wine', 10),"
                "       (1, 'Sparkling Water', 5)"
            )

    except Error as e:
        print(f"Error inserting test data: {e}")

def insert_data_from_excel(cursor, connection, table_name):
    file_path = os.path.join(os.path.dirname(__file__), f"../database/test_data_tables/{table_name}.xlsx")
    try:
        data = pd.read_excel(file_path)
        columns = data.columns.tolist()
        columns_placeholder = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        insert_query = f"INSERT IGNORE INTO {table_name}({columns_placeholder}) VALUES ({placeholders})"
        for _, row in data.iterrows():
            values = list(row)
            cursor.execute(insert_query, values)
        connection.commit()
        print(f"✅ Data from '{table_name}.xlsx' inserted successfully into '{table_name}'.")

    except Error as e:
        print(f"❌ Error inserting data into {table_name}: {e}")
    except Exception as ex:
        print(f"❌ General error: {ex}")
    except Error as e:
        print(f"Error inserting data from Excel: {e}")