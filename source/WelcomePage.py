from AdminPage import AdminPage
from AttendeePage import AttendeePage
from crud_operations import Database
from crud_operations import Attendees

class WelcomePage:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection
        self.database = Database(cursor, connection)

    def display(self):
        print("\nWelcome to the Banquet Registration System!")
        print("Please login to continue.")
        print("1. Log in")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            self.login()
        elif choice == '2':
            self.register_attendee()
        elif choice == '3':
            self.exit_program()
        else:
            print("Invalid choice. Please try again.")
            self.display()

    def login(self):
        print("\nEnter Login Information")
        email = [input("Enter Email: ").strip()]
        password = input("Enter Password: ")
        user_type = self.database.check_email(self.connection, email[0], password)

        if user_type is None:
            print("Invalid credentials.")
            self.display()
        elif user_type[0] == "Administrator":
            admin_page = AdminPage(self.cursor, self.connection, email[0])
            admin_page.display()
        elif user_type[0] == "Attendee":
            attendee_page = AttendeePage(self.cursor, self.connection, email[0])
            attendee_page.display()

    def register_attendee(self):
        print("\nEnter Registration Information")
        email = [input("Enter Email: ").strip()]
        password = input("Enter Password: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        phone = input("Enter Phone Number: ")
        address = input("Enter Address: ")
        attendee_type = input("Enter Attendee Type (Student, Alumni, Staff, Guest): ")
        affiliate_organization = input("Enter Affiliate Organization: ")

        # Validate inputs
        if self.database.check_email_exists(self.connection, email):
            print("Email already exists.")
        elif attendee_type not in ["Student", "Alumni", "Staff", "Guest"]:
            print("Invalid attendee type.")
        else:
            attendees = Attendees(self.cursor, self.connection)
            attendees.create(
                email[0], password, address, last_name, first_name, phone, attendee_type, affiliate_organization
            )
            print(f"Registration successful! Welcome, {first_name}.\n")
            attendee_page = AttendeePage(self.cursor, self.connection, email[0])
            attendee_page.display()

    def exit_program(self):
        print("Exiting program...")
        exit()