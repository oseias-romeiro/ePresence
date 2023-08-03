from flask import Blueprint, request, render_template, flash, redirect, url_for, Response
from flask_login import login_required
from flask_login import current_user
import qrcode, io, datetime


from app import db
from models.User import User
from models.Call import Call, Frequency, Class, UserClass
from help.required import prof_required
from forms.TurmaForm import TurmaForm, AddAluno
from api.GeoDB import get_nearby_cities, get_distance


chamada_app = Blueprint("chamada_app", __name__)


@chamada_app.route("/home", methods=["GET"])
@login_required
def home():
    
    minhas_turmas = db.session.query(Class).join(UserClass).filter_by(id_user=current_user.id).all()

    form_turma = TurmaForm()

    return render_template("home.jinja2", current_user=current_user, turmas=minhas_turmas, form_turma=form_turma)


@chamada_app.route("/class/new", methods=["POST"])
@login_required
@prof_required
def class_new():

    form = TurmaForm()
    if form.validate_on_submit():
        try:

            classe = Class(name=form.name.data)
            db.session.add(classe)
            db.session.commit()

            turmas = Class(
                id_user = current_user.id,
                id_class = classe.id
            )
            db.session.add(turmas)
            db.session.commit()

            flash("Class created", "success")
        except Exception as e:
            flash("Error creating class", "danger")
    else:
        flash("invalid token", "danger")

    return redirect(url_for("chamada_app.home"))
    

@chamada_app.route("/class/<int:id_class>/delete", methods=["GET"])
@login_required
@prof_required
def class_delete(id_class):
    try:

        classe = db.session.query(Class).filter_by(id=id_class).first()
        
        for c in classe.calls:
            for f in c.frequencies:
                db.session.delete(f)
            db.session.delete(c)

        for t in classe.calls:
            db.session.delete(t)
        
        db.session.delete(classe)
        db.session.commit()

        flash("Class removed", "success")
        return redirect(url_for("chamada_app.home"))
    except:
        flash("Error removing class", "danger")
    
    return redirect(url_for("chamada_app.home"))


@chamada_app.route("/class/<int:id_class>/student", methods=["GET"])
@login_required
@prof_required
def class_students(id_class):
    try: 
        students = db.session.query(User).join(UserClass).filter_by(id_class=id_class).all()
        
        form_student = AddAluno()
        return render_template("rollcall/list_students.jinja2", students=students, id_class=id_class, form_student=form_student)
    
    except Exception as e:
        flash("Error listing users", "danger")
        
    return redirect(url_for("chamada_app.home"))


@chamada_app.route("/class/<int:id_class>/students/<int:id_student>/delete", methods=["GET"])
@login_required
@prof_required
def student_delete(id_class, id_student):
    try:
        classes = db.session.query(Class).filter_by(id_class=id_class, id_user=id_student).first()
        
        db.session.delete(classes)
        db.session.commit()
        
        flash("Student removed", "success")
        
    except:
        flash("Error romoving student", "danger")
        
    return redirect(url_for("chamada_app.home"))


@chamada_app.route("/class/<int:id_class>/students/join", methods=["POST"])
@login_required
@prof_required
def student_join(id_class):
    try:
        mat = request.form.get("mat")

        id_user = db.session.query(User).filter_by(matricula=mat).first().id

        user_class = UserClass(
            id_user = id_user,
            id_class = id_class
        )
        db.session.add(user_class)
        db.session.commit()
        

        flash("Student joined", "success")
        return redirect(url_for("chamada_app.home"))
    except:
        flash("Error joining student", "danger")
        
    return redirect(url_for("chamada_app.add_student"))


@chamada_app.route("/class/<int:id_class>/day/new", methods=["POST"])
@login_required
@prof_required
def call_new(id_class):
    lat = request.form.get("lat")
    lon = request.form.get("lon")

    geoloc=None
    if lat and lon:
        geoloc = get_nearby_cities(lat,lon)
    
    try:
        day = datetime.datetime.now()
        call = Call(
            date = day.date(),
            id_class = id_class,
            location = geoloc if geoloc else None
        )
        db.session.add(call)
        db.session.commit()

        return render_template("call/qrcode.jinja2", id_call=call.id)
        
    except Exception as e:
        flash("Call already has created", "info")
    
    return redirect(url_for("chamada_app.home"))
        

