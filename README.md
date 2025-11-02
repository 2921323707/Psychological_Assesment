# 心理测评网站

一个基于Flask框架开发的专业心理测评平台，提供60+种心理学量表测评服务。

## 功能特点

- 📊 **专业量表库**：涵盖情绪、人格、认知、性心理等多个领域的60+种心理学量表
- 🔒 **数据安全**：严格的数据加密和隐私保护机制
- 📈 **详细报告**：专业的测评结果分析和建议
- ⚡ **即时反馈**：测试完成即刻获得结果
- 📱 **响应式设计**：支持PC和移动端访问
- 🎨 **现代化UI**：简洁美观的用户界面

## 技术栈

- **后端框架**：Flask 3.0
- **数据库**：SQLite (开发环境) / PostgreSQL (生产环境)
- **ORM**：SQLAlchemy
- **数据库迁移**：Flask-Migrate
- **跨域支持**：Flask-CORS

## 项目结构

```
psychological/
├── app/
│   ├── __init__.py          # 应用主文件和工厂函数
│   ├── routes.py            # 路由定义
│   ├── models.py            # 数据模型
│   ├── templates/           # 模板文件
│   │   ├── base.html
│   │   ├── index.html
│   │   └── scales.html
│   └── static/              # 静态文件
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── app.py                   # 向后兼容入口
├── run.py                   # 快速启动脚本 ⭐
├── config.py                # 配置文件
├── requirements.txt         # 依赖列表
├── .gitignore               # Git忽略文件
├── README.md                # 项目说明
└── ScaleSrc.md              # 量表资源库
```

## 快速开始

### 1. 环境要求

- Python 3.8+
- pip

### 2. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 运行应用

```bash
# 方式1：使用run.py（推荐，更友好）
python run.py

# 方式2：直接运行app.py
python app.py
```

应用将在 `http://localhost:5000` 启动

### 4. 数据库迁移（可选）

如果需要进行数据库迁移：

```bash
flask db init      # 初始化迁移
flask db migrate -m "Initial migration"  # 创建迁移
flask db upgrade   # 应用迁移
```

## 环境变量配置

创建 `.env` 文件（可选）：

```env
# 密钥（生产环境必须修改）
SECRET_KEY=your-secret-key-here

# 数据库URL
DATABASE_URL=sqlite:///psychological.db

# 环境
FLASK_ENV=development

# 日志级别
LOG_LEVEL=INFO
```

## API接口

### 健康检查
```
GET /api/health
```

### 获取量表列表
```
GET /api/scales/list
```

### 获取量表详情
```
GET /api/scales/<scale_id>
```

### 提交测试结果
```
POST /api/test/submit
Body: {
    "scale_id": 1,
    "answers": {...}
}
```

## 量表资源

详细量表列表和资源链接请参考 [ScaleSrc.md](ScaleSrc.md)

## 开发计划

- [ ] 用户注册登录系统
- [ ] 完整的量表测评功能
- [ ] 测评结果历史记录
- [ ] 个性化推荐系统
- [ ] 数据可视化报告
- [ ] 管理员后台
- [ ] 量表导入工具

## 注意事项

⚠️ **重要提示**：

1. 本项目仅用于学习和研究目的
2. 使用量表前请确认版权和授权信息
3. 测评结果仅供参考，不能替代专业诊断
4. 建议在专业人士指导下进行测评和解读
5. 生产环境请修改SECRET_KEY等敏感配置

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过Issue反馈。

---

*持续更新中...*

