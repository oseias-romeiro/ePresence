from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from models.User import User

Base = declarative_base()


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

