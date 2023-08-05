from flask import Blueprint, request, render_template, flash, redirect, url_for, Response
from flask_login import login_required
from flask_login import current_user
import qrcode, io, datetime


from app import db
from models.User import User, UserRole
from models.Call import Call, Frequency, Class, UserClass
from help.required import prof_required
from forms.ClassForm import ClassForm, JoinStudent
from api.GeoDB import get_nearby_cities, get_distance


call_app = Blueprint("call_app", __name__)


@call_app.route("/home", methods=["GET"])
@login_required
def home():
    
    classes = db.session.query(Class).join(UserClass).filter_by(register=current_user.register).all()

    class_form = ClassForm()

    return render_template("home.jinja2", current_user=current_user, classes=classes, class_form=class_form, role=UserRole)


@call_app.route("/class/new", methods=["POST"])
@login_required
@prof_required
def class_new():

    form = ClassForm()
    if form.validate_on_submit():
        try:

            classe = Class(name=form.name.data)
            db.session.add(classe)
            db.session.commit()

            classes = UserClass(
                id_user = current_user.id,
                id_class = classe.id
            )
            db.session.add(classes)
            db.session.commit()

            flash("Class created", "success")
        except Exception as e:
            flash("Error creating class", "danger")
    else:
        flash("invalid token", "danger")

    return redirect(url_for("call_app.home"))
    

@call_app.route("/class/<slug>/delete", methods=["GET"])
@login_required
@prof_required
def class_delete(slug):
    try:

        classe = db.session.query(Class).filter_by(slug=slug).first()
        
        # remove rollscall
        for c in classe.calls:
            for f in c.frequencies: db.session.delete(f)
            db.session.delete(c)
        for t in classe.calls: db.session.delete(t)

        # remove users from class
        for u in classe.user_class:
            db.session.delete(u)
        
        db.session.delete(classe)
        db.session.commit()

        flash("Class removed", "success")
        return redirect(url_for("call_app.home"))
    except:
        flash("Error removing class", "danger")
    
    return redirect(url_for("call_app.home"))


@call_app.route("/class/<slug>/students", methods=["GET"])
@login_required
@prof_required
def class_students(slug:str):
    try: 
        students = db.session.query(User).filter_by(role=UserRole.STUDENT).join(UserClass).filter_by(slug=slug).all()
        print(students)
        return render_template("rollcall/list_students.jinja2", students=students, slug=slug, form_join=JoinStudent())
    
    except Exception as e:
        print(e)
        flash("Error listing users", "danger")
        
    return redirect(url_for("call_app.home"))


@call_app.route("/class/<slug>/student/<register>/delete", methods=["GET"])
@login_required
@prof_required
def student_delete(slug, register):
    try:
        user_class = db.session.query(UserClass).filter_by(slug=slug, register=register).first()
        
        db.session.delete(user_class)
        db.session.commit()
        
        flash("Student removed", "success")
        
    except:
        flash("Error romoving student", "danger")
    
    return redirect(url_for("call_app.class_students", slug=slug))


@call_app.route("/class/<slug>/students/join", methods=["POST"])
@login_required
@prof_required
def student_join(slug):
    try:
        register = request.form.get("register")

        user = db.session.query(User).filter_by(register=register).first()
        # check if user is student
        if(not user.role == UserRole.STUDENT): raise Exception("User should be a Student")

        # create association user and class
        user_class = UserClass(
            register = user.register,
            slug = slug
        )
        db.session.add(user_class)
        db.session.commit()
        
        flash("Student joined", "success")
    except Exception as e:
        flash(e.__str__(), "danger")
        
    return redirect(url_for("call_app.class_students", slug=slug))


@call_app.route("/class/<int:id_class>/day/new", methods=["POST"])
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
    
    return redirect(url_for("call_app.home"))
        

@call_app.route("/frequencies/<int:id_call>/qrcode", methods=["GET"])
@login_required
def gen_qrcode(id_call):

    expiration = datetime.datetime.now() + datetime.timedelta(minutes=10)
    temp_url = url_for("call_app.frequencia_confirm", expiration=expiration, id_call=id_call, _external=True)
    print("# url temporária:", temp_url)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(temp_url)
    qr.make(fit=True)

    img_buffer = io.BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(img_buffer, "PNG")
    img_buffer.seek(0)

    return Response(img_buffer, mimetype="image/png")


@call_app.route("/class/<slug>/rollscall", methods=["GET"])
@login_required
def class_frequency(slug):
    call_freqs = []
    
    try:
        calls = db.session.query(Call).filter_by(slug=slug).all()

        for c in calls:
            freqs = [f.id_call for f in c.frequencies]
            call_freqs.append({
                "date": c.date,
                "present": c.id in freqs,
                "id": c.id,
            })
        
    except:
        flash("Error collecting rollscall", "danger")
        return redirect(url_for("call_app.home"))
        
    return render_template("rollcall/rollscall.jinja2", rollscall=call_freqs, slug=slug, role=UserRole)


@call_app.route("/frequencies/<int:id_call>/confirm", methods=["GET"])
@login_required
def frequencia_confirm(id_call):
    expiration = request.args.get("expiration")

    return render_template("rollcall/confirm_frequencia.jinja2", expiration=expiration, id_call=id_call)
    

@call_app.route("/frequencies/<int:id_call>/new", methods=["POST"])
@login_required
def frequencia_new(id_call):
    expiration = request.args.get("expiration")
    
    lat = request.form.get("lat")
    lon = request.form.get("lon")

    geoloc=None
    if lat and lon:
        geoloc = get_nearby_cities(lat,lon)

    if expiration is not None:
        expiration = datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S.%f")
        if datetime.now() > expiration:
            flash("Code expired", "danger")
            return redirect(url_for("call_app.home"))

    freq = Frequency(
        id_user = current_user.id,
        id_call = id_call,
        location = geoloc if geoloc else None
    )
    try:
        db.session.add(freq)
        db.session.commit()
            
        flash("Frequency registrada", "success")
    except:
        flash("Houve um erro registrar frequencia", "danger")
    
    return redirect(url_for("call_app.home"))


@call_app.route("/frequencies/<int:id_call>/lista", methods=["GET"])
@login_required
def frequencia_lista(id_call):
    dia = request.args.get("dia")

    try:
        call = db.session.query(Call).filter_by(id=id_call).first()
        
        students = []
        for f in call.frequencies:
            dist=None
            if f.location and call.location:
                dist = get_distance(
                    (f.location["latitude"], f.location["longitude"]),
                    (call.location["latitude"], call.location["longitude"])
                )
            students.append((
                db.session.query(User).filter_by(id=f.id_user).first(),
                dist
            ))
        
    except:
        flash("Error listing frequencies", "danger")
        return redirect(url_for("call_app.home"))

    dia = datetime.datetime.strptime(dia.split(" ")[0], "%Y-%m-%d")
    return render_template("rollcall/lista.jinja2", students=students, dia=dia.strftime("%d/%m/%Y"), id_call=id_call)


@call_app.route("/frequencies/<int:id_call>/student/<int:id_user>/rejeitar", methods=["GET"])
@login_required
def frequencias_rejeitar(id_call, id_user):
    try:
        frequencias_list = db.session.query(Frequency).filter_by(id_user=id_user, id_call=id_call).all()
        
        for f in frequencias_list:
            db.session.delete(f)
        db.session.commit()
        
        flash("Frequency rejected", "success")
        return redirect(url_for("call_app.home"))
    except:
        flash("Error rejecting frequency", "danger")
        return redirect(url_for("call_app.home"))

