from flask import Flask, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, current_user

from routes import account, chamada
from models.User import User, Base, Turma, Turmas
from db import engine, Session

app = Flask(__name__)
app.secret_key = "s3cr3t"
login_manager = LoginManager(app)

# routes projects
app.register_blueprint(account.account_app, url_prefix="/account")
app.register_blueprint(chamada.chamada_app, url_prefix="/chamada")

@login_manager.user_loader
def load_user(user):
    sess = Session()
    res = sess.query(User).filter_by(
        id=user
    ).first()
    sess.close()
    return res


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", user_authed=current_user.is_authenticated)


@app.errorhandler(401)
def custom_401(error):
    flash("Need login", "failed")
    return redirect(url_for("account_app.sign_in"))


@app.errorhandler(404)
def custom_404(error):
    return redirect(url_for("index"))


def create_user():
    sess = Session()
    try:
        user = User(
            id=1,
            matricula="000000000",
            name="prof1",
            password=generate_password_hash("1234"),
            professor=True
        )
        sess.add(user)
        sess.commit()
    except:
        del user
        sess.rollback()
    sess.close()

def create_turma():
    sess = Session()
    try:
        turma = Turma(
            id=1,
            name="turma1"
        )
        sess.add(turma)
        sess.commit()
    except:
        del turma
        sess.rollback()
    sess.close()

def create_turmas():
    sess = Session()
    try:
        turma = Turmas(
            id = 1,
            id_user = 1,
            id_turma = 1
        )
        sess.add(turma)
        sess.commit()
    except:
        del turma
        sess.rollback()
    sess.close()

if __name__ == "__main__":
    # creating tables
    Base.metadata.create_all(engine)

    # run flask app
    app.run(
        host="0.0.0.0",
        port=5000
    )

