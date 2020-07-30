# Yummylog

Please find the website on Heroku:
[https://yummylog.herokuapp.com/](https://yummylog.herokuapp.com/)

## Project Goals

Do you like yummy food? Do you like to share your food with foodies? 
This website is to designed to help you to search yummy food 
and share your food with people who also love yummy food all around the world.


## APIs & Data Involved

This website connects to three APIs: 
TheMealDB API for food recipes 
([https://www.themealdb.com/api.php?ref=apilist.fun](https://www.themealdb.com/api.php?ref=apilist.fun)),
TheCocktailDB for drink recipes 
([https://www.thecocktaildb.com/api.php?ref=apilist.fun](https://www.thecocktaildb.com/api.php?ref=apilist.fun)),
the IBM text-to-speech API for transferring text to speech
([https://cloud.ibm.com/apidocs/text-to-speech?code=python](https://cloud.ibm.com/apidocs/text-to-speech?code=python)).

**Please Note**: Both TheMealDB and TheCocktailDB APIs are free.
The IBM text-to-speech API has free 10,000 Characters per Month.
We just transfer the names of food or drink to speech.

In addition, we have used the BeautifulSoup to grab the food nutrition data 
from the website [https://www.fatsecret.com"](https://www.fatsecret.com).
We have done rough data cleaning for those food nutrition data.


## Functionality

- Sign up with a unique username and E-Mail including hashed password.
- Edit user profile details.
- Reset password with answering security questions.
- Find username and reset password with E-Mail used when signing up.
- Search or create food and drink recipes from APIs.
- Edit food or drink recipes that you created.
- Four levels for users: Foodie (no recipes); Home Chef (1-5 recipes); Junior Chef (6-10 recipes); Head Chef (more than 11 recipes).
- Thumbs up for liking the food or drink recipes.
- Transfer the food or drink names to speech.


## Major Technologies

- Flask
- Flask SQLAlchemy
- PostgreSQL
- Flask-Login
- Flask-Email
- WTForms
- Bootstrap
- Jquery
- DOM manipulation
- Jinja
- BeautifulSoup
- Json
- Requests
- Fontawesome
- Matplotlib
- Numpy
- Unittest
