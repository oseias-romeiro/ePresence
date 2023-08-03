from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint, JSON, String

from models.User import User
from app import db

class Call(db.Model):
    __tablename__ = "calls"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(nullable=False)
    id_class: Mapped[int] = mapped_column(ForeignKey("class.id"))
    location: Mapped[dict] = mapped_column(JSON, nullable=True)

    __table_args__ = (UniqueConstraint(date, id_class, name="constDateClass"),)

    fclass: Mapped["Class"] = relationship(foreign_keys="Call.id_class")

    frequencies:  Mapped[list["Frequency"]] = relationship(back_populates="call")


class Frequency(db.Model):
    __tablename__ = "frequencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_call: Mapped[int] = mapped_column(ForeignKey("calls.id"))
    location: Mapped[dict] = mapped_column(JSON, nullable=True)

    __table_args__ = (UniqueConstraint(id_user, id_call, name="constUserCall"),)

    user: Mapped["User"] = relationship(foreign_keys="Frequency.id_user")
    call: Mapped["Call"] = relationship(foreign_keys="Frequency.id_call")


class Class(db.Model):
    __tablename__ = "class"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(127), nullable=False)

    user_class:  Mapped[list["UserClass"]] = relationship(back_populates="class")
    calls:  Mapped[list["Call"]] = relationship(back_populates="class")


class UserClass(db.Model):
    __tablename__ = "user_class"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_class: Mapped[int] = mapped_column(ForeignKey("class.id"))

    user: Mapped["User"] = relationship(foreign_keys="UserClass.id_user")
    f_class: Mapped["Class"] = relationship(foreign_keys="UserClass.id_class")
