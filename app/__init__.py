import os

from flask import Flask
from flask_moment import Moment
from flaskext.markdown import Markdown

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping({
        'POSTS_PER_PAGE': 5,
    })

    if test_config is None:
        app.config.from_pyfile('../config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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
