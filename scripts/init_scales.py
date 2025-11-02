"""
初始化数据库并导入量表数据
运行方式: python scripts/init_scales.py
"""
import sys
import os
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Scale, ScaleItem


# SDS（抑郁自评量表）题目数据
SDS_QUESTIONS = [
    {"question": "我觉得闷闷不乐，情绪低沉", "reverse": False},
    {"question": "我觉得一天之中早晨最好", "reverse": True},
    {"question": "我一阵阵地哭出来或觉得想哭", "reverse": False},
    {"question": "我夜间睡眠不好", "reverse": False},
    {"question": "我吃的跟平常一样多", "reverse": True},
    {"question": "我与异性密切接触时和以往一样感到愉快", "reverse": True},
    {"question": "我感到体重减轻", "reverse": False},
    {"question": "我为便秘烦恼", "reverse": False},
    {"question": "我的心跳比平时快", "reverse": False},
    {"question": "我无故感到疲乏", "reverse": False},
    {"question": "我的头脑跟往常一样清楚", "reverse": True},
    {"question": "我觉得经常做的事情并不困难", "reverse": True},
    {"question": "我觉得不安而平静不下来", "reverse": False},
    {"question": "我对将来抱有希望", "reverse": True},
    {"question": "我比平常容易生气激动", "reverse": False},
    {"question": "我觉得作出决定是容易的", "reverse": True},
    {"question": "我觉得自己是个有用的人，有人需要我", "reverse": True},
    {"question": "我的生活过得很有意思", "reverse": True},
    {"question": "我认为如果我死了别人会过得更好", "reverse": False},
    {"question": "平常感兴趣的事我仍然照样感兴趣", "reverse": True},
]

# SAS（焦虑自评量表）题目数据
SAS_QUESTIONS = [
    {"question": "我觉得比平常容易紧张和着急", "reverse": False},
    {"question": "我无缘无故地感到害怕", "reverse": False},
    {"question": "我容易心里烦乱或觉得惊恐", "reverse": False},
    {"question": "我觉得我可能将要发疯", "reverse": False},
    {"question": "我觉得一切都很好，也不会发生什么不幸", "reverse": True},
    {"question": "我手脚发抖打颤", "reverse": False},
    {"question": "我因为头痛、颈痛和背痛而苦恼", "reverse": False},
    {"question": "我感觉容易衰弱和疲乏", "reverse": False},
    {"question": "我觉得心平气和，并且容易安静坐着", "reverse": True},
    {"question": "我觉得心跳得很快", "reverse": False},
    {"question": "我因为一阵阵头晕而苦恼", "reverse": False},
    {"question": "我有晕倒发作，或觉得要晕倒似的", "reverse": False},
    {"question": "我吸气呼气都感到很容易", "reverse": True},
    {"question": "我的手脚麻木和刺痛", "reverse": False},
    {"question": "我因为胃痛和消化不良而苦恼", "reverse": False},
    {"question": "我常常要小便", "reverse": False},
    {"question": "我的手脚常常是干燥温暖的", "reverse": True},
    {"question": "我脸红发热", "reverse": False},
    {"question": "我容易入睡并且一夜睡得很好", "reverse": True},
    {"question": "我做恶梦", "reverse": False},
]

# SDS和SAS的通用选项（4点量表）
COMMON_OPTIONS = [
    {"text": "没有或很少时间", "value": 1},
    {"text": "小部分时间", "value": 2},
    {"text": "相当多时间", "value": 3},
    {"text": "绝大部分或全部时间", "value": 4},
]


def init_scales():
    """初始化量表数据"""
    app = create_app()
    
    with app.app_context():
        # 删除所有表并重新创建（以包含新的字段）
        print("正在初始化数据库...")
        print("注意：将删除所有现有数据并重新创建表结构...")
        db.drop_all()  # 删除所有表
        db.create_all()  # 重新创建表
        print("数据库表结构已更新")
        
        # 检查是否已有数据
        if Scale.query.count() > 0:
            print("检测到已有量表数据，是否要重新初始化？")
            response = input("输入 'yes' 继续，其他任意键取消: ")
            if response.lower() != 'yes':
                print("取消初始化")
                return
            
            # 删除现有数据
            ScaleItem.query.delete()
            Scale.query.delete()
            db.session.commit()
            print("已清空现有数据")
        
        # 创建SDS量表
        print("\n正在导入 SDS（抑郁自评量表）...")
        sds_scale = Scale(
            name="抑郁自评量表（SDS）",
            description="用于评估成人抑郁症状的自评量表，由Zung于1965年编制。",
            category="情绪与心理健康",
            total_items=20
        )
        db.session.add(sds_scale)
        db.session.flush()  # 获取scale_id
        
        for idx, item_data in enumerate(SDS_QUESTIONS, 1):
            item = ScaleItem(
                scale_id=sds_scale.id,
                question=item_data["question"],
                item_type="likert",
                options=json.dumps(COMMON_OPTIONS, ensure_ascii=False),
                reverse_scoring=item_data["reverse"],
                order=idx
            )
            db.session.add(item)
        
        print(f"  [OK] 已导入 {len(SDS_QUESTIONS)} 道题目")
        
        # 创建SAS量表
        print("\n正在导入 SAS（焦虑自评量表）...")
        sas_scale = Scale(
            name="焦虑自评量表（SAS）",
            description="用于评估焦虑主观感受的自评量表，由Zung于1971年编制。",
            category="情绪与心理健康",
            total_items=20
        )
        db.session.add(sas_scale)
        db.session.flush()
        
        for idx, item_data in enumerate(SAS_QUESTIONS, 1):
            item = ScaleItem(
                scale_id=sas_scale.id,
                question=item_data["question"],
                item_type="likert",
                options=json.dumps(COMMON_OPTIONS, ensure_ascii=False),
                reverse_scoring=item_data["reverse"],
                order=idx
            )
            db.session.add(item)
        
        print(f"  [OK] 已导入 {len(SAS_QUESTIONS)} 道题目")
        
        # 提交所有更改
        db.session.commit()
        
        print("\n" + "="*50)
        print("[OK] 数据库初始化完成！")
        print("="*50)
        print(f"已导入量表数量: {Scale.query.count()}")
        print(f"已导入题目总数: {ScaleItem.query.count()}")
        
        # 显示导入的量表列表
        print("\n已导入的量表：")
        for scale in Scale.query.all():
            items_count = ScaleItem.query.filter_by(scale_id=scale.id).count()
            print(f"  - {scale.name} ({items_count}题)")


if __name__ == '__main__':
    try:
        init_scales()
    except Exception as e:
        print(f"\n[ERROR] 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

