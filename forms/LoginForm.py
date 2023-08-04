from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import input_required

from models.User import UserRole

class SignInForm(FlaskForm):
    register = IntegerField("Register", validators=[input_required()])
    password = PasswordField("Password", validators=[input_required()])


class SignUpForm(FlaskForm):
    register = IntegerField("Register", validators=[input_required()])
    name = StringField("Nome", validators=[input_required()])
    password1 = PasswordField("Password", validators=[input_required()])
    password2 = PasswordField("Digite novamente a senha", validators=[input_required()])
    role = SelectField("Role", choices=[('ADMIN', "Admin"), ('PROFESSOR', "Professor"), ('STUDENT', "Student")])

