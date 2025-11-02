"""
心理测评网站 Flask 应用主文件

注意：为了更好的项目结构，应用逻辑已迁移到 app/__init__.py
此文件保留用于向后兼容，推荐使用 run.py 或直接运行 app 包
"""
# 从app包导入所有内容
from app import *

# 保留原有的app实例作为别名
flask_app = app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
