from flask import Flask, redirect, url_for, flash, render_template
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from config import get_config


app = Flask(__name__)

# configs
config = get_config()
app.config.from_object(config)

# extensions
login_manager = LoginManager(app)
bootstrap = Bootstrap5(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

# lazy imports
from auth.loaders import load_user
from cli_cmds import seed_cli
from controllers import account, rollcall

# blueprints
app.register_blueprint(account.account_app, url_prefix="/account")
app.register_blueprint(rollcall.chamada_app, url_prefix="/")

# cli
app.cli.add_command(seed_cli)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.jinja2")

@app.errorhandler(401)
def custom_401(error):
    flash("Faça o login primeiro", "danger")
    return redirect(url_for("account_app.sign_in"))


@app.errorhandler(404)
def custom_404(error):
    return redirect(url_for("index"))

