from crud_operations import ReportGeneration
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

def print_user_tips():
    print("\n" + "=" * 54)
    print("🚪 Press: 'Enter' to leave information fields empty")
    print("🚪 Type:  '##'    to quit any operation")

class AdminPage:
    def __init__(self, cursor, connection, email, database):
        self.cursor = cursor
        self.connection = connection
        self.email = email
        self.db = database
        self.report_generation = ReportGeneration(self.cursor, self.connection)
        self.userLogged = True

    # This method is called when the admin logs in, and it displays the admin dashboard
    def display(self):
        while self.userLogged:
            print("\n" + "=" * 50)
            print(f"👨‍💼 Admin Dashboard (Logged in as: {self.email}) 👩‍💼")
            print("=" * 50)
            print("Please choose an action:\n")
            print("1️⃣  Create a New Banquet")
            print("2️⃣  Search for Banquets")
            print("3️⃣  Edit Banquet")
            print("4️⃣  Delete Banquet")
            print("5️⃣  Search for Attendees")
            print("6️⃣  Edit Attendee Information")
            print("7️⃣  Generate Reports")
            print("8️⃣  Logout")
            print("=" * 50)

            choice = input("👉 Enter your choice (1-8): ").strip()

            successful_operation = False
            if choice == '1':
                while not successful_operation:
                    successful_operation = self.create_banquet()
            elif choice == '2':
                while not successful_operation:
                    successful_operation = self.search_banquets()
            elif choice == '3':
                while not successful_operation:
                    successful_operation = self.edit_banquet()
            elif choice == '4':
                while not successful_operation:
                    successful_operation = self.delete_banquet()
            elif choice == '5':
                while not successful_operation:
                    successful_operation = self.search_attendees()
            elif choice == '6':
                while not successful_operation:
                    successful_operation = self.edit_attendee_info()
            elif choice == '7':
                    self.generate_report()
            elif choice == '8':
                self.logout()
                return True
            else:
                print("❌ Invalid choice. Please try again. ❌\n")
        return True

    # This method is called when the admin wants to create a new banquet
    def create_banquet(self):
        print_user_tips()
        print("=" * 50)
        print("🎉 Create a New Banquet")
        print("=" * 50)

        banquet_name = self.db.input_banquet_name()
        if self.db.back(banquet_name):
            return True

        banquet_date = self.db.get_valid_date("📅 Enter Banquet Date (YYYY-MM-DD): ")
        if self.db.back(banquet_date):
            return True

        banquet_time = self.db.get_valid_time("⏰ Enter Banquet Time (HH:MM:SS): ")
        if self.db.back(banquet_time):
            return True

        banquet_location = self.db.input_location()
        if self.db.back(banquet_location):
            return True

        banquet_address = self.db.input_address()
        if self.db.back(banquet_address):
            return True

        banquet_seats = self.db.get_valid_number("💺 Enter Total Seats: ")
        if self.db.back(banquet_seats):
            return True

        staff_email = self.db.input_staff_email()
        if self.db.back(staff_email):
            return True
            
        print("\nCreating banquet... 🔄")
        result = self.db.banquet.create(banquet_name, banquet_address, banquet_location, staff_email, banquet_date, banquet_time, 1, banquet_seats)
        
        if "created successfully" in result:
            banquet_id = self.db.banquet.get_id(banquet_date, banquet_time, banquet_address)
            print(result)
            if not self.add_meals_to_banquet(banquet_id):
                return True
            if not self.add_drinks_to_banquet(banquet_id):
                return True
        else:
            print(result)
        print("✅ Banquet created successfully")
        return True

    def add_meals_to_banquet(self, banquet_id):
        print("\n" + "=" * 50)
        print("🍽️ Add Meals to Banquet")
        print("=" * 50)
        read_meals = self.db.meal.read().split("\n")

        # Gets list of only meals
        meal_names = [meal.split(',')[0].strip() for meal in read_meals]

        print("\nAvailable Meals:\n")
        items_per_row = 3
        for i in range(0, len(meal_names), items_per_row):
            print(" | ".join(meal_names[i:i + items_per_row]))
        print("\n" + "=" * 50)

        print("\nYou must assign four meals to the banquet.")
        for i in range(1, 5):
            while True:
                meal_name = self.db.input_meal_name(meal_names)
                if self.db.back(meal_name):
                    self.db.banquet.delete(banquet_id)
                    return False
                if self.db.banquet_meal.check_meal_exists(banquet_id, meal_name):
                    print("\n❌ Meal already exists in the banquet. Please select a different meal.")
                    continue
                meal_price = self.db.get_valid_number(f"💵 Enter Price for '{meal_name}': ")
                self.db.banquet_meal.create(banquet_id, meal_name, meal_price)
                print(f"✅ Meal '{meal_name}' added successfully.\n")
                break
        print("\n✅ Meals added successfully")
        return True

    # This method is called when the admin wants to add drinks to a banquet
    def add_drinks_to_banquet(self, banquet_id):
        available_drinks = self.db.drink.read().split('\n')
        alcoholic_drinks = []
        non_alcoholic_drinks = []

        for drink in available_drinks:
            drink_details = drink[:-2].split(',') 
            is_alcoholic = int(drink_details[1])  
            drink_name = drink_details[0].strip()  
            if is_alcoholic:
                alcoholic_drinks.append(drink_name)
            else:
                non_alcoholic_drinks.append(drink_name)
      
        if not alcoholic_drinks or not non_alcoholic_drinks:
            print("\n❌ Unable to add drinks. Make sure the drink table has both alcoholic and non-alcoholic options.")
            return False

        print("\n" + "=" * 50)
        print("🍹 Drinks for the Banquet")
        print("=" * 50)
        print("\nAlcoholic Drinks:")
        for drink in alcoholic_drinks:
            print(f"  - {drink}")
        print("\nAlcohol-Free Drinks:")
        for drink in non_alcoholic_drinks:
            print(f"  - {drink}")

        print("\n" + "=" * 50)
        print("At least one drink must be assigned, at most you can assign four drinks.\n")
        for i in range(0, 4):
            while True:
                drink_name = self.db.input_drink_name(alcoholic_drinks, non_alcoholic_drinks)
                if self.db.back(drink_name) or not drink_name:
                    if i != 0:
                        print("\n✅ Drinks added successfully")
                        return True    #if drinks were added terminates correctly
                    choice = None
                    while choice != "no":
                        choice = input("\nYou haven't added any drinks\nGoing back now will cause the deletion of the Banquet\nDo you want to proceed? [Yes/No]").lower()
                        if choice == "yes":
                            self.db.banquet.delete(banquet_id)
                            return False
                    continue
                if self.db.banquet_drink.check_drink_exists(banquet_id, drink_name):
                    print("\n❌ Drink already exists in the banquet. Please select a different drink.")
                    continue
                meal_price = self.db.get_valid_number(f"💵 Enter Price for '{drink_name}': ")
                print(self.db.banquet_drink.create(banquet_id, drink_name, meal_price))
                break
        print("\n✅ Drinks added successfully")
        return True

    # This method is called to validate the meal name entered by the admin
    def validate_meal_name(self, meal_name):
        available_meals = self.db.meal.read()
        available_meal_names = [meal.split(", ")[0] for meal in available_meals.split("\n") if meal]
        return meal_name in available_meal_names
    
    def delete_banquet(self):
        print_user_tips()
        print("=" * 50)
        print("🗑️ Delete a Banquet")
        print("=" * 50)
        
        banquet_id = input("🆔 Enter the Banquet ID you want to delete: ").strip()
        
        # Check if the banquet ID is valid
        banquet_ids = [str(banquet[0]) for banquet in self.db.banquet.read()]
        if not banquet_id.isdigit() or banquet_id not in banquet_ids:
            print("\n❌ Invalid Banquet ID. Please enter a valid Banquet ID.")
            return True
        banquet_id = int(banquet_id)
        
        self.db.banquet.delete(banquet_id)
        print("\n✅ Banquet deleted successfully.")
        return True
             
    # This method is called when the admin wants to search for a banquet      
    def search_banquets(self):
        print_user_tips()
        print("=" * 50)
        print("🔍 Search for a Banquet")
        print("=" * 50)
        print("Enter the details to search, or leave fields blank to skip.\n")

        banquet_name = self.db.input_banquet_name(False)
        if self.db.back(banquet_name):
            return True
        banquet_date = self.db.get_valid_date("📅 Enter Banquet Date (YYYY-MM-DD): ", True)
        if self.db.back(banquet_date):
            return True
        banquet_address = self.db.input_address(False)
        if self.db.back(banquet_address):
            return True
        banquet_location = self.db.input_location(False)
        if self.db.back(banquet_location):
            return True

        if not (banquet_name and banquet_date and banquet_address and banquet_location):
            print("\nAll fields are empty. All banquets will be displayed\n")

        print("\nSearching for banquets... 🔄")
        result = self.db.banquet.read_by_filter( banquet_name, banquet_date, banquet_location, banquet_address)
        if result:
            print("\n✅ Search Results:\n")
            for i, banquet in enumerate(result, start=1):
                banquet_date_time = f"{banquet[4]} at {banquet[5]}"
                available = "Yes" if int(banquet[6]) else "No"
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
        return True
    
    # This method is called when the admin wants to edit a banquet   
    def edit_banquet(self):
        print_user_tips()
        print("=" * 54)
        print("✏️ Edit Banquet")
        print("=" * 54)
        print("Enter the details to search, or leave fields blank to skip.\n")

        banquet_id = input("\n🆔 Enter the Banquet ID you want to edit: ").strip()
        # Check if the banquet ID is valid
        if not banquet_id.isdigit():
            print("\n❌ Invalid Banquet ID. Please enter a valid Banquet ID.")
            return False
        banquet_id = int(banquet_id)
        print("If you want to skip a field, just press Enter.")
        banquet_name = self.db.input_banquet_name(False)
        banquet_date = input("📅 Enter Banquet Date (YYYY-MM-DD): ").strip()
        if banquet_date:
            while True:
                try:
                    # Try to parse the input into a datetime object
                    banquet_date_obj = datetime.strptime(banquet_date, "%Y-%m-%d")
                    break  # Exit the loop if the date is valid
                except ValueError:
                    # Catch any errors related to invalid date format or invalid dates
                    print("\n❌ Invalid date value. Please ensure the date is valid.")
                    banquet_date = input("📅 Enter Banquet Date (YYYY-MM-DD): ").strip()
        else:
            banquet_date = None
        banquet_time = input("⏰ Enter Banquet Time (HH:MM:SS): ").strip()
        if banquet_time:
            while len(banquet_time) != 8 or banquet_time[2] != ":" or banquet_time[5] != ":":
                print("\n❌ Invalid time format. Please enter the time in HH:MM:SS format. ❌")
                banquet_time = input("⏰ Enter Banquet Time (HH:MM:SS): ").strip()
        else:
            banquet_time = None
        banquet_location = self.db.input_location(False)
        banquet_address = input("🏠 Enter Address: ").strip() or None
        banquet_seats = input("💺 Enter Total Seats: ").strip()
        if banquet_seats:
            while not banquet_seats.isdigit():
                print("\n❌ Total Seats must be a number. Please try again. ❌")
                banquet_seats = input("💺 Enter Total Seats: ").strip()
        else:
            banquet_seats = None
        staff_email = self.db.input_staff_email(False)
        banquet_available = input("🟢 Enter Availability (Yes/No): ").strip().lower()
        if banquet_available:
            while banquet_available not in ["yes", "no"]:
                print("\n❌ Availability must be 'Yes' or 'No'. Please try again. ❌")
                banquet_available = input("🟢 Enter Availability (Yes/No): ").strip().lower()
            banquet_available = (banquet_available == "yes")
        else:
            banquet_available = None
        print("\nUpdating banquet... 🔄")
        self.db.banquet.update(banquet_id, banquet_name, banquet_address, banquet_location, staff_email, banquet_date, banquet_time, banquet_available, banquet_seats)
        
        print("\n✅ Banquet updated successfully.")
        
        print("\nDo you want to update the meals for this banquet?\nThis will cause all current meals to be deleted before adding new ones.")
        choice = None
        while choice not in ["yes", "no"]:
            choice = input("👉 Enter your choice (Yes/No): ").strip().lower()
            if choice == 'yes':
                print("\nUpdating meals... 🔄")
                self.db.banquet_meal.delete(banquet_id)
                available_meals = self.db.meal.read()
                print("\nAvailable Meals:\n")
                print(available_meals)

                print("\nYou need to assign four meals to the banquet.")
                for i in range(1, 5):
                    while True:
                        meal_name = input(f"👉 Enter Meal {i} Name: ").strip()
                        if self.db.banquet_meal.check_meal_exists(banquet_id, meal_name):
                            print("\n❌ Meal already exists in the banquet. Please select a different meal.")
                        elif self.validate_meal_name(meal_name):
                            meal_price = self.db.get_valid_number(f"💵 Enter Price for '{meal_name}': ")
                            print(self.db.banquet_meal.create(banquet_id, meal_name, meal_price))
                            print(f"✅ Meal '{meal_name}' added successfully.")
                            break
                        elif not meal_name:
                            print("\n❌ Meal name cannot be empty. Please enter a valid meal name.")
                        else:
                            print("\n❌ Invalid meal name. Please select a meal from the available list.")
                print("\n✅ Meals updated successfully.")
            elif choice == "no":
                print("\nReturning to dashboard.")
        return True
    
    # This method is called when the admin wants to search for attendees 
    def search_attendees(self):
        print_user_tips()
        print("=" * 50)
        print("🔍 Search for Attendees")
        print("=" * 50)
        search_query = self.db.input_email(False)
        print("\nSearching attendees... 🔄")
        
        # Fetch attendee information
        result = self.db.attendees.get(search_query)  # Assuming a function to get attendee info
        if result:
            print("\n✅ Search completed! Attendee Information:\n")
            print(f"""
    📧 Email: {result['email']}
    👤 Name: {result['firstName']} {result['lastName']}
    📞 Phone: {result['phone']}
    🏠 Address: {result['address']}
    🎓 Type: {result['attendeeType']}
    🏢 Organization: {result['affiliateOrganization']}
            """)
        else:
            print("\n❌ No attendee found with the provided email.")
            return True
        
        # Ask to edit the attendee's information
        choice = None
        while choice not in ["yes", "no"]:
            choice = input("\nDo you want to edit this attendee's information? (Yes/No): ").strip().lower()
            if choice == 'yes':
                self.edit_attendee_info(search_query)
            elif choice == 'no':
                return True
        return True

    # This method is called when the admin wants to edit an attendee's information
    def edit_attendee_info(self, attendee_email=None):
        print_user_tips()
        print("=" * 54)
        print("✏️ Edit Attendee Info")
        print("=" * 54)

        if not attendee_email:
            print("\n" + "=" * 50)
            print("✏️ Edit Attendee Information")
            print("=" * 50)
            attendee_email = input("📧 Enter Attendee Email: ").strip()
        
            # Fetch current information for reference
            current_info = self.db.attendees.get(attendee_email)  # Assuming a function to get attendee info
            if not current_info:
                print("\n❌ Attendee not found. Returning to dashboard.")
                return True

            print("\nCurrent Information:")
            print(f"""
        📧 Email: {current_info['email']}
        👤 Name: {current_info['firstName']} {current_info['lastName']}
        📞 Phone: {current_info['phone']}
        🏠 Address: {current_info['address']}
        🎓 Type: {current_info['attendeeType']}
        🏢 Organization: {current_info['affiliateOrganization']}
            """)
        print("Leave fields blank to keep them unchanged.")

        # Update fields
        new_phone = self.db.input_phone(False)
        if self.db.back(new_phone):
            return True
        new_address = self.db.input_address(False)
        if self.db.back(new_address):
            return True
        new_type = self.db.input_attendee_type(False)
        if self.db.back(new_type):
            return True
        new_org = self.db.input_affiliate_organization(False)
        if self.db.back(new_org):
            return True

        # Update attendee information
        print("\nUpdating attendee information... 🔄")
        update_result = self.db.attendees.admin_update_attendee_info(attendee_email, new_phone, new_address, new_type,
                                                                  new_org)
        if "successfully" in update_result:
            print(f"\n✅ Attendee '{attendee_email}' updated successfully! ✅")
        else:
            print(f"\n❌ Failed to update attendee information.\n{update_result}")
        return True

    # This method is called when the admin wants to generate a registration status report
    def generate_report(self):
        print_user_tips()
        print("=" * 50)
        print("📊 Generate Reports")
        print("=" * 50)
        print("1️⃣ Registration Status")
        print("2️⃣ Popular Meals")
        print("3️⃣ Attendance Behavior")
        print("4️⃣ Summary by Attendee Type")
        report_type = input("👉 Select report type (1-4): ").strip()

        if report_type == '1':
            self.generate_registration_status_report()
        elif report_type == '2':
            self.generate_popular_meals_report()
        elif report_type == '3':
            self.generate_attendance_behavior_report()
        elif report_type == '4':
            self.generate_attendee_type_summary()
        else:
            print("\n❌ Invalid choice. Returning to dashboard.")
        return True
    
    def generate_registration_status_report(self):
        data = pd.DataFrame(
            self.report_generation.get_registration_status(),
            columns=["Banquet Name", "Total Seats", "Registered", "Available"]
        )
        print("\n🔍 Registration Status Report:")
        print(tabulate(data, headers="keys", tablefmt="pretty", showindex=False))

        # remove total column otherwise will get displayed and histogram heights double
        data = data.drop("Total Seats", axis=1)
        # Visualization: Bar chart of registration status
        data.plot(kind='bar', x="Banquet Name", stacked=True, figsize=(10, 6),
                  title="Registration Status per Banquet")
        plt.ylabel("Seats")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def generate_popular_meals_report(self):
        # Fetch data from the database
        meal_data = self.report_generation.get_popular_meals()  # Ensure this returns a list of tuples like [(mealName, popularity)]
        
        if not meal_data:
            print("\n❌ No data available for popular meals.")
            return

        # Create a DataFrame for better processing and visualization
        data = pd.DataFrame(meal_data, columns=["Meal Name", "Popularity"])
        print("\n🔍 Popular Meals Report:")
        print(tabulate(data, headers="keys", tablefmt="pretty", showindex=False))

        # Check if data contains at least one non-zero popularity
        if data["Popularity"].sum() == 0:
            print("\n⚠️ All meals have zero popularity.")
            return True

        # Visualization: Bar chart of meal popularity
        data.sort_values("Popularity", ascending=False, inplace=True)  # Sort by popularity
        plt.figure(figsize=(10, 6))
        plt.bar(data["Meal Name"], data["Popularity"], color="skyblue")
        plt.xlabel("Meal Name")
        plt.ylabel("Popularity")
        plt.title("Meal Popularity Distribution")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

        # Visualization: Pie chart of meal popularity
        plt.figure(figsize=(8, 8))
        data.set_index("Meal Name").plot(
            kind="pie", 
            y="Popularity", 
            autopct='%1.1f%%', 
            figsize=(8, 8),
            title="Popular Meals Distribution",
            legend=False
        )
        plt.ylabel("")
        plt.show()
        return True

    def generate_attendance_behavior_report(self):
        data = pd.DataFrame(
            self.report_generation.get_attendance_behavior(),
            columns=["Banquet Date", "Attendance"]
        )
        print("\n🔍 Attendance Behavior Report:")
        print(tabulate(data, headers="keys", tablefmt="pretty", showindex=False))

        # Visualization: Line chart of attendance over time
        data.plot(kind="line", x="Banquet Date", y="Attendance", marker='o', figsize=(10, 6),
                  title="Attendance Behavior Over Time")
        plt.ylabel("Number of Attendees")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        return True

    def generate_attendee_type_summary(self):
        data = pd.DataFrame(
            self.report_generation.get_attendee_type_summary(),
            columns=["Attendee Type", "Registrations"]
        )
        print("\n🔍 Summary by Attendee Type:")
        print(tabulate(data, headers="keys", tablefmt="pretty", showindex=False))

        # Visualization: Horizontal bar chart of attendee type summary
        data.plot(kind="barh", x="Attendee Type", y="Registrations", figsize=(8, 6),
                  title="Registrations by Attendee Type")
        plt.xlabel("Registrations")
        plt.tight_layout()
        plt.show()
        return True

    def logout(self):
        self.userLogged = False
        print("\n" + "=" * 50)
        print("👋 Logging out of Admin Dashboard...")
        print("=" * 50)
        return True