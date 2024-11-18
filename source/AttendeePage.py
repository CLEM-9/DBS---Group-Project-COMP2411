from crud_operations import Database
from crud_operations import Attendees
from crud_operations import Banquet

class AttendeePage:
    def __init__(self, cursor, connection, email):
        self.cursor = cursor
        self.connection = connection
        self.email = email
        self.database = Database(cursor, connection)
        self.attendees = Attendees(cursor, connection)
        self.banquet = Banquet(cursor, connection)

    def display(self):
        print("User Page")
        print("1. Search for a Banquet")
        print("2. Register for a Banquet")
        print("3. Update Account Information")
        print("4. Search in Registered Banquets")
        print("5. Logout")
        choice = input("Enter choice: ")
        if choice == '1':
            self.search_banquet()
        elif choice == '2':
            self.register_for_banquet()
        elif choice == '3':
            self.update_account_info()
        elif choice == '4':
            self.search_registered_banquets()
        elif choice == '5':
            print("Logging out...")
            exit()
        else:
            print("Invalid choice.")
            self.display()

    # Define other methods like search_banquet(), register_for_banquet(), etc., here
    def update_account_info(self):
        print("\nEnter Updated Information")
        email = self.email
        password = input("Enter Password: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        phone = input("Enter Phone Number: ")
        address = input("Enter Address: ")
        attendee_type = input("Enter Attendee Type (Student, Alumni, Staff, Guest): ")
        affiliate_organization = input("Enter Affiliate Organization: ")

        # Validate inputs
        self.attendees.update(email, password, phone, address, attendee_type, affiliate_organization)
        print("Account information updated.")
        self.display()

    
    