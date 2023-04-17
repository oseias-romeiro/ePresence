from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import input_required


class SignInForm(FlaskForm):
    matricula = IntegerField("Matricula", validators=[input_required()])
    password = PasswordField("Senha", validators=[input_required()])


class SignUpForm(FlaskForm):
    matricula = IntegerField("Matricula", validators=[input_required()])
    name = StringField("Nome", validators=[input_required()])
    password1 = PasswordField("Senha", validators=[input_required()])
    password2 = PasswordField("Digite novamente a senha", validators=[input_required()])
    professor = BooleanField("Professor")

