from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint, JSON, String

from models.User import User
from db import db


class Chamada(db.Model):
    __tablename__ = "chamadas"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(nullable=False)
    id_turma: Mapped[int] = mapped_column(ForeignKey("turma.id"))
    location: Mapped[dict] = mapped_column(JSON, nullable=True)

    __table_args__ = (UniqueConstraint(date, id_turma, name="constDateTurma"),)

    turma: Mapped["Turma"] = relationship(foreign_keys="Chamada.id_turma")

    frequencias:  Mapped[list["Frequencia"]] = relationship(back_populates="chamada")


class Frequencia(db.Model):
    __tablename__ = "frequencias"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_chamada: Mapped[int] = mapped_column(ForeignKey("chamadas.id"))
    location: Mapped[dict] = mapped_column(JSON, nullable=True)

    __table_args__ = (UniqueConstraint(id_user, id_chamada, name="constUserChamada"),)

    user: Mapped["User"] = relationship(foreign_keys="Frequencia.id_user")
    chamada: Mapped["Chamada"] = relationship(foreign_keys="Frequencia.id_chamada")


class Turma(db.Model):
    __tablename__ = "turma"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(127), nullable=False)

    turmas:  Mapped[list["Turmas"]] = relationship(back_populates="turma")
    chamadas:  Mapped[list["Chamada"]] = relationship(back_populates="turma")


class Turmas(db.Model):
    __tablename__ = "turmas"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_turma: Mapped[int] = mapped_column(ForeignKey("turma.id"))

    user: Mapped["User"] = relationship(foreign_keys="Turmas.id_user")
    turma: Mapped["Turma"] = relationship(foreign_keys="Turmas.id_turma")

    