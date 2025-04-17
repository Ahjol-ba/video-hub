# app/api/__init__.py
from flask import Blueprint

api = Blueprint('api', __name__)

from .api_get_csrf_token import api_get_csrf_token
from .api_regenerate_thumbnail import api_regenerate_thumbnail
from .api_upload_video import api_upload_video
from .api_update_video import api_update_video
from .api_query_videos import api_videos