from datetime import datetime

import pytest

from app import create_app, db
from app.models import User, Post


class AuthActions(object):
    def __init__(self, client):
        self._clien = client

    def login(self, username='test', password='test'):
        return self._clien.post(
            '/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._clien.get('/logout')


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': "sqlite://",
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test',
        'POSTS_PER_PAGE': 1
    })

    with app.app_context():
        db.create_all()
        user1 = User(username='test', is_staff=True)
        user1.set_password('test')
        user2 = User(username='other')
        user2.set_password('other')
        db.session.add(user1)
        db.session.add(user2)

        post1 = Post(title='test title 1', body='test body', user_id=1, created_at=datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
        post2 = Post(title='test title 2', body='test body', user_id=1, created_at=datetime.strptime('2019-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
        post3 = Post(title='test title 3', body='test body', user_id=2, created_at=datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))

        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)

        db.session.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def admin_login(auth):
    auth.login()
    yield
