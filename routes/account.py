from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from db import Session
from models.User import User
from help.validators import valid_pw
from forms.LoginForm import SignInForm, SignUpForm

account_app = Blueprint("account_app", __name__)


@account_app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    form = SignInForm()
    if request.method == "GET":
        return render_template("account/sign_in.html", form=form)

    if form.validate_on_submit():
        sess = Session()
        user = sess.query(User).filter_by(
            matricula=form.matricula.data
        ).first()
        sess.close()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("chamada_app.home"))
        else:
            flash("Matricula/senha invalida", "danger")
            return redirect(url_for("account_app.sign_in"))
    else:
        flash("Token invalido", "danger")
        return redirect(url_for("account_app.sign_in"))


@account_app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if request.method == "GET":
        return render_template("account/sign_up.html", form=form)

    if form.validate_on_submit():
        try:
            if form.password1.data != form.password2.data and valid_pw(form.password1.data):
                raise Exception

            user = User(
                matricula=form.matricula.data,
                name=form.name.data,
                password=generate_password_hash(form.password1.data),
                professor=form.professor.data
            )
            sess = Session()
            sess.add(user)
            sess.commit()
            sess.close()

            flash("Usuário criado com sucesso", "success")

            return redirect(url_for("account_app.sign_in"))
        except Exception as e:
            flash("Entradas inválidas", "danger")
            return redirect(url_for("account_app.sign_up"))
    else:
        flash("Token inválido", "danger")
        return redirect(url_for("account_app.sign_in"))


@account_app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = SignUpForm()
    if request.method == "GET":
        form.matricula.data = current_user.matricula
        form.name.data = current_user.name
        form.professor.data = current_user.professor

        return render_template("account/profile.html", form=form)

    if form.validate_on_submit():
        try:
            if form.password1.data != form.password2.data and valid_pw(form.password1.data):
                raise Exception

            sess = Session()

            user = sess.query(User).filter_by(id=current_user.id).first()
            sess.delete(user)
            sess.commit()

            user = User(
                id=current_user.id,
                matricula=form.matricula.data,
                name=form.name.data,
                password=generate_password_hash(form.password1.data),
                professor=form.professor.data
            )
            sess.add(user)
            sess.commit()

            sess.close()

            flash("Usuário editado", "success")

            return redirect(url_for("chamada_app.home"))
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
