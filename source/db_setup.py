from crud_operations import *
import numpy as np
from mysql.connector import Error
import pandas as pd
import os
import re

class BanquetDatabase:
    def __init__(self, cursor, connection, name):
        self.cursor = cursor
        self.connection = connection
        self.database_name = name

        # initializes the tables
        self.TABLES = {
            'Attendees':
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
            ,
            'Administrators':
                "CREATE TABLE IF NOT EXISTS Administrators ("
                "  adminEmail VARCHAR(100) PRIMARY KEY,"
                "  adminName VARCHAR(50) NOT NULL,"
                "  adminLastName VARCHAR(50) NOT NULL,"
                "  adminPassword VARCHAR(50) NOT NULL"
                ")"
            ,
            'Banquet':
                "CREATE TABLE IF NOT EXISTS Banquet ("
                "  BID INT AUTO_INCREMENT PRIMARY KEY,"
                "  banquetName VARCHAR(100) NOT NULL,"
                "  address VARCHAR(100) NOT NULL,"
                "  location VARCHAR(50) NOT NULL,"
                "  staffEmail VARCHAR(100) NOT NULL,"
                "  banquetDate DATE NOT NULL,"
                "  banquetTime TIME NOT NULL,"
                "  available BIT,"
                "  totalSeats INT NOT NULL,"
                "  FOREIGN KEY (staffEmail) REFERENCES Attendees(email)"
                "    ON UPDATE CASCADE ON DELETE RESTRICT,"
                "  CONSTRAINT unique_banquet UNIQUE (address, location, banquetDate)"
                ")"
            ,
            'Meal':
                "CREATE TABLE IF NOT EXISTS Meal ("
                "  mealName VARCHAR(100) PRIMARY KEY,"
                "  special VARCHAR(100),"
                "  type VARCHAR(50)"
                ")"
            ,
            'Drink':
                "CREATE TABLE IF NOT EXISTS Drink ("
                "  drinkName VARCHAR(100) PRIMARY KEY,"
                "  isAlcoholic BIT"
                ")"
            ,
            'BanquetMeals':
                "CREATE TABLE IF NOT EXISTS BanquetMeals ("
                "  BID INT,"
                "  mealName VARCHAR(100),"
                "  price INT,"
                "  PRIMARY KEY (BID, mealName),"
                "  FOREIGN KEY (BID) REFERENCES Banquet(BID) ON DELETE CASCADE ON UPDATE CASCADE,"
                "  FOREIGN KEY (mealName) REFERENCES Meal(mealName) ON UPDATE CASCADE ON DELETE CASCADE"
                ")"
            ,
                'BanquetDrinks':
                "CREATE TABLE IF NOT EXISTS BanquetDrinks ("
                "  BID INT,"
                "  drinkName VARCHAR(100),"
                "  price INT,"
                "  PRIMARY KEY (BID, drinkName),"
                "  FOREIGN KEY (BID) REFERENCES Banquet(BID) ON DELETE CASCADE ON UPDATE CASCADE,"
                "  FOREIGN KEY (drinkName) REFERENCES Drink(drinkName) ON UPDATE CASCADE ON DELETE CASCADE"
                ")"
                ,
            'UserBanquetRegistration':
                "CREATE TABLE IF NOT EXISTS UserBanquetRegistration ("
                "  BID INT,"
                "  email VARCHAR(100),"
                "  mealName VARCHAR(100) NOT NULL,"
                "  alcoholicDrink BIT NOT NULL,"
                "  seatAssigned INT,"
                "  specialNeeds VARCHAR(128),"
                "  regDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                "  seatingPreference1 VARCHAR(100),"
                "  seatingPreference2 VARCHAR(100),"
                "  PRIMARY KEY (BID, email),"
                "  CHECK (seatingPreference1 LIKE '%_@_%._%'),"
                "  CHECK (seatingPreference2 LIKE '%_@_%._%'),"
                "  FOREIGN KEY (BID) REFERENCES BanquetMeals(BID) ON DELETE CASCADE ON UPDATE CASCADE,"
                "  FOREIGN KEY (mealName) REFERENCES BanquetMeals(mealName) ON UPDATE CASCADE ON DELETE CASCADE,"
                "  FOREIGN KEY (email) REFERENCES Attendees(email) ON UPDATE CASCADE ON DELETE RESTRICT"
                ")"
        }

        # creates the objects to work with the tables
        # NOTE: it does NOT create the table
        self.attendees = Attendees(self.cursor, self.connection)
        self.administrators = Administrators(self.cursor, self.connection)
        self.banquet = Banquet(self.cursor, self.connection)
        self.meal = Meal(self.cursor, self.connection)
        self.drink = Drink(self.cursor, self.connection)
        self.banquet_drink = BanquetDrink(self.cursor, self.connection)
        self.banquet_meal = BanquetMeal(self.cursor, self.connection)
        self.user_banquet_registration = UserBanquetRegistration(self.cursor, self.connection)

    @staticmethod
    def back(var):
        return var == "##"

    @staticmethod
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def input_email(self, check_existence = True):
        email = input("📧 Enter Email: ").strip()
        while not self.back(email) and check_existence and self.check_email_exists(email):
            print("\n❌ This email is already registered. Please log in or use a different email to register. ❌\n")
            email = input("📧 Enter Email: ").strip()
        while not self.back(email) and not self.is_valid_email(email):
            print("\n❌ Invalid email format. Please enter a valid email. ❌\n")
            email = input("📧 Enter Email: ").strip()
        return email

    @staticmethod
    def input_password():
        #TODO switch to getpass on delivery
        #password = getpass("🔒 Enter Password (your password is invisible): ").strip()
        password = input("🔒 Enter Password: ").strip()
        while not password:
            print("\n❌ Password is required. Please provide a secure password. ❌\n")
            #TODO switch to getpass on delivery
            #password = getpass("🔒 Create Password: ").strip()
            password = input("🔒 Create Password: ").strip()
        return password

    def input_name(self, word= "First", empty_not_allowed = True):
        name = input(f"👤 Enter {word} Name: ").strip()
        while not self.back(name) and (empty_not_allowed and not name or not name.isalpha()):
            print(f"\n❌ {word} name is required and must only contain letters. Please try again. ❌\n")
            name = input(f"👤 Enter {word} Name: ").strip()
        return name

    def input_phone(self, empty_not_allowed = True):
        while True:
            phone = input("📞 Enter Phone Number: ").strip()
            if self.back(phone):
                return phone
            if phone.isdigit() and len(phone) == 8:
                return phone
            if not (phone or empty_not_allowed): # accepts empty entry
                return phone
            print("\n❌ Phone number is invalid. Please enter a valid phone. ❌\n")

    def input_address(self, empty_not_allowed = True):
        address = input("🏠 Enter Address: ").strip()
        while not self.back(address) and (empty_not_allowed and not address):
            print("\n❌ Address cannot be empty. Please enter a valid address. ❌\n")
            address = input("🏠 Enter Address: ").strip()
        return address

    def input_attendee_type(self, empty_not_allowed = True):
        while True:
            attendee_type = input("🎓 Enter Attendee Type (Student, Alumni, Staff, Guest): ").strip()
            if self.back(attendee_type):
                return attendee_type
            if attendee_type in ["Student", "Alumni", "Staff", "Guest"]:
                return attendee_type
            if not (empty_not_allowed or attendee_type): # accepts empty entry
                return attendee_type
            print("\n❌ Please select a valid attendee type: Student, Alumni, Staff, or Guest. ❌\n")

    def input_affiliate_organization(self, empty_not_allowed = True):
        affiliate_organization = input("🏢 Enter Affiliate Organization: ").strip()
        while not self.back(affiliate_organization) and (empty_not_allowed and not affiliate_organization):
            print("\n❌ Organization name is required. Please provide a valid name. ❌\n")
            affiliate_organization = input("🏢 Enter Affiliate Organization: ").strip()
        return affiliate_organization

    def input_meal_name(self, available_meals):
        meal_name = input("👉 Enter Meal Name: ").strip()
        while not self.back(meal_name) and (meal_name not in available_meals and not self.back(meal_name)) :
            print("❌ Invalid meal name. Beware of Caps. Please choose from the list below:")
            meal_name = input("👉 Enter Meal Name: ").strip()
        return meal_name

    def input_alcoholic_drink(self):
        alcoholic_drink = input("🍷 Do you want an alcoholic drink? (Yes/No): ").strip().lower()
        while alcoholic_drink not in ["yes", "no"] and not self.back(alcoholic_drink):
            print("❌ Invalid choice. Please enter 'Yes' or 'No'.")
            alcoholic_drink = input("🍷 Do you want an alcoholic drink? (Yes/No): ").strip().lower()
        return alcoholic_drink

    def input_seating_preference(self, word = "first"):
        seating_preference = input(f"👉 Enter Email of {word} preference (or press Enter to skip): ").strip()
        # Validate seating preferences
        while not self.back(seating_preference) and seating_preference and not self.is_valid_email(seating_preference):
            print("❌ Email address is invalid. Please try again.")
            seating_preference = input(f"👉 Enter Email of {word} preference (or press Enter to skip): ").strip()
        return seating_preference

    def input_banquet_name(self, empty_not_allowed= True):
        banquet_name = input("🏷️ Enter Banquet Name: ").strip()
        while not self.back(banquet_name) and (empty_not_allowed and not banquet_name):
            print("\n❌ Banquet Name cannot be empty. Please try again.")
            banquet_name = input("🏷️ Enter Banquet Name: ").strip()
        return banquet_name

    def input_location(self, empty_not_allowed= True):
        banquet_location = input("📍 Enter Location: ").strip()
        while not self.back(banquet_location) and (empty_not_allowed and not banquet_location):
            print("\n❌ Banquet Location cannot be empty.")
            banquet_location = input("📍 Enter Location: ").strip()
        return banquet_location

    def validate_staff(self, staff_email):
        self.cursor.execute("SELECT attendeeType FROM Attendees WHERE email = %s", [staff_email])
        is_staff = self.cursor.fetchone()
        if is_staff and (is_staff[0] == "Staff"):
            return True
        return False

    def input_staff_email(self, empty_not_allowed= True):
        staff_email = input("📧 Enter Staff Email: ")
        while not self.back(staff_email) and (empty_not_allowed or staff_email):
            if self.is_valid_email(staff_email):
                if self.validate_staff(staff_email):
                    return staff_email
                else:
                    print("\n❌ Email does not belong to staff. Please input staff email")
            else:
                print("\n❌ Email format is incorrect. Please try again")
            staff_email = input("📧 Enter Staff Email: ")
        return staff_email

    def check_connection(self):
        if self.connection is None:
            print("Error: No self.connection to the database.")
            exit(1)

    def create_database(self):
        self.check_connection()
        print("Please wait, creating database...")
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name} DEFAULT CHARACTER SET 'utf8'")
            self.cursor.execute(f"USE {self.database_name}")
        except Error as err:
            print(f"Failed creating database.\nError Code: {err}")
            exit(1)
        pass

    def create_tables_load_testing_data(self):
        error_log_path = os.path.join(os.path.dirname(__file__), f"../resources/error_log.txt")
        os.remove(error_log_path)
        error_log_file = open(error_log_path, "w")

        self.check_connection()
        print("\nPlease wait, populating database with test data...")
        try:
            for table_name, table_sql in self.TABLES.items():
                self.cursor.execute(table_sql)
                error_log_file.write(f"ATTEMPT LOADING FROM {table_name}\n\n")
                self.insert_data_from_excel(table_name, error_log_file)
            print("\n✅ Testing data loaded successfully")
        except Error as err:
            print(f"Failed populating tables:\nError Code: {err}")
        finally:
            self.connection.commit()
            error_log_file.close()

    def setup_database(self):
        self.create_database()
        print("✅ Database setup successfully.")

    def check_email(self, email, password):
    # checks if logging_in user is attendee or administrator
        try:
            self.cursor.execute(
                "SELECT * FROM Attendees WHERE email = %s AND password = %s",
                (email, password)
            )
            if_attendee = self.cursor.fetchone()
            self.cursor.execute(
                "SELECT * FROM Administrators WHERE adminEmail = %s AND adminPassword = %s",
                (email, password)
            )
            if_admin = self.cursor.fetchone()
            if if_attendee:
                print("Login successful!")
                return ["Attendee", if_attendee[0], if_attendee[1], if_attendee[2], if_attendee[3], if_attendee[4], if_attendee[5], if_attendee[6], if_attendee[7]]
            elif if_admin:
                print("Login successful!")
                return ["Administrator", if_admin[0], if_admin[1], if_admin[2], if_admin[3]]
            else:
                print("Login failed. Please try again.")

        except Error as e:
            print(f"Error code: {e}")

    def check_email_exists(self, email):
        try:
            # Query attendees
            self.cursor.execute("SELECT * FROM Attendees WHERE email = %s", [email])
            if_attendee = self.cursor.fetchone()

            # Query administrators
            self.cursor.execute("SELECT * FROM Administrators WHERE adminEmail = %s", [email])
            if_admin = self.cursor.fetchone()

            # Check existence
            if if_attendee or if_admin:
                return True
            return False

        except Error as e:
            print(f"Error code: {e}")
            return False

    def drop_database(self):
        try:
            self.cursor.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
        except Error as err:
            print(f"Failed dropping database:\nError Code: {err}")

    def insert_data_from_excel(self, table_name, error_log_file):
        file_path = os.path.join(os.path.dirname(__file__), f"../database/test_data_tables/{table_name}.xlsx")
        data = pd.read_excel(file_path)
        data = data.replace({np.nan: None})
        columns = data.columns.tolist()
        columns_placeholder = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        insert_query = f"INSERT INTO {table_name}({columns_placeholder}) VALUES ({placeholders})"

        sql_update_seats = """
                UPDATE Banquet
                SET totalSeats = totalSeats - 1
                WHERE BID = %s AND totalSeats > 0
                """

        for _, row in data.iterrows():
            values = tuple(row)
            try:
                if table_name == "UserBanquetRegistration":
                    self.cursor.execute(sql_update_seats, [values[0]])
                self.cursor.execute(insert_query, values)
            except Error as e:
                error_log_file.write(f"\tERROR inserting data into {table_name}: {e}\n\t\t{values}\n")
            except Exception as ex:
                error_log_file.write(f"\tERROR General error: {ex}\n\t\t{values}\n")
        self.connection.commit()
        print(f"✅ Data from '{table_name}.xlsx' inserted successfully into '{table_name}'.")

    def insert_test_data(self):
        try:
            # Check if test data already exists
            self.cursor.execute("SELECT COUNT(*) FROM Attendees")
            attendee_count = self.cursor.fetchone()[0]
            if attendee_count == 0:
                self.cursor.execute(
                    "INSERT INTO Attendees (email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization) "
                    "VALUES ('johndoe@example.com', 'password123', '123 Elm St', 'Doe', 'John', '12345678', 'Student', 'University'),"
                    "       ('janedoe@example.hk', 'securepass', '456 Oak St', 'Doe', 'Jane', '87654321', 'Alumni', 'TechCorp'),"
                    "       ('b@gmail.com', 'b123', '789 Maple St', 'Doe', 'Bob', '12348765', 'Staff', 'University')"
                )

            self.cursor.execute("SELECT COUNT(*) FROM Administrators")
            admin_count = self.cursor.fetchone()[0]
            if admin_count == 0:
                self.cursor.execute(
                    "INSERT INTO Administrators (adminEmail, adminName, adminLastName, adminPassword) "
                    "VALUES ('buse@gmail.com', 'Buse', 'Kaya', 'buse123')"
                )

            self.cursor.execute("SELECT COUNT(*) FROM Banquet")
            banquet_count = self.cursor.fetchone()[0]
            if banquet_count == 0:
                self.cursor.execute(
                "INSERT INTO Banquet (banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats) "
                "VALUES ('Graduation Banquet', '123 Elm St', 'Ballroom', 'buse@gmail.com', '2022-06-30', '18:00:00', 1, 100)"
                )

            self.cursor.execute("SELECT COUNT(*) FROM Meal")
            meal_count = self.cursor.fetchone()[0]
            if meal_count == 0:
                self.cursor.execute(
                    "INSERT INTO Meal (mealName, special, type) "
                    "VALUES ('Vegan Plate', 'Gluten-Free', 'Main Course'),"
                    "       ('Chicken Dish', 'Spicy', 'Main Course'),"
                    "       ('Cheesecake', 'None', 'Dessert'),"
                    "       ('Fruit Salad', 'Vegan', 'Appetizer'),"
                    "       ('Beef Stew', 'None', 'Main Course')"

                )

            self.cursor.execute("SELECT COUNT(*) FROM Drink")
            drink_count = self.cursor.fetchone()[0]
            if drink_count == 0:
                self.cursor.execute(
                    "INSERT INTO Drink (drinkName, isAlcoholic) "
                    "VALUES ('Red Wine', 1),"
                    "       ('Sparkling Water', 0)"
                )

            self.cursor.execute("SELECT COUNT(*) FROM UserBanquetRegistration")
            reg_count = self.cursor.fetchone()[0]
            if reg_count == 0:
                self.cursor.execute(
                    "INSERT INTO UserBanquetRegistration (BID, email, mealName, alcoholicDrink, seatAssigned, specialNeeds, seatingPreference1, seatingPreference2) "
                    "VALUES (1, 'johndoe@example.com', 'Vegan Plate', 'No', 1, 'None', 'Front', 'Back')"
                )

            self.cursor.execute("SELECT COUNT(*) FROM BanquetMeals")
            meal_count = self.cursor.fetchone()[0]
            if meal_count == 0:
                self.cursor.execute(
                    "INSERT INTO BanquetMeals (BID, mealName, price) "
                    "VALUES (1, 'Vegan Plate', 10),"
                    "       (1, 'Chicken Dish', 10),"
                    "       (1, 'Cheesecake', 10),"
                    "       (1, 'Fruit Salad', 10)"
                )

            self.cursor.execute("SELECT COUNT(*) FROM BanquetDrinks")
            drink_count = self.cursor.fetchone()[0]
            if drink_count == 0:
                self.cursor.execute(
                    "INSERT INTO BanquetDrinks (BID, drinkName, price) "
                    "VALUES (1, 'Red Wine', 10),"
                    "       (1, 'Sparkling Water', 5)"
                )

        except Error as e:
            print(f"Error inserting test data: {e}")