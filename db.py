from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pathlib

from models.User import Turmas

PATH = pathlib.Path(__file__).parent.resolve()

engine = create_engine(f"sqlite:///{PATH}/flask_template_db.sqlite", echo=True)
Session = sessionmaker(bind=engine)

# verificar se o usuario é professor e registrado na turma
def professor_required(current_user, id_turma):
    try:
        with Session() as sess: turmas = sess.query(Turmas).filter_by(id_turma=id_turma, id_user=current_user.id).first()
        
        return current_user.professor and turmas
        
    except:
        return False