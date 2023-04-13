from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required
from flask_login import current_user

from db import Session
from models.User import User, Turmas, Turma, Frequencia, Chamada
from forms.TurmaForm import TurmaForm, AddAluno

import datetime

chamada_app = Blueprint("chamada_app", __name__)

@chamada_app.route("/", methods=["GET"])
@login_required
def home():
    sess = Session()

    turmas_total = sess.query(Turmas).filter_by(id_user=current_user.id).all()
    minhas_turmas = []
    for t in turmas_total:
        minhas_turmas.append(sess.query(Turma).filter_by(id=t.id_turma).first())
    
    sess.close()

    return render_template("home.html", current_user=current_user, turmas=minhas_turmas)

@chamada_app.route("/add_turma", methods=["GET", "POST"])
@login_required
def add_turma():
    form = TurmaForm()
    if request.method == "GET":
        return render_template("chamada/add_turma.html", form=form)
    
    if form.validate_on_submit():
        try:
            sess = Session()

            turma_total = sess.query(Turma).all()
            if (len(turma_total) > 0):
                turma_id = max([t.id for t in turma_total])
            else:
                turma_id = 0

            turma = Turma(
                id = turma_id+1,
                name=form.name.data
            )
            sess.add(turma)

            turmas = Turmas(
                id_user = current_user.id,
                id_turma = turma_id+1,
            )
            sess.add(turmas)

            sess.commit()
            sess.close()

            flash("Turma adicionada", "success")

            return redirect(url_for("chamada_app.home"))
        except Exception as e:
            flash("Erro ao adicionar turma", "failed")
            return redirect(url_for("chamada_app.add_turma"))
    else:
        flash("Token inválido", "failed")
        return redirect(url_for("chamada_app.add_turma"))
    

@chamada_app.route("/del_turma", methods=["GET"])
@login_required
def del_turma():
    id_turma = request.args.get("id_turma")

    try:
        sess = Session()

        turmas = sess.query(Turmas).filter_by(id_turma=id_turma).all()
        turma = sess.query(Turma).filter_by(id=id_turma).first()

        for t in turmas:
            sess.delete(t)
        sess.delete(turma)

        sess.commit()
        sess.close()

        flash("Turma removida", "success")

        return redirect(url_for("chamada_app.home"))
    except:
        flash("Erro ao remover turma", "failed")
        return redirect(url_for("chamada_app.home"))


@chamada_app.route("/add_aluno", methods=["GET", "POST"])
@login_required
def add_aluno():
    form = AddAluno()
    if request.method == "GET":
        id_turma = request.args.get("id_turma")
        return render_template("chamada/add_aluno.html", form=form, id_turma=id_turma)
    
    elif request.method == "POST":
        id_turma = request.form.get("id_turma")
        mat = request.form.get("mat")

        try:
            sess = Session()

            id_user = sess.query(User).filter_by(matricula=mat).first().id

            turmas = Turmas(
                id_user = id_user,
                id_turma = id_turma
            )
            print("###", turmas.id_user, turmas.id_turma)
            sess.add(turmas)

            sess.commit()
            sess.close()

            flash("Aluno adicionado", "success")

            return redirect(url_for("chamada_app.home"))
        except:
            flash("Erro ao adicionar aluno", "failed")
            return redirect(url_for("chamada_app.add_aluno"))
    else:
        flash("Token inválido", "failed")
        return redirect(url_for("chamada_app.add_aluno"))

@chamada_app.route("/chamada", methods=["GET"])
@login_required
def chamada():

    id_turma = request.args.get("turma_id")
    
    if request.method == "GET":
        sess = Session()
        dia = datetime.datetime.now()
        try:
            ch = sess.query(Chamada).filter_by(date=dia.date(), id_turma=id_turma).all()
            if(current_user.professor):
                if len(ch) == 0:
                    chamada = Chamada(
                        date = dia.date(),
                        id_turma = id_turma
                    )
                    sess.add(chamada)
                    sess.commit()
                    flash("Chamada criada", "success")
                else:
                    raise Exception("Chamada já foi criada")
            else:
                
                if len(ch) > 0:
                    responida = sess.query(Frequencia).filter_by(id_user=current_user.id, id_chamada=ch[0].id).all()
                    
                    if len(responida) == 0:
                        frequencia = Frequencia(
                            id_user = current_user.id,
                            id_chamada = ch[0].id
                        )
                        sess.add(frequencia)
                        sess.commit()
                        flash("Frequencia Respondida", "success")
                    else:
                        flash("Frequencia ja foi responida", "failed")
                else:
                    raise Exception("Chamada não foi criada ainda")
            

        except Exception as e:
            flash(e.__str__(), "failed")
            return redirect(url_for("chamada_app.home"))

        freq = []
        try:
            for f in sess.query(Frequencia).all():
                freq.append(sess.query(User).filter_by(id=f.id_user).first())
        except Exception as e:
            flash("Erro ao buscar usuarios", "failed")
            return redirect(url_for("chamada_app.home"))

        sess.close()
        return render_template("chamada/chamada.html", freq=freq, dia=str(dia).split(' ')[0])


