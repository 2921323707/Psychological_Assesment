"""
路由模块
"""
from flask import Blueprint, render_template, jsonify, request
from app.models import db, Scale, ScaleItem

# 主页面蓝图
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首页"""
    return render_template('index.html')


@main_bp.route('/scales')
def scales():
    """量表列表页"""
    return render_template('scales.html')


@main_bp.route('/test')
def test():
    """测评页面"""
    return render_template('test.html')


@main_bp.route('/report')
def report():
    """报告页面"""
    return render_template('report.html')


# API蓝图
api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'message': '心理测评系统运行正常'
    })


@api_bp.route('/scales/list', methods=['GET'])
def get_scales_list():
    """获取量表列表"""
    try:
        scales = Scale.query.order_by(Scale.id).all()
        scales_list = []
        
        for scale in scales:
            # 估算时间：每题约0.5分钟
            estimated_time = max(5, (scale.total_items or 0) * 0.5)
            
            scales_list.append({
                'id': scale.id,
                'name': scale.name,
                'category': scale.category or '未分类',
                'items': scale.total_items or 0,
                'time': int(estimated_time)
            })
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': scales_list
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取量表列表失败: {str(e)}',
            'data': []
        }), 500


@api_bp.route('/scales/<int:scale_id>', methods=['GET'])
def get_scale_detail(scale_id):
    """获取量表详情"""
    try:
        scale = Scale.query.get_or_404(scale_id)
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'id': scale.id,
                'name': scale.name,
                'description': scale.description or '暂无描述',
                'category': scale.category or '未分类',
                'total_items': scale.total_items or 0,
                'instruction': '请根据最近一周的情况，选择最符合您的选项'
            }
        })
    except Exception as e:
        return jsonify({
            'code': 404,
            'message': f'量表不存在: {str(e)}',
            'data': None
        }), 404


@api_bp.route('/scales/<int:scale_id>/items', methods=['GET'])
def get_scale_items(scale_id):
    """获取量表题目列表"""
    try:
        scale = Scale.query.get_or_404(scale_id)
        items = ScaleItem.query.filter_by(scale_id=scale_id).order_by(ScaleItem.order).all()
        
        items_list = []
        for item in items:
            items_list.append(item.to_dict())
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'scale_id': scale_id,
                'scale_name': scale.name,
                'items': items_list,
                'total': len(items_list)
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取题目列表失败: {str(e)}',
            'data': None
        }), 500


@api_bp.route('/test/submit', methods=['POST'])
def submit_test():
    """提交测试结果"""
    try:
        data = request.get_json()
        scale_id = data.get('scale_id')
        answers = data.get('answers', {})
        duration = data.get('duration', 0)
        
        if not scale_id:
            return jsonify({
                'code': 400,
                'message': '缺少量表ID',
                'data': None
            }), 400
        
        # 获取量表和题目信息
        scale = Scale.query.get_or_404(scale_id)
        items = ScaleItem.query.filter_by(scale_id=scale_id).order_by(ScaleItem.order).all()
        
        if not items:
            return jsonify({
                'code': 404,
                'message': '量表题目不存在',
                'data': None
            }), 404
        
        # 转换为字典格式供评分函数使用
        items_dict = [item.to_dict() for item in items]
        
        # 计算分数
        from app.utils.scoring import calculate_score
        score_result = calculate_score(scale.name, answers, items_dict)
        
        # 保存测试记录到数据库
        from app.models import Test
        from datetime import datetime
        import json as json_lib
        
        test_record = Test(
            user_id=None,  # 匿名测试，后续可关联用户
            scale_id=scale_id,
            score=score_result['standard_score'],
            result_level=score_result['level'],
            answers=json_lib.dumps(answers, ensure_ascii=False),
            duration=duration,  # 保存测试时长
            completed_at=datetime.now()  # 使用本地时间而不是UTC
        )
        
        db.session.add(test_record)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '测试提交成功',
            'data': {
                'test_id': test_record.id,
                'scale_id': scale_id,
                'scale_name': scale.name,
                'raw_score': score_result['raw_score'],
                'standard_score': score_result['standard_score'],
                'level': score_result['level'],
                'level_en': score_result['level_en'],
                'interpretation': score_result['interpretation'],
                'duration': duration
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'提交失败: {str(e)}',
            'data': None
        }), 500


@api_bp.route('/test/<int:test_id>', methods=['GET'])
def get_test_result(test_id):
    """获取测试结果详情"""
    try:
        from app.models import Test
        test = Test.query.get_or_404(test_id)
        scale = Scale.query.get(test.scale_id)
        
        import json
        answers = json.loads(test.answers) if test.answers else {}
        items = ScaleItem.query.filter_by(scale_id=test.scale_id).order_by(ScaleItem.order).all()
        items_dict = [item.to_dict() for item in items]
        
        # 重新计算分数（确保数据一致性）
        from app.utils.scoring import calculate_score
        score_result = calculate_score(scale.name if scale else '', answers, items_dict)
        
        # 处理时间显示（转换为本地时间字符串）
        completed_at_str = None
        if test.completed_at:
            # 使用本地时间格式化（datetime.now()保存的时间已经是本地时间）
            completed_at_str = test.completed_at.strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'test_id': test.id,
                'scale_id': test.scale_id,
                'scale_name': scale.name if scale else '未知量表',
                'raw_score': score_result['raw_score'],
                'standard_score': test.score if test.score is not None else score_result['standard_score'],  # 修复：正确处理0值
                'level': test.result_level if test.result_level else score_result['level'],
                'level_en': score_result['level_en'],
                'interpretation': score_result['interpretation'],
                'completed_at': completed_at_str,
                'duration': test.duration if test.duration else 0
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取测试结果失败: {str(e)}',
            'data': None
        }), 500

