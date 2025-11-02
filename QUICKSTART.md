# 快速启动指南

## 一键启动

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **启动应用**
```bash
# 方式1：使用run.py（推荐）
python run.py

# 方式2：直接运行app.py
python app.py
```

3. **访问应用**
打开浏览器访问：`http://localhost:5000`

## 目录结构说明

```
psychological/
├── app/                    # 应用主目录
│   ├── __init__.py        # 包初始化（定义db）
│   ├── models.py          # 数据模型
│   ├── routes.py          # 路由定义
│   ├── templates/         # HTML模板
│   │   ├── base.html      # 基础模板
│   │   ├── index.html     # 首页
│   │   └── scales.html    # 量表列表页
│   └── static/            # 静态文件
│       ├── css/
│       │   └── style.css  # 样式文件
│       └── js/
│           └── main.js    # JavaScript文件
├── app.py                 # 应用入口（工厂模式）
├── run.py                 # 快速启动脚本
├── config.py              # 配置文件
├── requirements.txt       # 依赖列表
├── .gitignore            # Git忽略文件
├── README.md             # 项目说明
├── ScaleSrc.md           # 量表资源库
└── QUICKSTART.md         # 本文件
```

## 已实现的功能

✅ **基础框架**
- Flask应用工厂模式
- 蓝图路由组织
- 数据库ORM（SQLAlchemy）
- 跨域支持（CORS）

✅ **页面**
- 首页展示
- 量表列表
- 响应式设计

✅ **API接口**
- 健康检查 `/api/health`
- 量表列表 `/api/scales/list`
- 量表详情 `/api/scales/<id>`
- 提交测试 `/api/test/submit`

✅ **数据库模型**
- User（用户）
- Scale（量表）
- ScaleItem（量表题目）
- Test（测试记录）

## 下一步开发

- [ ] 完善量表测评界面
- [ ] 实现量表题目加载
- [ ] 添加评分算法
- [ ] 生成测评报告
- [ ] 用户登录注册
- [ ] 测评历史记录
- [ ] 管理员后台

## 常见问题

**Q: 导入错误？**
A: 确保在项目根目录运行，使用 `python run.py` 而非直接运行 `app.py`

**Q: 端口被占用？**
A: 修改 `run.py` 或 `app.py` 中的 `port=5000` 为其他端口

**Q: 数据库问题？**
A: 首次运行会自动创建SQLite数据库文件

## 技术支持

- Flask官方文档：https://flask.palletsprojects.com/
- SQLAlchemy文档：https://docs.sqlalchemy.org/
- 项目README：查看 README.md

