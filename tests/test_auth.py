import pytest
from flask import g, session
from app.models import User


def test_register(client, app):
    assert client.get('/register').status_code == 200
    response = client.post(
        '/register', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/login' == response.headers['Location']

    with app.app_context():
        assert User.query.filter_by(username='a').first() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_registered_validate_input(client, username, password, message):
    response = client.post(
        '/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user.username == 'test'


@pytest.mark.parametrize('path', (
    '/register',
    '/login'
))
def test_logged_in(client, auth, path):
    auth.login()
    response = client.get(path)
    assert response.status_code == 302


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrent username or password.'),
    ('test', 'a', b'Incorrent username or password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
