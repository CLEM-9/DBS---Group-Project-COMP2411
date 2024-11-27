from mysql.connector import Error
from pyexpat.errors import messages

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

    def update(self, emailID, email= None, password= None, phone= None, firstName= None, lastName= None, address= None, attendeeType= None, affiliateOrganization= None):
        sql = "UPDATE Attendees SET "
        values = []
        message = "Following fields are successfully updated:\n"

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

    def user_update_own_info(self, emailID, email= None, password= None, address= None, phone= None, attendeeType= None, affiliateOrganization= None):
        self.update(emailID, email=email, password=password, phone=phone, address=address, attendeeType=attendeeType,
                    affiliateOrganization=affiliateOrganization)

    def admin_update_attendee_info(self, emailID, phone= None, address= None, attendee_type= None, organization= None):
        return self.update(emailID, phone=phone, address=address, attendeeType=attendee_type,
                    affiliateOrganization=organization)

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

    def get(self, email):
        """
        Fetch full information of an attendee based on their email address.
        """
        sql = "SELECT * FROM Attendees WHERE email = %s"
        try:
            self.cursor.execute(sql, (email,))
            row = self.cursor.fetchone()
            if row:
                return {
                    'email': row[0],
                    'password': row[1],
                    'address': row[2],
                    'lastName': row[3],
                    'firstName': row[4],
                    'phone': row[5],
                    'attendeeType': row[6],
                    'affiliateOrganization': row[7],
                }
            return None
        except Error as e:
            print(f"Error fetching attendee by email: {e}")
            return None


