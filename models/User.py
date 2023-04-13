from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from flask_login import UserMixin

Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    matricula = Column(String(9), nullable=False, unique=True)
    name = Column(String(127), nullable=False)
    password = Column(String(127), nullable=False)
    professor = Column(Boolean, nullable=False)

    def __repr__(self):
        return "mat: %r" % self.matricula
    
class Turma(Base):
    __tablename__ = "turma"

    id = Column(Integer, primary_key=True)
    name = Column(String(127), nullable=False)

class Turmas(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey(User.id))
    id_turma = Column(Integer, ForeignKey(Turma.id))

    user = relationship('User', foreign_keys='Turmas.id_user')
    turma = relationship('Turma', foreign_keys='Turmas.id_turma')


class Chamada(Base):
    __tablename__ = "chamada"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, unique=True)
    id_turma = Column(Integer, ForeignKey(Turma.id))

    turma = relationship('Turma', foreign_keys='Chamada.id_turma')

class Frequencia(Base):
    __tablename__ = "frequencia"

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey(User.id))
    id_chamada = Column(Integer, ForeignKey(Chamada.id))

    user = relationship('User', foreign_keys='Frequencia.id_user')
    chamada = relationship('Chamada', foreign_keys='Frequencia.id_chamada')

