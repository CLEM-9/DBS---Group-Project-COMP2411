import datetime
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
        self.banquet_registration = UserBanquetRegistration(cursor, connection)
        
    def is_valid_email(self, email):
        pattern = r'^[^@]+@[^@]+\.[^@]+$'
        return re.match(pattern, email) is not None

    def display(self):
        print("\n" + "=" * 50)
        print(f"👤 Welcome to Your Dashboard ({self.email})")
        print("=" * 50)
        print("1️⃣  Search for a Banquet")
        print("2️⃣  Register for a Banquet")
        print("3️⃣  Update Account Information")
        print("4️⃣  View Registered Banquets")
        print("5️⃣  Logout")
        print("=" * 50)
        
        choice = input("👉 Enter your choice (1-5): ").strip()
        
        if choice == '1':
            self.search_banquet()
        elif choice == '2':
            self.register_for_banquet()
        elif choice == '3':
            self.update_account_info()
        elif choice == '4':
            self.search_registered_banquets()
        elif choice == '5':
            self.logout()
        else:
            print("\n❌ Invalid choice. Please try again. ❌")
            self.display()
    
    def update_account_info(self):
        print("\n" + "=" * 50)
        print("✏️ Update Your Account Information")
        print("=" * 50)
        print("Leave fields blank to keep them unchanged.")
        
        email = input("📧 New Email: ").strip() or self.email
        password = input("🔒 New Password: ").strip()
        first_name = input("👤 New First Name: ").strip()
        last_name = input("👤 New Last Name: ").strip()
        phone = input("📞 New Phone Number: ").strip()
        address = input("🏠 New Address: ").strip()
        attendee_type = input("🎓 New Attendee Type (Student, Alumni, Staff, Guest): ").strip()
        affiliate_organization = input("🏢 New Affiliate Organization: ").strip()
        
        result = self.attendees.update(self.email, email, password, phone, first_name, last_name, address,
                                       attendee_type, affiliate_organization)
        print(result)
        self.display()

    def search_banquet(self):
        print("\n" + "=" * 50)
        print("🔍 Search for a Banquet")
        print("=" * 50)
        print("Enter the details to filter, or leave fields blank to skip.\n")
        print("📝 Note down the Banquet ID which you want to register.")
        
        banquet_name = input("🏷️  Banquet Name: ").strip()
        banquet_date = input("📅 Banquet Date (YYYY-MM-DD): ").strip()
        banquet_address = input("🏠 Banquet Address: ").strip()
        banquet_location = input("📍 Banquet Location: ").strip()

        print("\nSearching for banquets... 🔄")
        result = self.banquet.read_by_filter(banquet_name, banquet_date, banquet_location, banquet_address)

        if result:
            print("\n✅ Search Results:\n")
            for i, banquet in enumerate(result, start=1):
                banquet_date_time = f"{banquet[6]} at {banquet[7]}"
                print(f"""
        Banquet {i}:
            🆔 BID: {banquet[0]}
            🏷️ Name: {banquet[1]}
            🏠 Address: {banquet[2]}
            📍 Location: {banquet[3]}
            📅 Date & Time: {banquet_date_time}
            🟢 Available: {banquet[8]}
            🪑 Total Seats: {banquet[9]}
            📞 Contact: {banquet[4]} {banquet[5]}
                """)
        else:
            print("\n❌ No banquets found matching the criteria.")

        self.display()
        
    def register_for_banquet(self):
        print("\n" + "=" * 50)
        print("📝 Register for a Banquet")
        print("=" * 50)
        banquet_id = input("🆔 Enter Banquet ID: ").strip()

        # Check if user already joined the banquet
        if self.banquet_registration.read_by_user_and_banquet(self.email, banquet_id):
            print("❌ You have already registered for this banquet.")
            self.display()
            return

        # Check if the banquet ID exists
        banquet_details = self.banquet.read_by_id(banquet_id)
        if not banquet_details:
            print("❌ Banquet ID not found. Please try again.")
            self.register_for_banquet()
            return

        # Show available meals
        print("\n🍽️  Banquet Meals:")
        banquet_meals = self.meals.show_meals(banquet_id)

        # Display available meals
        if banquet_meals:
            print("\n".join([f"{meal[0]}, ${meal[1]:.2f}" for meal in banquet_meals]))
        else:
            print("❌ No meals found for this banquet.")
            return  # Exit the process if no meals are available

        meal_name = input("👉 Enter Meal Name: ").strip()
        if meal_name:
            # Extract only the meal names for validation
            available_meals = [meal[0] for meal in banquet_meals]
            while meal_name not in available_meals:
                print("❌ Invalid meal name. Please choose from the list below:")
                print("\n".join(available_meals))  # Display available meal names
                meal_name = input("👉 Enter Meal Name: ").strip()
                # Show available drinks
                print("\n🥂 Banquet Drinks:")
                banquet_drinks = self.drinks.show_drinks(banquet_id)
                print(banquet_drinks)

        alcoholic_drink = input("🍷 Do you want an alcoholic drink? (Yes/No): ").strip()
        while alcoholic_drink not in ["Yes", "No"]:
            print("❌ Invalid choice. Please enter 'Yes' or 'No'.")
            alcoholic_drink = input("🍷 Do you want an alcoholic drink? (Yes/No): ").strip()

        # Collect additional information
        special_needs = input("💬 Special Needs (or press Enter for None): ").strip() or "None"
        print("👥 Seating Preferences:")
        seating_preference1 = input("👉 Enter Email of First Person (or press Enter to skip): ").strip()
        seating_preference2 = input("👉 Enter Email of Second Person (or press Enter to skip): ").strip()
        # Validate seating preferences
        while seating_preference1 and self.database.check_email_exists(self.connection, seating_preference1):
            print("❌ Email address already registered. Please try again.")
            seating_preference1 = input("👉 Enter Email of First Person (or press Enter to skip): ").strip()
        while seating_preference2 and self.database.check_email_exists(self.connection, seating_preference2):
            print("❌ Email address already registered. Please try again.")
            seating_preference2 = input("👉 Enter Email of Second Person (or press Enter to skip): ").strip()
        if seating_preference1 or seating_preference2:
            while (seating_preference1 and not self.is_valid_email(seating_preference1)) or \
                (seating_preference2 and not self.is_valid_email(seating_preference2)):
                print("❌ Invalid email address. Please try again.")
                seating_preference1 = input("👉 Enter Email of First Person (or press Enter to skip): ").strip()
                seating_preference2 = input("👉 Enter Email of Second Person (or press Enter to skip): ").strip()

        # Register for the banquet
        result = self.banquet_registration.create(
            banquet_id, self.email, meal_name, alcoholic_drink, special_needs, seating_preference1 or None, seating_preference2 or None
        )
        print("\nRegistered successfully!")
        self.display()

    def format_datetime(self, date, time):
        try:
            date_obj = datetime.datetime.strptime(str(date), "%Y-%m-%d")
            time_obj = datetime.datetime.strptime(str(time), "%H:%M:%S")
            formatted_date = date_obj.strftime("%B %d, %Y")
            formatted_time = time_obj.strftime("%I:%M %p")
            return f"{formatted_date} at {formatted_time}"
        except Exception:
            return "Invalid Date/Time"

    def search_registered_banquets(self):
        print("\n" + "=" * 50)
        print("📋 Registered Banquets")
        print("=" * 50)
        
        registered_banquets = self.banquet_registration.read_by_user(self.email)
        if not registered_banquets.strip():
            print("❌ No registered banquets.")
            self.display()
            return

        banquet_entries = registered_banquets.split("\n")
        for i, entry in enumerate(banquet_entries, start=1):
            try:
                fields = entry.split(", ")
                BID = fields[0]
                banquet_details = self.banquet.read_by_id(BID)
                if banquet_details:
                    banquet_date_time = self.format_datetime(banquet_details[7], banquet_details[8])
                    print(f"""
Banquet {i}:
    🆔 BID: {BID}
    🏷️  Name: {banquet_details[1]}
    🏠 Address: {banquet_details[2]}
    📍 Location: {banquet_details[3]}
    📅 Date & Time: {banquet_date_time}
    🪑 Seat No: {fields[4]}
    🍽️  Meal: {fields[2]}
    🥂 Alcoholic Drink: {fields[3]}
    💬 Special Needs: {fields[5]}
    👥 Seating Preferences: {fields[7]}, {fields[8]}
    📞 Contact: {banquet_details[4]} {banquet_details[5]}
""")
                else:
                    print(f"❌ Banquet {i}: Could not fetch details for BID {BID}")
            except IndexError:
                print(f"❌ Error processing entry: {entry}")

        print("\n1️⃣  Delete a Registration")
        print("2️⃣  Edit your Registration")
        print("3️⃣  Go back to Dashboard")
        choice = input("👉 Enter your choice (1/2/3): ").strip()

        if choice == '1':
            self.delete_registration()
        elif choice == '2':
            self.edit_registration()
        elif choice == '3':
            self.display()
        else:
            print("❌ Invalid choice. Please try again.")
            self.search_registered_banquets()

    def delete_registration(self):
        print("\n" + "=" * 50)
        print("🗑️ Delete a Registration")
        print("=" * 50)
        
        choice = input("❓ Are you sure you want to delete a registration? (Yes/No): ").strip()
        if choice.lower() == 'no':
            self.display()
        elif choice.lower() == 'yes':
            BID = input("🆔 Enter Banquet ID to delete the registration: ").strip()
            if not self.banquet_registration.read_by_user_and_banquet(self.email, BID):
                print("❌ You have not registered for this banquet.")
                self.display()
            elif not BID:
                print("❌ Banquet ID is required to delete registration.")
                self.delete_registration()
            result = self.banquet_registration.delete(BID, self.email)
            print(result)
            self.display()
        else:
            print("❌ Invalid choice. Please try again.")
            self.delete_registration()

    def edit_registration(self):
        print("\n" + "=" * 50)
        print("✏️ Edit your Registration")
        print("=" * 50)
        print("Enter the details to update, or press enter to skip but you have to provide a Banquet ID\n")
        BID = input("🆔 Enter Banquet ID: ").strip()
        if not BID:
            print("❌ Banquet ID is required to update registration.")
            self.search_registered_banquets()
        elif not self.banquet_registration.read_by_user_and_banquet(self.email, BID):
            print("❌ You have not registered for this banquet or there is no Banquet with this BID.")
            self.display()
            
        meals = self.meals.show_meals(BID)  # Fetch meals for the banquet
        print("\n🍽️  Banquet Meals:")

        if meals:
            # Display available meals in a formatted manner
            print("\n".join([f"{meal[0]}, ${meal[1]:.2f}" for meal in meals]))
        else:
            print("❌ No meals found for this banquet.")
            return  # Exit if no meals are available

        meal_name = input("🍽️  Enter New Meal Name: ").strip() or None
        if meal_name:
            # Extract the list of valid meal names for the banquet
            available_meals = [meal[0] for meal in meals]
            while meal_name not in available_meals:
                print("❌ Invalid meal name. Please choose from the list below:")
                print("\n".join(available_meals))  # Display valid meal names
                meal_name = input("👉 Enter Meal Name: ").strip()
                
        drink_options = ["Yes", "No"]
        alcoholic_drink = input("🍷 Do you want an alcoholic drink? (Yes/No): ").strip() or None
        if alcoholic_drink:
            while alcoholic_drink not in drink_options:
                print("❌ Invalid choice. Please enter 'Yes' or 'No'.")
                alcoholic_drink = input("🍷 Do you want an alcoholic drink? (Yes/No): ").strip()
                
        special_needs = input("💬 Special Needs (or press Enter for None): ").strip() or None
        
        seating_preference1 = input("👉 Enter Email of First Person (or press Enter to skip): ").strip() or None
        seating_preference2 = input("👉 Enter Email of Second Person (or press Enter to skip): ").strip() or None
        if seating_preference1 or seating_preference2:
            while (seating_preference1 and not self.is_valid_email(seating_preference1)) or (seating_preference2 and not self.is_valid_email(seating_preference2)):
                print("❌ Invalid email address. Please try again.")
                seating_preference1 = input("👉 Enter Email of First Person (or press Enter to skip): ").strip()
                seating_preference2 = input("👉 Enter Email of Second Person (or press Enter to skip): ").strip()
        print("\nUpdating registration... 🔄")
        result = self.banquet_registration.update(
            BID, self.email, meal_name, alcoholic_drink, special_needs, seating_preference1, seating_preference2
        )
        self.display()
        
    def logout(self):
        print("\n" + "=" * 50)
        print("👋 Logging out... Goodbye!")
        print("=" * 50)
        exit()