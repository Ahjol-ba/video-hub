# app/routes/__init__.py
from flask import Blueprint

routes = Blueprint('routes', __name__)

from .index import index
from .play import play
from .upload import upload
from .manage import manage
from .update import update
__all__ = {
    'index',
    'play',
    'upload',
    'manage',
    'update'
}
