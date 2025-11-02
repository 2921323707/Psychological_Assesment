"""
心理测评应用包初始化文件
"""
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
import os

# 初始化扩展
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """
    应用工厂函数
    """
    from config import config
    from app.routes import main_bp, api_bp
    
    app = Flask(__name__)
    
    # 加载配置
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 启用CORS（跨域支持）
    CORS(app)
    
    # 注册蓝图
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 注册错误处理器
    @app.errorhandler(404)
    def not_found(error):
        from flask import jsonify
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import jsonify
        return jsonify({'error': 'Internal server error'}), 500
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app


# 创建应用实例（用于直接运行app包时）
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """
    Flask shell上下文
    """
    return {'db': db}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
