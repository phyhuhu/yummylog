from flask import Flask, url_for, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from werkzeug import secure_filename
import requests, json, os

from forms import UserSignUpForm, UserEditForm, UserLoginForm, UsernameForm, AnswerForm, ResetPWForm, EmailForm
from forms import SearchFoodRecipesForm, SearchDrinkRecipesForm, CreateFoodRecipesForm, CreateDrinkRecipesForm

from models import db, connect_db, Users, Questions, APIs
from models import UsersFoodRecipesLikes, UsersDrinkRecipesLikes, FoodCategories, FoodAreas, FoodRecipes, DrinkCategories, DrinkRecipes
from calculate_nutritions import calculate_nutritions
from plot_nutritions import plot_nutritions
from create_speech import IBM_Text_To_Speech

# from secret import PW_GMAIL


CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///recipes'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
# toolbar = DebugToolbarExtension(app)

bcrypt = Bcrypt()
connect_db(app)

# for sending gmail
PW_GMAIL=os.environ.get('PW_GMAIL')

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'yummylog2020@gmail.com',
    "MAIL_PASSWORD": PW_GMAIL
}

app.config.update(mail_settings)
mail = Mail(app)
URL_HOME='https://yummylog.herokuapp.com/' #'http://127.0.0.1:5000/'


######################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If user logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = Users.query.get(session[CURR_USER_KEY])

        posts_num=0
        if g.user:
            if g.user.food_posts:
                posts_num+=len(g.user.food_posts)
            if  g.user.drink_posts:
                posts_num+=len(g.user.drink_posts)
            if posts_num==0:
                g.user.level='Foodie'
                db.session.commit()
            elif posts_num>0 and posts_num<=5:
                g.user.level='Home Chef'
                db.session.commit()
            elif posts_num>5 and posts_num<=10:
                g.user.level='Junior Chef'
                db.session.commit()
            elif posts_num>10:
                g.user.level='Head Chef'
                db.session.commit()

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if 'food_speech' in session:
        del session['food_speech']

    if 'drink_speech' in session:
        del session['drink_speech']

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


##############################################################################
# Homepage and error pages

@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404


######################################################################
# User pages for sign up and sign in

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserSignUpForm()

    questions = [('0', 'Choose ...')] + [(str(que.id), que.question) for que in Questions.query.all()]

    form.question.choices = questions

    if form.validate_on_submit():
        user=Users.query.filter(Users.username==form.username.data)
        if user.count()>0:
            flash("Username already has been taken. Please choose another username.")
            return render_template('users/signup.html', form=form)

        user=Users.query.filter(Users.email==form.email.data)
        if user.count()>0:
            flash("E-mail already has been used. Please use another E-mail.")
            return render_template('users/signup.html', form=form)

        user = Users.signup(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            question_id=int(form.question.data),
            answer=form.answer.data,
            location=form.location.data,
            image_url=form.image_url.data or Users.image_url.default.arg,
            level=Users.level.default.arg,
            bio=form.bio.data or Users.bio.default.arg
        )
        db.session.commit()

        do_login(user)
        add_user_to_g()

        return redirect(f"/users/{g.user.id}/home")

    return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = UserLoginForm()

    if form.validate_on_submit():
        user = Users.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            add_user_to_g()
            return redirect(f"/users/{g.user.id}/home")

        flash("Wrong username or password, please try again.")

    return render_template('users/login.html', form=form)


@app.route('/inputusername', methods=["GET", "POST"])
def inputusername():
    """Check user's answer for reseting password."""
    
    form=UsernameForm()

    if form.validate_on_submit():
        user=Users.query.filter(Users.username==form.username.data)
        if(user.count()>0):
            question_id=user[0].question_id
            question=Questions.query.get_or_404(question_id).question

            session['question'] = question
            session['username'] = form.username.data
            return redirect('/checkanswer')
        
        flash("Wrong username, please try again.")

    return render_template('users/inputusername.html', form=form)

