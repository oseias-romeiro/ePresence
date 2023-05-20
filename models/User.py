from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from flask_login import UserMixin

from db import db

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    matricula: Mapped[str] = mapped_column(String(9), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(127), nullable=False)
    password: Mapped[str] = mapped_column(String(127), nullable=False)
    professor: Mapped[bool] = mapped_column(nullable=False)

    def __repr__(self):
        return "mat: %r" % self.matricula

