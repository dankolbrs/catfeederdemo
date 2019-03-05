from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('User', validators=[DataRequired()])
    password = PasswordField('Password')
    confirm = BooleanField('Confirm?')
    submit = SubmitField('Feed')


class FeedKitties(FlaskForm):
    confirm = BooleanField('Confirm?')
    submit = SubmitField('Feed')
