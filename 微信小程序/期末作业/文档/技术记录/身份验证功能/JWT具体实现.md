# JWT 认证系统 —— 企业级实现文档

> 项目: mongodb_service (FastAPI + MongoDB + Redis)  
> 日期: 2026-06-11  
> 作者: yandifei + Claude Code

---

## 一、架构总览

```
┌──────────────────────────────────────────────────────────────────┐
│                         客户端 (浏览器/小程序)                      │
│                                                                   │
│   Access Token  ──→  存内存                                       │
│   Refresh Token ──→  存内存（开发环境）或 httpOnly Cookie（生产）    │
└──────────────────────────────┬───────────────────────────────────┘
                               │
         ① POST /auth/send-code │  Header: Authorization: Bearer <access>
         ② POST /auth/login     │
         ③ POST /auth/refresh   │
         ④ POST /auth/logout    │
                               │
┌──────────────────────────────┴───────────────────────────────────┐
│                        FastAPI 服务端                              │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  第 5 层: router.py        认证路由层                         │ │
│  │  /auth/send-code  /auth/login  /auth/refresh  /auth/logout  │ │
│  │  /auth/me                                                    │ │
│  │  职责: 定义 HTTP 接口，编排下层调用，返回标准响应              │ │
│  ├─────────────────────────────────────────────────────────────┤ │
│  │  第 4 层: verification.py  验证码服务层  ★ 新增              │ │
│  │  send_code() / verify_and_consume_code()                     │ │
│  │  职责: 生成、存储、校验、发送邮箱验证码                        │ │
│  ├─────────────────────────────────────────────────────────────┤ │
│  │  第 3 层: dependencies.py  依赖注入层  ★★★ 核心              │ │
│  │  get_current_user() / get_optional_user() / require_role()  │ │
│  │  职责: Header 提取 token → 验证 → 查库 → 注入 User 对象      │ │
│  ├─────────────────────────────────────────────────────────────┤ │
│  │  第 2 层: session_service.py  会话管理层                      │ │
│  │  save / exists / delete / rotate / revoke_all / count       │ │
│  │  职责: Redis 中 Refresh Token 的 CRUD + 轮换 + 撤销          │ │
│  ├─────────────────────────────────────────────────────────────┤ │
│  │  第 1 层: jwt.py            加密工具层                        │ │
│  │  create / verify / decode / extract  + 自定义异常体系         │ │
│  │  职责: JWT 编码、解码、签名验证、载荷校验                      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌──────────┐  ┌──────────┐                                      │
│  │ MongoDB  │  │  Redis   │                                      │
│  │ 用户数据  │  │ Refresh  │                                      │
│  │ (pymongo)│  │ Token +  │                                      │
│  │          │  │ 验证码    │                                      │
│  └──────────┘  └──────────┘                                      │
└──────────────────────────────────────────────────────────────────┘
```

---

## 二、文件结构

```
services/auth/
├── __init__.py          # 统一导出接口，一行 import 引入全部功能
├── jwt.py               # JWT 创建/验证/解码 + 自定义异常体系
├── session_service.py   # Redis 会话管理 (Refresh Token 生命周期)
├── verification.py      # 邮箱验证码服务 (生成/存储/校验/发送)
├── dependencies.py      # FastAPI 依赖注入 (核心认证层)
└── router.py            # 认证路由 (/auth/*)

data_models/
├── auth_model/
│   ├── __init__.py      # 认证模型导出
│   └── schemas.py       # 请求/响应 Pydantic 模型
└── database/
    ├── __init__.py      # 数据模型导出
    ├── user.py          # User (嵌入 browse/favorite 数组)
    ├── image.py         # Image
    ├── browse.py        # BrowseItem 子文档
    └── favorite.py      # FavoriteItem 子文档

services/database/
├── __init__.py          # 数据库模块导出
├── mongodb.py           # pymongo AsyncMongoClient 连接管理
├── redis.py             # Redis 异步客户端 (RESP2 模式)
└── index_manager.py     # MongoDB 索引管理

main.py                  # FastAPI 入口 (注册路由 + 异常处理器 + lifespan)
```

---

## 三、双 Token 设计

