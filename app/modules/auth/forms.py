from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import  Email, EqualTo, DataRequired, Length


# Define the login form (WTForms)

class LoginForm(FlaskForm):
    email    = StringField('Email Address', [Email(),
                DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [
                DataRequired(message='Must provide a password.')])


class SignupForm(FlaskForm):
    username = StringField('Username', [Length(min=4, max=25)])
    email = StringField('Email Address', [Length(min=6, max=35)])
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
