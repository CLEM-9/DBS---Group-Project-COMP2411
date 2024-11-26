from AdminPage import AdminPage
from AttendeePage import AttendeePage
from getpass import getpass

class WelcomePage:
    def __init__(self, cursor, connection, database):
        self.cursor = cursor
        self.connection = connection
        self.database = database
        self.exit = False

    def display(self):
        print("\n" + "=" * 50)
        print("🚪 Welcome to the Banquet Registration System! 🚪")
        print("=" * 50)

        while not self.exit:
            print("Please select an option below to proceed and click enter:\n")
            print("1️⃣  Log in to your account")
            print("2️⃣  Register as a new attendee")
            print("3️⃣  Exit the system\n")
            print("=" * 50)

            choice = input("👉 Enter your choice (1/2/3): ").strip()

            successful_operation = False
            if choice == '1':
                print("\n" + "=" * 50)
                print("🔑 Login to Your Account")
                print("    ## to quit anytime")
                print("=" * 50 + "\n")
                while not successful_operation:
                    successful_operation = self.login()
            elif choice == '2':
                print("\n" + "=" * 50)
                print("📝 Register as a New Attendee")
                print("    ## to quit anytime\n")
                print("=" * 50 + "\n")
                while not successful_operation:
                    successful_operation = self.register_attendee()
            elif choice == '3':
                self.exit_program()
            else:
                print("\n❌ Invalid choice. Please try again. ❌")

    def login(self):
        email = input("📧 Enter Email: ").strip()

        if self.database.back(email):
            return True

        #TODO switch to getpass on delivery
        #password = getpass("🔒 Enter Password (your password is invisible): ").strip()
        password = input("🔒 Enter Password: ").strip()

        if self.database.back(password):
            return True

        print("\nAuthenticating your credentials... 🔄")
        user_type = self.database.check_email(email, password)

        if not user_type:
            print("\n❌ Invalid email or password. Please check your credentials and try again. ❌\n")
            return False
        elif user_type[0] == "Administrator":
            print("\n✅ Login successful! Welcome self.database.back, Administrator! ✅")
            admin_page = AdminPage(self.cursor, self.connection, email, self.database)
            admin_page.display()
            return True
        elif user_type[0] == "Attendee":
            print("\n✅ Login successful! Welcome self.database.back, Attendee! ✅\n")
            attendee_page = AttendeePage(self.cursor, self.connection, email, self.database)
            attendee_page.display()
            return True
        else:
            return False

    def register_attendee(self):
        email = self.database.input_email()
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
        print("\n" + "=" * 50)
        print("👋 Thank you for using the Banquet Registration System!")
        print("Goodbye! Have a great day! 🌟")
        print("=" * 50)
        exit()