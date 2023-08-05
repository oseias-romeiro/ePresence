from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app import db, bcrypt
from models.User import User, UserRole
from forms.LoginForm import SignInForm, SignUpForm

account_app = Blueprint("account_app", __name__)


@account_app.route("/sign_in", methods=["GET"])
def sign_in():
    form = SignInForm()
    if request.method == "GET":
        return render_template("account/sign_in.jinja2", form=form)


@account_app.route("/sign_in", methods=["POST"])
def sign_in_create():
    form = SignInForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(
            register=form.register.data
        ).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("call_app.home"))
        else:
            flash("Invalid inputs", "danger")
    else:
        errors = list(form.errors.values())[0][0]
        flash(errors, "danger")
        
    return redirect(url_for("account_app.sign_in"))


@account_app.route("/sign_up", methods=["GET"])
def sign_up():
    return render_template("account/sign_up.jinja2", form=SignUpForm())


@account_app.route("/sign_up", methods=["POST"])
def sign_up_create():
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User(
                name=form.name.data,
                register=db.session.query(User).order_by(User.register.desc()).first().register+1,
                password=bcrypt.generate_password_hash(form.password1.data),
                role=form.role.data
            )
            db.session.add(user)
            db.session.commit()

            flash(f"User created (register: {user.register})", "success")

            return redirect(url_for("account_app.sign_in"))
        except Exception as e:
            flash("Error persisting data", "danger")
    else:
        errors = list(form.errors.values())[0][0]
        flash(errors, "danger")
    
    return redirect(url_for("account_app.sign_up"))


@account_app.route("/profile", methods=["GET"])
@login_required
def profile():
    form = SignUpForm()
    if request.method == "GET":
        form.name.data = current_user.name
        form.role.data = current_user.role.__str__()

        return render_template("account/profile.jinja2", form=form)


@account_app.route("/profile", methods=["POST"])
@login_required
def profile_edit():
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = db.session.query(User).filter_by(id=current_user.id).first()
            user.name=form.name.data
            user.password=bcrypt.generate_password_hash(form.password1.data)
            user.role=form.role.data
            db.session.commit()

            flash("User edited", "success")
            return redirect(url_for("call_app.home"))
        except Exception as e:
            flash("Erro in persist data", "danger")
    else:
        errors = list(form.errors.values())[0][0]
        flash(errors, "danger")

    return redirect(url_for("account_app.profile"))
    

@account_app.route("/logout", methods=["GET"])
@login_required
def log_out():
    logout_user()
    flash("Exited", "success")
    return redirect(url_for("account_app.sign_in"))
