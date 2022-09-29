from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class SearchForm(FlaskForm):
    """Form for searching IP Address."""

    search = StringField('Look up an IP Address', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    """Sign up form."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])