@app.route('/checkanswer', methods=["GET", "POST"])
def checkanswer():
    """Check user's answer for reseting password."""
    
    form=AnswerForm()
    username=session['username']

    if form.validate_on_submit():
        if Users.checkanswer(username, form.answer.data):
            return redirect('/resetpw')

        flash("Wrong answer, please try again.")

    question=session['question']
    return render_template('users/checkanswer.html', form=form, question=question)

@app.route('/inputemail', methods=["GET", "POST"])
def inputemail():
    """Through Email to get a link for reseting password."""
    
    form=EmailForm()

    if form.validate_on_submit():
        user=Users.query.filter(Users.email==form.email.data)

        if user.count() != 1:
            flash("Wrong email, please try again.")

        else:
            username=user[0].username
            email=user[0].email

            msg=Message(
                f'for {username}', 
                sender ='yummylog2020@gmail.com', 
                recipients = [f'{email}']
                )
            msg.body = URL_HOME+'resetpw'
            mail.send(msg)

            session['username'] = username

            return 'Mail Sent. Please check your E-mail.'

    return render_template('users/inputemail.html', form=form)

@app.route('/resetpw', methods=["GET", "POST"])
def restepw():
    """Check user's answer for reseting password."""
    
    form=ResetPWForm()
    username=session['username']

    if form.validate_on_submit():
        user=Users.query.filter(Users.username==username)[0]
        
        user.password=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')

        db.session.commit()

        return redirect('/login')

    return render_template('users/resetpw.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    add_user_to_g()

    return redirect("/login")


##############################################################################
# General user routes:

@app.route('/users/<int:user_id>/home')
def list_all(user_id):
    """Page with listing of users.

    Can take a 'q' param in querystring to search by that username.
    """

    user=g.user

    users=Users.query.all()

    all_food=FoodRecipes.query.all()
    num=[]
    for i in range(len(all_food)):
        num.append((i, len(all_food[i].users_like_food)))
    num=sorted(num, key=lambda x: x[1], reverse=True)
    five_food=[]
    for k in range(min(5, len(num))):
        i,j=num[k]
        five_food.append(all_food[i])

    all_drink=DrinkRecipes.query.all()
    num=[]
    for i in range(len(all_drink)):
        num.append((i, len(all_drink[i].users_like_drink)))
    num=sorted(num, key=lambda x: x[1], reverse=True)
    five_drink=[]
    for k in range(min(5, len(num))):
        i,j=num[k]
        five_drink.append(all_drink[i])

    return render_template('users/user_home.html', user=user, users=users,
            five_food=five_food, five_drink=five_drink, all_food=all_food, all_drink=all_drink)

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show user profile."""

    user=g.user

    all_food=FoodRecipes.query.all()
    all_drink=DrinkRecipes.query.all()

    food_recipes=FoodRecipes.query.filter(FoodRecipes.user_id==user_id)
    drink_recipes=DrinkRecipes.query.filter(DrinkRecipes.user_id==user_id)

    food_recipes_likes=user.food_likes
    drink_recipes_likes=user.drink_likes

    return render_template('users/detail.html', user=user, food_recipes=food_recipes, drink_recipes=drink_recipes, food_recipes_likes=food_recipes_likes, drink_recipes_likes=drink_recipes_likes, all_food=all_food, all_drink=all_drink)


@app.route('/food/<int:food_id>/likes', methods=['POST'])
def add_food_like(food_id):
    """Toggle a liked food for the currently-logged-in user."""

    food = FoodRecipes.query.get_or_404(food_id)

    user_likes = g.user.food_likes

    if food in user_likes:
        g.user.food_likes = [like for like in user_likes if like != food]
    else:
        g.user.food_likes.append(food)

    db.session.commit()

    if not food.source:
        return redirect(f'/food/search/{food.id_in_api}')
    else:
        return redirect(f'/food/create/{food_id}')

@app.route('/drink/<int:drink_id>/likes', methods=['POST'])
def add_drink_like(drink_id):
    """Toggle a liked drink for the currently-logged-in user."""

    drink = DrinkRecipes.query.get_or_404(drink_id)

    user_likes = g.user.drink_likes

    if drink in user_likes:
        g.user.drink_likes = [like for like in user_likes if like != drink]
    else:
        g.user.drink_likes.append(drink)

    db.session.commit()

    if not drink.source:
        return redirect(f'/drink/search/{drink.id_in_api}')
    else:
        return redirect(f'/drink/create/{drink_id}')

@app.route('/food/<int:food_id>/speech', methods=['POST'])
def add_food_speech(food_id):
    """Toggle a liked food for the currently-logged-in user."""

    food = FoodRecipes.query.get_or_404(food_id)
    food_id_speech, speech=session['food_speech']

    if food_id_speech == food_id:
        session['food_speech']=(food_id,True)

        if not food.source:
            filename='search_food_'+str(food.id_in_api)
        else:
            filename='create_food_'+str(food.id)
        IBM_Text_To_Speech(food.food_name,filename).create_speech()

    if not food.source:
        return redirect(f'/food/search/{food.id_in_api}')
    else:
        return redirect(f'/food/create/{food_id}')

@app.route('/drink/<int:drink_id>/speech', methods=['POST'])
def add_drink_speech(drink_id):
    """Toggle a liked drink for the currently-logged-in user."""

    drink = DrinkRecipes.query.get_or_404(drink_id)
    drink_id_speech, speech=session['drink_speech']

    if drink_id_speech == drink_id:
        session['drink_speech']=(drink_id,True)

        if not drink.source:
            filename='search_drink_'+str(drink.id_in_api)
        else:
            filename='create_drink_'+str(drink.id)
        IBM_Text_To_Speech(drink.drink_name,filename).create_speech()

    if not drink.source:
        return redirect(f'/drink/search/{drink.id_in_api}')
    else:
        return redirect(f'/drink/create/{drink_id}')

@app.route('/users/profile', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if Users.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.location = form.location.data
            user.image_url = form.image_url.data or Users.image_url.default.arg
            user.bio = form.bio.data or Users.bio.default.arg

            db.session.commit()
            return redirect(f"/users/{user.id}")

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/edit.html', form=form, user_id=user.id)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    curr_user=g.user
    db.session.delete(curr_user)
    db.session.commit()

    return redirect("/signup")


##############################################################################
# Search Food Recipes routes:

@app.route('/food/search', methods=["GET", "POST"])
def search_food_recipes():
    """search food recipes."""

    form = SearchFoodRecipesForm()

    searchby = [('0', 'Choose ...'), ('1', 'Categories'), ('2', 'Areas'), ('3', 'Ingredients')]
    form.searchby.choices = searchby

    if form.validate_on_submit():
        base_url='https://www.themealdb.com/api/json/v1/1/filter.php?'
        if form.searchby.data == '1':

            meals=requests.get('https://www.themealdb.com/api/json/v1/1/list.php?c=list')
            categories=json.loads(meals.text)['meals']

            food_categories={i['strCategory'] for i in categories}
            if form.searchinput.data.capitalize() not in food_categories:
                flash("The key words are not in our database. Please try others.")

                return render_template('foodrecipes/searchfoodrecipes.html', form=form)

            url=base_url+'c='+form.searchinput.data.capitalize()

        elif form.searchby.data == '2':

            meals=requests.get('https://www.themealdb.com/api/json/v1/1/list.php?a=list')
            areas=json.loads(meals.text)['meals']

            food_areas={i['strArea'] for i in areas}
            if form.searchinput.data.capitalize() not in food_areas:
                flash("The key words are not in our database. Please try others.")

                return render_template('foodrecipes/searchfoodrecipes.html', form=form)

            url=base_url+'a='+form.searchinput.data.capitalize()

        elif form.searchby.data == '3':

            meals=requests.get('https://www.themealdb.com/api/json/v1/1/list.php?i=list')
            ingredients=json.loads(meals.text)['meals']

            food_ingredients={i['strIngredient'] for i in ingredients}
            if form.searchinput.data.capitalize() not in food_ingredients:
                flash("The key words are not in our database. Please try others.")

                return render_template('foodrecipes/searchfoodrecipes.html', form=form)

            url=base_url+'i='+form.searchinput.data.capitalize()

        session['food_url']=(form.searchby.data,form.searchinput.data,url)
        return redirect(f'/food/search/{form.searchby.data}/{form.searchinput.data}')

    return render_template('foodrecipes/searchfoodrecipes.html', form=form)


@app.route('/food/search/<int:searchby>/<string:searchinput>', methods=["GET"])
def results_food_recipes(searchby,searchinput):
    """show results of food recipes."""

    searchby,searchinput,url=session['food_url']

    meals=json.loads(requests.get(url).text)['meals']

    return render_template('foodrecipes/resultsfoodrecipes.html', meals=meals, searchby=searchby, searchinput=searchinput)

@app.route('/food/search/<int:id>', methods=["GET"])
def food_recipes_by_id(id):
    """show food recipes by id."""

    meal_database=FoodRecipes.query.filter(FoodRecipes.id_in_api==id)
    
    if meal_database.count()==0:

        url_id=f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}'
        full_meal=json.loads(requests.get(url_id).text)['meals'][0]

        food_category_id=FoodCategories.query.filter(FoodCategories.food_category==full_meal['strCategory'])[0].id
        food_area_id=FoodAreas.query.filter(FoodAreas.food_area==full_meal['strArea'])[0].id

        food_ingredients_dict={}
        food_ingredients=''
        for item in full_meal:
            if item[:13]=="strIngredient" and full_meal[item]:
                food_ingredients_dict[full_meal[item]]=full_meal['strMeasure'+item[13:]]
                food_ingredients+=full_meal[item]+':'+full_meal['strMeasure'+item[13:]].replace(' ','')+', '

        temp_instructions=full_meal['strInstructions'].replace('\r', ' ').replace('\n', ' ').split('.')
        for i in range(len(temp_instructions)):
            if i<len(temp_instructions)-1:
                if temp_instructions[i].replace(' ','').isdigit():
                    temp_instructions[i+1]=temp_instructions[i]+': '+temp_instructions[i+1]
                    temp_instructions[i]=''
            if len(temp_instructions[i])>=1 and temp_instructions[i][0]==')':
                temp_instructions[i-1]=temp_instructions[i-1]+temp_instructions[i]
                temp_instructions[i]=''
        meal_instructions='.'.join(temp_instructions)

        meal = FoodRecipes.add_food(
                food_name=full_meal['strMeal'],
                food_category_id=food_category_id,
                food_area_id=food_area_id,
                food_ingredients=food_ingredients,
                food_instructions=meal_instructions,
                food_photo_url=full_meal['strMealThumb'],
                source=False,
                api_id=1,
                id_in_api=full_meal['idMeal'],
                user_id=None
                )
        db.session.commit()

    else:

        meal=meal_database[0]

        food_ingredients_dict={}
        for item in meal.food_ingredients.split(','):
            if item!='' or item!=' ':
                temp=item.split(':')
                if len(temp)>1:
                    food_ingredients_dict[temp[0].lstrip()]=temp[1]

    food_nutritions_dict={}
    for ingredient in food_ingredients_dict:
        food_nutritions_dict[ingredient]=calculate_nutritions(ingredient, food_ingredients_dict[ingredient]).find()

    total_nutritions_dict={'Calories':0, 'Total Fat':0, 'Total Carbohydrate': 0, 'Protein':0}
    for item in food_nutritions_dict:
        if food_nutritions_dict[item]!=None and food_nutritions_dict[item]!={}:
            for i in food_nutritions_dict[item]:
                total_nutritions_dict[i]+=food_nutritions_dict[item][i]
                total_nutritions_dict[i]=round(total_nutritions_dict[i],2)
                food_nutritions_dict[item][i]=round(food_nutritions_dict[item][i],2)

    plot_url=plot_nutritions(total_nutritions_dict).plot_figure()

    if 'food_speech' not in session:
        session['food_speech']=(meal.id,False)
        speech=False
    elif session['food_speech'][0]!=meal.id:
        session['food_speech']=(meal.id,False)
        speech=False
    else:
        food_id_speech, speech=session['food_speech']

    return render_template('foodrecipes/detailsfoodrecipe.html', meal=meal, total_nutritions=total_nutritions_dict['Calories'], food_nutritions=food_nutritions_dict, food_ingredients=food_ingredients_dict, url=plot_url, speech=speech)


##############################################################################
# Search Drink Recipes routes:


@app.route('/drink/search', methods=["GET", "POST"])
def search_drink_recipes():
    """search drink recipes."""

    form = SearchDrinkRecipesForm()

    searchby = [('0', 'Choose ...'), ('1', 'Categories'), ('2', 'Ingredients')]
    form.searchby.choices = searchby

    if form.validate_on_submit():
        base_url='https://www.thecocktaildb.com/api/json/v1/1/filter.php?'
        if form.searchby.data == '1':

            drinks=requests.get('https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list')
            categories=json.loads(drinks.text)['drinks']

            drink_categories={i['strCategory'] for i in categories}
            if form.searchinput.data.capitalize() not in drink_categories:
                flash("The key words are not in our database. Please try others.")

                return render_template('drinkrecipes/searchdrinkrecipes.html', form=form)

            url=base_url+'c='+form.searchinput.data.capitalize()

        elif form.searchby.data == '2':

            drinks=requests.get('https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list')
            ingredients=json.loads(drinks.text)['drinks']

            drink_ingredients={i['strIngredient1'] for i in ingredients}
            if form.searchinput.data.capitalize() not in drink_ingredients:
                flash("The key words are not in our database. Please try others.")

                return render_template('drinkrecipes/searchdrinkrecipes.html', form=form)

            url=base_url+'i='+form.searchinput.data.capitalize()

        session['drink_url']=(form.searchby.data,form.searchinput.data,url)
        return redirect(f'/drink/search/{form.searchby.data}/{form.searchinput.data}')

    return render_template('drinkrecipes/searchdrinkrecipes.html', form=form)

@app.route('/drink/search/<int:searchby>/<string:searchinput>', methods=["GET"])
def results_drink_recipes(searchby,searchinput):
    """show results of drink recipes."""

    searchby,searchinput,url=session['drink_url']

    drinks=json.loads(requests.get(url).text)['drinks']

    return render_template('drinkrecipes/resultsdrinkrecipes.html', drinks=drinks, searchby=searchby, searchinput=searchinput)

@app.route('/drink/search/<int:id>', methods=["GET"])
def drink_recipes_by_id(id):
    """show drink recipes by id."""

    drink_database=DrinkRecipes.query.filter(DrinkRecipes.id_in_api==id)
    
    if drink_database.count()==0:
        url_id=f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={id}'
        full_drink=json.loads(requests.get(url_id).text)['drinks'][0]

        drink_category_id=DrinkCategories.query.filter(DrinkCategories.drink_category==full_drink['strCategory'])[0].id

        drink_ingredients_dict={}
        drink_ingredients=''
        for item in full_drink:
            if item[:13]=="strIngredient" and full_drink[item]:
                drink_ingredients_dict[full_drink[item]]=full_drink['strMeasure'+item[13:]]
                if full_drink['strMeasure'+item[13:]]:
                    drink_ingredients+=full_drink[item]+':'+full_drink['strMeasure'+item[13:]].replace(' ','')+', '
                else:
                    drink_ingredients+=full_drink[item]+':'+', '

        if full_drink['strAlcoholic']=='Alcoholic':
            drink_alcoholic=True
        else:
            drink_alcoholic=False

        drink_instructions='.'.join(full_drink['strInstructions'].replace('\r', '').replace('\n', '').split('.'))

        drink = DrinkRecipes.add_drink(
                drink_name=full_drink['strDrink'],
                drink_category_id=drink_category_id,
                drink_ingredients=drink_ingredients,
                drink_instructions=drink_instructions,
                drink_photo_url=full_drink['strDrinkThumb'],
                alcoholic=drink_alcoholic,
                source=False,
                api_id=2,
                id_in_api=full_drink['idDrink'],
                user_id=None
                )
        db.session.commit()

    else:

        drink=drink_database[0]

        drink_ingredients_dict={}
        for item in drink.drink_ingredients.split(','):
            if item!='' or item!=' ':
                temp=item.split(':')
                if len(temp)>1:
                    drink_ingredients_dict[temp[0].lstrip()]=temp[1]


    if 'drink_speech' not in session:
        session['drink_speech']=(drink.id,False)
        speech=False
    elif session['drink_speech'][0]!=drink.id:
        session['drink_speech']=(drink.id,False)
        speech=False
    else:
        drink_id_speech, speech=session['drink_speech']

    return render_template('drinkrecipes/detailsdrinkrecipe.html', drink=drink, drink_ingredients=drink_ingredients_dict, speech=speech)

##############################################################################
# Create Food Recipes routes:


@app.route('/food/create', methods=["GET", "POST"])
def create_food_recipes():
    """create food recipes."""

    form = CreateFoodRecipesForm()

    categories = [('0', 'Choose ...')] + [(str(category.id), category.food_category) for category in FoodCategories.query.all()]
    form.food_category_id.choices = categories

    areas = [('0', 'Choose ...')] + [(str(area.id), area.food_area) for area in FoodAreas.query.all()]
    form.food_area_id.choices = areas

    if form.validate_on_submit():
        name_ingredients=request.form.getlist('food_ingredients_name')
        quantity_ingredients=request.form.getlist('food_ingredients_quantity')
        instructions=request.form.getlist('food_instructions')

        food_ingredients=''
        for i in range(20):
            if name_ingredients[i]!='':
                name_ingredients[i]=name_ingredients[i].replace(',', ' ')
                food_ingredients+=name_ingredients[i]+':'+quantity_ingredients[i]+','

        food_instructions=''
        for i in range(20):
            if instructions[i]!='':
                instructions[i]=instructions[i].replace('.', ' ')
                food_instructions+=f'Step {str(i+1)}: '+instructions[i]+'.'

        meal = FoodRecipes.add_food(
                food_name=form.food_name.data,
                food_category_id=int(form.food_category_id.data),
                food_area_id=int(form.food_area_id.data),
                food_ingredients=food_ingredients,
                food_instructions=food_instructions,
                food_photo_url=form.food_photo_url.data or FoodRecipes.food_photo_url.default.arg,
                source=True,
                api_id=None,
                id_in_api=None,
                user_id=g.user.id
                )
        db.session.commit()

        posts_num=len(g.user.food_posts)+len(g.user.drink_posts)
        if posts_num==0:
            g.user.level='Foodie'
            db.session.commit()
        elif posts_num>0 and posts_num<=10:
            g.user.level='Home Chef'
            db.session.commit()
        elif posts_num>10 and posts_num<=40:
            g.user.level='Junior Chef'
            db.session.commit()
        elif posts_num>40 and posts_num<=100:
            g.user.level='Head Chef'
            db.session.commit()

        return redirect(f'/food/create/{meal.id}')

    return render_template('foodrecipes/createfoodrecipes.html', form=form)

@app.route('/food/create/<int:id>', methods=["GET"])
def food_recipes_create_by_id(id):
    """show food recipes that created by users through id."""

    meal=FoodRecipes.query.get_or_404(id)

    food_ingredients_dict={}
    for item in meal.food_ingredients.split(','):
        if item!='':
            temp=item.split(':')
            food_ingredients_dict[temp[0]]=temp[1]

    food_nutritions_dict={}
    for ingredient in food_ingredients_dict:
        food_nutritions_dict[ingredient]=calculate_nutritions(ingredient, food_ingredients_dict[ingredient]).find()

    total_nutritions_dict={'Calories':0, 'Total Fat':0, 'Total Carbohydrate': 0, 'Protein':0}
    for item in food_nutritions_dict:
        if food_nutritions_dict[item]!=None and food_nutritions_dict[item]!={}:
            for i in food_nutritions_dict[item]:
                total_nutritions_dict[i]+=food_nutritions_dict[item][i]
                total_nutritions_dict[i]=round(total_nutritions_dict[i],2)
                food_nutritions_dict[item][i]=round(food_nutritions_dict[item][i],2)

    plot_url=plot_nutritions(total_nutritions_dict).plot_figure()

    if 'food_speech' not in session:
        session['food_speech']=(meal.id,False)
        speech=False
    elif session['food_speech'][0]!=meal.id:
        session['food_speech']=(meal.id,False)
        speech=False
    else:
        food_id_speech, speech=session['food_speech']

    return render_template('foodrecipes/detailsfoodrecipe.html', meal=meal, total_nutritions=total_nutritions_dict['Calories'], food_nutritions=food_nutritions_dict, food_ingredients=food_ingredients_dict, url=plot_url, speech=speech)


@app.route('/food/edit/<int:id>', methods=["GET", "POST"])
def food_recipes_edit_by_id(id):
    """edit food recipes that created by users through id."""

    meal=FoodRecipes.query.get_or_404(id)

    form = CreateFoodRecipesForm(obj=meal)

    categories = [('0', 'Choose ...')] + [(str(category.id), category.food_category) for category in FoodCategories.query.all()]
    form.food_category_id.choices = categories

    areas = [('0', 'Choose ...')] + [(str(area.id), area.food_area) for area in FoodAreas.query.all()]
    form.food_area_id.choices = areas

    if form.validate_on_submit():
        meal.food_name=form.food_name.data
        meal.food_category_id=int(form.food_category_id.data)
        meal.food_area_id=int(form.food_area_id.data)
        meal.food_photo_url=form.food_photo_url.data

        name_ingredients=request.form.getlist('food_ingredients_name')
        quantity_ingredients=request.form.getlist('food_ingredients_quantity')
        instructions=request.form.getlist('food_instructions')

        food_ingredients=''
        for i in range(20):
            if name_ingredients[i]!='':
                food_ingredients+=name_ingredients[i]+':'+quantity_ingredients[i]+','

        food_instructions=''
        for i in range(20):
            if instructions[i]!='':
                food_instructions+=f'Step {str(i+1)}: '+instructions[i]+'.'

        meal.food_ingredients=food_ingredients
        meal.food_instructions=food_instructions

        db.session.commit()

        return redirect(f'/food/create/{meal.id}')

    food_ingredients=[["display:none;",'',''] for _ in range(20)]
    items=meal.food_ingredients.split(',')
    for i in range(len(items)):
        if items[i]!='':
            temp=items[i].split(':')
            food_ingredients[i][0]=''
            food_ingredients[i][1]=temp[0]
            food_ingredients[i][2]=temp[1]

    food_instructions=[["display:none;",''] for _ in range(20)]
    items=meal.food_instructions.split('.')
    for i in range(len(items)):
        if items[i]!='':
            temp=items[i].split(':')
            food_instructions[i][0]=''
            food_instructions[i][1]=temp[1]

    return render_template('foodrecipes/editfoodrecipes.html', form=form, meal_id=id, food_ingredients=food_ingredients, food_instructions=food_instructions)


##############################################################################
# Create Drink Recipes routes:


@app.route('/drink/create', methods=["GET", "POST"])
def create_drink_recipes():
    """create drink recipes."""

    form = CreateDrinkRecipesForm()

    categories = [('0', 'Choose ...')] + [(str(category.id), category.drink_category) for category in DrinkCategories.query.all()]
    form.drink_category_id.choices = categories

    alcoholic = [('0', 'Choose ...')] + [('1', True), ('2', False)]
    form.alcoholic.choices = alcoholic

    if form.validate_on_submit():
        name_ingredients=request.form.getlist('drink_ingredients_name')
        quantity_ingredients=request.form.getlist('drink_ingredients_quantity')
        instructions=request.form.getlist('drink_instructions')

        drink_ingredients=''
        for i in range(20):
            if name_ingredients[i]!='':
                name_ingredients[i]=name_ingredients[i].replace(',', '.')
                drink_ingredients+=name_ingredients[i]+':'+quantity_ingredients[i]+','

        drink_instructions=''
        for i in range(20):
            if instructions[i]!='':
                instructions[i]=instructions[i].replace('.', ',')
                drink_instructions+=f'Step {str(i+1)}: '+instructions[i]+'.'

        drink = DrinkRecipes.add_drink(
                drink_name=form.drink_name.data,
                drink_category_id=int(form.drink_category_id.data),
                drink_ingredients=drink_ingredients,
                drink_instructions=drink_instructions,
                drink_photo_url=form.drink_photo_url.data or DrinkRecipes.drink_photo_url.default.arg,
                alcoholic=True if form.alcoholic.data=='1' else False,
                source=True,
                api_id=None,
                id_in_api=None,
                user_id=g.user.id
                )
        db.session.commit()

        posts_num=len(g.user.food_posts)+len(g.user.drink_posts)
        if posts_num==0:
            g.user.level='Foodie'
            db.session.commit()
        elif posts_num>0 and posts_num<=10:
            g.user.level='Home Chef'
            db.session.commit()
        elif posts_num>10 and posts_num<=40:
            g.user.level='Junior Chef'
            db.session.commit()
        elif posts_num>40 and posts_num<=100:
            g.user.level='Head Chef'
            db.session.commit()

        return redirect(f'/drink/create/{drink.id}')

    return render_template('drinkrecipes/createdrinkrecipes.html', form=form)

@app.route('/drink/create/<int:id>', methods=["GET"])
def drink_recipes_create_by_id(id):
    """show drink recipes that created by users through id."""

    drink=DrinkRecipes.query.get_or_404(id)

    drink_ingredients_dict={}
    for item in drink.drink_ingredients.split(','):
        if item!='':
            temp=item.split(':')
            drink_ingredients_dict[temp[0]]=temp[1]

    if 'drink_speech' not in session:
        session['drink_speech']=(drink.id,False)
        speech=False
    elif session['drink_speech'][0]!=drink.id:
        session['drink_speech']=(drink.id,False)
        speech=False
    else:
        drink_id_speech, speech=session['drink_speech']

    return render_template('drinkrecipes/detailsdrinkrecipe.html', drink=drink, drink_ingredients=drink_ingredients_dict, speech=speech)


@app.route('/drink/edit/<int:id>', methods=["GET", "POST"])
def drink_recipes_edit_by_id(id):
    """edit drink recipes that created by users through id."""

    drink=DrinkRecipes.query.get_or_404(id)

    form = CreateDrinkRecipesForm(obj=drink)

    categories = [('0', 'Choose ...')] + [(str(category.id), category.drink_category) for category in DrinkCategories.query.all()]
    form.drink_category_id.choices = categories

    alcoholic_choice = [('0', 'Choose ...')] + [('1', True), ('2', False)]
    form.alcoholic.choices = alcoholic_choice

    if form.validate_on_submit():
        drink.drink_name=form.drink_name.data
        drink.drink_category_id=int(form.drink_category_id.data)
        drink.alcoholic=True if form.alcoholic.data=='1' else False

        name_ingredients=request.form.getlist('drink_ingredients_name')
        quantity_ingredients=request.form.getlist('drink_ingredients_quantity')
        instructions=request.form.getlist('drink_instructions')

        drink_ingredients=''
        for i in range(20):
            if name_ingredients[i]!='':
                drink_ingredients+=name_ingredients[i]+':'+quantity_ingredients[i]+','

        drink_instructions=''
        for i in range(20):
            if instructions[i]!='':
                drink_instructions+=f'Step {str(i+1)}: '+instructions[i]+'.'

        drink.drink_ingredients=drink_ingredients
        drink.drink_instructions=drink_instructions

        db.session.commit()

        return redirect(f'/drink/create/{drink.id}')

    drink_ingredients=[["display:none;",'',''] for _ in range(20)]
    items=drink.drink_ingredients.split(',')
    for i in range(len(items)):
        if items[i]!='':
            temp=items[i].split(':')
            drink_ingredients[i][0]=''
            drink_ingredients[i][1]=temp[0]
            drink_ingredients[i][2]=temp[1]

    drink_instructions=[["display:none;",''] for _ in range(20)]
    items=drink.drink_instructions.split('.')
    for i in range(len(items)):
        if items[i]!='':
            temp=items[i].split(':')
            drink_instructions[i][0]=''
            drink_instructions[i][1]=temp[1]

    return render_template('drinkrecipes/editdrinkrecipes.html', form=form, drink_id=id, drink_ingredients=drink_ingredients, drink_instructions=drink_instructions)


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


if __name__ == '__main__':
    app.debug = True
    app.run()