"""
数据模型
"""
from datetime import datetime

# 导入db
from app import db


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class Scale(db.Model):
    """量表模型"""
    __tablename__ = 'scales'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    total_items = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    items = db.relationship('ScaleItem', backref='scale', lazy=True, cascade='all, delete-orphan')
    tests = db.relationship('Test', backref='scale', lazy=True)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'total_items': self.total_items,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ScaleItem(db.Model):
    """量表题目模型"""
    __tablename__ = 'scale_items'
    
    id = db.Column(db.Integer, primary_key=True)
    scale_id = db.Column(db.Integer, db.ForeignKey('scales.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    item_type = db.Column(db.String(20), default='multiple_choice')  # multiple_choice, likert
    order = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'scale_id': self.scale_id,
            'question': self.question,
            'item_type': self.item_type,
            'order': self.order
        }


class Test(db.Model):
    """测试记录模型"""
    __tablename__ = 'tests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    scale_id = db.Column(db.Integer, db.ForeignKey('scales.id'), nullable=False)
    score = db.Column(db.Float)
    result_level = db.Column(db.String(50))  # 轻度、中度、重度等
    answers = db.Column(db.Text)  # JSON格式存储答案
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'scale_id': self.scale_id,
            'score': self.score,
            'result_level': self.result_level,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

