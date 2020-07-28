"""User tests."""

# run these tests like:
#
#    python -m unittest test_user.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, connect_db, Users, Questions, APIs
from models import UsersFoodRecipesLikes, UsersDrinkRecipesLikes, FoodCategories, FoodAreas, FoodRecipes, DrinkCategories, DrinkRecipes


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgres:///recipes"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserTestCase(TestCase):
    """Test user signup and sign in."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        que1=Questions(question='What is the name of your first pet?')
        que2=Questions(question='Where did you grow up?')
        que3=Questions(question='What is your favorite food?')

        db.session.add_all([que1,que2,que3])
        db.session.commit()

        u1 = Users.signup("test1", "email1@email.com", "password", 1, 'answer', None, None, None, None)
        uid1 = 1111
        u1.id = uid1

        u2 = Users.signup("test2", "email2@email.com", "password", 2, 'answer', None, None, None, None)
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = Users.query.get(uid1)
        u2 = Users.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_user_model(self):
        """Does basic model work?"""

        u = Users(
            username="testuser",
            email="test@test.com",
            password="HASHED_PASSWORD",
            question_id=1,
            answer="HASHED_ANSWER",
            location='LOCATION',
            image_url=None,
            level=None,
            bio=None
        )

        db.session.add(u)
        db.session.commit()

        # User should have no food and drink recipes
        self.assertEqual(len(u.food_posts), 0)
        self.assertEqual(len(u.drink_posts), 0)
        self.assertEqual(len(u.food_likes), 0)
        self.assertEqual(len(u.drink_likes), 0)

    ####
    #
    # Signup Tests
    #
    ####
    def test_valid_signup(self):
        u_test = Users.signup("testtesttest", "testtest@test.com", "password", 1, 'answer', None, None, None, None)
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = Users.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtesttest")
        self.assertEqual(u_test.email, "testtest@test.com")
        self.assertNotEqual(u_test.password, "password")
        self.assertEqual(u_test.question_id, 1)
        self.assertNotEqual(u_test.answer, "answer")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = Users.signup(None, "test@test.com", "password", 1, 'answer', None, None, None, None)
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = Users.signup("testtest", None, "password", 1, 'answer', None, None, None, None)
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            Users.signup("testtest", "email@email.com", "", 1, 'answer', None, None, None, None)
        
        with self.assertRaises(ValueError) as context:
            Users.signup("testtest", "email@email.com", None, 1, 'answer', None, None, None, None)

    def test_invalid_answer_signup(self):
        with self.assertRaises(ValueError) as context:
            Users.signup("testtest", "email@email.com", "password", 1, '', None, None, None, None)
        
        with self.assertRaises(ValueError) as context:
            Users.signup("testtest", "email@email.com", "password", 1, None, None, None, None, None)
    
    ####
    #
    # Authentication Tests
    #
    ####
    def test_valid_authentication(self):
        u = Users.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        self.assertFalse(Users.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(Users.authenticate(self.u1.username, "badpassword"))