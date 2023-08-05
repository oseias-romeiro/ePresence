from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, Integer, Sequence, text
from flask_login import UserMixin
import enum 

from app import db

class UserRole(enum.Enum):
    ADMIN = "Admin"
    PROFESSOR = "Professor"
    STUDENT = "Student"

    def __str__(self):
        return self.name
    def __html__(self):
        return self.value

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    register: Mapped[str] = mapped_column(Integer, unique=True)
    name: Mapped[str] = mapped_column(String(127), nullable=False)
    password: Mapped[str] = mapped_column(String(127), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)

    def __repr__(self):
        return "user: (%d, %s, %s, %s)" % (self.id, self.register, self.name, self.role)

