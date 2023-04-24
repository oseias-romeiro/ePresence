from flask import Flask, redirect, url_for, flash
from flask_login import LoginManager
from os import getenv

from routes import account, chamada
from models.User import User, Base
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
    return redirect(url_for("chamada_app.home"))


@app.errorhandler(401)
def custom_401(error):
    flash("Faça o login primeiro", "danger")
    return redirect(url_for("account_app.sign_in"))


@app.errorhandler(404)
def custom_404(error):
    return redirect(url_for("index"))


if __name__ == "__main__":
    # creating tables
    Base.metadata.create_all(engine)

    # api
    if not getenv("RAPID_KEY"): print("A chave da api GeoDB não foi encontrada")

    # run flask app
    app.run(
        host="0.0.0.0",
        port=5000
    )

