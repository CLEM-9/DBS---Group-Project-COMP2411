from mysql.connector import Error
from pyexpat.errors import messages


class Database:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    # checks if logging_in user is attendee or administrator
    def check_email(self, connection, email, password):
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

    def check_email_exists(self, connection, email):
        try:
            self.cursor.execute(
                "SELECT * FROM Attendees WHERE email = %s", (email) )
            if_attendee = self.cursor.fetchone()
            self.cursor.execute(
                "SELECT * FROM Administrators WHERE adminEmail = %s", (email) )
            if_admin = self.cursor.fetchone()
            if if_attendee or if_admin:
                return True
            else:
                return False
        except Error as e:
            print(f"Error code: {e}")
                
    def drop_database(self):
        try:
            self.cursor.execute("DROP DATABASE IF EXISTS banquet_database")
        except Error as e:
            print(f"Error code: {e}")


class Tables:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection
        self.table_name = ""

    # gets the fetched result from the read operation and unpacks it in a string before return
    @staticmethod
    def unpack_read_info(info):
        message = ""
        for line in info:
            for item in line:
                message = message + str(item) + ", "
            message = message + "\n"
        #delete last \n
        message = message[:-1]
        return message

    def delete_all_entries(self):
        try:
            sql = f"DELETE FROM {self.table_name}"
            self.cursor.execute(sql)
            self.connection.commit()
            print(f"Successfully deleted all entries from {self.table_name} table")
        except Error as e:
            print(f"Error code : {e}")


