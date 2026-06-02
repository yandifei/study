## MongoDB 速通文档（Python 全栈视角）

### 1. 还需要画 E-R 图吗？
**答：不需要传统 E-R 图，但需要画“文档关系图”。**
- 传统 E-R 图为关系型数据库的**表结构**和**外键**设计。
- MongoDB 里你要表达的是：
  - **嵌入（Embedding）**：子数据直接放在一个文档内（一对少，经常一起读）。
  - **引用（Reference）**：只存另一个文档的 `_id`，类似逻辑外键（多对多、独立生命周期、数据过大时）。
- 推荐做法：画 JSON 结构草图，标注哪些是嵌入对象，哪些是引用 ID；工具可使用 Moon Modeler、Hackolade 等。
- 核心原则：**按读写模式设计**——一起读的字段就放一个文档里，避免过多 `$lookup`。

---

### 2. 用户数据存储有什么要求？
用户数据敏感，存储时必须关注：
- **密码**：绝对用 `bcrypt` / `argon2` 等强哈希加盐，不存明文。
- **敏感字段**：身份证、银行卡等用应用层加密（AES），密钥与数据库分离（如 AWS KMS）。
- **唯一性**：邮箱、手机号等建立唯一索引 `db.users.createIndex({email:1},{unique:true})`。
- **Schema 验证**：建议开启 JSON Schema 校验，强制字段类型和必填项。
- **文档大小控制**：不要把日志、订单全部嵌入用户文档，单文档上限 16MB，且过大会拖慢性能。
- **合规与软删除**：满足 GDPR，支持软删除和匿名化，可设 TTL 索引自动清理过期数据。
- **常用查询字段加索引**：注册时间、状态等按需建索引。

---

### 3. 需要构建 ODM 模型吗？
**非常建议，尤其对 Python 全栈。** ODM 让你像操作 ORM 一样操作 MongoDB，保留类型安全。
- **同步场景**：MongoEngine（最像 Django ORM）。
- **异步场景（推荐）**：Beanie（Pydantic v2 + Motor，完美配合 FastAPI），或 ODMantic。
- **轻量方案**：Pydantic + Motor 薄封装，自己控制。
- **选择建议**：新项目异步 FastAPI 用 Beanie；老 Django/Flask 同步用 MongoEngine。

---

### 4. ODM 难不难？我会 OOP 能上手吗？
**非常容易，ODM 本质就是 OOP。**
- 定义文档就是定义一个 Python 类，属性即字段。
- 操作实例就是操作数据库文档：`user.insert()`、`user.save()`。
- 没有复杂的 JOIN，关联要么嵌入（子文档类），要么手动查 ID。
- 异步只多了 `await`，其他调用习惯不变。
- 学习路线：定义类 → 连接并插入 → 查询与更新 → 嵌入和引用，30 分钟足够入门。

---

### 5. MongoDB 基础入门（从零到 CRUD）

#### 核心概念转换
| SQL 概念      | MongoDB 概念        | 说明                      |
|---------------|---------------------|---------------------------|
| 数据库        | Database            | 相同                      |
| 表            | Collection（集合）   | 存储文档                  |
| 行            | Document（文档）     | JSON 对象                 |
| 列            | Field（字段）        | 键值对                    |
| 主键          | `_id`               | 自动 ObjectId             |
| Join          | 嵌入 或 `$lookup`   | 无真正外键                |

#### Shell 快速 CRUD
```javascript
use myapp
db.users.insertOne({ email: "a@b.com", name: "Alice", age: 30 })
db.users.find({ age: { $gte: 30 } })
db.users.updateOne({ email: "a@b.com" }, { $set: { age: 31 } })
db.users.deleteOne({ email: "a@b.com" })
```

#### Python 同步（pymongo）
```python
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client.myapp
users = db.users
users.insert_one({"email": "a@b.com", "name": "Alice"})
users.find_one({"email": "a@b.com"})
users.update_one({"email": "a@b.com"}, {"$set": {"age": 31}})
```

#### Python 异步（motor）
```python
from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.myapp
await db.users.insert_one({"email": "bob@test.com", "name": "Bob"})
```

#### 使用 Beanie ODM（推荐）
```python
from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import EmailStr

class User(Document):
    email: EmailStr
    name: str
    age: int
    class Settings:
        name = "users"

client = AsyncIOMotorClient("mongodb://localhost:27017")
await init_beanie(database=client.myapp, document_models=[User])

user = User(email="a@b.com", name="Alice", age=30)
await user.insert()
alice = await User.find_one(User.email == "a@b.com")
```

---

### 6. 索引（这次彻底看懂）
**索引 = 书的目录**，没有目录只能逐页翻（全集合扫描 `COLLSCAN`），有索引直达目标（`IXSCAN`）。

- 索引附着在**集合**上，查看索引：
  - Shell: `db.users.getIndexes()`
  - Python: `users.list_indexes()`
- 创建索引：
  ```javascript
  db.users.createIndex({ email: 1 })                // 升序索引
  db.users.createIndex({ email: 1 }, { unique: true }) // 唯一索引
  db.users.createIndex({ name: 1, age: -1 })        // 复合索引
  ```
- 用 `explain()` 看有无索引的区别：
  `db.users.find({ name: "user5000" }).explain("executionStats")`
  若 `stage` 为 `COLLSCAN` 则缺索引；建索引后变为 `IXSCAN`。
- 应用启动时确保索引存在（幂等操作，重复执行不报错）。
- Beanie 中直接用 `Indexed` 字段自动创建：
  `email: Indexed(str, unique=True)`

#### 数据建模原则
- **嵌入**：数据总是一起读、一起写、不独立增长（如用户地址数组）。
- **引用**：各自独立生命周期，或数量过大（如用户与订单），存 `_id`，必要时用 `$lookup` 聚合。

#### 聚合框架简介
流水线式处理数据：
```javascript
db.users.aggregate([
  { $group: { _id: "$age", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```

---

### 7. 最终解答：能像 ORM 那样换数据库吗？
- **ODM 编码体验确实像 ORM**，你可以写对象映射代码。
- **但换数据库类型（如从 MongoDB 到 PostgreSQL）绝对不是只换 ODM 就行的**，因为数据建模完全不同（嵌入 vs 关联），迁移需要重新设计模型。
- 如果未来可能切换，建议用 **仓库模式（Repository Pattern）** 隔离持久化细节，业务层只依赖接口，底层可替换不同实现。

---

**这份文档可以作为你 MongoDB 开发的速查手册，配合实际项目敲一遍，就能快速上手。**