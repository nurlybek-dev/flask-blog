from app.auth.routes import login
from flask import Blueprint, g
from flask.globals import request
from werkzeug.exceptions import abort

from app.auth import login_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.before_app_request
def admin_access():
    if str(request.url_rule).startswith('/admin'):
        if not g.user or not g.user.is_staff:
            abort(403, '')

from app.admin import routes
