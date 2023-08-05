from app import db
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

from models.Call import UserClass
from models.User import UserRole
    
    
def prof_required(func):
    
    @wraps(func)
    def decorated(*args, **kwargs):
        id_class = kwargs.get("id_class")

        if current_user.role == UserRole.PROFESSOR and id_class:
            try:
                classe = db.session.query(UserClass).filter_by(id_class=id_class, id_user=current_user.id).first()
                
                if classe:
                    return func(*args, **kwargs)
                else:
                    flash("User is not a professor of this class", "danger")
            except:
                flash("Error confering classes", "danger")
            
        elif current_user.role == UserRole.PROFESSOR:
            return func(*args, **kwargs)
        else:
            flash("User is not a professor!", "danger")

        return redirect(url_for("call_app.home"))
        
    return decorated
