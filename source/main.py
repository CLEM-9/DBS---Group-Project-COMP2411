from db_connection import get_db_connection
import mysql.connector as mysql
from mysql.connector import Error
from crud_operations import *
from db_setup import initialize_database

def register_attendee():
    connection = get_db_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    #write the warnings to the user
    cursor = connection.cursor()
    print("Enter Attendee Information")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    address = input("Enter Address: ")
    last_name = input("Enter Last Name: ")
    first_name = input("Enter First Name: ")
    phone = input("Enter Phone: ")
    attendee_type = input("Enter Attendee Type (Student, Alumni, Staff, Guest): ")
    affiliate_organization = input("Enter Affiliate Organization: ")

    register(cursor, connection, email, password, address, last_name, first_name, phone, attendee_type, affiliate_organization)
    result = check_email(cursor, connection, email, password)

def login():
    connection = get_db_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return

    cursor = connection.cursor()
    print("Enter Login Information")
    email = input("Enter Email: ")
    password = input("Enter Password: ")

    result = check_email(cursor, connection, email, password)

    return result

def exit_program():
    connection = get_db_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    cursor = connection.cursor()
    
    drop_database(connection, cursor)
    
    print("Exiting program...")
    exit()

def attend_banquet():
    connection= get_db_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    cursor = connection.cursor()
    print("Choose banquet to attend")
    cursor.execute("SELECT * FROM Banquet")
    result = cursor.fetchall()
    for row in result:
        print(row)
    banquet = input("Enter Banquet ID: ")
    cursor.execute("SELECT totalSeats, available FROM Banquet WHERE BID = %s", (banquet,))
    result = cursor.fetchone()
    available_seats, isAvailable = result
    if available_seats > 0 and isAvailable == "Y":
        print("Enter Banquet Registration Information")
        email = input("Enter Email: ")
        meal = input("Enter Meal Name: ")
        alcoholic_drink = input("Enter Alcoholic Drink (Yes/No): ")
        seat_assignment = input("Enter Seat Assignment: ")
        special_needs = input("Enter Special Needs: ")
        seating_preference1 = input("Enter Seating Preference 1: ")
        seating_preference2 = input("Enter Seating Preference 2: ")
        cursor.execute(
            "INSERT INTO UserBanquetRegistration (BID, email, mealName, alcoholicDrink, seatAssignment, specialNeeds, seatingPreference1, seatingPreference2) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (banquet, email, meal, alcoholic_drink, seat_assignment, special_needs, seating_preference1, seating_preference2)
        )
        cursor.execute("UPDATE Banquet SET totalSeats= totalSeats - 1 WHERE BID = %s", (banquet,))
        connection.commit()
        print("Banquet Registration successful!")
    elif available_seats == 0:
        print("Banquet is full. Please choose another banquet.")
    
# Function to show main menu
def main_menu():
    print("Welcome to the Banquet Registration System")
    print("1. Register")
    print("2. Log In")
    print("3. Exit")

    choice = input("Select an option: ")
    if choice == "1":
        register_attendee()
        print("1. Attend Banquet")
        print("2. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            attend_banquet()
        elif choice == "2":
            exit_program()
    elif choice == "2":
        result = login()
        if result == 2:
            print("1. Attend Banquet")
            print("2. Exit")
            choice = input("Select an option: ")
            if choice == "1":
                attend_banquet()
            elif choice == "2":
                exit_program()
        elif result == 1:
            print("1. Exit")
            choice = input("Select an option: ")
            if choice == "1":
                exit_program()
    elif choice == "3":
        exit_program()
        

# Run the main menu
if __name__ == "__main__":
    if get_db_connection() is None:
        initialize_database()
    main_menu()