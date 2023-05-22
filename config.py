from os import getenv
import pathlib
from uuid import uuid4

class Base:
    # all consts used
    PATH = pathlib.Path(__file__).parent.resolve()
    ENV = getenv("ENV")
    RAPID_KEY = getenv("RAPID_KEY")
    DB_URI = None
    SECRET_KEY = "s3cr3t"
    HOST = "127.0.0.1"
    PORT = 5000

class Config(Base):

    def __init__(self):
        if self.ENV == "PRD": self.production()
        elif self.ENV == "DEV": self.development()
        elif self.ENV == "TST": self.test()
        else: self.development()

    def production(self):
        print("# Production environment")
        self.DB_URI = f"sqlite:///{self.PATH}/db.sqlite"
        self.SECRET_KEY = str(uuid4())
        self.HOST = "0.0.0.0"
        self.PORT = 80
        print("SECRET_KEY:", self.SECRET_KEY)


    def development(self):
        print("# Development environment")
        self.DB_URI = f"sqlite:///{self.PATH}/db.sqlite"

    def test(self):
        print("# Test environment")
        self.DB_URI = f"sqlite:///:memory:?cache=shared"


config = Config()
