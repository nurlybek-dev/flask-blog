from flask import redirect, url_for

from flask.globals import request
from flask.helpers import flash
from flask.templating import render_template

from app import db
from app.admin.users import bp
from app.models import User, get_user


@bp.route('/', methods=('GET', ))
def index():
    users = User.query.all()
    return render_template('admin/users/index.html', users=users)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            user = User(username=username)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()
            flash("User create successfully.")
            return redirect(url_for('users.read', id=user.id))
        
        flash(error)

    return render_template('admin/users/create.html')


@bp.route('/<int:id>', methods=('GET',))
def read(id):
    model = get_user(id)
    return render_template('admin/users/read.html', model=model)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    user = get_user(id)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_staff = request.form.get('is_staff')
        error = None

        if not username:
            error = 'Username is required.'

        if error is None:
            user.username = username
            user.is_staff = is_staff == 'on'

            if password:
                user.set_password(password)

            db.session.add(user)
            db.session.commit()
            flash("User update successfully.")
            return redirect(url_for('users.read', id=id))
        
        flash(error)

    return render_template('admin/users/update.html', user=user)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    user = get_user(id)
    db.session.delete(user)
    db.session.commit()
    flash("User delete successfully.")
    return redirect(url_for('users.index'))