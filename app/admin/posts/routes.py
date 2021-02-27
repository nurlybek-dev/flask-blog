from flask import redirect, url_for

from flask.globals import request
from flask.helpers import flash
from flask.templating import render_template

from app import db
from app.admin.posts import bp
from app.models import Post, get_post


@bp.route('/', methods=('GET',))
def index():
    posts = Post.query.all()
    return render_template('admin/posts/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        user_id = request.form['user_id']
        title = request.form['title']
        body = request.form['body']
        error = None

        if not user_id:
            error = 'Author is required.'
        elif not title:
            error = 'Title is required.'
        elif not body:
            error = 'Body is required.'

        if error is None:
            post = Post(user_id=user_id, title=title, body=body)
            db.session.add(post)
            db.session.commit()
            flash("Post create successfully.")
            return redirect(url_for('posts.read', id=post.id))
        
        flash(error)

    return render_template('admin/posts/create.html')


@bp.route('/<int:id>', methods=('GET',))
def read(id):
    model = get_post(id, False)
    return render_template('admin/posts/read.html', model=model)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    post = get_post(id, False)

    if request.method == 'POST':
        user_id = request.form['user_id']
        title = request.form['title']
        body = request.form['body']
        error = None

        if not user_id:
            error = 'Author is required.'
        elif not title:
            error = 'Title is required.'
        elif not body:
            error = 'Body is required.'

        if error is None:
            post.user_id = user_id
            post.title = title
            post.body = body
            db.session.add(post)
            db.session.commit()
            flash("Post update successfully.")
            return redirect(url_for('posts.read', id=post.id))
        
        flash(error)

    return render_template('admin/posts/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    flash("Post delete successfully.")
    return redirect('posts.index')
