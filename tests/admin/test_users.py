import pytest
from app.models import User
from werkzeug.security import check_password_hash


def test_index(client, admin_login):
    assert client.get('/admin/users/').status_code == 200


def test_create(client, app, admin_login):
    assert client.get('/admin/users/create').status_code == 200

    client.post('/admin/users/create', data={'username': 'user', 'password': 'user'})
    
    with app.app_context():
        assert User.query.count() == 3


def test_update(client, app, admin_login):
    assert client.get('/admin/users/2/update').status_code == 200

    client.post('/admin/users/2/update', data={'username': 'updated'})
    with app.app_context():
        user = User.query.get(2)
        assert user.username == 'updated'


def test_change_password(client, app, admin_login):
    assert client.get('/admin/users/2/update').status_code == 200

    client.post('/admin/users/2/update', data={'username': 'updated', 'password': 'new'})
    with app.app_context():
        user = User.query.get(2)
        assert check_password_hash(user.password_hash, 'new')


@pytest.mark.parametrize(('path', 'username', 'password', 'message'), (
    ('/admin/users/create', '', 'pass', b'Username is required.'),
    ('/admin/users/create', 'user', '', b'Password is required.'),
    ('/admin/users/2/update', '', 'pass', b'Username is required.'),
))
def test_create_update_validate(client, admin_login, path, username, password, message):
    response = client.post(path, data={'username': username, 'password': password})
    assert message in response.data


def test_read(client, admin_login):
    assert client.get('/admin/users/1').status_code == 200


def test_delete(client, app, admin_login):
    client.post('/admin/users/2/delete')
    with app.app_context():
        assert User.query.get(2) is None
