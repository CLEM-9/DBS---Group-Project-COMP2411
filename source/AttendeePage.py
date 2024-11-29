import datetime

def print_user_tips():
    print("\n" + "=" * 54)
    print("🚪 Press: 'Enter' to leave information fields empty")
    print("🚪 Type:  '##'    to quit any operation")

class AttendeePage:
    def __init__(self, cursor, connection, email, database):
        self.cursor = cursor
        self.connection = connection
        self.email = email
        self.db = database
        self.userLogged = True

    def display(self):
        while self.userLogged:
            print_user_tips()
            print("=" * 54)
            print(f"👤 Welcome to Your Dashboard ({self.email})")
            print("=" * 54)
            print("1️⃣  Search for a Banquet")
            print("2️⃣  Register for a Banquet")
            print("3️⃣  Update Account Information")
            print("4️⃣  View Registered Banquets")
            print("5️⃣  Logout")
            print("=" * 54)

            choice = input("👉 Enter your choice (1-5): ").strip()

            successful_operation = False
            if choice == '1':
                while not successful_operation:
                    successful_operation= self.search_banquet()
            elif choice == '2':
                while not successful_operation:
                    successful_operation = self.register_for_banquet()
            elif choice == '3':
                while not successful_operation:
                    successful_operation = self.update_account_info()
            elif choice == '4':
                while not successful_operation:
                    successful_operation = self.search_registered_banquets()
                    if successful_operation:    # if search_registered_banquet is successful
                        successful_operation = False  # resets state
                        while not successful_operation: # proceeds to next operation
                            successful_operation = self.delete_edit_registration()
                    else:
                        successful_operation = not successful_operation
            elif choice == '5':
                self.logout()
            else:
                print("❌ Invalid choice. Please try again. ❌\n")
        return True

    def update_account_info(self):
        print_user_tips()
        print("=" * 54)
        print("✏️ Update Your Account Information")
        print("=" * 54)
        print("Leave fields blank to keep them unchanged.")

        # false parameter means the input can be null
        email = self.db.input_email(empty_not_allowed= False) or self.email
        if self.db.back(email): return True

        password = self.db.input_password(empty_not_allowed= False) or None
        if self.db.back(password): return True

        first_name = self.db.input_name("First", empty_not_allowed= False) or None
        if self.db.back(first_name): return True

        last_name = self.db.input_name("Last", empty_not_allowed= False) or None
        if self.db.back(last_name): return True

        phone = self.db.input_phone(empty_not_allowed= False) or None
        if self.db.back(phone): return True

        address = self.db.input_address(empty_not_allowed= False) or None
        if self.db.back(address): return True

        attendee_type = self.db.input_attendee_type(empty_not_allowed= False) or None
        if self.db.back(attendee_type): return True

        affiliate_organization = self.db.input_affiliate_organization(empty_not_allowed= False) or None
        if self.db.back(affiliate_organization): return True

        result = self.db.attendees.update(self.email, email, password, phone, first_name, last_name, address,
                                       attendee_type, affiliate_organization)
        print(result)
        return True

    def search_banquet(self):
        print_user_tips()
        print("=" * 54)
        print("🔍 Search for a Banquet")
        print("=" * 54)
        print("📝 Note down the Banquet ID which you want to register.")

        banquet_name = self.db.input_banquet_name(empty_not_allowed= False)
        if self.db.back(banquet_name):
            return True

        banquet_date = self.db.get_valid_date("📅 Enter Banquet Date (YYYY-MM-DD): ", allow_empty=True)
        if self.db.back(banquet_date):
            return True

        banquet_address = self.db.input_address(empty_not_allowed= False)
        if self.db.back(banquet_address):
            return True

        banquet_location = self.db.input_location(empty_not_allowed= False)
        if self.db.back(banquet_location):
            return True

        print("\nSearching for banquets... 🔄")

        result = self.db.banquet.read_by_filter(banquet_name, banquet_date, banquet_location, banquet_address)

        if result:
            print("\n✅ Search Results:\n")
            for i, banquet in enumerate(result, start=1):
                banquet_date_time = f"{banquet[4]} at {banquet[5]}"
                available = "Yes" if banquet[6] else "No"
                print(f"""
Banquet {i}:
    🆔 BID: {banquet[0]}
    🏷️ Name: {banquet[1]}
    🏠 Address: {banquet[2]}
    📍 Location: {banquet[3]}
    📅 Date & Time: {banquet_date_time}
    🟢 Available: {available}
    🪑 Total Seats: {banquet[7]}
    """)
        else:
            print("\n❌ No banquets found matching the criteria.")
        return True # takes back to main selection

    def register_for_banquet(self):
        print_user_tips()
        print("=" * 54)
        print("📝 Register for a Banquet")
        print("=" * 54)

        banquet_id = input("🆔 Enter Banquet ID: ").strip()
        while not banquet_id:
            banquet_id = input("❌ Please insert a Banquet ID: ").strip()

        # returning True will stop the registration loop and effectively let the user back
        if self.db.back(banquet_id):
            return True # takes back to main selection

        # Check if the banquet ID exists
        banquet_details = self.db.banquet.read_by_id(banquet_id)
        if not banquet_details:
            print("❌ Banquet ID not found. Please try again.")
            return False  # user tries again

        # Check if user already joined the banquet
        if self.db.user_banquet_registration.read_by_user_and_banquet(self.email, banquet_id):
            print("❌ You have already registered for this banquet.")
            return True # takes back to main selection

        #fetches meals
        banquet_meals = self.db.banquet_meal.show_meals(banquet_id)
        if not banquet_meals:
            print("❌ No meals found for this banquet.")
            return True  # Exit the process if no meals are available

        #fetches drinks
        banquet_drinks = self.db.banquet_drink.show_drinks(banquet_id)
        if not banquet_drinks:
            print("❌ No drinks found for this banquet.")
            return True  # Exit the process if no meals are available

        # Show available meals
        print("\n🍽️  Banquet Meals:")
        print("\n".join([f"\t{meal[0]}, ${meal[1]:.2f}" for meal in banquet_meals]) + "\n")

        # Formats meal lists to pass into input_meal_name
        available_meals = []
        for meal in banquet_meals:
            available_meals.append(meal[0])

        # Extract only the meal names for validation
        meal_name = self.db.input_meal_name(available_meals)
        if self.db.back(meal_name):
            return True

        # Display available Drinks
        print("\n🍽️  Banquet Drinks:")
        print("\n".join([f"\n{drink[0]}, ${drink[1]:.2f}" for drink in banquet_drinks]) + "\n")

        alcoholic_drink = self.db.input_alcoholic_drink()
        if self.db.back(alcoholic_drink):
            return True
        if alcoholic_drink:
            alcoholic_drink = (alcoholic_drink == "yes")    # saved as bit -> if "yes" then 1 else 0

        # Collect additional information
        special_needs = input("💬 Special Needs (or press Enter for None): ").strip() or "None"
        if self.db.back(special_needs):
            return True

        print("👥 Seating Preferences:")
        seating_preference1 = self.db.input_seating_preference("first")
        seating_preference2 = None
        if self.db.back(seating_preference1):
            return True

        if seating_preference1:
            seating_preference2 = self.db.input_seating_preference("second")
            if self.db.back(seating_preference2):
                return True

       # Register for the banquet
        reg_msg = self.db.user_banquet_registration.create(
            banquet_id, self.email, meal_name, alcoholic_drink, special_needs, seating_preference1 or None, seating_preference2 or None)
        print(reg_msg)
        return True

    @staticmethod
    def format_datetime(date, time):
        try:
            date_obj = datetime.datetime.strptime(str(date), "%Y-%m-%d")
            time_obj = datetime.datetime.strptime(str(time), "%H:%M:%S")
            formatted_date = date_obj.strftime("%B %d, %Y")
            formatted_time = time_obj.strftime("%I:%M %p")
            return f"{formatted_date} at {formatted_time}"
        except Exception:
            return "Invalid Date/Time"

    def search_registered_banquets(self):
        print_user_tips()
        print("=" * 54)
        print("📋 Registered Banquets")
        print("=" * 54)
        
        registered_banquets = self.db.user_banquet_registration.read_by_user(self.email)
        if not registered_banquets.strip():
            print("❌ No registered banquets.")
            return False

        banquet_entries = registered_banquets.split("\n")
        for i, entry in enumerate(banquet_entries, start=1):
            try:
                fields = entry.split(", ")
                BID = fields[0]
                banquet_details = self.db.banquet.read_by_id(BID)
                if banquet_details:
                    banquet_date_time = self.format_datetime(banquet_details[4], banquet_details[5])
                    isAlcoholic = "Yes" if int(fields[3]) else "No"
                    print(f"""
Banquet {i}:
    🆔 BID: {BID}
    🏷️ Name: {banquet_details[1]}
    🏠 Address: {banquet_details[2]}
    📍 Location: {banquet_details[3]}
    📅 Date & Time: {banquet_date_time}
    🪑 Seat No: {"Will be communicated at a later date"}
    🍽️ Meal: {fields[2]}
    🥂 Alcoholic Drink: {isAlcoholic}
    💬 Special Needs: {fields[5]}
    👥 Seating Preferences: {fields[7]}, {fields[8]}
""")
                else:
                    print(f"❌ Banquet {i}: Could not fetch details for BID {BID}")
                    return False
            except IndexError:
                print(f"❌ Error processing entry: {entry}")
                return False
        return True

    def delete_edit_registration(self):
        print_user_tips()
        print("=" * 54)
        print("1️⃣  Delete a Registration")
        print("2️⃣  Edit your Registration")
        print("3️⃣  Go back to Dashboard")
        print("=" * 54 + "\n")
        choice = input("👉 Enter your choice (1/2/3): ").strip()

        successful_operation = False
        if choice == '1':
            while not successful_operation:
                successful_operation = self.delete_registration()
        elif choice == '2':
            while not successful_operation:
                successful_operation = self.edit_registration()
        elif choice == '3':
            return True
        else:
            print("❌ Invalid choice. Please try again.")
            return False
        return True

    def delete_registration(self):
        print_user_tips()
        print("=" * 54)
        print("✏️ Delete your Registration")
        print("=" * 54)
        while True:
            BID = input("🆔 Enter Banquet ID to delete the registration: ").strip()
            if self.db.back(BID):
                return True
            if not BID:
                print("❌ Banquet ID is required to delete registration.\n")
                continue
            elif not self.db.user_banquet_registration.read_by_user_and_banquet(self.email, BID):
                print("❌ You have not registered for this banquet.\n")
                continue
            else:
                choice = input("❓ Are you sure you want to delete a registration? (Yes/No): ").strip().lower()
                if choice == 'no':
                    print("Registration NOT deleted")
                elif choice == 'yes':
                    result = self.db.user_banquet_registration.delete(BID, self.email)
                    print(result)
            return True

    def edit_registration(self):
        print_user_tips()
        print("=" * 54)
        print("✏️ Edit your Registration")
        print("=" * 54)
        print("Enter the details to update, or press enter to skip but you have to provide a Banquet ID")

        while True:
            BID = input("🆔 Enter Banquet ID: ").strip()
            if self.db.back(BID):
                break
            if not BID:
                print("❌ Banquet ID is required to update registration.\n")
                continue
            if not BID.isdigit():
                print("❌ Please enter a valid BID.\n")
                continue
            if self.db.user_banquet_registration.read_by_user_and_banquet(self.email, BID):
                break
            print("❌ You have not registered for this banquet or there is no Banquet with this BID.\n")

        meals = self.db.banquet_meal.show_meals(BID)  # Fetch meals for the banquet
        if not meals:
            print("❌ No meals found for this banquet.\n")
            return  True    # Exit if no meals are available
        drinks = self.db.banquet_drink.show_drinks(BID)
        if not drinks:
            print("❌ No drinks found for this banquet.\n")
            return  True    # Exit if no meals are available

        # Display available meals in a formatted manner
        print("\n🍽️  Banquet Meals:")
        print("\n".join([f"\t\t{meal[0]}, ${meal[1]:.2f}" for meal in meals]) + "\n")

        # Formats available_meals to be passed to the funct
        available_meals = []
        for meal in meals:
            available_meals.append(meal[0])

        meal_name = self.db.input_meal_name(available_meals, empty_not_allowed=False) #false means can be null
        if self.db.back(meal_name):
            return True

        # Display available drinks in a formatted manner
        print("\n🍽️  Banquet Drinks:")
        print("\n".join([f"\t\t{drink[0]}, ${drink[1]:.2f}" for drink in drinks]) + "\n")

        alcoholic_drink = self.db.input_alcoholic_drink(empty_not_allowed=False)
        if self.db.back(alcoholic_drink):
            return True
        if alcoholic_drink:
            alcoholic_drink = (alcoholic_drink == "yes")

        special_needs = input("💬 Special Needs (or press Enter for None): ").strip() or None

        print("👥 Seating Preferences:")
        seating_preference1 = self.db.input_seating_preference("first")
        seating_preference2 = None
        if self.db.back(seating_preference1):
            return True

        if seating_preference1:
            seating_preference2 = self.db.input_seating_preference("second")
            if self.db.back(seating_preference2):
                return True

        result = self.db.user_banquet_registration.update(
            BID, self.email, meal_name, alcoholic_drink, special_needs, seating_preference1, seating_preference2)
        print(result)
        return True


    def logout(self):
        print("=" * 54)
        print("👋 Logging out... Goodbye!")
        print("=" * 54)
        self.userLogged = False
        return True