### 3.1 为什么需要两个 Token？

| 维度 | Access Token | Refresh Token |
|------|-------------|---------------|
| **有效期** | 15 分钟（短） | 30 天（长） |
| **存储位置** | 前端内存 | Redis（服务端） |
| **作用** | 每次 API 请求的身份凭证 | 换取新的 Access Token |
| **泄露后果** | 低风险（15分钟后自动失效） | 高风险（可通过 Redis 撤销） |
| **撤销能力** | 不可撤销（依赖过期） | 可精确撤销（删除 Redis key） |

### 3.2 JWT 载荷（Payload）设计

**Access Token:**
```json
{
  "iss": "AGC鉴赏画廊",
  "sub": "507f1f77bcf86cd799439011",
  "jti": "a1b2c3d4-e5f6-...",
  "type": "access",
  "iat": "2026-06-09T10:00:00Z",
  "nbf": "2026-06-09T10:00:00Z",
  "exp": "2026-06-09T10:15:00Z"
}
```

**Refresh Token:**
```json
{
  "iss": "AGC鉴赏画廊",
  "sub": "507f1f77bcf86cd799439011",
  "jti": "b2c3d4e5-f6a7-...",
  "type": "refresh",
  "iat": "2026-06-09T10:00:00Z",
  "nbf": "2026-06-09T10:00:00Z",
  "exp": "2026-07-09T10:00:00Z"
}
```

> JWT 载荷中**不含** `email`、`role` 等业务字段。用户信息通过 `sub`（MongoDB ObjectId）按需查询。

### 3.3 密钥分离

Access Token 和 Refresh Token 使用**不同的密钥和算法**：

| Token 类型 | 环境变量 | 密钥用途 |
|-----------|---------|---------|
| Access | `ACCESS_TOKEN_SECRET_KEY` + `ACCESS_TOKEN_ALGORITHM` | 签名短期访问令牌 |
| Refresh | `REFRESH_TOKEN_SECRET_KEY` + `REFRESH_TOKEN_ALGORITHM` | 签名长期刷新令牌 |

---

## 四、自定义异常体系

### 4.1 设计理由

企业级做法是**抛出自定义异常**，由全局异常处理器捕获并返回精确的 HTTP 响应。

### 4.2 异常继承树

```
Exception
 └── AuthException (认证异常基类)
      ├── TokenExpiredError       → HTTP 401, X-Token-Error: expired
      ├── TokenInvalidError       → HTTP 401, X-Token-Error: invalid
      ├── TokenMissingError       → HTTP 401
      ├── TokenTypeError          → HTTP 401, X-Token-Error: wrong-type
      └── InsufficientPermissionError → HTTP 403
```

### 4.3 全局异常处理器（main.py）

```python
@app.exception_handler(TokenExpiredError)
async def token_expired_handler(request, exc: TokenExpiredError):
    return JSONResponse(
        status_code=401,
        content={"code": 401, "msg": exc.message, "data": None},
        headers={"X-Token-Error": "expired"},  # ← 前端可根据此头判断刷新还是跳转登录
    )
```

---

## 五、核心模块详解

### 5.1 `jwt.py` —— 加密工具层

#### 公开函数

| 函数 | 用途 | 何时使用 |
|------|------|---------|
| `create_access_token(user_id)` | 生成 Access Token | 登录时、刷新时 |
| `create_refresh_token(user_id)` | 生成 Refresh Token | 登录时、刷新时 |
| `verify_token(token, type)` | **完整校验**（签名+过期+iss+sub+type） | 外部请求的 token 验证 |
| `decode_token(token, type)` | **轻量解码**（仅签名+过期） | 内部读取刚创建的 token 载荷 |
| `extract_user_id_from_access_token(token)` | 验证 access token 并返回用户 ID | 依赖注入层使用 |

#### `verify_token` vs `decode_token` 的区别

```
verify_token:  签名 ✅ + 过期 ✅ + 签发者 ✅ + 用户ID ✅ + 类型 ✅  → 外部请求
decode_token:  签名 ✅ + 过期 ✅                                     → 内部使用
```

### 5.2 `verification.py` —— 验证码服务层

#### Redis Key 设计

