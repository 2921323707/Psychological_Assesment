"""
验证评分修复
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Test, ScaleItem
from app.utils.scoring import calculate_score
import json

app = create_app()
with app.app_context():
    test = Test.query.order_by(Test.id.desc()).first()
    
    if test:
        print(f"Test ID: {test.id}")
        print(f"Saved Score in DB: {test.score}")
        print(f"Scale ID: {test.scale_id}")
        
        # 加载答案和题目
        answers = json.loads(test.answers) if test.answers else {}
        items = ScaleItem.query.filter_by(scale_id=test.scale_id).order_by(ScaleItem.order).all()
        items_dict = [item.to_dict() for item in items]
        
        # 获取量表名称
        from app.models import Scale
        scale = Scale.query.get(test.scale_id)
        scale_name = scale.name if scale else ''
        
        print(f"\nAnswers (first 5): {dict(list(answers.items())[:5])}")
        print(f"Items count: {len(items_dict)}")
        print(f"First item ID: {items_dict[0]['id'] if items_dict else 'N/A'} (type: {type(items_dict[0]['id']) if items_dict else 'N/A'})")
        
        # 重新计算分数
        result = calculate_score(scale_name, answers, items_dict)
        
        print(f"\nRecalculated Results:")
        print(f"  Raw Score: {result['raw_score']}")
        print(f"  Standard Score: {result['standard_score']}")
        print(f"  Level: {result['level']}")
        
        # 修复数据库中的分数
        if test.score != result['standard_score']:
            print(f"\n[INFO] 发现分数不一致，正在更新数据库...")
            test.score = result['standard_score']
            test.result_level = result['level']
            db.session.commit()
            print(f"[OK] 已更新数据库中的分数")
    else:
        print("没有找到测试记录")

