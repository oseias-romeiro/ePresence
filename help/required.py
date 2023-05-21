from db import Session
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

from models.Chamada import Turmas
    
    
def prof_required(func):
    """
        Verifica se o usuario é professor e caso o id_turma seja um parametro do controlller, verifica também se o professor está na turma
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        id_turma = kwargs.get("id_turma")

        if current_user.professor and id_turma:
            try:
                with Session() as sess: turmas = sess.query(Turmas).filter_by(id_turma=id_turma, id_user=current_user.id).first()
                
                if turmas:
                    return func(*args, **kwargs)
                else:
                    flash("Usuário não é professor dessa turma", "danger")
            except:
                flash("Erro ao consultar suas turmas", "danger")
            
        elif current_user.professor:
            return func(*args, **kwargs)
        else:
            flash("Usuário não é professor", "danger")

        return redirect(url_for("chamado.home"))
        
    return decorated
