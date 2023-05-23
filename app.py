from flask import Flask, redirect, url_for, flash
from flask_login import LoginManager

from config import config
from db import engine, Session, db
from models.User import User
from controllers import account, chamada


app = Flask(__name__)
app.secret_key = config.SECRET_KEY
login_manager = LoginManager(app)

# routes projects
app.register_blueprint(account.account_app, url_prefix="/account")
app.register_blueprint(chamada.chamada_app, url_prefix="/")

@login_manager.user_loader
def load_user(user):
    sess = Session()
    res = sess.query(User).filter_by(
        id=user
    ).first()
    sess.close()
    return res


@app.errorhandler(401)
def custom_401(error):
    flash("Faça o login primeiro", "danger")
    return redirect(url_for("account_app.sign_in"))


@app.errorhandler(404)
def custom_404(error):
    return redirect(url_for("index"))


if __name__ == "__main__":
    # creating tables
    db.metadata.create_all(engine)

    # run flask app
    app.run(config.HOST, config.PORT)

