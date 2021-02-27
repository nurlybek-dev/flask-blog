import click
from app import db
from app.models import User
from flask.cli import with_appcontext


@click.command()
@click.option('--username', default='')
@click.option('--password', default='')
@with_appcontext
def createsuperuser(username, password):
    if not username:
        username = input("Enter username:")
    if not password:
        password = input("Enter password:")

    user = User(username=username, is_staff=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print('Super user create successfully.')


@click.command()
@with_appcontext
def create_db():
    db.create_all()
    print("Database create successfully.")


def init_app(app):
    app.cli.add_command(createsuperuser)
    app.cli.add_command(create_db)
