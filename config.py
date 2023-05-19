from os import getenv
import pathlib

class Base:
    PATH = pathlib.Path(__file__).parent.resolve()
    ENV = getenv("ENV")
    RAPID_KEY = getenv("RAPID_KEY")
    DB_URI = None

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

config = Config()
