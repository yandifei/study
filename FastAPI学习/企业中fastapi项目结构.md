project/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # 应用创建和配置
│   ├── core/            # 核心模块（配置，常量，工具函数等）
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── api/             # API路由
│   │   ├── __init__.py
│   │   ├── v1/          # 版本v1
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/   # 各个端点（按功能分文件）
│   │   │   │   ├── __init__.py
│   │   │   │   ├── items.py
│   │   │   │   └── users.py
│   │   │   └── api.py      # 聚合v1的所有路由
│   │   └── v2/          # 版本v2（如果有）
│   ├── models/          # 数据模型（Pydantic模型，数据库模型等）
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/         # Pydantic模型（有时和models合并，但为了清晰可以分开）
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── services/        # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   ├── repositories/    # 数据访问层（如果使用数据库）
│   │   ├── __init__.py
│   │   ├── user_repo.py
│   │   └── item_repo.py
│   ├── database/        # 数据库配置
│   │   ├── __init__.py
│   │   └── session.py
│   └── utils/           # 工具函数
│       ├── __init__.py
│       └── helpers.py
│
├── tests/               # 测试
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   └── test_services/
│
├── requirements.txt     # 依赖
├── Dockerfile
└── docker-compose.yml

分层和解耦：
路由层（API endpoints）：只负责接收请求、验证参数（通过Pydantic模型）、调用服务层处理业务、返回响应。
服务层（services）：实现业务逻辑，调用数据访问层（repositories）来获取和存储数据。
数据访问层（repositories）：负责与数据库交互，执行CRUD操作。
模型层（models/schemas）：定义数据模型，包括数据库模型（如使用SQLAlchemy）和请求/响应模型（Pydantic）。