from AdminPage import AdminPage
from AttendeePage import AttendeePage

def print_user_tips():
    print("\n" + "=" * 54)
    print("🚪 Press: 'Enter' to leave information fields empty")
    print("🚪 Type:  '##'    to quit any operation")

class WelcomePage:
    def __init__(self, cursor, connection, database):
        self.cursor = cursor
        self.connection = connection
        self.database = database
        self.exit = False

    def display(self):
        print("\n" + "=" * 54)
        print("🚪 Welcome to the Banquet Registration System!      🚪")
        print("=" * 54 + "\n")
        choice = None
        successful_operation = False

        while not self.exit:
            print("=" * 54)
            print("Please select an option below to proceed and click enter:")
            print("1️⃣  Log in to your account")
            print("2️⃣  Register as a new attendee")
            print("3️⃣  Exit the system")
            print("=" * 54)

            choice = input("👉 Enter your choice (1/2/3): ").strip()

            successful_operation = False
            if choice == '1':
                print_user_tips()
                print("=" * 54)
                print("🔑 Login to Your Account")
                print("=" * 54)
                while not successful_operation:
                    successful_operation = self.login()
            elif choice == '2':
                print_user_tips()
                print("=" * 54)
                print("📝 Register as a New Attendee")
                print("=" * 54)
                while not successful_operation:
                    successful_operation = self.register_attendee()
            elif choice == '3':
                self.exit_program()
            else:
                print("❌ Invalid choice. Please try again. ❌\n")

    def login(self):
        email = self.database.input_email()
        if self.database.back(email):
            return True

        password = self.database.input_password()
        if self.database.back(password):
            return True

        print("\nAuthenticating your credentials... 🔄")
        user_type = self.database.check_email(email, password)

        if not user_type:
            print("❌ Invalid email or password. Please check your credentials and try again. ❌\n")
            return False
        elif user_type[0] == "Administrator":
            print("✅ Login successful! Welcome back Administrator! ✅")
            admin_page = AdminPage(self.cursor, self.connection, email, self.database)
            admin_page.display()
            return True
        elif user_type[0] == "Attendee":
            print("✅ Login successful! Welcome back Attendee! ✅\n")
            attendee_page = AttendeePage(self.cursor, self.connection, email, self.database)
            attendee_page.display()
            return True
        else:
            return False

    def register_attendee(self):
        email = self.database.input_email(new_registration=True)
        if self.database.back(email):
            return True

        password = self.database.input_password()

        first_name = self.database.input_name("First")
        if self.database.back(first_name):
            return True

        last_name = self.database.input_name("Last")
        if self.database.back(last_name):
            return True

        phone = self.database.input_phone()
        if self.database.back(phone):
            return True

        address = self.database.input_address()
        if self.database.back(address):
            return True

        attendee_type = self.database.input_attendee_type()
        if self.database.back(attendee_type):
            return True

        affiliate_organization = self.database.input_affiliate_organization()
        if self.database.back(affiliate_organization):
            return True

        print("\nValidating your information... 🔄")

        self.database.attendees.create(
            email, password, address, last_name, first_name, phone, attendee_type, affiliate_organization
        )
        print(f"\n✅ Registration successful! Welcome, {first_name}. You can now explore your dashboard! ✅\n")
        attendee_page = AttendeePage(self.cursor, self.connection, email, self.database)
        attendee_page.display()
        return True

    def exit_program(self):
        self.exit = True
        print("=" * 54)
        print("👋 Thank you for using the Banquet Registration System!")
        print("Goodbye! Have a great day! 🌟")
        print("=" * 54)
        exit()