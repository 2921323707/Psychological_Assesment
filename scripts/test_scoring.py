"""
测试评分函数
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.scoring import calculate_sds_score, calculate_sas_score

# 测试数据：答案的key是字符串（从JSON中来的）
test_answers = {
    "1": 3, "2": 4, "3": 4, "4": 2, "5": 3,
    "6": 2, "7": 2, "8": 3, "9": 2, "10": 3,
    "11": 2, "12": 1, "13": 3, "14": 2, "15": 3,
    "16": 4, "17": 1, "18": 3, "19": 1, "20": 2
}

# 模拟items数据（item_id是整数）
test_items = []
for i in range(1, 21):
    test_items.append({
        'id': i,
        'order': i,
        'reverse_scoring': False
    })

# 设置反向计分题目（SDS）
reverse_items = [2, 5, 6, 11, 12, 14, 16, 17, 18, 20]
for idx in reverse_items:
    if idx <= len(test_items):
        test_items[idx-1]['reverse_scoring'] = True

print("测试SDS评分函数...")
print(f"答案数量: {len(test_answers)}")
print(f"题目数量: {len(test_items)}")

result = calculate_sds_score(test_answers, test_items)
print(f"\n结果:")
print(f"  原始分: {result['raw_score']}")
print(f"  标准分: {result['standard_score']}")
print(f"  等级: {result['level']}")

