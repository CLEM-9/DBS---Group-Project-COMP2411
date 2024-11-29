from crud_operations import *
from datetime import datetime
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
                "  registeredUsers INT NOT NULL,"
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
                "  FOREIGN KEY (BID, mealName) REFERENCES BanquetMeals(BID, mealName) ON DELETE CASCADE ON UPDATE CASCADE,"
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

    @staticmethod
    def is_alphanumeric(string):
        # Use a regular expression to check if the string contains only a-z, A-Z, and 0-9
        return bool(re.fullmatch(r'[a-zA-Z0-9]+', string))

    def input_email(self, check_existence = True, empty_not_allowed = True, new_registration= False):
        while True:
            email = input("📧 Enter Email: ").strip()
            if not (empty_not_allowed or email):
                return None
            if self.back(email):    #if back, go back
                return email
            if self.is_valid_email(email):
                if check_existence:
                    if self.check_email_exists(email):
                        if not new_registration:
                            return email
                        else:
                            print("❌ This email is already registered. Please log in or use a different email to register. ❌\n")
                    else:
                        if new_registration:
                            return email
                        else:
                            print("❌ This email is not registered. ❌\n")
                else:
                    return email
            else:
                print("❌ Invalid email format. Please enter a valid email. ❌\n")

    def input_password(self, empty_not_allowed = True):
        while True:
            #TODO switch to getpass on delivery
            #password = getpass("🔒 Enter Password (your password is invisible): ").strip()
            password = input("🔒 Enter Password: ").strip()
            if self.back(password):
                return password
            if not empty_not_allowed or password:
                if not password:
                    return None
                return password
            print("❌ Password is required. Please provide a secure password. ❌\n")

    def input_name(self, word= "First", empty_not_allowed = True):
        while True:
            name = input(f"👤 Enter {word} Name: ").strip()
            if not (empty_not_allowed or name): # accepts only empty entry
                return None
            if self.back(name):
                return name
            if name and name.isalpha():
                return name
            print(f"❌ {word} name is required and must only contain letters. Please try again. ❌\n")

    def input_phone(self, empty_not_allowed = True):
        while True:
            phone = input("📞 Enter Phone Number: ").strip()
            if not (empty_not_allowed or phone): # accepts only empty entry
                return None
            if self.back(phone):
                return phone
            if phone and phone.isdigit() and len(phone) == 8:
                return phone
            print("❌ Phone number is invalid. Please enter a valid phone. ❌\n")

    def input_address(self, empty_not_allowed = True):
        while True:
            address = input("🏠 Enter Address: ").strip()
            if not (empty_not_allowed or address):  # passes only empty string if allowed
                return None
            if self.back(address):
                return address
            if address and self.is_alphanumeric(address):
                return address
            print("❌ Address is invalid. Please enter a valid address. ❌\n")

    def input_attendee_type(self, empty_not_allowed = True):
        while True:
            attendee_type = input("🎓 Enter Attendee Type (Student, Alumni, Staff, Guest): ").strip()
            if not (empty_not_allowed or attendee_type): # accepts only empty entry
                return None
            if self.back(attendee_type):
                return attendee_type
            if attendee_type in ["Student", "Alumni", "Staff", "Guest"]:
                return attendee_type
            print("❌ Please select a valid attendee type: Student, Alumni, Staff, or Guest. ❌\n")

    def input_affiliate_organization(self, empty_not_allowed = True):
        while True:
            affiliate_organization = input("🏢 Enter Affiliate Organization: ").strip()
            if not (empty_not_allowed or affiliate_organization):
                return None
            if self.back(affiliate_organization):
                return affiliate_organization
            if affiliate_organization and self.is_alphanumeric(affiliate_organization):
                return affiliate_organization
            print("❌ Organization name is required. Please provide a valid name. ❌\n")

    def input_meal_name(self, available_meals, empty_not_allowed = True):
        all_meals = []
        for meals in available_meals:
            meals = list(meals)  #transforms into a list the in case it's a tuple
            all_meals.append(meals[0])

        while True:
            meal_name = input("👉 Enter Meal Name: ").strip()
            if not (empty_not_allowed or meal_name):
                return None
            if self.back(meal_name):
                return meal_name
            if meal_name in all_meals:
                    return meal_name
            print("❌ Invalid meal name. Beware of Caps. Please choose from the list above: ❌\n")

    def input_drink_name(self, alcoholic, alcohol_free):
        while True:
            drink_name = input("👉 Enter Drink Name: ").strip()
            if not drink_name or self.back(drink_name) or (drink_name in alcoholic) or (drink_name in alcohol_free):
                return drink_name
            print("❌ Invalid drink name. Beware of Caps. Please choose from the list above: ❌\n")

    def input_alcoholic_drink(self, empty_not_allowed = True):
        while True:
            alcoholic_drink= input("🍷 Do you want an alcoholic drink? (Yes/No): ").strip().lower()
            if not (empty_not_allowed or alcoholic_drink):
                return None
            if self.back(alcoholic_drink):
                return alcoholic_drink
            if alcoholic_drink in ["yes", "no"]:
                return alcoholic_drink
            print("❌ Invalid choice. Please enter 'Yes' or 'No' ❌\n")

    def input_seating_preference(self, word = "first"):
        # Validate seating preferences
        while True:
            seating_preference = input(f"👉 Enter Email of {word} preference (or press Enter to skip): ").strip()
            if not seating_preference:
                return None
            if self.back(seating_preference):
                return seating_preference
            if self.is_valid_email(seating_preference):
                return seating_preference
            print("❌ Email address is invalid. Please try again ❌\n")

    def input_banquet_name(self, empty_not_allowed= True):
        while True:
            banquet_name = input("🏷️ Enter Banquet Name: ").strip()
            if not (empty_not_allowed or banquet_name):
                return None
            if self.back(banquet_name):
                return banquet_name
            if banquet_name and self.is_alphanumeric(banquet_name):
                return banquet_name
            print("❌ Banquet Name is required. Please enter a valid Name. ❌\n")

    def input_location(self, empty_not_allowed= True):
        while True:
            banquet_location = input("📍 Enter Location: ").strip()
            if not (empty_not_allowed or banquet_location):
                return None
            if self.back(banquet_location):
                return banquet_location
            if banquet_location and self.is_alphanumeric(banquet_location):
                return banquet_location
            print("❌ Banquet Location is required. Please enter a valid Location ❌\n")

    def validate_staff(self, staff_email):
        self.cursor.execute("SELECT attendeeType FROM Attendees WHERE email = %s", [staff_email])
        is_staff = self.cursor.fetchone()
        if is_staff and (is_staff[0] == "Staff"):
            return True
        return False

    def input_staff_email(self, empty_not_allowed= True):
        while True:
            staff_email = input("📧 Enter Staff Email: ")
            if not (empty_not_allowed or staff_email):
                return None
            if self.back(staff_email):
                return staff_email
            if staff_email and self.is_valid_email(staff_email):
                return staff_email
            print("❌ Staff Email is required. Please enter a valid email ❌\n")

    def get_valid_date(self, prompt, allow_empty=False):
        date_input = None
        while not self.back(date_input):
            date_input = input(prompt).strip()
            if allow_empty and not date_input:
                return None
            try:
                return datetime.strptime(date_input, "%Y-%m-%d").date()
            except ValueError:
                print("\n❌ Invalid date format. Please use YYYY-MM-DD.")
        return date_input

    def get_valid_time(self, prompt, allow_empty=False):
        time_input = None
        while not self.back(time_input):
            time_input = input(prompt).strip()
            if allow_empty and not time_input:
                return None
            try:
                datetime.strptime(time_input, "%H:%M:%S")
                return time_input
            except ValueError:
                print("\n❌ Invalid time format. Please use HH:MM:SS.")
        return time_input

    def get_valid_number(self, prompt, allow_empty=False):
        number_input = None
        while not self.back(number_input):
            number_input = input(prompt).strip()
            if allow_empty and not number_input:
                return None
            if number_input.isdigit():
                return int(number_input)
            print("\n❌ Please enter a valid number.")
        return number_input

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
        error_log_path = os.path.join(os.path.dirname(__file__), "../resources/error_log.txt")
        error_log_file = open(error_log_path, "w")

        sql_file_path = os.path.join(os.path.dirname(__file__), "../database/insert_query.sql")
        sql_file = None
        if not os.path.exists(sql_file_path):
            sql_file = open(sql_file_path, "w")
            sql_file.write("-- ----------------------------------\n")
            sql_file.write(f"-- REMEMBER TO CHANGE None TO NULL --\n")
            sql_file.write("-- ----------------------------------\n\n")

        self.check_connection()
        print("\nPlease wait, populating database with test data...")
        try:
            for table_name, table_sql in self.TABLES.items():
                self.cursor.execute(table_sql)
                error_log_file.write(f"ATTEMPT LOADING FROM {table_name}\n\n")
                self.insert_data_from_excel(table_name, error_log_file)
                if sql_file:
                    self.create_sql_insert_file(table_name, sql_file)
            print("✅ Testing data loaded successfully \n")
        except Error as err:
            print(f"❌ Failed populating tables: ❌\nError Code: {err}\n")
        finally:
            self.connection.commit()
            error_log_file.close()
            if sql_file:
                sql_file.close()

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
                return ["Attendee", if_attendee[0], if_attendee[1], if_attendee[2], if_attendee[3], if_attendee[4], if_attendee[5], if_attendee[6], if_attendee[7]]
            elif if_admin:
                return ["Administrator", if_admin[0], if_admin[1], if_admin[2], if_admin[3]]
            else:
                return None

        except Error as e:
            print(f"❌ Error code: {e} ❌\n")

    def check_email_exists(self, email):
        try:
            # Query attendees
            self.cursor.execute("SELECT * FROM Attendees WHERE email = %s", [email])
            if_attendee = bool(self.cursor.fetchone())

            # Query administrators
            self.cursor.execute("SELECT * FROM Administrators WHERE adminEmail = %s", [email])
            if_admin = bool(self.cursor.fetchone())

            # Check existence
            if if_attendee or if_admin:
                return True
            return False

        except Error as e:
            print(f"❌ Error code: {e} ❌\n")
            return False

    def drop_database(self):
        try:
            self.cursor.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
        except Error as err:
            print(f"❌ Failed dropping database: ❌\nError Code: {err}\n")

    @staticmethod
    def create_sql_insert_file(table_name, sql_file):
        file_path = os.path.join(os.path.dirname(__file__), f"../database/test_data_tables/{table_name}.xlsx")
        data = pd.read_excel(file_path)
        data = data.replace({np.nan: None})
        columns = data.columns.tolist()
        columns_placeholder = ", ".join(columns)

        sql_statement_query = f"INSERT INTO {table_name}({columns_placeholder})\nVALUES"

        # Builds the sql statement from the excell file
        sql_file.write(f"-- {table_name} INSERT STATEMENT\n")
        sql_file.write(sql_statement_query)

        firstLine = 0
        for _, row in data.iterrows():
            sql_values = list(row)
            if table_name == "Banquet":
                hour = sql_values[6].hour
                minute = sql_values[6].minute
                second = sql_values[6].second
                if not hour:
                    hour = "00"
                if not minute:
                    minute = "00"
                if not second:
                    second = "00"
                sql_values[6] = f'{hour}:{minute}:{second}'
            sql_values = tuple(sql_values)
            if firstLine:
                sql_file.write(f",\n\t{sql_values}")
            else:
                sql_file.write(f"\n\t{sql_values}")
            firstLine += 1
        sql_file.write(";\n\n\n")

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
                SET registeredUsers = registeredUsers + 1
                WHERE BID = %s AND registeredUsers < totalSeats
                """

        for _, row in data.iterrows():
            values = tuple(row)
            try:
                if table_name == "UserBanquetRegistration":
                    self.cursor.execute(sql_update_seats, [values[0]])  # when inserting the banquets registrations also updates the count
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
            print(f"❌ Error inserting test data: {e} ❌\n")