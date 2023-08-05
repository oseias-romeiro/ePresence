from flask.cli import AppGroup

from app import db, bcrypt
from models.User import User
from models.Call import Class, UserClass
from seed import users, classes, userclass

seed_cli = AppGroup("seed")

@seed_cli.command("users")
def seed_users():
    for user in users:
        user['password'] = bcrypt.generate_password_hash(user.get('password')) # encrypt password
        db.session.add(User(**user))
    db.session.commit()

@seed_cli.command("classes")
def seed_classes():
    for classe in classes:
        db.session.add(Class(**classe))
    db.session.commit()

@seed_cli.command("userclass")
def seed_userclass():
    for uc in userclass:
        db.session.add(UserClass(**uc))
    db.session.commit()
