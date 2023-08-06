from flask.cli import AppGroup
import click

from app import db, bcrypt
from models.User import User
from models.Call import Class, UserClass, Call, Frequency
from seed import users, classes, userclass, rollscall, frequencies

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

@seed_cli.command("rollscall")
def seed_rollscall():
    for rc in rollscall:
        db.session.add(Call(**rc))
    db.session.commit()

@seed_cli.command("frequencies")
def seed_frequencies():
    for f in frequencies:
        db.session.add(Frequency(**f))
    db.session.commit()

@seed_cli.command("all")
@click.pass_context
def seed_all(ctx: click.Context):
    ctx.invoke(seed_users)
    ctx.invoke(seed_classes)
    ctx.invoke(seed_userclass)
    ctx.invoke(seed_rollscall)
    ctx.invoke(seed_frequencies)

