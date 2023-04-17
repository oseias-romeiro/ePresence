from flask import Blueprint, request, render_template, flash, redirect, url_for, Response
from flask_login import login_required
from flask_login import current_user
from datetime import datetime, timedelta
import qrcode, io

from db import Session, professor_required
from models.User import User, Turmas, Turma, Frequencia, Chamada
from forms.TurmaForm import TurmaForm, AddAluno


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

    if not current_user.professor:
        flash("Usuário não é professor", "danger")
        return redirect(url_for("chamada_app.home"))

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
            flash("Erro ao adicionar turma", "danger")
            return redirect(url_for("chamada_app.add_turma"))
    else:
        flash("Token inválido", "danger")
        return redirect(url_for("chamada_app.add_turma"))
    

@chamada_app.route("/del_turma", methods=["GET"])
@login_required
def del_turma():
    id_turma = request.args.get("id_turma")
    
    if professor_required(current_user, id_turma):
        try:
            sess = Session()
            turmas = sess.query(Turmas).filter_by(id_turma=id_turma).all()
            
            chamadas = sess.query(Chamada).filter_by(id_turma=id_turma).all()
            
            for c in chamadas:
                freqs = sess.query(Frequencia).filter_by(id_chamada=c.id).all()
                for f in freqs:
                    sess.delete(f)
                sess.delete(c)

            for t in turmas:
                sess.delete(t)
            
            turma = sess.query(Turma).filter_by(id=id_turma).first()
            
            sess.delete(turma)
            sess.commit()
            sess.close()

            flash("Turma removida", "success")
            return redirect(url_for("chamada_app.home"))
        except:
            flash("Erro ao remover turma", "danger")
    else:
        flash("Usuário precisa ser um professor registrado na turma", "denger")
    
    return redirect(url_for("chamada_app.home"))


@chamada_app.route("/list_alunos", methods=["GET"])
@login_required
def list_alunos():
    id_turma = request.args.get("id_turma")
    
    if professor_required(current_user, id_turma):
        try: 
            sess = Session()
            
            turma_alunos = sess.query(Turmas).filter_by(id_turma=id_turma).all()
            
            alunos = []
            for t in turma_alunos:
                alunos.append(sess.query(User).filter_by(id=t.id_user).first())
            
            sess.close()
            
            return render_template("chamada/list_alunos.html", alunos=alunos, id_turma=id_turma)
        except:
            flash("Erro ao listar usuarios", "danger")
    else:
        flash("Usuário precisa ser um professor matriculado na turma", "danger")
        
    return redirect(url_for("chamada_app.home"))


@chamada_app.route("/del_aluno", methods=["GET"])
@login_required
def del_aluno():
    id_aluno = request.args.get("id_aluno")
    id_turma = request.args.get("id_turma")
    
    if professor_required(current_user, id_turma):
        try:
            sess = Session()
            
            turma_alunos = sess.query(Turmas).filter_by(id_turma=id_turma).all()

            for t in turma_alunos:
                if t.id_user == int(id_aluno):
                    sess.delete(t)
                    sess.commit()
                    break
            
            sess.close()
            
            flash("Aluno removido com sucesso", "success")
            
        except:
            flash("Erro ao remover usuario", "danger")
    else:
        flash("Usuário precisa ser um professor matriculado na turma", "danger")
        
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

        if professor_required(current_user, id_turma):
            try:
                sess = Session()

                id_user = sess.query(User).filter_by(matricula=mat).first().id

                turmas = Turmas(
                    id_user = id_user,
                    id_turma = id_turma
                )
                sess.add(turmas)

                sess.commit()
                sess.close()

                flash("Aluno adicionado", "success")
                return redirect(url_for("chamada_app.home"))
            except:
                flash("Erro ao adicionar aluno", "danger")
        else:
            flash("Usuário precisa ser um professor matriculado na turma", "danger")
        
    return redirect(url_for("chamada_app.add_aluno"))



@chamada_app.route("/frequencias", methods=["GET"])
@login_required
def frequencias():
    id_turma = request.args.get("id_turma")
    chamadas_frequencias = []
    
    if professor_required(current_user, id_turma):
        try:
            sess = Session()
    
            chamadas = sess.query(Chamada).filter_by(id_turma=id_turma).all()

            for c in chamadas:
                freqs = sess.query(Frequencia).filter_by(
                    id_user=current_user.id,
                    id_chamada=c.id
                ).all()
                freqs_chamada = [f.id_chamada for f in freqs]
                chamadas_frequencias.append({
                    "date": c.date,
                    "presente": c.id in freqs_chamada,
                    "id": c.id,
                })
            sess.close()
        except:
            flash("Erro ao coletar frequencias", "danger")
            return redirect(url_for("chamada_app.home"))
        
    return render_template("chamada/frequencias.html", chamadas=chamadas_frequencias, id_turma=id_turma)



@chamada_app.route("/add_chamada", methods=["GET"])
@login_required
def add_chamada():
    id_turma = request.args.get("id_turma")
    
    if professor_required(current_user, id_turma):
        try:
            sess = Session()
            dia = datetime.now()
            ch = sess.query(Chamada).filter_by(date=dia.date(), id_turma=id_turma).all()
            if len(ch) == 0:
                chamada = Chamada(
                    date = dia.date(),
                    id_turma = id_turma
                )
                sess.add(chamada)
                sess.commit()

                id_chamada = sess.query(Chamada).filter_by(date=dia.date()).first().id
                expiration = datetime.now() + timedelta(minutes=10)
                temp_url = url_for("chamada_app.add_frequencia", expiration=expiration, id_chamada=id_chamada, _external=True)

                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                qr.add_data(temp_url)
                qr.make(fit=True)

                img_buffer = io.BytesIO()
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(img_buffer, "PNG")
                img_buffer.seek(0)

                return Response(img_buffer, mimetype="image/png")
            
            else:
                flash("Chamada já foi criada", "info")
            
        except:
            flash("Houve um erro na consluta", "danger")
    
    else:
        flash("Usuário precisa ser um professor matriculado na turma", "danger")
    
    return redirect(url_for("chamada_app.home"))
        

@chamada_app.route("/add_frequencia", methods=["GET"])
@login_required
def add_frequencia():
    expiration = request.args.get("expiration")
    id_chamada = request.args.get("id_chamada")

    if expiration is not None:
        expiration = datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S.%f")
        if datetime.now() > expiration:
            flash("Código expirado", "danger")
            return redirect(url_for("chamada_app.home"))

    freq = Frequencia(
        id_user = current_user.id,
        id_chamada = id_chamada
    )
    try:
        with Session() as sess:
            sess.add(freq)
            sess.commit()
            
        flash("Frequencia registrada", "success")
    except:
        flash("Houve um erro registrar frequencia", "danger")
    
    return redirect(url_for("chamada_app.home"))


@chamada_app.route("/lista", methods=["GET"])
@login_required
def lista():
    dia = request.args.get("dia")
    id_chamada = request.args.get("id_chamada")

    try:
        sess = Session()
        frequencias_list = sess.query(Frequencia).filter_by(id_chamada=id_chamada).all()
        
        alunos = []
        for f in frequencias_list:
            alunos.append(sess.query(User).filter_by(id=f.id_user).first())
        
        sess.close()
    except:
        flash("Houve um erro ao coletar a lista de frequecia", "danger")
        return redirect(url_for("chamada_app.home"))

    dia = datetime.strptime(dia, "%Y-%m-%d")
    return render_template("chamada/lista.html", alunos=alunos, dia=dia.strftime("%d/%m/%Y"))

