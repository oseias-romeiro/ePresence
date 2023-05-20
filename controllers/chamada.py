from flask import Blueprint, request, render_template, flash, redirect, url_for, Response
from flask_login import login_required
from flask_login import current_user
from datetime import datetime, timedelta
import qrcode, io

from db import Session
from models.User import User
from models.Chamada import Chamada, Frequencia, Turma, Turmas
from help.required import professor_required
from forms.TurmaForm import TurmaForm, AddAluno
from api.GeoDB import get_nearby_cities, get_distance

chamada_app = Blueprint("chamada_app", __name__)


@chamada_app.route("/", methods=["GET"])
@login_required
def home():
    with Session() as sess: minhas_turmas = sess.query(Turma).join(Turmas).filter_by(id_user=current_user.id).all()

    form_turma = TurmaForm()

    return render_template("home.html", current_user=current_user, turmas=minhas_turmas, form_turma=form_turma)


@chamada_app.route("/add_turma", methods=["POST"])
@login_required
def add_turma():

    if not current_user.professor:
        flash("Usuário não é professor", "danger")
        return redirect(url_for("chamada_app.home"))

    form = TurmaForm()
    if form.validate_on_submit():
        try:
            sess = Session()

            turma = Turma(name=form.name.data)
            sess.add(turma)
            sess.commit()

            turmas = Turmas(
                id_user = current_user.id,
                id_turma = turma.id
            )
            sess.add(turmas)
            sess.commit()

            sess.close()

            flash("Turma adicionada", "success")
        except Exception as e:
            flash("Erro ao adicionar turma", "danger")
    else:
        flash("Token inválido", "danger")

    return redirect(url_for("chamada_app.home"))
    

@chamada_app.route("/del_turma", methods=["GET"])
@login_required
def del_turma():
    id_turma = request.args.get("id_turma")
    
    if professor_required(current_user, id_turma):
        try:
            sess = Session()

            turma = sess.query(Turma).filter_by(id=id_turma).first()
            
            for c in turma.chamadas:
                for f in c.frequencias:
                    sess.delete(f)
                sess.delete(c)

            for t in turma.turmas:
                sess.delete(t)
            
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
            with Session() as sess: alunos = sess.query(User).join(Turmas).filter_by(id_turma=id_turma).all()
            
            form_aluno = AddAluno()
            return render_template("chamada/list_alunos.html", alunos=alunos, id_turma=id_turma, form_aluno=form_aluno)
        
        except Exception as e:
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
            
            turmas = sess.query(Turmas).filter_by(id_turma=id_turma, id_user=id_aluno).first()
            
            sess.delete(turmas)
            sess.commit()

            sess.close()
            
            flash("Aluno removido com sucesso", "success")
            
        except:
            flash("Erro ao remover usuario", "danger")
    else:
        flash("Usuário precisa ser um professor matriculado na turma", "danger")
        
    return redirect(url_for("chamada_app.home"))


@chamada_app.route("/add_aluno", methods=["POST"])
@login_required
def add_aluno():
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
    
    try:
        sess = Session()

        chamadas = sess.query(Chamada).filter_by(id_turma=id_turma).all()

        for c in chamadas:
            freqs = [f.id_chamada for f in c.frequencias]
            chamadas_frequencias.append({
                "date": c.date,
                "presente": c.id in freqs,
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
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    geoloc=None
    if lat and lon:
        geoloc = get_nearby_cities(lat,lon)
    

    if professor_required(current_user, id_turma):
        try:
            sess = Session()
            dia = datetime.now()
            chamada = Chamada(
                date = dia.date(),
                id_turma = id_turma,
                location = geoloc if geoloc else None
            )
            sess.add(chamada)
            sess.commit()

            return render_template("chamada/qrcode.html", id_chamada=chamada.id)
            
        except Exception as e:
            flash("Chamada já foi criada", "info")

    else:
        flash("Usuário precisa ser um professor matriculado na turma", "danger")
    
    return redirect(url_for("chamada_app.home"))
        

@chamada_app.route("/gen_qrcode", methods=["GET"])
@login_required
def gen_qrcode():
    id_chamada = request.args.get("id_chamada")
    expiration = datetime.now() + timedelta(minutes=10)
    temp_url = url_for("chamada_app.add_frequencia", expiration=expiration, id_chamada=id_chamada, _external=True)
    print("# url temporária:", temp_url)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(temp_url)
    qr.make(fit=True)

    img_buffer = io.BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(img_buffer, "PNG")
    img_buffer.seek(0)

    return Response(img_buffer, mimetype="image/png")

@chamada_app.route("/add_frequencia", methods=["GET", "POST"])
@login_required
def add_frequencia():
    expiration = request.args.get("expiration")
    id_chamada = request.args.get("id_chamada")

    if request.method == "GET":
        return render_template("chamada/confirm_frequencia.html", expiration=expiration, id_chamada=id_chamada)
    
    elif request.method == "POST":
        lat = request.form.get("lat")
        lon = request.form.get("lon")

        geoloc=None
        if lat and lon:
            geoloc = get_nearby_cities(lat,lon)

        if expiration is not None:
            expiration = datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S.%f")
            if datetime.now() > expiration:
                flash("Código expirado", "danger")
                return redirect(url_for("chamada_app.home"))

        freq = Frequencia(
            id_user = current_user.id,
            id_chamada = id_chamada,
            location = geoloc if geoloc else None
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
        chamada = sess.query(Chamada).filter_by(id=id_chamada).first()
        
        alunos = []
        for f in chamada.frequencias:
            dist=None
            if f.location and chamada.location:
                dist = get_distance(
                    (f.location["latitude"], f.location["longitude"]),
                    (chamada.location["latitude"], chamada.location["longitude"])
                )
            alunos.append((
                sess.query(User).filter_by(id=f.id_user).first(),
                dist
            ))
        sess.close()
    except:
        flash("Houve um erro ao coletar a lista de frequecia", "danger")
        return redirect(url_for("chamada_app.home"))

    dia = datetime.strptime(dia.split(" ")[0], "%Y-%m-%d")
    return render_template("chamada/lista.html", alunos=alunos, dia=dia.strftime("%d/%m/%Y"), id_chamada=id_chamada)


@chamada_app.route("/rejeitar_freq", methods=["GET"])
@login_required
def rejeitar_freq():
    id_user = request.args.get("id_user")
    id_chamada = request.args.get("id_chamada")

    try:
        sess = Session()
        frequencias_list = sess.query(Frequencia).filter_by(id_user=id_user, id_chamada=id_chamada).all()
        
        for f in frequencias_list:
            sess.delete(f)
        
        sess.commit()
        sess.close()

        flash("Frequencia rejeitada com sucesso", "success")
        return redirect(url_for("chamada_app.home"))
    except:
        flash("Houve um erro rejeitar a frequencia", "danger")
        return redirect(url_for("chamada_app.home"))

