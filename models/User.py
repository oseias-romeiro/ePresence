from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum
from flask_login import UserMixin
import enum 

from app import db

class UserRole(enum.Enum):
    ADMIN = "Admin"
    PROFESSOR = "Professor"
    STUDENT = "Student"

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    registration: Mapped[str] = mapped_column(String(9), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(127), nullable=False)
    password: Mapped[str] = mapped_column(String(127), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)

    def __repr__(self):
        return "mat: %r" % self.registration

