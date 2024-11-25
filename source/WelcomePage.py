from AdminPage import AdminPage
from AttendeePage import AttendeePage
from getpass import getpass

def back(var):
    return var == "##"

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
                print("=" * 50)
                print("## to quit anytime\n")
                while not successful_operation:
                    successful_operation = self.login()
            elif choice == '2':
                self.register_attendee()
            elif choice == '3':
                self.exit_program()
            else:
                print("\n❌ Invalid choice. Please try again. ❌")

    def login(self):
        email = input("📧 Enter Email: ").strip()

        if back(email):
            return True

        #TODO switch to getpass on delivery
        #password = getpass("🔒 Enter Password (your password is invisible): ").strip()
        password = input("🔒 Enter Password: ").strip()

        if back(password):
            return True

        print("\nAuthenticating your credentials... 🔄")
        user_type = self.database.check_email(email, password)

        if not user_type:
            print("\n❌ Invalid email or password. Please check your credentials and try again. ❌\n")
            return False
        elif user_type[0] == "Administrator":
            print("\n✅ Login successful! Welcome back, Administrator! ✅")
            admin_page = AdminPage(self.cursor, self.connection, email, self.database)
            admin_page.display()
            return True
        elif user_type[0] == "Attendee":
            print("\n✅ Login successful! Welcome back, Attendee! ✅\n")
            attendee_page = AttendeePage(self.cursor, self.connection, email, self.database)
            attendee_page.display()
            return True
        else:
            return False

    def register_attendee(self):
        print("\n" + "=" * 50)
        print("📝 Register as a New Attendee")
        print("=" * 50)
        print("## to quit anytime\n")

        email = input("📧 Enter Email: ").strip()

        while not back(email) and self.database.check_email_exists(email):
            print("\n❌ This email is already registered. Please log in or use a different email to register. ❌\n")
            email = input("📧 Enter Email: ").strip()
        while not back(email) and not self.database.is_valid_email(email):
            print("\n❌ Invalid email format. Please enter a valid email. ❌\n")
            email = input("📧 Enter Email: ").strip()

        # returns to previous
        if back(email):
            return True

        #TODO switch to getpass on delivery
        #password = getpass("🔒 Enter Password (your password is invisible): ").strip()
        password = input("🔒 Enter Password: ").strip()
        while not password:
            print("\n❌ Password is required. Please provide a secure password. ❌\n")
            #TODO switch to getpass on delivery
            #password = getpass("🔒 Create Password: ").strip()
            password = input("🔒 Create Password: ").strip()

        first_name = input("👤 Enter First Name: ").strip()
        while not back(first_name) and not first_name or not first_name.isalpha():
            print("\n❌ First name is required and must only contain letters. Please try again. ❌\n")
            first_name = input("👤 Enter First Name: ").strip()

        if back(first_name):
            return True

        last_name = input("👤 Enter Last Name: ").strip()
        while not back(last_name) and not last_name or not last_name.isalpha():
            print("\n❌ Last name is required and must only contain letters. Please try again. ❌\n")
            last_name = input("👤 Enter Last Name: ").strip()

        if back(last_name):
            return True

        phone = input("📞 Enter Phone Number: ").strip()
        while not back(phone) and phone and (not phone.isdigit() or len(phone) != 8):
            print("\n❌ Phone number must be 8 digits and numeric. Please enter a valid number. ❌\n")
            phone = input("📞 Enter Phone Number: ").strip()

        if back(phone):
            return True

        address = input("🏠 Enter Address: ").strip()
        while not back(address) and not address:
            print("\n❌ Address cannot be empty. Please enter a valid address. ❌\n")
            address = input("🏠 Enter Address: ").strip()

        if back(address):
            return True

        attendee_type = input("🎓 Enter Attendee Type (Student, Alumni, Staff, Guest): ").strip()
        while not back(attendee_type) and attendee_type not in ["Student", "Alumni", "Staff", "Guest"]:
            print("\n❌ Please select a valid attendee type: Student, Alumni, Staff, or Guest. ❌\n")
            attendee_type = input("🎓 Enter Attendee Type: ").strip()

        if back(attendee_type):
            return True

        affiliate_organization = input("🏢 Enter Affiliate Organization: ").strip()
        while not back(affiliate_organization) and not affiliate_organization:
            print("\n❌ Organization name is required. Please provide a valid name. ❌\n")
            affiliate_organization = input("🏢 Enter Affiliate Organization: ").strip()

        if back(affiliate_organization):
            return True

        print("\nValidating your information... 🔄")

        self.database.attendees.create(
            email, password, address, last_name, first_name, phone, attendee_type, affiliate_organization
        )
        print(f"\n✅ Registration successful! Welcome, {first_name}. You can now explore your dashboard! ✅\n")
        attendee_page = AttendeePage(self.cursor, self.connection, email, self.database)
        attendee_page.display()

    def exit_program(self):
        self.exit = True
        print("\n" + "=" * 50)
        print("👋 Thank you for using the Banquet Registration System!")
        print("Goodbye! Have a great day! 🌟")
        print("=" * 50)
        exit()