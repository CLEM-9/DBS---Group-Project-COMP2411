from unittest import TestCase
from source.crud_operations import *
from source.db_connection import get_db_connection

connection, cursor = get_db_connection("banquet_database")
user = Attendees(cursor, connection)
email = "<EMAIL@MAIL.IT>"
password = "<PASSWORD>"
address = "<ADDRESS>"
lastName = "<LASTNAME>"
firstName = "<FIRSTNAME>"
phone = "<PHONE>"
attendeeType = "Staff"
affiliation = "<AFFILIATION>"

class TestAttendees(TestCase):
    def test_create_read(self):
        user.delete_all_entries()
        print(user.create(email, password, address, lastName, firstName, phone, attendeeType, affiliation))
        message = user.read()
        print(message)
        self.assertEqual(message, "<EMAIL@MAIL.IT>, <PASSWORD>, <ADDRESS>, <LASTNAME>, <FIRSTNAME>, <PHONE>, Staff, <AFFILIATION>, \n")
        print(user.delete_all_entries())
        self.assertEqual(user.read(), "")

    def test_update(self):
        user.delete_all_entries()
        user.create(email, password, address, lastName, firstName, phone, attendeeType, affiliation)
        print(user.user_update_own_info(email, "TEST@TEST.TEST", None, None, None, None, None))
        message = user.read()
        print(message)
        self.assertEqual(message, "TEST@TEST.TEST, <PASSWORD>, <ADDRESS>, <LASTNAME>, <FIRSTNAME>, <PHONE>, Staff, <AFFILIATION>, \n")
        print(user.user_update_own_info("TEST@TEST.TEST", None, None, None, "33333333", None, None))
        message = user.read()
        print(message)
        self.assertEqual(message, "TEST@TEST.TEST, <PASSWORD>, <ADDRESS>, <LASTNAME>, <FIRSTNAME>, 33333333, Staff, <AFFILIATION>, \n")
        print(user.delete_all_entries())

    def test_delete_all_entries(self):
        user.create(email, password, address, lastName, firstName, phone, attendeeType, affiliation)
        user.delete(email)
        self.assertEqual(user.read(), "")
