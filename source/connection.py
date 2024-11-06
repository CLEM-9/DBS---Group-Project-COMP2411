import mysql.connector

class Connection:
    def __init__(self, username, password, database):
        self.connection = mysql.connector.connect(
            host= "localhost",   # will run locally
            user= username,   # name of the user that is allowed to access
            password= password,  # password for the user
            database= database # name of the database
        )

        self.cursor = self.connection.cursor()