@chamada_app.route("/frequencias/<int:id_chamada>/qrcode", methods=["GET"])
@login_required
def gen_qrcode(id_chamada):

    expiration = datetime.datetime.now() + datetime.timedelta(minutes=10)
    temp_url = url_for("chamada_app.frequencia_confirm", expiration=expiration, id_chamada=id_chamada, _external=True)
    print("# url temporária:", temp_url)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(temp_url)
    qr.make(fit=True)

    img_buffer = io.BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(img_buffer, "PNG")
    img_buffer.seek(0)

    return Response(img_buffer, mimetype="image/png")


@chamada_app.route("/class/<int:id_class>/frequencias/show", methods=["GET"])
@login_required
def turma_frequencias(id_class):
    chamadas_frequencias = []
    
    try:
        calls = db.session.query(Call).filter_by(id_class=id_class).all()

        for c in calls:
            freqs = [f.id_chamada for f in c.frequencias]
            chamadas_frequencias.append({
                "date": c.date,
                "presente": c.id in freqs,
                "id": c.id,
            })
        
    except:
        flash("Erro ao coletar frequencias", "danger")
        return redirect(url_for("chamada_app.home"))
        
    return render_template("rollcall/frequencias.jinja2", chamadas=chamadas_frequencias, id_class=id_class)


@chamada_app.route("/frequencias/<int:id_chamada>/confirm", methods=["GET"])
@login_required
def frequencia_confirm(id_chamada):
    expiration = request.args.get("expiration")

    return render_template("rollcall/confirm_frequencia.jinja2", expiration=expiration, id_chamada=id_chamada)
    

@chamada_app.route("/frequencias/<int:id_chamada>/new", methods=["POST"])
@login_required
def frequencia_new(id_chamada):
    expiration = request.args.get("expiration")
    
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

    freq = Frequency(
        id_user = current_user.id,
        id_chamada = id_chamada,
        location = geoloc if geoloc else None
    )
    try:
        db.session.add(freq)
        db.session.commit()
            
        flash("Frequency registrada", "success")
    except:
        flash("Houve um erro registrar frequencia", "danger")
    
    return redirect(url_for("chamada_app.home"))


@chamada_app.route("/frequencias/<int:id_chamada>/lista", methods=["GET"])
@login_required
def frequencia_lista(id_chamada):
    dia = request.args.get("dia")

    try:
        chamada = db.session.query(Chamada).filter_by(id=id_chamada).first()
        
        students = []
        for f in chamada.frequencias:
            dist=None
            if f.location and chamada.location:
                dist = get_distance(
                    (f.location["latitude"], f.location["longitude"]),
                    (chamada.location["latitude"], chamada.location["longitude"])
                )
            students.append((
                db.session.query(User).filter_by(id=f.id_user).first(),
                dist
            ))
        
    except:
        flash("Houve um erro ao coletar a lista de frequecia", "danger")
        return redirect(url_for("chamada_app.home"))

    dia = datetime.datetime.strptime(dia.split(" ")[0], "%Y-%m-%d")
    return render_template("rollcall/lista.jinja2", students=students, dia=dia.strftime("%d/%m/%Y"), id_chamada=id_chamada)


@chamada_app.route("/frequencias/<int:id_chamada>/student/<int:id_user>/rejeitar", methods=["GET"])
@login_required
def frequencias_rejeitar(id_chamada, id_user):
    try:
        frequencias_list = db.session.query(Frequency).filter_by(id_user=id_user, id_chamada=id_chamada).all()
        
        for f in frequencias_list:
            db.session.delete(f)
        db.session.commit()
        
        flash("Frequency rejeitada com sucesso", "success")
        return redirect(url_for("chamada_app.home"))
    except:
        flash("Houve um erro rejeitar a frequencia", "danger")
        return redirect(url_for("chamada_app.home"))

