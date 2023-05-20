from db import Session

from models.Chamada import Turmas

# verificar se o usuario é professor e registrado na turma
def professor_required(current_user, id_turma):
    try:
        with Session() as sess: turmas = sess.query(Turmas).filter_by(id_turma=id_turma, id_user=current_user.id).first()
        
        return current_user.professor and turmas
        
    except:
        return False
    