from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app import db, bcrypt
from models.User import User
from help.validators import valid_pw
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
            registration=form.register.data
        ).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("call_app.home"))
        else:
            flash("Matricula/senha invalida", "danger")
            return redirect(url_for("account_app.sign_in"))
    else:
        flash("Token invalido", "danger")
        return redirect(url_for("account_app.sign_in"))


@account_app.route("/sign_up", methods=["GET"])
def sign_up():
    return render_template("account/sign_up.jinja2", form=SignUpForm())


@account_app.route("/sign_up", methods=["POST"])
def sign_up_create():
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            if form.password1.data != form.password2.data and valid_pw(form.password1.data):
                raise Exception

            user = User(
                registration=form.register.data,
                name=form.name.data,
                password=bcrypt.generate_password_hash(form.password1.data),
                role=form.role.data
            )
            db.session.add(user)
            db.session.commit()

            flash("Usuário criado com sucesso", "success")

            return redirect(url_for("account_app.sign_in"))
        except Exception as e:
            print(e)
            flash("Entradas inválidas", "danger")
            return redirect(url_for("account_app.sign_up"))
    else:
        flash("Token inválido", "danger")
        return redirect(url_for("account_app.sign_in"))


@account_app.route("/profile", methods=["GET"])
@login_required
def profile():
    form = SignUpForm()
    if request.method == "GET":
        form.register.data = current_user.register
        form.name.data = current_user.name
        form.role.data = current_user.role

        return render_template("account/profile.jinja2", form=form)


@account_app.route("/profile", methods=["POST"])
@login_required
def profile_edit():
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            if form.password1.data != form.password2.data and valid_pw(form.password1.data):
                raise Exception

            user = db.session.query(User).filter_by(id=current_user.id).first()
            db.session.delete(user)
            db.session.commit()

            user = User(
                id=current_user.id,
                registration=form.register.data,
                name=form.name.data,
                password=bcrypt.generate_password_hash(form.password1.data),
                role=form.role.data
            )
            db.session.add(user)
            db.session.commit()

            flash("Usuário editado", "success")

            return redirect(url_for("call_app.home"))
        except:
            flash("Entradas invalidas", "danger")
            return redirect(url_for("account_app.profile"))
    else:
        flash("Token inválido", "danger")
        return redirect(url_for("account_app.profile"))
    

@account_app.route("/logout", methods=["GET"])
@login_required
def log_out():
    logout_user()
    flash("Saindo...", "success")
    return redirect(url_for("account_app.sign_in"))