class Banquet(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = "Banquet"

    # creates new banquet entry, banquetID is handled automatically by the database
    def create(self, banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats):
        sql = """
        INSERT INTO Banquet(banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats, registeredUsers)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats, 0)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"\n✅ Banquet '{banquetName}' created successfully! ✅"
        except Error as e:
            return f"\nCould not create banquet\nError code: {e}"

    # returns an array of arrays containing all information available
    def read(self):
        sql = "SELECT * FROM Banquet"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result  # Return all banquet details including new staff info
        except Error as e:
            return f"Could not read banquets\nError code: {e}"

    def read_by_filter(self, banquetName, banquetDate, banquetLocation, address):
        sql = """
        SELECT BID, banquetName, address, location, banquetDate, banquetTime, available, totalSeats
        FROM Banquet
        WHERE TRUE
        """
        values = []

        if banquetName:
            sql += " AND banquetName LIKE %s"
            values.append(f"%{banquetName}%")
        if banquetDate:
            sql += " AND banquetDate = %s"
            values.append(banquetDate)
        if banquetLocation:
            sql += " AND location = %s"
            values.append(banquetLocation)
        if address:
            sql += " AND address = %s"
            values.append(address)

        try:
            self.cursor.execute(sql, values)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Could not read banquets\nError code: {e}")
            return []

    def read_by_filter_and_staff(self, staffEmail, banquetName, banquetDate, banquetLocation, address):
        sql = "SELECT * FROM Banquet WHERE staffEmail = %s"
        values = [staffEmail]
        message = "Following fields are filtered:\n"

        if banquetName:
            sql += " AND banquetName LIKE %s"
            values.append(f"%{banquetName}%") 
            message += f"banquetName = {banquetName}\n"
        if banquetDate:
            sql += " AND banquetDate = %s"
            values.append(banquetDate)
            message += f"banquetDate = {banquetDate}\n"
        if banquetLocation:
            sql += " AND location = %s"
            values.append(banquetLocation)
            message += f"location = {banquetLocation}\n"
        if address:
            sql += " AND address = %s"
            values.append(address)
            message += f"address = {address}\n"

        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"Could not read banquets\nError code: {e}")
            return None
        
    def read_by_id(self, BID):
        sql = """
        SELECT BID, banquetName, address, location, banquetDate, banquetTime, available, totalSeats
        FROM Banquet
        WHERE BID = %s
        """
        values = [BID]
        try:
            self.cursor.execute(sql, values)
            return self.cursor.fetchone()
        except Error as e:
            print(f"Could not read banquet\nError code: {e}")
            return None
    
    def get_banquets_by_admin(self, staffEmail):
        sql = "SELECT * FROM Banquet WHERE staffEmail = %s"
        values = [staffEmail]
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            return f"Could not read banquets\nError code: {e}"

    def get_id(self, banquet_date, banquet_time, banquet_address):
        sql = "SELECT BID FROM Banquet WHERE banquetDate = %s AND banquetTime = %s AND address = %s"
        values = [banquet_date, banquet_time, banquet_address]
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchone()
            return result[0]
        except Error as e:
            return f"Could not read banquet\nError code: {e}"
         
    def update(self, BID, banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats):
        sql = "UPDATE Banquet SET "
        values = []
        message = "Following fields are updated:\n"

        if banquetName:
            sql += "banquetName = %s, "
            values.append(banquetName)
            message += f"banquetName = {banquetName}\n"
        if address:
            sql += "address = %s, "
            values.append(address)
            message += f"address = {address}\n"
        if location:
            sql += "location = %s, "
            values.append(location)
            message += f"location = {location}\n"
        if staffEmail:
            sql += "staffEmail = %s, "
            values.append(staffEmail)
            message += f"staffEmail = {staffEmail}\n"
        if banquetDate:
            sql += "banquetDate = %s, "
            values.append(banquetDate)
            message += f"banquetDate = {banquetDate}\n"
        if banquetTime:
            sql += "banquetTime = %s, "
            values.append(banquetTime)
            message += f"banquetTime = {banquetTime}\n"
        if available:
            sql += "available = %s, "
            values.append(available)
            message += f"available = {available}\n"
        if totalSeats:
            sql += "totalSeats = %s, "
            values.append(totalSeats)
            message += f"totalSeats = {totalSeats}\n"

        sql = sql.rstrip(", ")  # Remove the trailing comma
        sql += " WHERE BID = %s"
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


class BanquetDrink(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = "BanquetDrinks"

    def create(self, BID, drinkName, price):
        sql = "INSERT INTO BanquetDrinks(BID, drinkName, price) VALUES (%s, %s, %s)"
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
        sql = "SELECT drinkName, price FROM BanquetDrinks WHERE BID = %s"
        values = [BID]
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall()
            if result:
                return result  # Return a list of tuples (mealName, price)
            return []  # Return an empty list if no meals are found
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
        sql = "INSERT INTO BanquetMeals(BID, mealName, price) VALUES (%s, %s, %s)"
        values = (BID, mealName, price)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"Meal '{mealName}' added successfully to Banquet ID {BID}."
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
        sql = "SELECT mealName, price FROM BanquetMeals WHERE BID = %s"
        values = [BID]
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall()
            if result:
                return result  # Return a list of tuples (mealName, price)
            return []  # Return an empty list if no meals are found
        except Error as e:
            print(f"Could not fetch meals for the banquet. Error: {e}")
            return []

    def check_meal_exists(self, BID, mealName):
        sql = "SELECT * FROM BanquetMeals WHERE BID = %s AND mealName = %s"
        values = [BID, mealName]
        try:
            self.cursor.execute(sql, values)
            return self.cursor.fetchone() is not None
        except Error as e:
            print(f"Could not check if meal exists. Error: {e}")
            return False
         
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

    def delete(self, BID):
        sql = "DELETE FROM BanquetMeals WHERE BID = %s"
        values = [BID]
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{BID} deleted successfully."
        except Error as e:
            return f"Could not delete Meal from Banquet\nError code: {e}"


class UserBanquetRegistration(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = "UserBanquetRegistration"

    def create(self, BID, email, mealName, alcoholicDrink, specialNeeds, seatingPref1, seatingPref2):
        # SQL query to insert a new registration
        sql_insert = """
        INSERT INTO UserBanquetRegistration
        (BID, email, mealName, alcoholicDrink, specialNeeds, seatingPreference1, seatingPreference2)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # SQL query to decrement the available seats for the banquet
        sql_update_seats = """
                        UPDATE Banquet
                        SET registeredUsers = registeredUsers + 1
                        WHERE BID = %s AND registeredUsers < totalSeats
                        """

        try:
            # Insert the registration
            self.cursor.execute(
                sql_insert,
                (BID, email, mealName, alcoholicDrink, specialNeeds, seatingPref1, seatingPref2)
            )
            
            # Decrement the total seats, ensure no negative seats
            affected_rows = self.cursor.execute(sql_update_seats, [BID])
            if affected_rows == 0:
                raise ValueError("No available seats left for this banquet.")
            
            # Commit the transaction
            self.connection.commit()
            return f"\nRegistration successful!\nAssigned Seat: Information will be provided at a later date.\nBanquet {BID}\nMeal: {mealName}\nAlcoholic Drink: {alcoholicDrink}\n"

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

    def read_by_user_and_banquet(self, email, BID):
        sql = "SELECT * FROM UserBanquetRegistration WHERE email = %s AND BID = %s"
        values = [email, BID]
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

        # Dynamically add fields to update
        if mealName is not None:
            sql += "mealName = %s, "
            values.append(mealName)
            message += f"mealName = {mealName}\n"
        if alcoholicDrink is not None:
            sql += "alcoholicDrink = %s, "
            values.append(alcoholicDrink)
            message += f"alcoholicDrink = {alcoholicDrink}\n"
        if specialNeeds is not None:
            sql += "specialNeeds = %s, "
            values.append(specialNeeds)
            message += f"specialNeeds = {specialNeeds}\n"
        if seatingPref1 is not None:
            sql += "seatingPreference1 = %s, "
            values.append(seatingPref1)
            message += f"seatingPreference1 = {seatingPref1}\n"
        if seatingPref2 is not None:
            sql += "seatingPreference2 = %s, "
            values.append(seatingPref2)
            message += f"seatingPreference2 = {seatingPref2}\n"

        # Remove trailing comma and space
        sql = sql.rstrip(", ")

        # Add the WHERE clause if there are fields to update
        if values:
            sql += " WHERE BID = %s AND email = %s"
            values.extend([BID, email])
        else:
            return "No fields to update. Please provide at least one field to update."

        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return message
        except Error as e:
            return f"Could not update User Registration in Banquet\nError code: {e}"

    def delete(self, BID, email):
        sql = "DELETE FROM UserBanquetRegistration WHERE BID = %s AND email = %s"
        values = [BID, email]
        sql_update_seats = """
                        UPDATE Banquet
                        SET registeredUsers = registeredUsers - 1
                        WHERE BID = %s and registeredUsers > 0
                        """
        try:
            self.cursor.execute(sql_update_seats, [BID])
            self.cursor.execute(sql, values)
            self.connection.commit()
            return "User Registration deleted successfully."
        except Error as e:
            return f"Could not delete User Registration\nError code: {e}"


class Administrators(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = "Administrators"

    def create(self, adminEmail, adminName, adminLastName, adminPassword):
        sql = "INSERT INTO Administrators(adminEmail, adminName, adminLastName, adminPassword) VALUES (%s, %s, %s, %s)"
        values = (adminEmail, adminName, adminLastName, adminPassword)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{adminName} {adminLastName} added successfully to Admins."
        except Error as e:
            return f"Could not create Administrator\nError code: {e}"
        
    def get_staff_info(self, staffEmail):
        sql = "SELECT firstName, lastName FROM Attendees WHERE email = %s"
        values = [staffEmail]
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchone()
            if result:
                return {"staffFirstName": result[0], "staffLastName": result[1]}
            return None
        except Error as e:
            print(f"Error fetching staff info: {e}")
            return None
        
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


class ReportGeneration(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.table_name = "UserBanquetRegistration"
        
    def get_registration_status(self):
        sql = """
        SELECT b.banquetName, b.totalSeats, b.registeredUsers, 
               (b.totalSeats - b.registeredUsers) AS available
        FROM Banquet b
        GROUP BY b.BID
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_popular_meals(self):
        sql = """
        SELECT bm.mealName, COUNT(ubr.mealName) AS popularity
        FROM BanquetMeals bm
        LEFT JOIN UserBanquetRegistration ubr ON bm.mealName = ubr.mealName
        GROUP BY bm.mealName
        ORDER BY popularity DESC;
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_attendance_behavior(self):
        sql = """
        SELECT b.banquetDate, COUNT(r.email) AS attendance
        FROM Banquet b
        LEFT JOIN UserBanquetRegistration r ON b.BID = r.BID
        GROUP BY b.banquetDate
        ORDER BY b.banquetDate
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_attendee_type_summary(self):
        sql = """
        SELECT a.attendeeType, COUNT(r.email) AS registrations
        FROM Attendees a
        JOIN UserBanquetRegistration r ON a.email = r.email
        GROUP BY a.attendeeType
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    


