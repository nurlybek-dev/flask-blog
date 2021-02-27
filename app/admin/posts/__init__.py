from flask import Blueprint

bp = Blueprint('posts', __name__, url_prefix='/admin/posts')

from app.admin.posts import routes
