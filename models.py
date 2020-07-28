"""SQLAlchemy models for Recipes."""

from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)


# APIs part
class APIs(db.Model):
    """ apis """

    __tablename__ = 'apis'

    id = db.Column(db.Integer, primary_key=True)
    api = db.Column(db.String, nullable=False, unique=True)
    api_url = db.Column(db.String, nullable=False, unique=True)

    food_recipes = db.relationship("FoodRecipes", backref="food_api", cascade="all, delete-orphan")
    drink_recipes = db.relationship("DrinkRecipes", backref="drink_api", cascade="all, delete-orphan")

# food part
class FoodCategories(db.Model):
    """ food categories """

    __tablename__ = 'food_categories'

    id = db.Column(db.Integer, primary_key=True)
    food_category = db.Column(db.String, nullable=False, unique=True)

    food_recipes = db.relationship("FoodRecipes", backref="food_category", cascade="all, delete-orphan")

class FoodAreas(db.Model):
    """ food areas """

    __tablename__ = 'food_areas'

    id = db.Column(db.Integer, primary_key=True)
    food_area = db.Column(db.String, nullable=False, unique=True)

    food_recipes = db.relationship("FoodRecipes", backref="food_area", cascade="all, delete-orphan")

class FoodRecipes(db.Model):
    """food recipes"""

    __tablename__ = 'food_recipes'

    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String, nullable=False)
    food_category_id = db.Column(db.Integer, db.ForeignKey('food_categories.id', ondelete='CASCADE'))
    food_area_id = db.Column(db.Integer, db.ForeignKey('food_areas.id', ondelete='CASCADE'))
    food_ingredients = db.Column(db.String)
    food_instructions = db.Column(db.String)
    food_photo_url = db.Column(db.String)
    speech = db.Column(db.Boolean, default=False)
    source = db.Column(db.Boolean, default=False)
    api_id = db.Column(db.Integer, db.ForeignKey('apis.id', ondelete='CASCADE'))
    id_in_api = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    @classmethod
    def add_food(cls, food_name, food_category_id, food_area_id, food_ingredients, food_instructions, 
    food_photo_url, speech=False, source=False, api_id=None, id_in_api=None, user_id=None):
        """Add food recipes to database.
        """

        meal = FoodRecipes(
            food_name=food_name,
            food_category_id=food_category_id,
            food_area_id=food_area_id,
            food_ingredients=food_ingredients,
            food_instructions=food_instructions,
            food_photo_url=food_photo_url,
            speech=speech,
            source=source,
            api_id=api_id,
            id_in_api=id_in_api,
            user_id=user_id
            )
        db.session.add(meal)

        return meal

# drink part
class DrinkCategories(db.Model):
    """ drink categories """

    __tablename__ = 'drink_categories'

    id = db.Column(db.Integer, primary_key=True)
    drink_category = db.Column(db.String, nullable=False, unique=True)

    drink_recipes = db.relationship("DrinkRecipes", backref="drink_category", cascade="all, delete-orphan")

class DrinkRecipes(db.Model):
    """drink recipes"""

    __tablename__ = 'drink_recipes'

    id = db.Column(db.Integer, primary_key=True)
    drink_name = db.Column(db.String, nullable=False)
    drink_category_id = db.Column(db.Integer, db.ForeignKey('drink_categories.id', ondelete='CASCADE'))
    drink_ingredients = db.Column(db.String)
    drink_instructions = db.Column(db.String)
    drink_photo_url = db.Column(db.String)
    alcoholic = db.Column(db.Boolean, default=False)
    speech = db.Column(db.Boolean, default=False)
    source = db.Column(db.Boolean, default=False)
    api_id = db.Column(db.Integer, db.ForeignKey('apis.id', ondelete='CASCADE'))
    id_in_api = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    @classmethod
    def add_drink(cls, drink_name, drink_category_id, drink_ingredients, drink_instructions, 
    drink_photo_url, alcoholic, speech=False, source=False, api_id=None, id_in_api=None, user_id=None):
        """Add drink recipes to database.
        """

        drink = DrinkRecipes(
            drink_name=drink_name,
            drink_category_id=drink_category_id,
            drink_ingredients=drink_ingredients,
            drink_instructions=drink_instructions,
            drink_photo_url=drink_photo_url,
            alcoholic=alcoholic,
            speech=speech,
            source=source,
            api_id=api_id,
            id_in_api=id_in_api,
            user_id=user_id
            )
        db.session.add(drink)

        return drink


# users part
class Questions(db.Model):
    """ questions """

    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False, unique=True)

class Users(db.Model):
    """Users in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    answer = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    image_url = db.Column(db.String, default="/static/images/default-pic.png")
    level = db.Column(db.String, default='Foodie')
    bio = db.Column(db.String, default='N/A')

    question = db.relationship("Questions", backref="user")

    food_posts = db.relationship("FoodRecipes", backref="food_postby_user", cascade="all, delete-orphan")
    drink_posts = db.relationship("DrinkRecipes", backref="drink_postby_user", cascade="all, delete-orphan")

    food_likes = db.relationship('FoodRecipes', secondary="users_food_recipes_likes", backref='users_like_food')
    drink_likes = db.relationship('DrinkRecipes', secondary="users_drink_recipes_likes", backref='users_like_drink')

    def __repr__(self):
        return f"<Users #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password, question_id, answer, location, image_url, level, bio):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        hashed_ans = bcrypt.generate_password_hash(answer).decode('UTF-8')

        user = Users(
            username=username,
            email=email,
            password=hashed_pwd,
            question_id=question_id,
            answer=hashed_ans,
            location=location,
            image_url=image_url,
            level=level,
            bio=bio
            )
        db.session.add(user)

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    @classmethod
    def checkanswer(cls, username, answer):
        """Find user with `username` and `answer`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose answer hash matches this answer
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if answer is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.answer, answer)
            if is_auth:
                return user

        return False

class UsersFoodRecipesLikes(db.Model):
    """Mapping users like to food."""

    __tablename__ = 'users_food_recipes_likes' 

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    food_recipe_id = db.Column(db.Integer, db.ForeignKey('food_recipes.id', ondelete='cascade'), primary_key=True)

class UsersDrinkRecipesLikes(db.Model):
    """Mapping users like to drink."""

    __tablename__ = 'users_drink_recipes_likes' 

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    drink_recipe_id = db.Column(db.Integer, db.ForeignKey('drink_recipes.id', ondelete='cascade'), primary_key=True)