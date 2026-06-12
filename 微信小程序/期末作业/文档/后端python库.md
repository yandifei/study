# 后端 Python 库

ACG 智能图廊后端（mongodb_service）使用的 Python 依赖及用途说明。

---

## 一、依赖清单（pyproject.toml）

| 库 | 版本 | 用途 |
|------|------|------|
| `fastapi[standard]` | ≥0.136.3 | Web 框架，异步路由、依赖注入、自动 OpenAPI 文档 |
| `uvicorn` | ≥0.49.0 | ASGI 服务器，运行 FastAPI 应用 |
| `pymongo` | ≥4.17.0 | MongoDB 原生异步驱动（AsyncMongoClient），替代已弃用的 motor |
| `redis` | ≥8.0.0 | Redis 异步客户端，存储 Refresh Token、验证码、冷却标记 |
| `python-jose[cryptography]` | ≥3.5.0 | JWT 编码/解码/签名验证，支持 HS256，生产环境推荐 |
| `pydantic` | ≥2.13.4 | 数据校验与序列化，BaseModel 替代 Beanie ODM |
| `email-validator` | ≥2.3.0 | 邮箱格式校验（pydantic EmailStr 依赖） |
| `python-dotenv` | ≥1.2.2 | 加载 .env 环境变量 |
| `colorlog` | ≥6.10.1 | 彩色日志输出 |

---

## 二、技术选型说明

### 2.1 为什么用 pymongo 原生异步，不用 Beanie/motor？

- **motor 已官方弃用**：MongoDB 官方推荐 pymongo 4.x+ 自带的 `AsyncMongoClient`
- **不用 ODM**：企业实践中，ODM 引入隐式查询和黑箱行为。使用 pydantic BaseModel 做数据校验 + 原始 pymongo 操作更透明、性能更好
- 数据访问模式：`MongoDB dict → pydantic BaseModel(**doc)` ，`_id`（ObjectId）在数据访问层转为 `id: str`

### 2.2 为什么用 python-jose 而不是 PyJWT？

| 维度 | python-jose | PyJWT |
|------|------------|-------|
| 加密算法 | HS256 / RS256 等 | 基础算法 |
| Claims 校验 | 内置 options 参数强制要求字段 | 需手写 |
| 生态 | FastAPI 官方文档推荐 | 社区维护 |
| 企业实践 | ✅ 更完整的异常体系 | 需额外封装 |

### 2.3 Redis 的 RESP2 强制

`redis-py` 6.x 默认使用 RESP3 协议，会在认证前发送 `HELLO` 命令，导致 `AuthenticationError`。项目中显式设置 `protocol=2` 强制 RESP2 规避此问题。

```python
redis_client = Redis(
    host=...,
    port=...,
    password=...,
    db=0,
    decode_responses=True,
    protocol=2,  # 强制 RESP2
)
```

---

## 三、关键库的使用位置

| 库 | 使用模块 |
|------|---------|
| `fastapi` | `main.py`、`services/auth/router.py`、`services/browse/router.py`、`services/favorite/router.py` |
| `pymongo` | `services/database/mongodb.py`、`services/database/index_manager.py` |
| `redis` | `services/database/redis.py`、`services/auth/session_service.py`、`services/auth/verification.py` |
| `python-jose` | `services/auth/jwt.py` |
| `pydantic` | `data_models/database/`、`data_models/auth_model/` |
| `email-validator` | `data_models/auth_model/schemas.py`（EmailStr） |
| `python-dotenv` | `utils/config_manager.py` |
