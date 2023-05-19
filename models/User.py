from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
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

