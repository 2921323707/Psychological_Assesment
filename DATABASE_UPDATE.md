# 数据库更新说明

## 更新内容

Test模型新增了 `duration` 字段用于存储测试时长（秒）。

## 更新方法

由于添加了新字段，需要更新数据库表结构。有两种方法：

### 方法1：重新初始化数据库（会删除所有数据）

运行初始化脚本：
```bash
python scripts/init_scales.py
```

⚠️ **注意**：这会删除所有现有的测试记录和数据！

### 方法2：手动添加字段（保留现有数据）

使用SQLite命令行或数据库管理工具执行：

```sql
ALTER TABLE tests ADD COLUMN duration INTEGER DEFAULT 0;
```

或者使用Python脚本：

```python
from app import create_app, db
from app.models import Test
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # 检查字段是否已存在
        result = db.session.execute(text("PRAGMA table_info(tests)"))
        columns = [row[1] for row in result]
        
        if 'duration' not in columns:
            db.session.execute(text("ALTER TABLE tests ADD COLUMN duration INTEGER DEFAULT 0"))
            db.session.commit()
            print("✓ duration字段添加成功")
        else:
            print("✓ duration字段已存在")
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        db.session.rollback()
```

## 修复的问题

1. ✅ 分值显示为0的问题 - 修复了分数判断逻辑
2. ✅ 时间差8小时的问题 - 使用本地时间而不是UTC
3. ✅ 测评时长未显示的问题 - 添加了duration字段并正确保存/返回

