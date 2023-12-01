from flask import Flask, redirect, url_for, flash, render_template
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from config import get_config

BASE_ROUTE = ""
app = Flask(__name__, static_url_path=BASE_ROUTE+"/static")

# configs
config = get_config()
app.config.from_object(config)
app.secret_key = config.SECRET_KEY

# extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
bootstrap = Bootstrap5(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

# lazy imports
from auth.loaders import load_user
from cli_cmds import seed_cli
from controllers import account, call

# blueprints
app.register_blueprint(account.account_app, url_prefix=BASE_ROUTE+"/account")
app.register_blueprint(call.call_app, url_prefix=BASE_ROUTE+"/")

# cli
app.cli.add_command(seed_cli)

@app.route(BASE_ROUTE+"/", methods=["GET"])
def index():
    return render_template("index.jinja2")

@app.errorhandler(401)
def custom_401(error):
    flash("Need login", "danger")
    return redirect(url_for("account_app.sign_in"))


@app.errorhandler(404)
def custom_404(error):
    return render_template("handler/404.jinja2")

