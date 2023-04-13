from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import input_required


class TurmaForm(FlaskForm):
    name = StringField("Nome", validators=[input_required()])

class AddAluno(FlaskForm):
    mat = StringField("Matricula do aluno", validators=[input_required()])

    