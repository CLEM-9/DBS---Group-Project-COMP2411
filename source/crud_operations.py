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
                "SELECT * FROM attendees WHERE email = %s AND password = %s",
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

class Attendees(Database):
    def __init__(self):
        super().__init__(self.cursor, self.connection)

    # creates users
    def create(self, email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization):
        sql = "INSERT INTO attendees(email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization)
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            return f"{firstName} {lastName} added successfully."
        except Error as e:
            return f"Could not add user\nError code: {e}"

    # returns an array of arrays containing all information available
    def read(self):
        sql = "SELECT * FROM attendees"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    # if the information is not provided by the user, pass None as argument
    def update(self, email, password, address, phone, attendeeType, affiliateOrganization):
        sql = "UPDATE attendees SET "
        values = []
        message = "Following fields are updated:\n"

        # appends all the information fields that need to be updated
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
        self.cursor.execute(sql, values)
        self.connection.commit()
        return message

    # deletes user with the primary key "email"
    def delete(self, email):
        sql = "DELETE FROM attendees WHERE email = %s"
        values = email
        self.cursor.execute(sql, values)
        self.connection.commit()
        return "User deleted successfully."


