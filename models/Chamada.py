from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint, JSON

from models.Turma import Turma
from models.User import User
from db import db


class Chamada(db.Model):
    __tablename__ = "chamadas"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(nullable=False, unique=True)
    id_turma: Mapped[int] = mapped_column(ForeignKey("turma.id"))
    location: Mapped[dict] = mapped_column(JSON, nullable=True)

    turma: Mapped["Turma"] = relationship(foreign_keys="Chamada.id_turma")


class Frequencia(db.Model):
    __tablename__ = "frequencias"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_chamada: Mapped[int] = mapped_column(ForeignKey("chamadas.id"))
    location: Mapped[dict] = mapped_column(JSON, nullable=True)

    __table_args__ = (UniqueConstraint(id_user, id_chamada, name="constUserChamada"),)

    user: Mapped["User"] = relationship(foreign_keys="Frequencia.id_user")
    chamada: Mapped["Chamada"] = relationship(foreign_keys="Frequencia.id_chamada")

