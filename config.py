from os import getenv
import pathlib
from uuid import uuid4

class Base:
    # all consts used
    PATH = pathlib.Path(__file__).parent.resolve()
    ENV = getenv("ENV")
    RAPID_KEY = getenv("RAPID_KEY")
    DB_URI = None
    SECRET_KEY = None

class Config(Base):

    def __init__(self):
        match self.ENV:
            case "PRD": self.production()
            case "DEV": self.development()
            case _: self.development()

    def production(self):
        None

    def development(self):
        print("# Development environment")
        self.DB_URI = f"sqlite:///{self.PATH}/flask_template_db.sqlite"
        self.SECRET_KEY = str(uuid4())


config = Config()
