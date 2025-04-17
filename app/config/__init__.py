import json
import os
from flask import current_app
# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构造 config.json 的绝对路径
config_path = os.path.join(script_dir, 'config.json')

class Config:
    SQLALCHEMY_DATABASE_URI =  "sqlite:////data/database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "f4d9e1627243f36d0e1b0cdf734c6259003dc63e27b7811e"
    ALLOWED_EXTENSIONS = ["mp4", "avi", "mov", "mkv"]
    VIDEO_FOLDER = '/static/videos'
    ABS_VIDEO_FOLDER = '/app/static/videos'
    THUMB_FOLDER = '/static/videos/.thumbs'
    ABS_THUMB_FOLDER = '/app/static/videos/.thumbs'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            json_config = json.load(f)
            SQLALCHEMY_DATABASE_URI = json_config['DATABASE']
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            SECRET_KEY = json_config['SECRET_KEY']
            ALLOWED_EXTENSIONS = json_config['ALLOWED_EXTENSIONS']
            VIDEO_FOLDER = '/static/videos'
            THUMB_FOLDER = '/static/videos/.thumbs'
    except Exception as e:
        current_app.logger.error(f"{e}\nDue to the current error, use default configuration to start app.")

