from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

from config import config

engine = create_engine(config.DB_URI, echo=True)
Session = sessionmaker(bind=engine)

db = SQLAlchemy()
