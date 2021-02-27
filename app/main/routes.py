from flask import (
    flash, g, redirect, render_template, request, url_for, current_app
)


from app import db
from app.main import bp
from app.auth import login_required
from app.models import Post, Comment, get_post


@bp.route('/')
def index():
    page = request.args.get('page', 1, int)
    search_text = request.args.get('search', '')
    posts = Post.query.filter(
        Post.title.like('%{}%'.format(search_text))
        ).order_by(Post.created_at.desc()) \
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    return render_template('blog/index.html', posts=posts, search_text=search_text)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        
        if error is None:
            post = Post(title=title, body=body, user_id=g.user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post successfully created.')
            return redirect(url_for('main.view', id=post.id))

        flash(error)
    
    return render_template('blog/create.html')

@bp.route('/post/<int:id>/', methods=('GET', ))
def view(id):
    post = get_post(id, False)
    return render_template('blog/view.html', post=post)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is None:
            post.title = title
            post.body = body
            db.session.commit()
            flash('Post successfully updated.')
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.index'))


@bp.route('/<int:id>/comment', methods=('POST',))
@login_required
def comment(id):
    get_post(id, False)
    message = request.form['message']
    error = None

    if not message:
        error = 'Message is required.'

    if error is None:
        comment = Comment(post_id=id, user_id=g.user.id, message=message)
        db.session.add(comment)
        db.session.commit()
        flash('Comment successfully send.')
        return redirect(url_for('main.view', id=id))

    flash(error)

    return redirect(url_for('main.view', id=id))