```
email_code:{email}      → 6位验证码，TTL 300s（5 分钟）
email_cooldown:{email}  → "1"，TTL 60s（发送冷却期）
```

#### 核心函数

| 函数 | 说明 |
|------|------|
| `send_code(email)` | 编排完整发码流程：冷却检查 → 生成 → 存 Redis → 发邮件 → 设冷却 |
| `verify_and_consume_code(email, code)` | 校验 + 一次性消费（验证后立即删除） |
| `generate_code()` | 生成 6 位随机数字验证码 |
| `check_send_cooldown(email)` | 检查是否在 60s 冷却期内 |
| `set_send_cooldown(email)` | 设置冷却标记 |

#### 发码流程

```
POST /auth/send-code { "email": "user@qq.com" }

① 检查冷却期 → 冷却期内 → 429 "请 X 秒后再试"
               → 可发送   → 继续
② 生成 6 位随机数字
③ 存入 Redis (email_code:{email}, TTL 300s)
④ 调用 utils/message_util.py 发送邮件
⑤ 设置冷却期 (email_cooldown:{email}, TTL 60s)
⑥ 返回 200 "验证码已发送"
```

### 5.3 `session_service.py` —— 会话管理层

#### Redis Key 设计

```
Key 格式:   refresh:{user_id}:{jti}
Value:      "1"  (简单存在标记)
TTL:        与 Refresh Token JWT 过期时间一致

示例: refresh:507f1f77bcf86cd799439011:a1b2c3d4-... → "1"
```

#### 核心操作

| 函数 | 说明 |
|------|------|
| `save_refresh_token(user_id, jti)` | 登录/刷新时存储新 Token |
| `exists_refresh_token(user_id, jti)` | 验证 Token 是否有效（未被撤销） |
| `delete_refresh_token(user_id, jti)` | 单设备登出 |
| `rotate_refresh_token(user_id, old_jti, new_jti)` | Token 轮换（核心安全机制） |
| `revoke_all_user_tokens(user_id)` | 全设备登出（使用 SCAN，非 KEYS） |
| `count_user_sessions(user_id)` | 统计活跃会话数 |

#### Token Rotation（防重放攻击）

```
正常流程:
  用户               服务端              Redis
  │                   │                   │
  │──refresh(old)──→  │                   │
  │                   │──exists(old)?──→  │  ← 存在 ✅
  │                   │←──True─────────   │
  │                   │──delete(old)───→  │  ← 立即作废
  │                   │──set(new)──────→  │  ← 创建新的
  │←──new pair────── │                   │

攻击场景 (攻击者窃取了 old token):
  用户               攻击者             服务端              Redis
  │                   │                   │                   │
  │──refresh(old)──→  │                   │                   │
  │                   │                   │──exists(old)?──→  │ ← 存在 ✅
  │                   │                   │──delete(old)───→  │
  │                   │                   │──set(new)──────→  │
  │←──new pair────── │                   │                   │
  │                   │                   │                   │
  │                   │──refresh(old)──→  │                   │
  │                   │                   │──exists(old)?──→  │ ← 不存在 ❌
  │                   │                   │──revoke_all()──→  │ ← 全设备撤销!
  │                   │←──401 reused──── │                   │
  │ (用户被强制登出)  │                   │                   │
```

#### SCAN vs KEYS

`revoke_all_user_tokens` 使用 `SCAN` 而非 `KEYS`，避免生产环境阻塞 Redis。

### 5.4 `dependencies.py` —— 依赖注入层

#### 核心依赖

```python
# 强制认证 —— 未登录返回 401
async def get_current_user(
    token: str = Depends(oauth2_scheme),  # ← 自动从 Authorization Header 提取
) -> User:
    user_id = extract_user_id_from_access_token(token)  # 验证 JWT
    user = await users.find_one({"_id": ObjectId(user_id)})  # pymongo 原生查询
    if user is None:
        raise TokenInvalidError("用户不存在或已被删除")
    doc["id"] = str(doc.pop("_id"))
    return User(**doc)
```

#### 使用方式

