"""
路由模块
"""
from flask import Blueprint, render_template, jsonify, request
from app.models import db

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
    scales_list = [
        {
            'id': 1,
            'name': '抑郁自评量表（SDS）',
            'category': '情绪与心理健康',
            'items': 20,
            'time': 10
        },
        {
            'id': 2,
            'name': '焦虑自评量表（SAS）',
            'category': '情绪与心理健康',
            'items': 20,
            'time': 10
        },
        {
            'id': 3,
            'name': '90项症状清单（SCL-90）',
            'category': '综合心理健康',
            'items': 90,
            'time': 30
        },
        {
            'id': 4,
            'name': '艾森克人格问卷（EPQ）',
            'category': '人格特质',
            'items': 88,
            'time': 25
        },
        {
            'id': 5,
            'name': '卡特尔16种人格因素问卷（16PF）',
            'category': '人格特质',
            'items': 187,
            'time': 45
        },
        {
            'id': 51,
            'name': '性压抑指数/RPI量表',
            'category': '性心理与性健康',
            'items': 40,
            'time': 15
        }
    ]
    
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': scales_list
    })


@api_bp.route('/scales/<int:scale_id>', methods=['GET'])
def get_scale_detail(scale_id):
    """获取量表详情"""
    # 这里后续从数据库查询
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'id': scale_id,
            'name': '抑郁自评量表（SDS）',
            'description': '用于评估成人抑郁症状',
            'instruction': '请根据最近一周的情况，选择最符合您的选项'
        }
    })


@api_bp.route('/test/submit', methods=['POST'])
def submit_test():
    """提交测试结果"""
    data = request.get_json()
    
    # 这里后续保存到数据库
    
    return jsonify({
        'code': 200,
        'message': '测试提交成功',
        'data': {
            'test_id': 1,
            'result': '您的抑郁程度为轻度'
        }
    })

