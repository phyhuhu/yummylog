"""Drink recipes tests."""

# run these tests like:
#
#    python -m unittest test_food.py


import os, requests, json
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


class DrinkTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        # ===============
        api1=APIs(api='TheMealDB', api_url='https://www.themealdb.com/api.php?ref=apilist.fun')
        api2=APIs(api='TheCockTailDB', api_url='https://www.thecocktaildb.com/api.php?ref=apilist.fun')
        api3=APIs(api='EDAMAM', api_url='https://www.edamam.com/')
        api4=APIs(api='IBM_text_to_speech', api_url='https://cloud.ibm.com/apidocs/text-to-speech?code=python')
        api5=APIs(api='Recipe Puppy', api_url='http://www.recipepuppy.com/about/api/?ref=apilist.fun')

        db.session.add_all([api1,api2,api3,api4,api5])
        db.session.commit()

        que1=Questions(question='What is the name of your first pet?')
        que2=Questions(question='Where did you grow up?')
        que3=Questions(question='What is your favorite food?')

        db.session.add_all([que1,que2,que3])
        db.session.commit()

        drinks=requests.get('https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list')
        categories=json.loads(drinks.text)['drinks']

        drink_categories=[DrinkCategories(drink_category=i['strCategory']) for i in categories]
        db.session.add_all(drink_categories)
        db.session.commit()
        # ===============

        self.uid = 94566
        u = Users.signup("test", "email@email.com", "password", 1, 'answer', None, None, None, None)
        u.id = self.uid
        db.session.commit()

        self.u = Users.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_drink_model(self):
        """Does basic model work?"""
        
        d = DrinkRecipes(
            drink_name='drink_name',
            drink_category_id=1,
            drink_ingredients='drink_ingredients',
            drink_instructions='drink_instructions',
            drink_photo_url='drink_photo_url',
            alcoholic=True,
            source=False,
            api_id=2,
            id_in_api=8,
            user_id=None
        )

        db.session.add(d)
        db.session.commit()

        self.assertEqual(d.drink_name, 'drink_name')
        self.assertEqual(d.drink_category_id, 1)
        self.assertEqual(d.alcoholic, True)
        self.assertEqual(d.drink_ingredients, 'drink_ingredients')
        self.assertEqual(d.drink_instructions, 'drink_instructions')
        self.assertEqual(d.drink_photo_url, 'drink_photo_url')
        self.assertEqual(d.source, False)
        self.assertEqual(d.api_id, 2)
        self.assertEqual(d.id_in_api, 8)

    def test_drink_likes(self):
        d = DrinkRecipes(
            drink_name='drink_name',
            drink_category_id=1,
            drink_ingredients='drink_ingredients',
            drink_instructions='drink_instructions',
            drink_photo_url='drink_photo_url',
            alcoholic=True,
            source=True,
            api_id=None,
            id_in_api=None,
            user_id=888
        )

        u = Users.signup("testtest", "emailtest@email.com", "password", 1, 'answer', None, None, None, None)
        uid = 888
        u.id = uid
        db.session.add_all([d, u])
        db.session.commit()

        u.drink_likes.append(d)

        db.session.commit()

        l = UsersDrinkRecipesLikes.query.filter(UsersDrinkRecipesLikes.user_id == uid).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].drink_recipe_id, d.id)


        