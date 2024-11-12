class RegisteredUsers:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    # creates users
    def create(self, email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization):
        sql = "INSERT INTO RegisteredUsers(email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (email, password, address, lastName, firstName, phone, attendeeType, affiliateOrganization)
        self.cursor.execute(sql, values)
        self.connection.commit()
        return f"{firstName} {lastName} added successfully."

    # returns an array of arrays containing all information available
    def read(self):
        sql = "SELECT * FROM RegisteredUsers"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    # if the information is not provided by the user, pass None as argument
    def update(self, email, password, address, phone, attendeeType, affiliateOrganization):
        sql = "UPDATE RegisteredUsers SET "

        # appends all the information fields that need to be updated
        if email is not None:
            sql = sql + "email = %s, "
        if password is not None:
            sql = sql + "password = %s, "
        if address is not None:
            sql = sql + "address = %s, "
        if phone is not None:
            sql = sql + "phone = %s, "
        if attendeeType is not None:
            sql = sql + "attendeeType = %s, "
        if affiliateOrganization is not None:
            sql = sql + "affiliateOrganization = %s, "



    # deletes user with the primary key "email"
    def delete(self, email):
        sql = "DELETE FROM RegisteredUsers WHERE email = %s"
        values = email
        self.cursor.execute(sql, values)
        self.connection.commit()
        return "User deleted successfully."


def create_user(name, email):
    sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
    values = (name, email)
    cursor.execute(sql, values)
    connection.commit()
    print(f"User {name} added successfully.")