```python
# 方式 1: 强制认证
@app.get("/protected")
async def protected_route(user: User = Depends(get_current_user)):
    return {"msg": f"你好, {user.username}"}

# 方式 2: 可选认证（登录/未登录都能访问）
@app.get("/content")
async def content(user: Optional[User] = Depends(get_optional_user)):
    if user:
        return {"msg": f"你好 {user.username}"}
    return {"msg": "你好，游客"}

# 方式 3: 角色控制（需 User 模型有 role 字段）
@app.delete("/admin/users/{id}")
async def delete_user(id: str, user: User = Depends(require_role("admin"))):
    ...
```

### 5.5 `router.py` —— 路由层

#### API 端点

| 方法 | 路径 | Auth | 说明 |
|------|------|------|------|
| POST | `/auth/send-code` | 无 | 发送 6 位验证码到邮箱（60s 冷却，5min 有效） |
| POST | `/auth/login` | 无 | 验证码校验 + 新用户自动注册 + 签发双 Token |
| POST | `/auth/refresh` | 无 | 用 Refresh Token 换新的 Token 对（Token Rotation） |
| POST | `/auth/logout` | Bearer | 撤销 Refresh Token（可选单设备或全设备） |
| GET | `/auth/me` | Bearer | 获取当前用户信息 |

#### 登录流程（验证码模式）

```
POST /auth/login { "email": "user@qq.com", "code": "123456" }

① 校验验证码 (verify_and_consume_code)
   → 不匹配或已过期 → 401 "验证码错误或已过期"
   → 匹配          → 立即删除验证码（一次性消费），继续

② 查找或创建用户
   → users.find_one({"email": ...}) → 找到 → 使用已有用户
                                    → 未找到 → 自动创建新用户（验证码即注册）

③ 签发双 Token (_issue_tokens)
   → create_access_token(user_id)
   → create_refresh_token(user_id)
   → save_refresh_token(user_id, jti)  # 存 Redis

④ 返回 { access_token, refresh_token, token_type: "bearer", expires_in: 900 }
```

#### 刷新流程（Token Rotation）

```
POST /auth/refresh { "refresh_token": "..." }

① verify_token(refresh_token, "refresh") → 验证签名+过期+类型
② exists_refresh_token(user_id, jti)     → 不存在? → 撤销所有 token → 401 "可疑重用"
                                          → 存在?   → 继续
③ create_access_token + create_refresh_token → 新 Token 对
④ rotate_refresh_token(user_id, old_jti, new_jti) → 删旧建新
⑤ 返回新的 Token 对
```

---

## 六、安全设计决策

### 6.1 已实现的安全措施

| 措施 | 实现方式 | 防护的攻击 |
|------|---------|-----------|
| **双 Token 体系** | Access(15min) + Refresh(30day) | 减少 Access Token 泄露影响 |
| **密钥分离** | Access 和 Refresh 使用不同密钥 | 单密钥泄露不影响另一个 |
| **Token 类型校验** | payload.type 必须匹配 | Access/Refresh 互换攻击 |
| **签发者校验** | payload.iss 必须匹配 APP_NAME | 跨应用 Token 滥用 |
| **JTI 唯一标识** | 每个 Token 带 uuid4 | 精确撤销能力 |
| **Refresh Token Rotation** | 刷新时旧 token 立即作废 | 重放攻击 |
| **重放检测** | 旧 token 被重复使用时检测 | 自动撤销所有设备 |
| **SCAN 而非 KEYS** | 增量迭代删除 | Redis 阻塞攻击 |
| **自定义异常体系** | 精确的 HTTP 状态码 + X-Token-Error 头 | 前端可据此判断刷新/跳转登录 |
| **验证码一次性消费** | 校验后立即 DELETE | 验证码重用攻击 |
| **发送冷却期** | 60s 内禁止重复发码 | 邮件轰炸攻击 |
| **RESP2 强制** | Redis protocol=2 | 认证时序问题 |

### 6.2 后续可增强的安全措施

