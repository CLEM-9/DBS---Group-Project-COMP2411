import mysql.connector as mysql
from mysql.connector import Error

class Database:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    # checks if logging_in user is attendee or administrator
    def check_email(self, connection, email, password):
        attendee = 2
        admin = 1
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
                return attendee
            elif if_admin:
                print("Login successful!")
                return admin
            else:
                print("Login failed. Please try again.")
                return 0

        except Error as e:
            print(f"Error code: {e}")

        finally:
            self.cursor.close()
            connection.close()

    def drop_database(self):
        try:
            self.cursor.execute("DROP DATABASE IF EXISTS banquet_database")
        except Error as e:
            print(f"Error: {e}")
        finally:
            self.cursor.close()
            self.connection.close()

class Tables:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    # gets the fetched result from the read operation and unpacks it in a string before return
    @staticmethod
    def unpack_read_info(info):
        message = ""
        for line in info:
            message = message + line + "\n"
        return message


class Attendees(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)

    # creates users
    def create(self, email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization):
        sql = "INSERT INTO Attendees(email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{firstName} {lastName} added successfully."
        except Error as e:
            return f"Could not add user\nError code: {e}"

    # returns an array of arrays containing all information available
    def read(self):
        sql = "SELECT * FROM Attendees"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            print(f"Error code: {e}")

    # if the information is not provided by the user, pass None as argument
    def update(self, email, password, address, phone, attendeeType, affiliateOrganization):
        sql = "UPDATE Attendees SET "
        values = []
        message = "Following fields are updated:\n"


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
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return message
        except Error as e:
            print(f"Error code: {e}")

    # deletes user with the primary key "email"
    def delete(self, email):
        sql = "DELETE FROM Attendees WHERE email = %s"
        values = email
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return "User deleted successfully."
        except Error as e:
            print(f"Error code: {e}")


class Banquet(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)

    # creates new banquet entry, banquetID is handled automatically by the database
    def create(self, banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats):
        sql = "INSERT INTO Banquet(banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (banquetName, address, location, staffEmail, banquetDate, banquetTime, available, totalSeats)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{banquetName} added successfully."
        except Error as e:
            return f"Could not add banquet\nError code: {e}"

    # returns an array of arrays containing all information available
    def read(self):
        sql = "SELECT * FROM Banquets"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read banquets\nError code: {e}"

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
            print(f"Error code: {e}")

    # deletes banquet with the primary key "BID"
    def delete(self, BID):
        sql = "DELETE FROM Banquet WHERE BID = %s"
        values = BID
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return "Banquet deleted successfully."
        except Error as e:
            print(f"Error code: {e}")

class Meal(Tables):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)

    def create(self, mealName, special, type):
        sql = "INSERT INTO Meal(mealName, special, type) VALUES (%s, %s, %s)"
        values = (mealName, special, type)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{mealName} added successfully."
        except Error as e:
            return f"Could not add meal\nError code: {e}

    def read(self):
        sql = "SELECT * FROM Meals"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            unpacked_result = Tables.unpack_read_info(result)
            return unpacked_result
        except Error as e:
            return f"Could not read meals\nError code: {e}"




