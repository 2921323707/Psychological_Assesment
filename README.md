# 心理测评网站

一个基于Flask框架开发的专业心理测评平台，提供60+种心理学量表测评服务。

## 功能特点

- 📊 **专业量表库**：涵盖情绪、人格、认知、性心理等多个领域的60+种心理学量表
- ✅ **完整测评流程**：量表列表 → 测评说明 → 答题 → 结果报告
- 📈 **详细报告**：专业的测评结果分析和建议
- 🧮 **自动评分系统**：支持正向/反向计分，自动计算标准分和等级
- ⚡ **即时反馈**：测试完成即刻获得结果
- 💾 **数据持久化**：答案自动保存，防止刷新丢失
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
│   ├── models.py            # 数据模型（User, Scale, ScaleItem, Test）
│   ├── utils/               # 工具模块
│   │   └── scoring.py      # 评分算法
│   ├── templates/           # 模板文件
│   │   ├── base.html       # 基础模板
│   │   ├── index.html      # 首页
│   │   ├── scales.html     # 量表列表页
│   │   ├── test.html       # 测评页面
│   │   └── report.html     # 报告页面
│   └── static/              # 静态文件
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── main.js
│           ├── test.js     # 测评交互逻辑
│           └── report.js   # 报告展示逻辑
├── scripts/                 # 脚本目录
│   ├── init_scales.py      # 数据库初始化脚本
│   ├── update_database.py  # 数据库更新脚本
│   └── verify_scoring.py  # 评分验证脚本
├── app.py                   # 向后兼容入口
├── run.py                   # 快速启动脚本 ⭐
├── config.py                # 配置文件
├── requirements.txt         # 依赖列表
├── psychological.db         # SQLite数据库（自动生成）
├── .gitignore               # Git忽略文件
├── README.md                # 项目说明
├── QUICKSTART.md           # 快速启动指南
├── DEVELOPMENT_ROADMAP.md   # 开发路线图
├── DATABASE_UPDATE.md      # 数据库更新说明
└── ScaleSrc.md             # 量表资源库
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

### 3. 初始化数据库

首次运行需要初始化数据库并导入量表数据：

```bash
# 初始化数据库并导入SDS和SAS量表
python scripts/init_scales.py
```

**注意**：此脚本会删除现有数据并重新创建表结构。如需保留数据，请先备份数据库。

如果只需更新数据库结构（添加新字段），使用：

```bash
python scripts/update_database.py
```

### 4. 运行应用

```bash
# 方式1：使用run.py（推荐，更友好）
python run.py

# 方式2：直接运行app.py
python app.py
```

应用将在 `http://localhost:5000` 启动

### 5. 访问应用

- **首页**：http://localhost:5000
- **量表列表**：http://localhost:5000/scales
- **测评页面**：http://localhost:5000/test?id=1（1为量表ID）
- **健康检查**：http://localhost:5000/api/health

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
响应: {
    "code": 200,
    "message": "success",
    "data": [
        {
            "id": 1,
            "name": "抑郁自评量表（SDS）",
            "category": "情绪与心理健康",
            "items": 20,
            "time": 10
        }
    ]
}
```

### 获取量表详情
```
GET /api/scales/<scale_id>
响应: {
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "name": "抑郁自评量表（SDS）",
        "description": "...",
        "total_items": 20
    }
}
```

### 获取量表题目列表
```
GET /api/scales/<scale_id>/items
响应: {
    "code": 200,
    "data": {
        "scale_id": 1,
        "items": [
            {
                "id": 1,
                "question": "题目内容",
                "options": [{"text": "选项", "value": 1}],
                "reverse_scoring": false,
                "order": 1
            }
        ]
    }
}
```

### 提交测试结果
```
POST /api/test/submit
Body: {
    "scale_id": 1,
    "answers": {"1": 3, "2": 4, ...},
    "duration": 120
}
响应: {
    "code": 200,
    "data": {
        "test_id": 1,
        "standard_score": 65.0,
        "level": "中度抑郁",
        "interpretation": {...}
    }
}
```

### 获取测试结果
```
GET /api/test/<test_id>
响应: {
    "code": 200,
    "data": {
        "test_id": 1,
        "standard_score": 65.0,
        "raw_score": 52,
        "level": "中度抑郁",
        "interpretation": {...}
    }
}
```

## 量表资源

详细量表列表和资源链接请参考 [ScaleSrc.md](ScaleSrc.md)

## 评分系统

### SDS（抑郁自评量表）
- **评分规则**：原始分 × 1.25 = 标准分
- **反向计分题目**：2, 5, 6, 11, 12, 14, 16, 17, 18, 20
- **等级划分**：
  - < 50：正常
  - 50-59：轻度抑郁
  - 60-69：中度抑郁
  - ≥ 70：重度抑郁

### SAS（焦虑自评量表）
- **评分规则**：原始分 × 1.25 = 标准分
- **反向计分题目**：5, 9, 13, 17, 19
- **等级划分**：
  - < 50：正常
  - 50-59：轻度焦虑
  - 60-69：中度焦虑
  - ≥ 70：重度焦虑

## Git使用指南

详细的Git操作和仓库更新指南请参考 [GIT_GUIDE.md](GIT_GUIDE.md)

**快速更新仓库**:
```bash
# 使用Python脚本（推荐）
python update_github.py

