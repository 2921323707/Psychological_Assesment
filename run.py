"""
简化的应用启动脚本
用于快速启动开发服务器
"""
# 从app包导入create_app函数和应用实例
from app import app

if __name__ == '__main__':
    print("=" * 50)
    print("心理测评系统启动中...")
    print("=" * 50)
    print("访问地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)

