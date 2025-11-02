import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """应用配置类"""
    
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "psychological.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 应用配置
    JSON_AS_ASCII = False  # 支持中文JSON
    JSON_SORT_KEYS = False
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    
    # 分页配置
    POSTS_PER_PAGE = 20


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

