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
        print("\n" + "=" * 50)
        print("🚪 Welcome to the Banquet Registration System! 🚪")
        print("=" * 50)
        print("Please select an option below to proceed:\n")
        print("1️⃣  Log in to your account")
        print("2️⃣  Register as a new attendee")
        print("3️⃣  Exit the system\n")
        print("=" * 50)
        
        choice = input("👉 Enter your choice (1/2/3): ").strip()
        
        if choice == '1':
            self.login()
        elif choice == '2':
            self.register_attendee()
        elif choice == '3':
            self.exit_program()
        else:
            print("\n❌ Invalid choice. Please try again. ❌")
            self.display()

    def login(self):
        print("\n" + "=" * 50)
        print("🔑 Login to Your Account")
        print("=" * 50)
        email = input("📧 Enter Email: ").strip()
        password = input("🔒 Enter Password: ").strip()

        print("\nAuthenticating your credentials... 🔄")
        user_type = self.database.check_email(self.connection, email, password)

        if user_type is None:
            print("\n❌ Invalid credentials. Please try again. ❌\n")
            self.display()
        elif user_type[0] == "Administrator":
            print("\n✅ Login successful! Welcome, Administrator! ✅\n")
            admin_page = AdminPage(self.cursor, self.connection, email)
            admin_page.display()
        elif user_type[0] == "Attendee":
            print("\n✅ Login successful! Welcome, Attendee! ✅\n")
            attendee_page = AttendeePage(self.cursor, self.connection, email)
            attendee_page.display()

    def register_attendee(self):
        print("\n" + "=" * 50)
        print("📝 Register as a New Attendee")
        print("=" * 50)
        
        email = input("📧 Enter Email: ").strip()
        password = input("🔒 Create Password: ").strip()
        first_name = input("👤 Enter First Name: ").strip()
        last_name = input("👤 Enter Last Name: ").strip()
        phone = input("📞 Enter Phone Number: ").strip()
        address = input("🏠 Enter Address: ").strip()
        attendee_type = input("🎓 Enter Attendee Type (Student, Alumni, Staff, Guest): ").strip()
        affiliate_organization = input("🏢 Enter Affiliate Organization: ").strip()

        print("\nValidating your information... 🔄")
        
        # Validate inputs
        if self.database.check_email_exists(self.connection, email):
            print("\n❌ Email already exists. Please try logging in or use a different email. ❌\n")
            self.display()
        elif attendee_type not in ["Student", "Alumni", "Staff", "Guest"]:
            print("\n❌ Invalid attendee type. Please enter one of the following: Student, Alumni, Staff, Guest. ❌\n")
            self.display()
        else:
            attendees = Attendees(self.cursor, self.connection)
            attendees.create(
                email, password, address, last_name, first_name, phone, attendee_type, affiliate_organization
            )
            print(f"\n✅ Registration successful! Welcome, {first_name}! ✅\n")
            attendee_page = AttendeePage(self.cursor, self.connection, email)
            attendee_page.display()

    def exit_program(self):
        print("\n" + "=" * 50)
        print("👋 Thank you for using the Banquet Registration System!")
        print("Goodbye! Have a great day! 🌟")
        print("=" * 50)
        exit()