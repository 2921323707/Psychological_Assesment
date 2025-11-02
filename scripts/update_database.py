"""
数据库更新脚本
添加duration字段，保留现有数据
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import text

def update_database():
    """更新数据库，添加duration字段"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查字段是否已存在
            result = db.session.execute(text("PRAGMA table_info(tests)"))
            columns = [row[1] for row in result]
            
            if 'duration' not in columns:
                print("正在添加duration字段...")
                db.session.execute(text("ALTER TABLE tests ADD COLUMN duration INTEGER DEFAULT 0"))
                db.session.commit()
                print("[OK] duration字段添加成功")
            else:
                print("[OK] duration字段已存在，无需更新")
                
            print("\n数据库更新完成！")
            
        except Exception as e:
            print(f"\n[ERROR] 更新失败: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    update_database()

