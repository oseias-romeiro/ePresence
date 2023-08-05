from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import input_required


class ClassForm(FlaskForm):
    name = StringField("Name", validators=[input_required()])
    slug = StringField("Slage", validators=[input_required()])

class JoinStudent(FlaskForm):
    register = StringField("student's register", validators=[input_required()])
