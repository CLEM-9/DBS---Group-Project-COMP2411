class RegisteredUsers:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    # creates users
    def create(self, email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization):
        sql = "INSERT INTO RegisteredUsers(email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization)
        self.cursor.execute(sql, values)
        self.connection.commit()
        return f"{firstName} {lastName} added successfully."

    # returns an array of arrays containing all information available
    def read(self):
        sql = "SELECT * FROM RegisteredUsers"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    # if the information is not provided by the user, pass None as argument
    def update(self, email, password, address, phone, attendeeType, affiliateOrganization):
        sql = "UPDATE RegisteredUsers SET "

        # appends all the information fields that need to be updated
        if email is not None:
            sql = sql + "email = %s, "
        if password is not None:
            sql = sql + "password = %s, "
        if address is not None:
            sql = sql + "address = %s, "
        if phone is not None:
            sql = sql + "phone = %s, "
        if attendeeType is not None:
            sql = sql + "attendeeType = %s, "
        if affiliateOrganization is not None:
            sql = sql + "affiliateOrganization = %s, "



    # deletes user with the primary key "email"
    def delete(self, email):
        sql = "DELETE FROM RegisteredUsers WHERE email = %s"
        values = email
        self.cursor.execute(sql, values)
        self.connection.commit()
        return "User deleted successfully."
import mysql.connector as mysql
from mysql.connector import Error

def register(cursor, connection,email, password, address, last_name, first_name, phone, attendee_type, affiliate_organization):
    try:
        cursor.execute(
            "INSERT INTO attendees (email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (email, password, address, last_name, first_name, phone, attendee_type, affiliate_organization)
        )
        connection.commit()
        print("Registration successful!")
        print("Loggin in...")
    except Error as e:
        print(f"Error: {e}")

def check_email(cursor, connection, email, password):
    try:
        attendee = 2
        admin = 1
        cursor.execute(
            "SELECT * FROM attendees WHERE email = %s AND password = %s",
            (email, password)
        )
        if_attendee = cursor.fetchone()
        cursor.execute(
            "SELECT * FROM Administrators WHERE adminEmail = %s AND adminPassword = %s",
            (email, password)
        )
        if_admin = cursor.fetchone()
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
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()

def drop_database(connection, cursor):
    try:
        cursor.execute("DROP DATABASE IF EXISTS banquet_database")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

def create_user(name, email):
    sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
    values = (name, email)
    cursor.execute(sql, values)
    connection.commit()
    print(f"User {name} added successfully.")