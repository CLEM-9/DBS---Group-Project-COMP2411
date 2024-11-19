from crud_operations import Database
from crud_operations import Attendees
from crud_operations import Banquet
from crud_operations import UserBanquetRegistration

class AttendeePage:
    def __init__(self, cursor, connection, email):
        self.cursor = cursor
        self.connection = connection
        self.email = email
        self.database = Database(cursor, connection)
        self.attendees = Attendees(cursor, connection)
        self.banquet = Banquet(cursor, connection)
        self.banquet_registration= UserBanquetRegistration(cursor, connection)

    def display(self):
        print("\nUser Page")
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
    
    
    def update_account_info(self):
        print("\nEnter the information you want to update, or press enter to keep the same.")
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        phone = input("Enter Phone Number: ")
        address = input("Enter Address: ")
        attendee_type = input("Enter Attendee Type (Student, Alumni, Staff, Guest): ")
        affiliate_organization = input("Enter Affiliate Organization: ")
        
        if email == "":
            email = self.email

        print(self.attendees.update_everything(email, password, phone, first_name, last_name, address, attendee_type, affiliate_organization, self.email))
        self.display()

    def search_banquet(self):
        print("\nEnter the information you want to search for, or press enter to skip. Please note down the Banquet id to register for the banquet later.")
        banquet_name = input("Enter Banquet Name: ")
        banquet_date = input("Enter Banquet Date (YYYY-MM-DD): ")
        banquet_address = input("Enter Banquet Adress: ")
        banquet_location = input("Enter Banquet Location: ")

        print(self.banquet.read_by_filter(banquet_name, banquet_date, banquet_location, banquet_address))
        self.display()
        
    def register_for_banquet(self):
        print("\nEnter the Banquet ID to register for the banquet.")
        banquet_id = input("Enter Banquet ID: ")
        
    