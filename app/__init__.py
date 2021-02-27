import os

from flask import Flask
from flask_moment import Moment
from flaskext.markdown import Markdown

from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)


    app.config.from_object(config_class)

    db.init_app(app)

    from app import auth
    app.register_blueprint(auth.bp)

    from app import main
    app.register_blueprint(main.bp)

    from app import admin
    app.register_blueprint(admin.bp)

    from app.admin import users
    app.register_blueprint(users.bp)

    from app.admin import posts
    app.register_blueprint(posts.bp)


    Moment(app)
    Markdown(app)

    from app import cli
    cli.init_app(app)

    return app
