import pytest
from app.models import Post


def test_index(client, admin_login):
    assert client.get('/admin/posts/').status_code == 200


def test_create(client, app, admin_login):
    assert client.get('/admin/posts/create').status_code == 200

    client.post('/admin/posts/create', data={'user_id': 1, 'title': 'title', 'body': 'body'})
    
    with app.app_context():
        assert Post.query.count() == 4


def test_update(client, app, admin_login):
    assert client.get('/admin/posts/1/update').status_code == 200

    client.post('/admin/posts/1/update', data={'user_id': 1, 'title': 'updated', 'body': 'body'})
    with app.app_context():
        post = Post.query.get(1)
        assert post.title == 'updated'


@pytest.mark.parametrize(('path', 'user_id', 'title', 'body', 'message'), (
    ('/admin/posts/create', '', '', '', b'Author is required.'),
    ('/admin/posts/create', 1, '', '', b'Title is required.'),
    ('/admin/posts/create', 1, 'title', '', b'Body is required.'),
    ('/admin/posts/1/update', '', '', '', b'Author is required.'),
    ('/admin/posts/1/update', 1, '', '', b'Title is required.'),
    ('/admin/posts/1/update', 1, 'title', '', b'Body is required.'),
))
def test_create_update_validate(client, admin_login, path, user_id, title, body, message):
    response = client.post(path, data={'user_id': user_id, 'title': title, 'body': body})
    assert message in response.data


def test_read(client, admin_login):
    assert client.get('/admin/posts/1').status_code == 200


def test_delete(client, app, admin_login):
    client.post('/admin/posts/1/delete')
    with app.app_context():
        assert Post.query.get(1) is None
