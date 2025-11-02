"""
评分算法模块
处理不同量表的评分逻辑
"""
import json


def calculate_sds_score(answers, items):
    """
    计算SDS（抑郁自评量表）分数
    
    SDS评分规则：
    1. 原始分 = 所有题目分数之和（反向计分题目已处理）
    2. 标准分 = 原始分 × 1.25
    3. 标准分 < 50: 正常
       50-59: 轻度抑郁
       60-69: 中度抑郁
       >= 70: 重度抑郁
    
    反向计分题目：2, 5, 6, 11, 12, 14, 16, 17, 18, 20 (按order，从1开始)
    """
    raw_score = 0
    total_items = len(items)
    
    # 反向计分的题目索引（从1开始）
    reverse_items = [2, 5, 6, 11, 12, 14, 16, 17, 18, 20]
    
    for item in items:
        item_id = item['id']
        # JSON序列化后，JavaScript的数字key会变成字符串，需要兼容两种格式
        answer_value = answers.get(item_id) or answers.get(str(item_id))
        
        if answer_value is None:
            continue
        
        # 确保answer_value是整数
        answer_value = int(answer_value)
        
        # 判断是否需要反向计分
        is_reverse = item.get('reverse_scoring', False) or item['order'] in reverse_items
        
        if is_reverse:
            # 反向计分：1->4, 2->3, 3->2, 4->1
            score = 5 - answer_value
        else:
            score = answer_value
        
        raw_score += score
    
    # 计算标准分
    standard_score = raw_score * 1.25
    
    # 判断等级
    if standard_score < 50:
        level = "正常"
        level_en = "normal"
    elif standard_score < 60:
        level = "轻度抑郁"
        level_en = "mild"
    elif standard_score < 70:
        level = "中度抑郁"
        level_en = "moderate"
    else:
        level = "重度抑郁"
        level_en = "severe"
    
    return {
        'raw_score': raw_score,
        'standard_score': round(standard_score, 2),
        'level': level,
        'level_en': level_en,
        'max_score': total_items * 4,
        'interpretation': get_sds_interpretation(level)
    }


def calculate_sas_score(answers, items):
    """
    计算SAS（焦虑自评量表）分数
    
    SAS评分规则：
    1. 原始分 = 所有题目分数之和（反向计分题目已处理）
    2. 标准分 = 原始分 × 1.25
    3. 标准分 < 50: 正常
       50-59: 轻度焦虑
       60-69: 中度焦虑
       >= 70: 重度焦虑
    
    反向计分题目：5, 9, 13, 17, 19 (按order，从1开始)
    """
    raw_score = 0
    total_items = len(items)
    
    # 反向计分的题目索引（从1开始）
    reverse_items = [5, 9, 13, 17, 19]
    
    for item in items:
        item_id = item['id']
        # JSON序列化后，JavaScript的数字key会变成字符串，需要兼容两种格式
        answer_value = answers.get(item_id) or answers.get(str(item_id))
        
        if answer_value is None:
            continue
        
        # 确保answer_value是整数
        answer_value = int(answer_value)
        
        # 判断是否需要反向计分
        is_reverse = item.get('reverse_scoring', False) or item['order'] in reverse_items
        
        if is_reverse:
            # 反向计分：1->4, 2->3, 3->2, 4->1
            score = 5 - answer_value
        else:
            score = answer_value
        
        raw_score += score
    
    # 计算标准分
    standard_score = raw_score * 1.25
    
    # 判断等级
    if standard_score < 50:
        level = "正常"
        level_en = "normal"
    elif standard_score < 60:
        level = "轻度焦虑"
        level_en = "mild"
    elif standard_score < 70:
        level = "中度焦虑"
        level_en = "moderate"
    else:
        level = "重度焦虑"
        level_en = "severe"
    
    return {
        'raw_score': raw_score,
        'standard_score': round(standard_score, 2),
        'level': level,
        'level_en': level_en,
        'max_score': total_items * 4,
        'interpretation': get_sas_interpretation(level)
    }


