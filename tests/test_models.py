"""
Test cases for Account Model
"""
import logging
import unittest
import os

from service import app
from service.models import Account,
DataValidationError, db
from tests.factories import AccountFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI",
    "postgresql://postgres:postgres@localhost:5432/postgres"
)

class TestAccount(unittest.TestCase):
    """Test Cases for Account Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Account.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        pass

    def setUp(self):
        """This runs before each test"""
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        
    def test_create_an_account(self):
        """It should Create an Account and assert that it exists"""
        fake_account = AccountFactory()

        account = Account(
            name=fake_account.name,
            email=fake_account.email,
            address=fake_account.address,
            phone_number=fake_account.phone_number,
            date_joined=fake_account.date_joined,
        )

        self.assertIsNotNone(account)
        self.assertEqual(account.id, None)
        self.assertEqual(account.name,
        fake_account.name)
        self.assertEqual(account.email,
        fake_account.email)
        self.assertEqual(account.address,
        fake_account.address)
        self.assertEqual(account.phone_number,
        fake_account.phone_number)
        self.assertEqual(account.date_joined,
        fake_account.date_joined)

    def test_add_a_account(self):
        """It should Create an account and add it to the database"""
        self.assertEqual(Account.all(), [])

        account = AccountFactory()
        account.create()

        self.assertIsNotNone(account.id)
        self.assertEqual(len(Account.all()), 1)

    def test_read_account(self):
        """It should Read an account"""
        account = AccountFactory()
        account.create()

        found = Account.find(account.id)

        self.assertEqual(found.id,
        account.id)
        self.assertEqual(found.name, 
        account.name)
        self.assertEqual(found.email, 
        account.email)
        self.assertEqual(found.address, 
        account.address)
        self.assertEqual(found.phone_number, 
        account.phone_number)
        self.assertEqual(found.date_joined, 
        account.date_joined)

    def test_update_account(self):
        """It should Update an account"""
        account = AccountFactory(email="advent@change.me")
        account.create()

        self.assertEqual(account.email, 
        "advent@change.me")

        account = Account.find(account.id)
        account.email = "XYZZY@plugh.com"
        account.update()

        updated = Account.find(account.id)
        self.assertEqual(updated.email, 
        "XYZZY@plugh.com")

    def test_delete_an_account(self):
        """It should Delete an account from the database"""
        self.assertEqual(Account.all(), [])

        account = AccountFactory()
        account.create()

        self.assertEqual(len(Account.all()), 1)

        account = Account.all()[0]
        account.delete()

        self.assertEqual(len(Account.all()), 0)

    def test_list_all_accounts(self):
        """It should List all Accounts in the database"""
        self.assertEqual(Account.all(), [])

        for account in AccountFactory.create_batch(5):
            account.create()

        self.assertEqual(len(Account.all()), 5)

    def test_find_by_name(self):
        """It should Find an Account by name"""
        account = AccountFactory()
        account.create()

        result = Account.find_by_name(account.name)[0]

        self.assertEqual(result.id, 
        account.id)
        self.assertEqual(result.name,
        account.name)

    def test_serialize_an_account(self):
        """It should Serialize an account"""
        account = AccountFactory()
        data = account.serialize()

        self.assertEqual(data["id"], 
        account.id)
        self.assertEqual(data["name"],
        account.name)
        self.assertEqual(data["email"], 
        account.email)
        self.assertEqual(data["address"], 
        account.address)
        self.assertEqual(data["phone_number"],
        account.phone_number)
        self.assertEqual(data["date_joined"], 
        str(account.date_joined))

    def test_deserialize_an_account(self):
        """It should Deserialize an account"""
        account = AccountFactory()
        account.create()

        data = account.serialize()
        new_account = Account()
        new_account.deserialize(data)

        self.assertEqual(new_account.name, 
        account.name)
        self.assertEqual(new_account.email, 
        account.email)
        self.assertEqual(new_account.address,
        account.address)
        self.assertEqual(new_account.phone_number,
        account.phone_number)
        self.assertEqual(new_account.date_joined, 
        account.date_joined)

    def test_deserialize_with_key_error(self):
        """It should not Deserialize an account with a KeyError"""
        account = Account()
        self.assertRaises(DataValidationError,
        account.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize an account with a TypeError"""
        account = Account()
        self.assertRaises(DataValidationError,
        account.deserialize, [])
