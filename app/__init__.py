from flask import Flask
from .routes import routes as routes_blueprint
from .api import api as api_blueprint
from .extensions import db, csrf
from .config import Config



def create_app(config_object=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config_object)
    
    # 初始化扩展
    db.init_app(app)
    csrf.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(routes_blueprint)
    # 自动创建数据库表（仅开发阶段使用，生产可用迁移工具）
    with app.app_context():
        db.create_all()                
    
    return app


