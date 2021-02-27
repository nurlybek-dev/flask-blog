from flask import Blueprint

bp = Blueprint('users', __name__, url_prefix='/admin/users')

from app.admin.users import routes
