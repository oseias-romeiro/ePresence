from app import db
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

from models.Call import UserClass
from models.User import UserRole
    
    
def prof_required(func):
    """
        Verifica se o usuario é professor e caso o id_turma seja um parametro do controlller, verifica também se o professor está na turma
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        id_turma = kwargs.get("id_turma")

        if current_user.role == UserRole.PROFESSOR and id_turma:
            try:
                turmas = db.session.query(UserClass).filter_by(id_turma=id_turma, id_user=current_user.id).first()
                
                if turmas:
                    return func(*args, **kwargs)
                else:
                    flash("User is not a professor of this class", "danger")
            except:
                flash("Error confering classes", "danger")
            
        elif current_user.role == UserRole.PROFESSOR:
            return func(*args, **kwargs)
        else:
            flash("User is not a professor!", "danger")

        return redirect(url_for("call.home"))
        
    return decorated
