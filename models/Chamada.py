from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, ForeignKey, Date, JSON, UniqueConstraint

from models.Turma import Turma
from models.User import User

Base = declarative_base()


class Chamada(Base):
    __tablename__ = "chamada"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, unique=True)
    id_turma = Column(Integer, ForeignKey(Turma.id))
    location = Column(JSON, nullable=True)

    turma = relationship('Turma', foreign_keys='Chamada.id_turma')


class Frequencia(Base):
    __tablename__ = "frequencia"

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey(User.id))
    id_chamada = Column(Integer, ForeignKey(Chamada.id))
    location = Column(JSON, nullable=True)

    __table_args__ = (UniqueConstraint(id_user, id_chamada, name="constUserChamada"),)

    user = relationship('User', foreign_keys='Frequencia.id_user')
    chamada = relationship('Chamada', foreign_keys='Frequencia.id_chamada')