| 措施 | 说明 | 优先级 |
|------|------|--------|
| **httpOnly Cookie** | Refresh Token 改为 httpOnly + Secure + SameSite Cookie | 🟡 中 |
| **速率限制** | 登录/刷新/发码接口加限流（可用 Redis 实现） | 🟡 中 |
| **IP 绑定** | Refresh Token 与登录 IP 绑定，IP 变更需重新登录 | 🟡 中 |
| **设备指纹** | 记录 User-Agent 等，异常设备拒绝 | 🟢 低 |
| **Token Family** | 为 Refresh Token 建立家族链，更精确的重放检测 | 🟢 低 |
| **RS256 算法** | 微服务架构下使用非对称加密 | 🟢 低 |

---

## 七、环境变量配置

`.env` 中的 JWT 相关配置：

```ini
# 应用名称（用于 JWT iss 签发者校验）
APP_NAME=AGC鉴赏画廊

# Access Token 配置
ACCESS_TOKEN_ALGORITHM=HS256
ACCESS_TOKEN_SECRET_KEY=<your-secret-key>
ACCESS_TOKEN_EXPIRE_MINUTES=15

# Refresh Token 配置
REFRESH_TOKEN_ALGORITHM=HS256
REFRESH_TOKEN_SECRET_KEY=<your-secret-key>
REFRESH_TOKEN_EXPIRE_DAYS=30

# 验证码配置
VERIFICATION_CODE_TTL=300    # 验证码有效期（秒，默认 5 分钟）
COOLDOWN_TTL=60              # 发送冷却期（秒，默认 60 秒）

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=<your-password>

# MongoDB 配置
MONGODB_URL=mongodb://localhost:27017/?directConnection=true
```

---

## 八、如何测试

### 8.1 启动服务

```bash
# 确保 MongoDB 和 Redis 运行中
python main.py
```

### 8.2 Swagger 手动测试

1. 访问 `http://127.0.0.1:<PORT>/docs`
2. 调用 `POST /auth/send-code`，传入邮箱
3. 查收邮箱中的 6 位验证码
4. 调用 `POST /auth/login`，传入邮箱 + 验证码
5. 拿到 `access_token`，点击右上角 "Authorize"，粘贴 token
6. 调用 `GET /auth/me` 验证认证是否生效
7. 调用 `POST /auth/refresh` 测试 Token 刷新
8. 调用 `POST /auth/logout` 测试登出

---

## 九、在业务路由中使用认证

### 9.1 基础用法

```python
from fastapi import APIRouter, Depends
from data_models.database import User
from services.auth import get_current_user

router = APIRouter(prefix="/api", tags=["业务"])

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    """获取当前用户资料（需要登录）"""
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "username": current_user.username,
    }
```

### 9.2 可选认证

```python
from typing import Optional
from services.auth import get_optional_user

@router.get("/content")
async def list_content(
    current_user: Optional[User] = Depends(get_optional_user)
):
    """公开接口——但登录用户看到个性化内容"""
    if current_user:
        return {"msg": f"你好 {current_user.username}"}
    return {"msg": "你好，游客"}
```

### 9.3 在 main.py 注册新路由

```python
from your_module import your_router
app.include_router(your_router)
# 所有 auth 保护的接口自动生效
```

---

## 十、文件修改记录

| 文件 | 操作 | 关键变更 |
|------|------|---------|
| `services/auth/jwt.py` | 重写 | 自定义异常体系 + `decode_token` + `_now_utc` 统一时间 |
| `services/auth/session_service.py` | 新建 | Token Rotation + SCAN 撤销 + 重放检测 + 会话统计 |
| `services/auth/verification.py` | 新建 | 邮箱验证码生成/存储/校验/发送 + 冷却期控制 |
| `services/auth/dependencies.py` | 新建 | `get_current_user` + `get_optional_user` + `require_role` |
| `services/auth/router.py` | 新建 | `/auth/send-code` + `/auth/login` + `/auth/refresh` + `/auth/logout` + `/auth/me` |
| `services/auth/__init__.py` | 新建 | 统一导出全部公开接口 |
| `data_models/auth_model/schemas.py` | 新建 | 认证请求/响应 Pydantic 模型 |
| `services/database/mongodb.py` | 重写 | 使用 pymongo AsyncMongoClient 替代 motor |
| `services/database/redis.py` | 新建 | Redis 异步客户端 (RESP2) |
| `main.py` | 修改 | 注册 auth_router + 全局异常处理器 + MongoDB lifespan |
