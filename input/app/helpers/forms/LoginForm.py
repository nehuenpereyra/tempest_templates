from .SpanishForm import SpanishForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(SpanishForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')
