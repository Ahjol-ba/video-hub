# app/routes/upload.py
from flask import render_template
from . import routes
@routes.route('/upload')
def upload():
    return render_template('upload.html')
