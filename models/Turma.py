from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from models.User import User
from db import db


class Turma(db.Model):
    __tablename__ = "turma"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(127), nullable=False)


class Turmas(db.Model):
    __tablename__ = "turmas"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_turma: Mapped[int] = mapped_column(ForeignKey("turma.id"))

    user: Mapped["User"] = relationship(foreign_keys='Turmas.id_user')
    turma: Mapped["Turma"] = relationship(foreign_keys='Turmas.id_turma')

