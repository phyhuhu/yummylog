# from csv import DictReader
from app import db
from models import db, connect_db, Users, Questions, APIs, UsersFoodRecipesLikes, UsersDrinkRecipesLikes, FoodCategories, FoodAreas, FoodRecipes, DrinkCategories, DrinkRecipes

import requests, json

db.drop_all()
db.create_all()

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

meals=requests.get('https://www.themealdb.com/api/json/v1/1/list.php?c=list')
categories=json.loads(meals.text)['meals']

food_categories=[FoodCategories(food_category=i['strCategory']) for i in categories]
food_categories.append(FoodCategories(food_category='Unknown'))
db.session.add_all(food_categories)
db.session.commit()

meals=requests.get('https://www.themealdb.com/api/json/v1/1/list.php?a=list')
areas=json.loads(meals.text)['meals']

food_areas=[FoodAreas(food_area=i['strArea']) for i in areas]
db.session.add_all(food_areas)
db.session.commit()

drinks=requests.get('https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list')
categories=json.loads(drinks.text)['drinks']

drink_categories=[DrinkCategories(drink_category=i['strCategory']) for i in categories]
db.session.add_all(drink_categories)
db.session.commit()