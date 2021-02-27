import pytest

from app.models import User, Post, Comment


def test_user_repr(app):
    with app.app_context():
        user = User(username='test')
        assert '<User test>' == str(user)


def test_post_repr(app):
    with app.app_context():
        post = Post(title='post title')
        assert '<Post post title>' == str(post)

    
def test_comment_repr(app):
    with app.app_context():
        comment = Comment(message='Comment message')
        assert '<Comment Comment message>' == str(comment)