class Attendees(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = "Attendees"

    # creates users
    def create(self, email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization):
        sql = """INSERT INTO Attendees(
            email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            str(email),
            str(password),
            str(address),
            str(lastName),
            str(firstName),
            str(phone) if phone else None,
            str(attendeeType),
            str(affiliateOrganization) if affiliateOrganization else None,
        )
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{firstName} {lastName} added successfully."
        except Error as e:
            import traceback
            traceback.print_exc()
            return f"Could not create attendee\nError code: {e}"
    # returns an array of arrays containing all information available
    def read(self):
        sql = "SELECT * FROM Attendees"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read attendee\nError code: {e}"

    # if the information is not provided by the user, pass None as argument
    def update(self, emailID, email, password, address, phone, attendeeType, affiliateOrganization):
    
        sql = "UPDATE Attendees SET "
        values = []
        message = "Following fields are updated:\n"

        # updates all fields that are not None
        if email is not None:
            sql = sql + "email = %s, "
            values.append(email)
            message += f"email = {email}\n"
        if password is not None:
            sql = sql + "password = %s, "
            message += f"password = {password}\n"
            values.append(password)
        if address is not None:
            sql = sql + "address = %s, "
            values.append(address)
            message += f"address = {address}\n"
        if phone is not None:
            sql = sql + "phone = %s, "
            values.append(phone)
            message += f"phone = {phone}\n"
        if attendeeType is not None:
            sql = sql + "attendeeType = %s, "
            values.append(attendeeType)
            message += f"attendeeType = {attendeeType}\n"
        if affiliateOrganization is not None:
            sql = sql + "affiliateOrganization = %s, "
            values.append(affiliateOrganization)
            message += f"affiliateOrganization = {affiliateOrganization}\n"

        # removes the last ", "
        sql = sql[:-2]
        sql = sql + " WHERE email = %s"
        values.append(emailID)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return message
        except Error as e:
            return f"Could not update attendee\nError code: {e}"

    def update_everything(self, email, password, phone, firstName, lastName, address, attendeeType, affiliateOrganization, emailID):    
        sql = "UPDATE Attendees SET "
        values = []
        message = "Following fields are updated:\n"

        # Normalize inputs
        email = email.strip() if email else None
        password = password.strip() if password else None
        phone = phone.strip() if phone else None
        firstName = firstName.strip().title() if firstName else None
        lastName = lastName.strip().title() if lastName else None
        address = address.strip() if address else None
        attendeeType = attendeeType.strip().title() if attendeeType else None
        affiliateOrganization = affiliateOrganization.strip() if affiliateOrganization else None

        # Update fields dynamically
        if email:
            sql = sql + "email = %s, "
            values.append(email)
            message += f"email = {email}\n"
        if password:
            sql = sql + "password = %s, "
            values.append(password)
            message += f"password = {password}\n"
        if phone:
            sql = sql + "phone = %s, "
            values.append(phone)
            message += f"phone = {phone}\n"
        if firstName:
            sql = sql + "firstName = %s, "
            values.append(firstName)
            message += f"firstName = {firstName}\n"
        if lastName:
            sql = sql + "lastName = %s, "
            values.append(lastName)
            message += f"lastName = {lastName}\n"
        if address:
            sql = sql + "address = %s, "
            values.append(address)
            message += f"address = {address}\n"
        if attendeeType:
            try:
                sql = sql + "attendeeType = %s, "
                values.append(attendeeType)
                message += f"attendeeType = {attendeeType}\n"
            except ValueError as e:
                return str(e)
        if affiliateOrganization:
            sql = sql + "affiliateOrganization = %s, "
            values.append(affiliateOrganization)
            message += f"affiliateOrganization = {affiliateOrganization}\n"

        # Check if there are fields to update
        if not values:
            return "No fields to update. Please provide at least one field to update."

        # Finalize the SQL query
        sql = sql[:-2]  # Remove trailing ", "
        sql = sql + " WHERE email = %s"
        values.append(emailID)

        # Execute the query
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return message
        except Error as e:
            return f"Could not update attendee\nError code: {e}"
        
    # deletes user with the primary key "email"
    def delete(self, email):
        sql = "DELETE FROM Attendees WHERE email = %s"
        values = [email]
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return "User deleted successfully."
        except Error as e:
            return f"Could not delete attendee\nError code: {e}"


class Banquet(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = "Banquet"

    # creates new banquet entry, banquetID is handled automatically by the database
    def create(self, banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats):
        sql = "INSERT INTO Banquet(banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{banquetName} added successfully."
        except Error as e:
            return f"Could not create banquet\nError code: {e}"

    # returns an array of arrays containing all information available
    def read(self):
        sql = "SELECT * FROM Banquet"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read banquets\nError code: {e}"

    def read_by_filter(self, banquetName, banquetDate, banquetLocation, address):
        sql = "SELECT * FROM Banquet WHERE "
        values = []
        message = "Following fields are filtered:\n"

        banquetName = banquetName.strip() if banquetName else None
        banquetDate = banquetDate if banquetDate else None
        banquetLocation = banquetLocation.strip() if banquetLocation else None
        address = address.strip() if address else None
        
        # appends all the information fields that need to be filtered
        if banquetName is not None:
            sql = sql + "banquetName = %s, "
            values.append(banquetName)
            message += f"banquetName = {banquetName}\n"
        if banquetDate is not None:
            sql = sql + "banquetDate = %s, "
            values.append(banquetDate)
            message += f"banquetDate = {banquetDate}\n"
        if banquetLocation is not None:
            sql = sql + "location = %s, "
            values.append(banquetLocation)
            message += f"location = {banquetLocation}\n"
        if address is not None:
            sql = sql + "address = %s, "
            values.append(address)
            message += f"adress = {address}\n"

        # removes the last ", "
        sql = sql[:-2]
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            return f"Could not read banquets\nError code: {e}"

    def read_by_id(self, BID):
        sql = "SELECT * FROM Banquet WHERE BID = %s"
        values = [BID]
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            return f"Could not read banquet\nError code: {e}"
        
    # if the information is not provided by the user, pass None as argument
    def update(self, BID, banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats):
        sql = "UPDATE Banquets SET "
        values = []
        message = "Following fields are updated:\n"

        # appends all the information fields that need to be updated
        if banquetName is not None:
            sql = sql + "banquetName = %s, "
            values.append(banquetName)
            message += f"banquetName = {banquetName}\n"
        if address is not None:
            sql = sql + "address = %s, "
            values.append(address)
            message += f"address = {address}\n"
        if location is not None:
            sql = sql + "location = %s, "
            values.append(location)
            message += f"location = {location}\n"
        if staffEmail is not None:
            sql = sql + "staffEmail = %s, "
            values.append(staffEmail)
            message += f"staffEmail = {staffEmail}\n"
        if banquetDate is not None:
            sql = sql + "banquetDate = %s, "
            values.append(banquetDate)
            message += f"banquetDate = {banquetDate}\n"
        if banquetTime is not None:
            sql = sql + "banquetTime = %s, "
            values.append(banquetTime)
            message += f"banquetTime = {banquetTime}\n"
        if available is not None:
            sql = sql + "available = %s, "
            values.append(available)
            message += f"available = {available}\n"
        if totalSeats is not None:
            sql = sql + "totalSeats = %s, "
            values.append(totalSeats)
            message += f"totalSeats = {totalSeats}\n"

        # removes the last ", "
        sql = sql[:-2]
        sql = sql + " WHERE BID = %s"
        values.append(BID)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return message
        except Error as e:
            return f"Could not update banquet\nError code: {e}"

    # deletes banquet with the primary key "BID"
    def delete(self, BID):
        sql = "DELETE FROM Banquet WHERE BID = %s"
        values = [BID]
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return "Banquet deleted successfully."
        except Error as e:
            return f"Could not delete banquet\nError code: {e}"

class Meal(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = "Meal"

    def create(self, mealName, special, mealType):
        sql = "INSERT INTO Meal(mealName, special, type) VALUES (%s, %s, %s)"
        values = (mealName, special, mealType)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{mealName} added successfully."
        except Error as e:
            return f"Could not create meal\nError code: {e}"

    def read(self):
        sql = "SELECT * FROM Meal"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read meals\nError code: {e}"

    def update(self, mealName, special, mealType):
        sql = "UPDATE Meal SET "
        values = []
        message = "Following fields are updated:\n"

        if special is not None:
            sql = sql + "special = %s, "
            values.append(special)
            message += f"special = {special}\n"
        if mealType is not None:
            sql = sql + "type = %s, "
            values.append(mealType)
            message += f"type = {mealType}\n"

        #removes the last ", "
        sql = sql[:-2]
        sql = sql + " WHERE mealName = %s"
        values.append(mealName)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return message
        except Error as e:
            return f"Could not update meal\nError code: {e}"

    def delete(self, mealName):
        sql = "DELETE FROM Meal WHERE mealName = %s"
        values = [mealName]
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{mealName} deleted successfully."
        except Error as e:
            return f"Could not delete meal\nError code: {e}"


class Drink(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = "Drink"

    def create(self, drinkName, isAlcoholic):
        sql = "INSERT INTO Drink(drinkName, isAlcoholic) VALUES (%s, %s)"
        values = (drinkName, isAlcoholic)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{drinkName} added successfully."
        except Error as e:
            return f"Could not create drink\nError code: {e}"

    def read(self):
        sql = "SELECT * FROM Drink"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read drinks\nError code: {e}"

    def update(self, drinkName, isAlcoholic):
        sql = "UPDATE Drink SET isAlcoholic = %s WHERE drinkName = %s"
        values = [isAlcoholic, drinkName]
        message = f"Following fields are updated:\nisAlcoholic = {isAlcoholic}"
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return message
        except Error as e:
            return f"Could not update drink\nError code: {e}"

    def delete(self, drinkName):
        sql = "DELETE FROM Drink WHERE drinkName = %s"
        values = [drinkName]
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{drinkName} deleted successfully."
        except Error as e:
            return f"Could not delete drink\nError code: {e}"


class BanquetDrinks(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = "BanquetDrinks"

    def create(self, BID, drinkName, price):
        sql = "INSERT INTO BanquetDrinks(BID, drinkName, price) FROM VALUES (%s, %s, %s)"
        values = (BID, drinkName, price)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{BID, drinkName} added successfully."
        except Error as e:
            return f"Could not create Drink in Banquet\nError code: {e}"

    def read(self):
        sql = "SELECT * FROM BanquetDrinks"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read BanquetDrinks\nError code: {e}"

    def show_drinks(self, BID):
        sql = "SELECT drinkName FROM BanquetDrinks WHERE BID = %s"
        values = [BID]
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read BanquetDrinks\nError code"
        
    def update(self, BID, drinkName, price):
        sql = "UPDATE BanquetDrinks SET price = %s WHERE BID = %s AND drinkName = %s"
        values = (price, BID, drinkName)
        message = f"Following fields are updated:\nprice = {price}"
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return message
        except Error as e:
            return f"Could not update Drink in Banquet\nError code: {e}"

    def delete(self, BID, drinkName):
        sql = "DELETE FROM BanquetDrinks WHERE BID = %s AND drinkName = %s"
        values = [BID, drinkName]
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{BID, drinkName} deleted successfully."
        except Error as e:
            return f"Could not delete Drink from Banquet\nError code: {e}"


class BanquetMeal(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = BanquetMeal

    def create(self, BID, mealName, price):
        sql = "INSERT INTO BanquetMeals(BID, mealName, price) FROM VALUES (%s, %s, %s)"
        values = (BID, mealName, price)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{BID, mealName} added successfully."
        except Error as e:
            return f"Could not create Meal in Banquet\nError code: {e}"

    def read(self):
        sql = "SELECT * FROM BanquetMeals"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read BanquetMeals\nError code: {e}"
        
    def show_meals(self, BID):
        sql = "SELECT mealName FROM BanquetMeals WHERE BID = %s"
        values = [BID]
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read BanquetMeals\nError code"
        
    def update(self, BID, mealName, price):
        sql = "UPDATE BanquetMeals SET price = %s WHERE BID = %s AND mealName = %s"
        values = (price, BID, mealName)
        message = f"Following fields are updated:\nprice = {price}"
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return message
        except Error as e:
            return f"Could not update Meal in Banquet\nError code: {e}"

    def delete(self, BID, mealName):
        sql = "DELETE FROM BanquetDrinks WHERE BID = %s AND mealName = %s"
        values = [BID, mealName]
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{BID, mealName} deleted successfully."
        except Error as e:
            return f"Could not delete Meal from Banquet\nError code: {e}"

class UserBanquetRegistration(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = "UserBanquetRegistration"

    def create(self, BID, email, mealName, alcoholicDrink, specialNeeds, seatingPref1, seatingPref2):
        # Default values for optional fields
        specialNeeds = specialNeeds or "None"
        seatingPref1 = seatingPref1 or "None"
        seatingPref2 = seatingPref2 or "None"

        # SQL query to fetch the next seat assignment
        seat_no_query = "SELECT COALESCE(MAX(seatAssignment), 0) + 1 AS nextSeat FROM UserBanquetRegistration"

        # SQL query to insert a new registration
        sql_insert = """
        INSERT INTO UserBanquetRegistration
        (BID, email, mealName, alcoholicDrink, seatAssignment, specialNeeds, seatingPreference1, seatingPreference2)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # SQL query to decrement the available seats for the banquet
        sql_update_seats = """
        UPDATE Banquet
        SET totalSeats = totalSeats - 1
        WHERE BID = %s AND totalSeats > 0
        """

        try:
            # Fetch the next seat number
            self.cursor.execute(seat_no_query)
            seat_no = self.cursor.fetchone()[0]  # Retrieve the next seat number
            
            # Insert the registration
            self.cursor.execute(
                sql_insert,
                (BID, email, mealName, alcoholicDrink, seat_no, specialNeeds, seatingPref1, seatingPref2)
            )
            
            # Decrement the total seats, ensure no negative seats
            affected_rows = self.cursor.execute(sql_update_seats, (BID,))
            if affected_rows == 0:
                raise ValueError("No available seats left for this banquet.")
            
            # Commit the transaction
            self.connection.commit()
            return f"Registration successful! Assigned Seat: {seat_no}. Banquet {BID}, Meal: {mealName}."

        except Exception as e:
            # Roll back the transaction in case of any error
            self.connection.rollback()
            return f"Could not register Attendee to Banquet\nError code: {e}"
            
    def read_by_user(self, email):
        sql = "SELECT * FROM UserBanquetRegistration WHERE email = %s"
        values = [email]
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read UserBanquetRegistration\nError code: {e}" 
        
    def read(self):
        sql = "SELECT * FROM UserBanquetRegistration"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read UserBanquetRegistration\nError code: {e}"

    def update(self, BID, email, mealName, alcoholicDrink, specialNeeds, seatingPref1, seatingPref2):
        sql = "UPDATE UserBanquetRegistration SET "
        values = []
        message = "Following fields are updated:\n"

        # Append fields dynamically if they are not None
        if mealName:
            sql += "mealName = %s, "
            values.append(mealName)
            message += f"mealName = {mealName}\n"
        if alcoholicDrink:
            sql += "alcoholicDrink = %s, "
            values.append(alcoholicDrink)
            message += f"alcoholicDrink = {alcoholicDrink}\n"
        if specialNeeds:
            sql += "specialNeeds = %s, "
            values.append(specialNeeds)
            message += f"specialNeeds = {specialNeeds}\n"
        if seatingPref1:
            sql += "seatingPreference1 = %s, "
            values.append(seatingPref1)
            message += f"seatingPreference1 = {seatingPref1}\n"
        if seatingPref2:
            sql += "seatingPreference2 = %s, "
            values.append(seatingPref2)
            message += f"seatingPreference2 = {seatingPref2}\n"

        # Remove the last comma and space, then add WHERE clause
        sql = sql.rstrip(", ") + " WHERE BID = %s AND email = %s"
        values.append(BID)
        values.append(email)

        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return message
        except Error as e:
            return f"Could not update User Registration in Banquet\nError code: {e}"

    def delete(self, BID, email):
        sql = "DELETE FROM UserBanquetRegistration WHERE BID = %s AND email = %s"
        values = [BID, email]
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return "User Registration deleted successfully from Banquet."
        except Error as e:
            return f"Could not delete User Registration from Banquet\nError code: {e}"

class Administrators(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = "Administrators"

    def create(self, adminEmail, adminName, adminLastName, adminPassword):
        sql = "INSERT INTO Administrators(adminEmail, adminName, adminLastName, adminPassword) FROM VALUES (%s, %s, %s, %s)"
        values = (adminEmail, adminName, adminLastName, adminPassword)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{adminName} {adminLastName} added successfully to Admins."
        except Error as e:
            return f"Could not create Administrator\nError code: {e}"

    def read(self):
        sql = "SELECT * FROM Administrators"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read Administrators\nError code: {e}"

    def update(self, adminEmail, adminPassword):
        sql = "UPDATE Administrators SET"
        values = []
        message = "Following fields are updated:\n"

        # appends all the information fields that need to be updated
        if adminEmail is not None:
            sql = sql + "adminEmail = %s"
            values.append(adminEmail)
            message += f"adminEmail = {adminEmail}\n"
        if adminPassword is not None:
            sql = sql + "adminPassword = %s"
            values.append(adminPassword)
            message += f"adminPassword = {adminPassword}\n"

        # removes last ", "
        sql = sql[:-2]
        sql = sql + "WHERE AdminEmail = %s"
        values.append(adminEmail)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return message
        except Error as e:
            return f"Could not update admin information\nError code: {e}"

    def delete(self, adminEmail):
        sql = "DELETE FROM Administrators WHERE AdminEmail = %s"
        values = [adminEmail]
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"Administrator {adminEmail} deleted successfully."
        except Error as e:
            return f"Could not delete Administrator\nError code: {e}"





