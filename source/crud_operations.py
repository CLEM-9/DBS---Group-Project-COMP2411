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