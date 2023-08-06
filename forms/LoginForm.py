from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import input_required, EqualTo, Regexp
from models.User import UserRole


class SignInForm(FlaskForm):
    register = IntegerField("Register", validators=[input_required()])
    password = PasswordField("Password", validators=[input_required()])


class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[input_required()])
    password1 = PasswordField("Password", validators=[
        input_required(),
        EqualTo('password2', 'Passwords must match'),
        Regexp(
            regex='^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,}$',
            message='Password must contain at least 8 characteres and one digit, one uppercase letter ad one special symbol'
        )
    ])
    password2 = PasswordField("Retype password", validators=[input_required()])
    role = SelectField("Role", choices=[(ur.name, ur.value) for ur in UserRole])

