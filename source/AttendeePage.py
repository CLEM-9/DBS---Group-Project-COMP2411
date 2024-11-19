import re
from crud_operations import Database
from crud_operations import Attendees
from crud_operations import Banquet
from crud_operations import UserBanquetRegistration
from crud_operations import BanquetMeal
from crud_operations import BanquetDrinks

class AttendeePage:
    def __init__(self, cursor, connection, email):
        self.cursor = cursor
        self.connection = connection
        self.email = email
        self.database = Database(cursor, connection)
        self.attendees = Attendees(cursor, connection)
        self.banquet = Banquet(cursor, connection)
        self.meals = BanquetMeal(cursor, connection)
        self.drinks = BanquetDrinks(cursor, connection)
        self.banquet_registration= UserBanquetRegistration(cursor, connection)
        
    def is_valid_email(self, email):
        pattern = r'^[^@]+@[^@]+\.[^@]+$'
        return re.match(pattern, email) is not None
    
    def display(self):
        print("\nUser Page")
        print("1. Search for a Banquet")
        print("2. Register for a Banquet")
        print("3. Update Account Information")
        print("4. Registered Banquets")
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
        banquet_id = input("Enter Banquet ID: ").strip()
        email = self.email

        # Show available meals
        print("Banquet Meals:")
        banquet_meals =self.meals.show_meals(banquet_id)
        print(banquet_meals)
        meal_name = input("Enter Meal name: ").strip()
        while banquet_meals.find(meal_name) == -1:
            print("Invalid meal name.")
            meal_name = input("Enter Meal name: ").strip()
        # Show available drinks
        print("Banquet Drinks:")
        banquet_drinks = self.drinks.show_drinks(banquet_id)
        print(banquet_drinks)
        alcoholicDrink = input("Do you want to have an alcoholic drink? (Yes/No): ").strip()
        while alcoholicDrink not in ["Yes", "No"]:
            print("Invalid choice.")
            alcoholicDrink = input("Do you want to have an alcoholic drink? (Yes/No): ").strip()
        # Collect special needs and seating preferences
        special_needs = input("Enter any special needs (press enter if none): ").strip() or "None"
        print("If you do not have a seating preference, please press enter.")
        seating_preference1 = input("Enter the first person email you want to sit next to: ").strip()
        seating_preference2 = input("Enter the second person email you want to sit next to: ").strip()

        # Validate seating preferences
        if seating_preference1 or seating_preference2:
            while (seating_preference1 and not self.is_valid_email(seating_preference1)) or \
                (seating_preference2 and not self.is_valid_email(seating_preference2)):
                print("Invalid email address. Please try again.")
                seating_preference1 = input("Enter the first person email you want to sit next to: ").strip()
                seating_preference2 = input("Enter the second person email you want to sit next to: ").strip()

        # Call the create method
        result = self.banquet_registration.create(
            banquet_id, email, meal_name, alcoholicDrink, special_needs, seating_preference1 or None, seating_preference2 or None
        )
        print(result)
        print("Registration successful.")
        self.display()
        
    def search_registered_banquets(self):
        print("\nRegistered Banquets")
        
        # Fetch registered banquets for the user
        registered_banquets = self.banquet_registration.read_by_user(self.email)

        # If there are no registered banquets, display a message
        if not registered_banquets.strip():
            print("No registered banquets.")
            self.display()
            return

        # Split the registered banquets into individual entries
        banquet_entries = registered_banquets.split("\n")

        for i, entry in enumerate(banquet_entries, start=1):
            try:
                # Parse the entry fields
                fields = entry.split(", ")
                BID = fields[0]  # Extract the Banquet ID
                
                # Fetch detailed banquet information using BID
                banquet_details = self.banquet.read_by_id(BID)
                if banquet_details:
                    banquet_info = f"""
        Banquet {i}:
            Name: {banquet_details[0][1]}
            Address: {banquet_details[0][2]}
            Location: {banquet_details[0][3]}
            Date: {banquet_details[0][5]}
            Time: {banquet_details[0][6]}
            Available: {banquet_details[0][7]}
            Total Seats: {banquet_details[0][8]}
        Registration Info:
            Meal Name: {fields[2]}
            Alcoholic Drink: {fields[3]}
            Seating Assignment: {fields[4]}
            Special Needs: {fields[5]}
            Seating Preference 1: {fields[7]}
            Seating Preference 2: {fields[8]}
        """
                    print(banquet_info)
                else:
                    print(f"Banquet {i}: Unable to fetch details for BID {BID}")
            except IndexError:
                print(f"Error processing entry: {entry}")

        # Provide options to the user
        print("\n1. Delete a registration")
        print("2. Go back")
        choice = input("Enter choice: ")
        if choice == '1':
            self.delete_registration()
        elif choice == '2':
            self.display()
        else:
            print("Invalid choice.")
            self.search_registered_banquets()
        
    def delete_registration(self):
        print("Are you sure to delete the registration? (Yes/No)")
        choice = input("Enter choice: ")
        if choice == 'No':
            self.display()
        elif choice == 'Yes':
            print("\nEnter the Banquet ID to delete the registration.")
            BID = input("Enter Banquet ID: ").strip()
            email = self.email
            print(self.banquet_registration.delete(BID, email))
            self.display()
        else:
            print("Invalid choice.")
            self.delete_registration()
