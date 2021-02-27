import pytest
from app.models import Post, Comment


def test_index(client, auth):
    response = client.get('/')
    assert b'Login' in response.data
    assert b'Register' in response.data

    auth.login()
    response = client.get('/')
    assert b'Logout' in response.data
    assert b'test title 3' in response.data
    assert b'href="/post/3/"' in response.data


def test_index_pages(client):
    response = client.get('/?page=1')
    assert b'test title 3' in response.data
    assert b'next' in response.data
    response = client.get('/?page=2')
    assert b'test title 2' in response.data
    assert b'next' in response.data
    assert b'prev' in response.data
    response = client.get('/?page=3')
    assert b'test title 1' in response.data
    assert b'prev' in response.data


def test_search(client):
    response = client.get('/?search=not%20found')
    assert b'<article class="post">' not in response.data

    response = client.get('/?search=test%20title%201')
    assert b'test title 1' in response.data
    assert b'href="/post/1/"' in response.data


def test_not_exists_page(client):
    assert client.get('/4/').status_code == 404


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
    '/1/comment'
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/login'


def test_author_required(client, auth):
    auth.login()

    assert client.post('/3/update').status_code == 403
    assert client.post('/3/delete').status_code == 403

    assert b'href="/3/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/100/'
    '/100/update',
    '/100/delete'
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': 'body'})

    with app.app_context():
        count = Post.query.count()
        assert count == 4


def test_guest_view(client):
    response = client.get('/post/1/')
    assert response.status_code == 200
    assert b'test title 1' in response.data
    assert b'test body' in response.data
    assert b'href="/1/update"' not in response.data
    assert b'<textarea name="message" id="comment-text" cols="30" rows="10">' not in response.data


def test_author_view(client, auth):
    auth.login()
    response = client.get('/post/1/')
    assert response.status_code == 200
    assert b'test title 1' in response.data
    assert b'test body' in response.data
    assert b'href="/1/update"' in response.data


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': 'body'})

    with app.app_context():
        post = Post.query.get(1)
        assert post.title == 'updated'


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        post = Post.query.get(1)
        assert post is None


def test_comment(client, auth, app):
    auth.login()
    response = client.post('/1/comment', data={'message': 'msg'})

    with app.app_context():
        count = Comment.query.filter_by(post_id=1).count()
        assert count == 1


def test_comment_validate(app, client, auth):
    auth.login()
    response = client.post('/1/comment', data={'message': ''})
    assert response.status_code == 302
    with app.app_context():
        count = Comment.query.filter_by(post_id=1).count()
        assert count == 0