# 或在Windows上使用批处理
update_github.bat
```

## 已实现功能

### ✅ 核心功能
- [x] 量表列表展示
- [x] 测评页面（题目展示、选项选择、进度跟踪）
- [x] 自动评分系统（SDS、SAS）
- [x] 测评报告生成
- [x] 数据持久化（答案保存、测试记录）
- [x] 响应式UI设计

### 📊 当前支持的量表
- ✅ **SDS（抑郁自评量表）** - 20题，支持反向计分
- ✅ **SAS（焦虑自评量表）** - 20题，支持反向计分

### 🔄 开发计划

- [ ] 添加更多量表（SCL-90、EPQ等）
- [ ] 用户注册登录系统
- [ ] 测评结果历史记录
- [ ] 个性化推荐系统
- [ ] 数据可视化图表
- [ ] 管理员后台
- [ ] 量表导入工具
- [ ] PDF报告导出

## 使用说明

### 首次使用

1. 安装依赖：`pip install -r requirements.txt`
2. 初始化数据库：`python scripts/init_scales.py`
3. 启动应用：`python run.py`
4. 访问 http://localhost:5000

### 进行测评

1. 访问量表列表页面
2. 选择量表，点击"开始测试"
3. 阅读测评说明，点击"开始测评"
4. 逐题作答，可使用"上一题"/"下一题"导航
5. 完成所有题目后提交
6. 查看详细的测评报告

### 数据管理

- **初始化量表**：`python scripts/init_scales.py`（会清空现有数据）
- **更新数据库结构**：`python scripts/update_database.py`（保留数据）
- **验证评分**：`python scripts/verify_scoring.py`（检查评分是否正确）

## 注意事项

⚠️ **重要提示**：

1. 本项目仅用于学习和研究目的
2. 使用量表前请确认版权和授权信息
3. 测评结果仅供参考，不能替代专业诊断
4. 建议在专业人士指导下进行测评和解读
5. 生产环境请修改SECRET_KEY等敏感配置
6. 定期备份数据库文件 `psychological.db`

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过Issue反馈。

## 故障排查

### 标准分显示为0
- 确保答案格式正确（item_id为整数或字符串均可）
- 检查评分算法是否正常运行
- 运行 `python scripts/verify_scoring.py` 验证

### 数据库字段缺失
- 运行 `python scripts/update_database.py` 更新数据库结构

### 量表数据未加载
- 检查是否运行了初始化脚本：`python scripts/init_scales.py`
- 验证数据库文件中是否有量表数据

## 更新日志

### v1.1.0 (2024-11)
- ✅ 实现完整测评流程（说明页 → 答题 → 报告）
- ✅ 添加评分算法（SDS、SAS）
- ✅ 修复标准分显示问题
- ✅ 修复时区问题
- ✅ 添加测试时长记录

### v1.0.0 (2024)
- ✅ 初始化Flask项目
- ✅ 搭建基础架构
- ✅ 实现首页和量表列表
- ✅ 完成60+量表资源整理

---

*持续更新中...*
