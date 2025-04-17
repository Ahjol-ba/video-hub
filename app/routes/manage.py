from flask import render_template, request, current_app
from . import routes
from app.models import Video
import os

@routes.route('/manage', methods=['GET'])
def manage():
    return render_template("manage.html")