def get_sds_interpretation(level):
    """获取SDS结果解释"""
    interpretations = {
        "正常": {
            "summary": "您的抑郁水平在正常范围内",
            "description": "根据测评结果，您目前没有明显的抑郁症状。继续保持健康的生活方式，关注心理健康。",
            "suggestions": [
                "保持规律的作息和充足的睡眠",
                "适量运动，保持身体健康",
                "与家人朋友保持良好的社交关系",
                "培养兴趣爱好，保持积极心态"
            ]
        },
        "轻度抑郁": {
            "summary": "您可能存在轻度抑郁倾向",
            "description": "测评结果显示您存在轻度的抑郁症状。这可能与近期生活压力、情绪波动等因素有关。",
            "suggestions": [
                "关注自己的情绪变化，尝试记录每天的心情",
                "增加户外活动，多接触阳光和新鲜空气",
                "尝试放松技巧，如深呼吸、冥想等",
                "与信任的亲友交流，分享您的感受",
                "如果症状持续或加重，建议寻求专业帮助"
            ]
        },
        "中度抑郁": {
            "summary": "您可能存在中度抑郁症状",
            "description": "测评结果显示您存在中度的抑郁症状。建议您关注心理健康，及时采取干预措施。",
            "suggestions": [
                "建议寻求专业心理咨询师的帮助",
                "保持规律的作息和健康的饮食",
                "进行适度的体育锻炼",
                "学习情绪管理技巧",
                "避免过度使用社交媒体，减少信息过载",
                "考虑参加心理健康支持小组"
            ]
        },
        "重度抑郁": {
            "summary": "您可能存在重度抑郁症状",
            "description": "测评结果显示您存在重度的抑郁症状。强烈建议您尽快寻求专业心理健康服务。",
            "suggestions": [
                "立即寻求专业心理健康服务或精神科医生的帮助",
                "不要独自承担，告诉家人或朋友您的情况",
                "如有自杀想法，请立即联系心理危机干预热线",
                "接受专业治疗，可能需要药物治疗配合心理治疗",
                "建立支持网络，不要孤立自己",
                "注意安全，避免做出冲动决定"
            ]
        }
    }
    return interpretations.get(level, interpretations["正常"])


def get_sas_interpretation(level):
    """获取SAS结果解释"""
    interpretations = {
        "正常": {
            "summary": "您的焦虑水平在正常范围内",
            "description": "根据测评结果，您目前没有明显的焦虑症状。继续保持健康的生活方式。",
            "suggestions": [
                "保持规律的作息和充足的睡眠",
                "适量运动，保持身体健康",
                "学习压力管理技巧",
                "培养兴趣爱好，保持积极心态"
            ]
        },
        "轻度焦虑": {
            "summary": "您可能存在轻度焦虑倾向",
            "description": "测评结果显示您存在轻度的焦虑症状。这可能与近期生活压力、工作学习等因素有关。",
            "suggestions": [
                "关注自己的情绪变化，尝试记录焦虑触发因素",
                "练习深呼吸、冥想等放松技巧",
                "保持规律的作息和充足的睡眠",
                "减少咖啡因和刺激性物质的摄入",
                "进行适度的体育锻炼",
                "如果症状持续或加重，建议寻求专业帮助"
            ]
        },
        "中度焦虑": {
            "summary": "您可能存在中度焦虑症状",
            "description": "测评结果显示您存在中度的焦虑症状。建议您关注心理健康，及时采取干预措施。",
            "suggestions": [
                "建议寻求专业心理咨询师的帮助",
                "学习认知行为疗法技巧",
                "进行规律的体育锻炼",
                "练习正念冥想",
                "建立健康的生活作息",
                "避免过度使用社交媒体和新闻",
                "考虑参加焦虑管理课程"
            ]
        },
        "重度焦虑": {
            "summary": "您可能存在重度焦虑症状",
            "description": "测评结果显示您存在重度的焦虑症状。强烈建议您尽快寻求专业心理健康服务。",
            "suggestions": [
                "立即寻求专业心理健康服务或精神科医生的帮助",
                "接受专业治疗，可能需要药物治疗配合心理治疗",
                "学习应对焦虑发作的技巧",
                "建立支持网络，不要孤立自己",
                "避免刺激性物质（咖啡因、酒精等）",
                "注意安全，避免在焦虑状态下做重要决定"
            ]
        }
    }
    return interpretations.get(level, interpretations["正常"])


def calculate_score(scale_name, answers, items):
    """
    通用评分函数，根据量表名称选择对应的评分算法
    """
    scale_name_lower = scale_name.lower()
    
    if 'sds' in scale_name_lower or '抑郁自评' in scale_name:
        return calculate_sds_score(answers, items)
    elif 'sas' in scale_name_lower or '焦虑自评' in scale_name:
        return calculate_sas_score(answers, items)
    else:
        # 默认评分（简单相加）
        raw_score = sum(answers.values()) if answers else 0
        return {
            'raw_score': raw_score,
            'standard_score': raw_score,
            'level': '未知',
            'level_en': 'unknown',
            'max_score': len(items) * 4 if items else 0,
            'interpretation': {
                'summary': '测评完成',
                'description': '测评已完成，请咨询专业人士解读结果。',
                'suggestions': []
            }
        }

