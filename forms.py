from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, Form, StringField, PasswordField, TextAreaField, SelectField, RadioField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename

class UserSignUpForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6), 
    EqualTo('reenterpassword', message='Password must match')])
    reenterpassword = PasswordField('Re-Enter Password', validators=[DataRequired()])
    question = SelectField('Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired(), Length(min=3), 
    EqualTo('reenteranswer', message='Answer must match')])
    reenteranswer = StringField('Re-Enter Answer', validators=[DataRequired()])
    location = StringField('Location (Optional)')
    image_url = StringField('Image URL (Optional)')
    bio = TextAreaField('Tell us about yourself (Optional)')


class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    location = StringField('Location (Optional)')
    image_url = StringField('Image URL (Optional)')
    bio = TextAreaField('Tell us about yourself (Optional)')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])


class UserLoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UsernameForm(FlaskForm):
    """Input username to get question."""

    username = StringField('Username', validators=[DataRequired()])


class AnswerForm(FlaskForm):
    """Input answer to reset password."""

    answer = StringField('Answer', validators=[DataRequired()])


class ResetPWForm(FlaskForm):
    """Form for resetting PW."""

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6), 
    EqualTo('reenterpassword', message='Password must match')])
    reenterpassword = PasswordField('Re-Enter Password', validators=[DataRequired()])


class EmailForm(FlaskForm):
    """Input email to get a link for resetting password."""

    email = StringField('E-mail', validators=[DataRequired(), Email()])


class SearchFoodRecipesForm(FlaskForm):
    """Search food recipes in APIs."""

    searchby = SelectField('Search By', validators=[DataRequired()])
    searchinput = StringField('Key Words', validators=[DataRequired()])

class SearchDrinkRecipesForm(FlaskForm):
    """Search food recipes in APIs."""

    searchby = SelectField('Search By', validators=[DataRequired()])
    searchinput = StringField('Key Words', validators=[DataRequired()])

class CreateFoodRecipesForm(FlaskForm):
    """Create food recipes."""

    food_name = StringField('Name', validators=[DataRequired()])
    food_category_id = SelectField('Category', validators=[DataRequired()])
    food_area_id = SelectField('Area', validators=[DataRequired()])
    food_photo_url = StringField('Image URL')

class CreateDrinkRecipesForm(FlaskForm):
    """Create drink recipes."""

    drink_name = StringField('Name', validators=[DataRequired()])
    drink_category_id = SelectField('Category', validators=[DataRequired()])
    alcoholic = SelectField('Alcoholic or Not?', validators=[DataRequired()])
    drink_photo_url = StringField('Image URL')
