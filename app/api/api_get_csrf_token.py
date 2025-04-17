# app/api/routes.py
from flask import jsonify
from flask_wtf.csrf import generate_csrf
from . import api


@api.route('/get_csrf_token')
def api_get_csrf_token():
    try:
        return jsonify({'csrf_token': generate_csrf()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500    
