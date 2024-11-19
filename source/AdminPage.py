from crud_operations import Database

class AdminPage:
    def __init__(self, cursor, connection, email):
        self.cursor = cursor
        self.connection = connection
        self.email = email
        self.database = Database(cursor, connection)

    def display(self):
        print("\n" + "=" * 50)
        print(f"👨‍💼 Admin Dashboard (Logged in as: {self.email}) 👩‍💼")
        print("=" * 50)
        print("Please choose an action:\n")
        print("1️⃣  Create a New Banquet")
        print("2️⃣  Update an Existing Banquet")
        print("3️⃣  Search for Attendees")
        print("4️⃣  Edit Attendee Information")
        print("5️⃣  Generate Reports")
        print("6️⃣  Logout")
        print("=" * 50)
        
        choice = input("👉 Enter your choice (1-6): ").strip()
        
        if choice == '1':
            self.create_banquet()
        elif choice == '2':
            self.update_banquet()
        elif choice == '3':
            self.search_attendees()
        elif choice == '4':
            self.edit_attendee_info()
        elif choice == '5':
            self.generate_report()
        elif choice == '6':
            self.logout()
        else:
            print("\n❌ Invalid choice. Please try again. ❌")
            self.display()

    def create_banquet(self):
        print("\n" + "=" * 50)
        print("🎉 Create a New Banquet")
        print("=" * 50)
        banquet_name = input("🏷️  Enter Banquet Name: ").strip()
        banquet_date = input("📅 Enter Banquet Date (YYYY-MM-DD): ").strip()
        banquet_time = input("⏰ Enter Banquet Time (HH:MM:SS): ").strip()
        banquet_location = input("📍 Enter Location: ").strip()
        banquet_address = input("🏠 Enter Address: ").strip()
        banquet_seats = input("💺 Enter Total Seats: ").strip()

        print("\nCreating banquet... 🔄")
        # Logic to create banquet goes here.
        print(f"\n✅ Banquet '{banquet_name}' created successfully! ✅")
        self.display()

    def update_banquet(self):
        print("\n" + "=" * 50)
        print("✏️ Update an Existing Banquet")
        print("=" * 50)
        banquet_id = input("🆔 Enter Banquet ID: ").strip()
        banquet_name = input("🏷️  Enter New Banquet Name (or press Enter to skip): ").strip()
        banquet_date = input("📅 Enter New Date (or press Enter to skip): ").strip()
        banquet_time = input("⏰ Enter New Time (or press Enter to skip): ").strip()
        banquet_location = input("📍 Enter New Location (or press Enter to skip): ").strip()
        banquet_address = input("🏠 Enter New Address (or press Enter to skip): ").strip()
        banquet_seats = input("💺 Enter New Total Seats (or press Enter to skip): ").strip()

        print("\nUpdating banquet... 🔄")
        # Logic to update banquet goes here.
        print(f"\n✅ Banquet '{banquet_id}' updated successfully! ✅")
        self.display()

    def search_attendees(self):
        print("\n" + "=" * 50)
        print("🔍 Search for Attendees")
        print("=" * 50)
        search_query = input("🔎 Enter attendee name or email to search: ").strip()
        print("\nSearching attendees... 🔄")
        # Logic to search attendees goes here.
        print("\n✅ Search completed! Here are the results:")
        # Display search results.
        self.display()

    def edit_attendee_info(self):
        print("\n" + "=" * 50)
        print("✏️ Edit Attendee Information")
        print("=" * 50)
        attendee_email = input("📧 Enter Attendee Email: ").strip()
        new_name = input("👤 Enter New Name (or press Enter to skip): ").strip()
        new_phone = input("📞 Enter New Phone Number (or press Enter to skip): ").strip()
        new_address = input("🏠 Enter New Address (or press Enter to skip): ").strip()

        print("\nUpdating attendee information... 🔄")
        # Logic to edit attendee information goes here.
        print(f"\n✅ Attendee '{attendee_email}' updated successfully! ✅")
        self.display()

    def generate_report(self):
        print("\n" + "=" * 50)
        print("📊 Generate Reports")
        print("=" * 50)
        report_type = input("📄 Select report type (1: Banquet Summary, 2: Attendee Details): ").strip()

        print("\nGenerating report... 🔄")
        # Logic to generate reports goes here.
        print(f"\n✅ Report generated successfully! Check your output folder. ✅")
        self.display()

    def logout(self):
        print("\n" + "=" * 50)
        print("👋 Logging out of Admin Dashboard...")
        print("=" * 50)
        exit()