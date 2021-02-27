from flask import render_template

from app.admin import bp


@bp.route('/', methods=('GET',))
def index():
    return render_template('admin/index.html')
