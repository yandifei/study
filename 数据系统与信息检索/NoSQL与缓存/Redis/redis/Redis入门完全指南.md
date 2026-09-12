# Redis 入门完全指南

> 📅 整理日期：2026-06-07
> 📖 内容来源：Redis 官方文档 + 完整对话学习记录
> 🎯 目标：从零到企业级，覆盖所有核心概念和数据类型的完整细节

---

## 目录

> 📖 按学习路径分为七大模块，建议按顺序阅读。

### 第一部分：基础认知

- [第 1 章：Redis 是什么？](#第-1-章redis-是什么)
  - [1.1 一句话定义](#11-一句话定义)
  - [1.2 核心特点](#12-核心特点)
  - [1.3 数据类型全景图](#13-数据类型全景图)
  - [1.4 Key 命名规范 — user:100 到底是什么？](#14-key-命名规范--user100-到底是什么)
  - [1.5 Redis 的多数据库模型 — SELECT 与 databases 参数](#15-redis-的多数据库模型--select-与-databases-参数)
  - [1.6 为什么默认 16 个数据库？— 一段历史债](#16-为什么默认-16-个数据库--一段历史债)
  - [1.7 多数据库的致命缺陷 — 弱隔离、无访问控制、集群不支持](#17-多数据库的致命缺陷--弱隔离无访问控制集群不支持)
  - [1.8 生产环境最佳实践 — databases 设为 1](#18-生产环境最佳实践--databases-设为-1)
- [第 23 章：快速上手 — 四种使用场景](#第-23-章快速上手--四种使用场景)
- [第 24 章：常见问题 FAQ（官方）](#第-24-章常见问题-faq官方)

### 第二部分：核心数据类型

- [第 2 章：String（字符串）](#第-2-章string字符串) — 最底层、最万能的瑞士军刀
- [第 3 章：List（列表）](#第-3-章list列表) — 双向链表，做队列/栈
- [第 4 章：Set（集合）](#第-4-章set集合) — 去重、抽奖、好友关系
- [第 5 章：Sorted Set（有序集合）](#第-5-章sorted-set有序集合) — 排行榜、延迟队列
- [第 6 章：Hash（哈希）](#第-6-章hash哈希) — 一行数据库记录
- [第 9 章：Bitmap（位图）](#第-9-章bitmap位图) — 签到、状态标记
- [第 10 章：Bitfield（位域）](#第-10-章bitfield位域) — 紧凑存整数
- [第 8 章：Geospatial（地理空间）](#第-8-章geospatial地理空间) — 附近的人
- [第 7 章：Stream（消息队列）](#第-7-章stream消息队列) — 持久化消息队列
- [第 16 章：Pub/Sub（发布订阅）](#第-16-章pubsub发布订阅) — 实时广播

### 第三部分：扩展模块类型

- [第 12 章：JSON](#第-12-章json) — 文档操作，JSONPath 精准定位
- [第 13 章：Time Series（时序数据）](#第-13-章time-series时序数据) — 监控指标、IoT
- [第 14 章：Vector Sets（向量集）](#第-14-章vector-sets向量集) — AI 语义搜索、RAG
- [第 15 章：Arrays](#第-15-章arrays) — JSON 数组操作补充

### 第四部分：概率数据类型

- [第 11 章：概率数据类型 — 小内存做大统计](#第-11-章概率数据类型)
  - [11.1 HyperLogLog — 基数统计](#111-hyperloglog--基数统计)
  - [11.2 Bloom Filter — 布隆过滤器](#112-bloom-filter--布隆过滤器)
  - [11.3 Cuckoo Filter — 布谷鸟过滤器](#113-cuckoo-filter--布谷鸟过滤器)
  - [11.4 Count-Min Sketch — 频率估算](#114-count-min-sketch--频率估算)
  - [11.5 Top-K — 热门排行榜](#115-top-k--热门排行榜)
  - [11.6 t-digest — 分位数估算](#116-t-digest--分位数估算)

### 第五部分：事务与持久化

- [第 17 章：事务](#第-17-章事务) — MULTI/EXEC、WATCH 乐观锁
- [第 18 章：持久化](#第-18-章持久化) — RDB、AOF、混合模式

### 第六部分：高可用与扩展

- [第 19 章：主从复制](#第-19-章主从复制) — 读写分离、数据冗余
- [第 20 章：Sentinel（哨兵模式）](#第-20-章sentinel哨兵模式) — 自动故障转移
- [第 21 章：Redis Cluster（集群模式）](#第-21-章redis-cluster集群模式) — 分片扩展
- [第 22 章：企业架构演进](#第-22-章企业架构演进) — 从单机到全球化

### 第七部分：附录

- [附录 A：完整命令速查](#附录-a完整命令速查)
- [附录 B：数据类型选型决策树](#附录-b数据类型选型决策树)
- [附录 C：常用工具](#附录-c常用工具)

---

<!-- ═══════════════════════════════════════════════════════ -->
<!--  第一部分：基础认知                                          -->
<!-- ═══════════════════════════════════════════════════════ -->

---

## 第 1 章：Redis 是什么？

### 1.1 一句话定义

**Redis（REmote DIctionary Server）是一个基于内存的键值存储数据库。** 所有数据存在内存里，所以极快；支持持久化到磁盘，所以重启不丢；支持主从复制和哨兵，所以高可用。

### 1.2 核心特点

- **内存存储**：所有数据在内存，读写 10 万+ QPS
- **丰富数据类型**：不只是 key-value，String/Hash/List/Set/Sorted Set/Stream/JSON/向量等
- **持久化**：RDB 快照 + AOF 日志，数据不丢
- **高可用**：主从复制 + Sentinel + Cluster
- **原子操作**：单个命令天然原子，Lua 脚本也原子
- **单线程模型**：Redis 6.0 之前网络 IO 和命令执行都是单线程；6.0+ 网络 IO 多线程，命令执行仍是单线程

### 1.3 数据类型全景图

```
Redis 的世界 = 一个巨大的 key-value 字典，key 是 String，value 可以是各种类型

┌──────────────────────────────────────────────────────────────┐
│              传统/核心类型（Redis 核心自带）                     │
│  String   — 最底层、最万能，所有其他类型的基石                    │
│  List     — 双向链表，做队列/栈                                 │
│  Set      — 无序不重复集合，做去重/关系运算                      │
│  SortedSet— 带分数的集合，做排行榜                              │
│  Hash     — 键值对集合，存一行记录                              │
│  Stream   — 持久化消息队列（5.0+）                             │
│  Geo      — 地理位置（3.2+）                                  │
│  Bitmap   — 位图操作（String 的子操作）                         │
│  Bitfield — 位域操作（String 的子操作，3.2+）                   │
├──────────────────────────────────────────────────────────────┤
│              模块扩展类型（Redis Stack / 企业版）                │
│  HyperLogLog  — 基数估计（2.8.9+，核心自带）                    │
│  Bloom/Cuckoo — 成员检测（RedisBloom 模块）                     │
│  CountMin/TopK/t-digest — 频率/排名/分位数（RedisBloom）         │
│  JSON         — JSON 文档（RedisJSON 模块）                     │
│  Time Series  — 时序数据（RedisTimeSeries 模块）                 │
│  Vector Sets  — 向量搜索（Redis 8.0+ / Redis Stack）           │
│  Arrays       — JSON 数组操作补充                              │
└──────────────────────────────────────────────────────────────┘
```

---

### 1.4 Key 命名规范 — `user:100` 到底是什么？

#### 问题拆解 1：`user:100` 是什么？是数据库操作吗？

**`user:100` 不是一个数据库操作，它就是一个 key 的名字。**
Redis 的 key 就是普通字符串，你起什么名字都可以——`x`、`zhangsan`、`user100`、`user:100` 都是合法的 key。

很多人第一次看到 `user:10086:name` 这种写法时会产生误解，以为冒号有特殊含义。**冒号在 Redis 里没有任何语法意义**，它只是 key 名字中的一个普通字符，就像下划线 `_` 一样。

Redis 的 key 名字是二进制安全的，可以包含任何字符（包括空格和换行，但强烈不建议）。

#### 问题拆解 2：这个命名风格叫什么？有什么规范？

**社区约定俗成叫「冒号分隔命名空间」（Colon-delimited namespacing），没有官方名称。**

它不是官方规范，而是 Redis 社区 15 年来自然形成的**约定**，类似 Python 的 `snake_case` 和 JavaScript 的 `camelCase`。

```
经典层级结构：
  user:10086:name
  user:10086:email
  user:10086:orders
  ↑     ↑      ↑
 对象   ID    字段

article:1001:views
article:1001:likes
article:1001:comments
```

**为什么大家不约而同选择冒号？**

```
1. 不是 Redis 关键字
   冒号在 Redis 命令语法中没有特殊含义，不会冲突

2. 图形界面友好
   RedisInsight、Redis Commander 等工具自动按冒号折叠 key 成树形：
   user
   ├── 10086
   │   ├── name
   │   ├── email
   │   └── orders
   └── 10087
       ├── name
       └── email

3. 方便批量操作
   KEYS user:10086:*     # 取 user:10086 的所有字段
   KEYS article:*:views  # 取所有文章的 views
   SCAN ... MATCH user:*:email

4. 可读性最好
   user:10086:name  vs  user_10086_name  vs  user.10086.name
   冒号在视觉上最适合做层级分隔
```

#### 问题拆解 3：还有什么其他命名规范？

```
1. 冒号分隔（最常见，推荐！）
   user:10086:profile
   order:20260608:status
   cache:article:hot_list

2. 点号分隔（类似域名反转，Java 项目常见）
   com.example.app.user.10086
   cache.config.timeout

3. 斜杠分隔（像 URL 路径，一些 REST 风格项目用）
   /user/10086/profile
   /order/20260608/status

4. 下划线分隔（最简单，但层级不清晰）
   user_10086_profile
   order_20260608_status

5. 井号分隔（表示临时/一次性 key）
   temp#session#abc123
   lock#order#10086

6. 带版本号（做缓存时常见）
   user:10086:v2
   config:app:v3
```

**企业里几乎全部用冒号分隔（第 1 种）。** 因为它被所有 Redis 客户端工具识别和折叠，也最符合 Redis 官方文档的习惯。

#### 命名设计的实战原则

```
一个好的 key 命名：
  ✅ 一眼看出数据归属：user:10086:email
  ✅ 可以模式匹配：article:*:views
  ✅ 层级清晰：business:object:id:field
  ✅ 不会太长：控制在合理长度

一个不好的 key 命名：
  ❌ u:10086:e       — 太简略，看不懂
  ❌ user_data_for_id_10086_with_field_email — 太长
  ❌ user:10086:邮箱  — 中英文混用，部分工具可能显示问题
  ❌ user10086email  — 没有层级，KEYS 匹配困难
```

---

### 1.5 Redis 的多数据库模型 — SELECT 与 databases 参数

#### 问题拆解 4：Redis 默认数据库是 0？可以切换吗？

**Redis 实例启动后，内部有多个逻辑数据库，编号从 0 开始。** 客户端连接后默认使用 0 号数据库。

```
Redis 实例
├── 数据库 0（默认）→ 存放 key1, key2, key3...
├── 数据库 1         → 存放 key4, key5, key6...
├── 数据库 2
├── ...
└── 数据库 15        → 最多 16 个（默认）

不同数据库的 key 空间完全隔开
同一个 key 名字在不同数据库里互不影响
```

```bash
# SELECT 命令切换数据库
127.0.0.1:6379> SET mykey "hello"     # 在 0 号库设置
127.0.0.1:6379> SELECT 1             # 切换到 1 号库
127.0.0.1:6379[1]> GET mykey         # → (nil)  ← 0 号库的数据看不到！

127.0.0.1:6379[1]> SET mykey "world" # 在 1 号库设置
127.0.0.1:6379[1]> SELECT 0          # 切回 0 号库
127.0.0.1:6379> GET mykey           # → "hello"

# 提示符的含义：
# 127.0.0.1:6379>      ← 0 号库（不显示编号）
# 127.0.0.1:6379[1]>   ← 1 号库
# 127.0.0.1:6379[15]>  ← 15 号库

# SELECT 范围外报错
SELECT 15    # → OK
SELECT 16    # → (error) ERR DB index is out of range
```

#### 问题拆解 5：可以增加/减少数据库数量吗？

```
运行时（动态修改）：❌ 不能！
redis-cli CONFIG SET databases 1
→ (error) ERR Unsupported CONFIG parameter: databases

原因：数据库数量决定了 Redis 启动时内部数据结构的初始化方式，
      所有 key 空间的哈希表在启动时就按 databases 的值分配好了。
      运行时改等于要把所有数据库重排 → 无法实现 → 不允许动态改

配置文件（静态设置）：✅ 可以！
redis.conf 中的 databases 参数
改完后重启 Redis 生效
```

#### databases 参数详解

```bash
# redis.conf 中的配置
databases 16    # 默认值：16 个数据库（编号 0~15）
databases 1     # 只有 1 个数据库（编号 0）
databases 32    # 32 个数据库（编号 0~31）
databases 0     # ❌ 不允许，最小是 1

# 查询当前配置
CONFIG GET databases
# → 1) "databases"
#    2) "16"
```

---

### 1.6 为什么默认 16 个数据库？— 一段历史债

#### 问题拆解 6：为什么要有这么多数据库？MySQL 不也是先建库再建表吗？

**Redis 的多数据库和 MySQL 的多数据库是两回事，只是碰巧叫了同一个名字。**

```
═══════════════════════════════════════════════════════════════
                      两种「数据库」的对比
═══════════════════════════════════════════════════════════════

MySQL 的 database（真正的逻辑隔离）：
────────────────────────────────────
  MySQL 实例
  ├── ecommerce（电商数据库）
  │   ├── 表: users（字段: id, name, email...）
  │   ├── 表: orders（字段: id, user_id, amount...）
  │   └── 表: products
  ├── blog（博客数据库）
  │   ├── 表: articles
  │   └── 表: comments
  └── analytics（分析数据库）
      └── 表: page_views

  database 之间有：
    ✅ 独立的用户权限（GRANT SELECT ON ecommerce.* TO 'user'）
    ✅ 独立的字符集（utf8mb4 vs latin1）
    ✅ 独立的存储引擎（InnoDB vs MyISAM）
    ✅ 独立的备份恢复
    ✅ 不同 database 可以同名表

Redis 的 database（只是编号前缀）：
──────────────────────────────────
  Redis 实例 → 一个巨大的 key 字典
    │
    内部用数据库编号（0~15）加在 key 前面做虚拟隔离
    所有 key 存在同一个哈希表里，没有物理隔离

  database 之间：
    ❌ 没有独立权限（6.0 ACL 之前）
    ❌ 没有独立的配置
    ❌ 没有独立的资源限制
    ❌ FLUSHALL 一键清空全部
    ✅ 只是 key 的名字前缀不同（内部实现）
```

#### 问题拆解 7：为什么偏偏是 16 个？

```
时间线：

2009 年，Redis 1.0：
  - 没有 SELECT 命令，连多数据库这个概念都没有
  - Redis 定位是单机缓存，一台机器可能跑多个不同应用
  - 但那时候内存贵、机器少，多个应用要共享一台 Redis

2010 年，Redis 2.0：
  - 加入了 SELECT 命令，默认 16 个数据库
  - 初衷很简单：让不同应用各用各的数据库编号
    → 应用 A 用 0 号库
    → 应用 B 用 1 号库
    → ...
    → 共 16 个应用共享一个 Redis 进程
  - 为什么是 16 不是 10 或 32？
    → 作者 antirez 拍脑袋定的
    → 16 = 2^4，二进制友好的数字
    → 再多就没必要了，一台机器也跑不了那么多应用

2015 年，Redis 3.0（Cluster 发布）：
  - Cluster 模式禁用 SELECT（只支持 db0）
  - 多数据库设计开始出现裂痕

2021 年，Redis 6.0（ACL 发布）：
  - 才第一次有了真正的用户权限隔离
  - 可以在 ACL 里限制用户只能访问哪些数据库
  - 但这个功能晚了 11 年

2024 年，Redis 7.X：
  - 多数据库仍然存在，但官方文档明确说「不推荐在生产中使用」
  - 推荐的做法：开多个 Redis 实例，而不是依赖多数据库
```

---

### 1.7 多数据库的致命缺陷 — 弱隔离、无访问控制、集群不支持

#### 缺陷 1：弱隔离（甚至没有隔离）

```bash
# FLUSHDB — 只清空当前数据库
SELECT 0
FLUSHDB                    # 清空 0 号库

# FLUSHALL — 清空全部 16 个数据库！
FLUSHALL                   # 0~15 全部清空！

# 如果你：
#   应用 A 用 0 号库存订单数据
#   应用 B 用 1 号库存缓存
#   应用 A 的开发者写了个 FLUSHALL → B 的数据也没了！
# MySQL 里一个库的 DROP DATABASE 不可能影响另一个
# Redis 里 FLUSHALL 无视数据库边界
```

#### 缺陷 2：没有访问控制（Redis 6.0 ACL 之前）

```
Redis 1.0 ~ 5.0（2009 ~ 2020，11 年）：
  只要是连上来的客户端：
    SELECT 0 → 能看 0 号库
    SELECT 1 → 能看 1 号库
    → 没有机制阻止应用 A 切到应用 B 的数据库

  对比 MySQL：
    GRANT SELECT ON ecommerce.* TO 'app_a';
    GRANT SELECT ON blog.* TO 'app_b';
    → app_a 只能看 ecommerce，绝对碰不到 blog

Redis 6.0 ACL 之后（2021+）：
  可以用 ACL 限制用户只能访问指定数据库
  ACL SETUSER app_a on >password ~* &* -@all +@read +@write
  → 但这只限制用户，不是数据库级别的真正隔离
```

#### 缺陷 3：Redis Cluster 完全不支持多数据库

```bash
# 这是最致命的一刀
# Redis Cluster 模式下：
SELECT 0    # → OK
SELECT 1    # → (error) ERR SELECT is not allowed in cluster mode

# 集群模式强制只能用 db0！
# 如果你用 Cluster → 那 15 个数据库的存在直接变成一个笑话
# 因为根本切不过去

# 而 Cluster 是 Redis 官方推荐的扩展方案
# → 多数据库在生产中越来越没有意义
```

#### 缺陷 4：性能影响（虽然小，但存在）

```
所有 16 个数据库的 key 存在同一个哈希表里
数据库编号只是内部 key 前缀

带来的开销：
  - 更多的 key 在同一个哈希表 → 哈希冲突概率略微增加
  - FLUSHDB 要遍历整个哈希表找出当前数据库的 key → O(N)，大 key 时可能慢
  - INFO keyspace 要逐个数据库报告 key 数量 → 16 次遍历
  - 每个数据库都维护独立的 expires 字典 → 占用额外内存

单数据库时这些都不成问题
```

#### 缺陷 5：客户端/云服务支持差

```
- redis-py 等客户端默认连 db0，要手动 SELECT 才能切
- 很多 ORM/缓存框架默认假设你在 db0
- AWS ElastiCache、Redis Cloud、阿里云 Redis → 绝大多数只开放 db0
- 用了非 db0 的系统迁移到云上可能需要改代码
```

---

### 1.8 生产环境最佳实践 — databases 设为 1

#### 问题拆解 8：生产环境该怎么做？

**你的判断完全正确：「另外 15 个数据库用不上、性能略降、弱隔离、无访问控制、集群不支持，留着干嘛？」生产环境的标准配置就是只留 1 个数据库。**

```bash
# 1. 修改 redis.conf
databases 1

# 2. 重启 Redis
# Linux:
sudo systemctl restart redis
# 或用 redis-cli SHUTDOWN 后重新启动

# 3. 验证
redis-cli CONFIG GET databases
# → "databases", "1"

redis-cli SELECT 0
# → OK

redis-cli SELECT 1
# → (error) ERR DB index is out of range
```

#### 问题拆解 9：运行时能动态改 databases 吗？

```
❌ 不能！
CONFIG SET databases 1
→ (error) ERR Unsupported CONFIG parameter: databases

这是 Redis 少数几个不能动态改的参数之一。

原因：
  Redis 启动时：
    1. 读 databases 参数（例如 16）
    2. 分配 16 个 redisDb 结构体
    3. 每个结构体里有独立的 dict（存 key）、expires（存过期时间）
    4. 所有客户端连接默认指向 redisDb[0]

  动态改 databases = 要改变结构体数组的大小
  = 所有现有的 key 要重新分配
  = 所有现有的客户端连接要重新映射
  → 代价太高，不值得实现 → 只能在启动时决定
```

#### 问题拆解 10：那 15 个数据库还有什么存在价值？

```
在现代 Redis 使用中，多数据库只剩几个边缘用途：

1. 开发/测试环境
   开发者的本机 Redis，不同项目用不同 db，不用改端口
   → 纯方便，不是最佳实践

2. 单元测试
   每个测试用例切到独立 db → 跑完 FLUSHDB → 干净
   比每次都起新 Redis 实例快得多

3. 历史遗留系统
   2012 年写的代码就是这么写的，没人敢动

4. 极少数单机多租户场景
   但多实例（不同端口）在任何方面都更好

总结：
  多数据库是一个过时的设计了
  在现代 Redis 体系里，真正有用的做法是：
  ✅ 生产环境 → databases 1 + 多实例部署
  ✅ 隔离 → 不同端口/不同机器/不同 Docker 容器
  ✅ 集群 → Cluster 模式（天然只能用 db0）
```

---

### 1.9 本章核心问题速答

| 问题 | 答案 |
|------|------|
| `user:100` 是什么？ | key 的名字，冒号只是命名风格，没有特殊语法含义 |
| 命名规范叫什么？ | 冒号分隔命名空间（社区约定，非官方规范） |
| 默认数据库是 0？ | 是，16 个数据库（0~15），默认连 0 |
| 能切换吗？ | `SELECT 0` ~ `SELECT 15` |
| 能增加/减少吗？ | 运行时不能，只能改 `redis.conf` → `databases` → 重启 |
| 为什么默认 16 个？ | 2010 年设计：让多个应用共享一个 Redis 进程 |
| MySQL 为什么先建库？ | MySQL 的 database 是真正的逻辑隔离（权限、字符集、存储引擎） |
| Redis 和 MySQL 的 database 一样吗？ | 完全不同！Redis 只是编号前缀，没有真正隔离 |
| Cluster 支持多数据库吗？ | ❌ 只支持 db0 |
| 多数据库有什么缺陷？ | 弱隔离、无访问控制（6.0 前）、FLUSHALL 一键全清、Cluster 不支持 |
| 生产环境数据库数量？ | **databases 1**，只用 db0 |
| 隔离怎么做？ | 多 Redis 实例（不同端口/容器），不靠多数据库 |
| 能动态改 databases？ | ❌ 不能，结构启动时固定，只能重启生效 |

---

<!-- ═══════════════════════════════════════════════════════ -->
<!--  第二部分：核心数据类型                                    -->
<!-- ═══════════════════════════════════════════════════════ -->

---

## 第 2 章：String（字符串）

### 2.1 是什么？

String 是 Redis 最底层、最基础、最万能的数据类型。你之前学的 Bitmap 和 Bitfield 本质上都是操作 String。它可以存文本、数字、JSON、序列化对象、二进制数据（图片），最大 512MB。

三个关键特性：

```
1. 二进制安全 — 不会因 \0 截断，底层用 SDS 实现不是 C 字符串
2. 最大 512MB — 但生产建议 < 10KB，大 value 拖慢网络和主从复制
3. 数值运算 — 内容是数字时可以 INCR/DECR/INCRBY/INCRBYFLOAT
```

### 2.2 底层编码（重要！）

Redis 对同一个 String 内部可能用三种不同编码存，对性能和内存影响巨大：

```
OBJECT ENCODING key  → 返回三种之一：

1. int（整数编码）
   - 内容可转成 long 整数 → 直接存在 RedisObject 的 ptr 字段
   - 不需要额外内存分配，内存最省
   - INCR/DECR 操作 → 直接改指针值，真正的 O(1)

2. embstr（嵌入式字符串）
   - ≤ 44 字节的短字符串
   - RedisObject + SDS 连续分配，一次 malloc 搞定
   - 读写最快，缓存友好

3. raw（原始 SDS）
   - > 44 字节的长字符串
   - RedisObject 和 SDS 分开分配
   - APPEND 操作时 embstr 会转成 raw

查看示例：
SET small "hello"                   → OBJECT ENCODING small → "embstr"
SET big "hello world this is ..."   → OBJECT ENCODING big → "raw"
SET counter 10086                   → OBJECT ENCODING counter → "int"
```

### 2.3 增

```bash
# ═══ 基本 SET ═══
SET key value
SET user:10086:name "张三"

# ═══ SET 的可选参数（非常重要！）═══
SET key value EX 10              # 10 秒后过期（替代 SETEX）
SET key value PX 5000            # 5000 毫秒后过期（替代 PSETEX）
SET key value EXAT 1717800000    # 到 Unix 时间戳时过期
SET key value NX                 # 仅当 key 不存在时才 set（分布式锁核心！）
SET key value XX                 # 仅当 key 已存在时才 set
SET key value KEEPTTL            # 保畝原有的 TTL（6.0+）
SET key value GET                # 返回旧值（6.2+，替代 GETSET）

# ═══ 分布式锁标准写法 ═══
SET lock:order:1001 "req-uuid-xxx" EX 30 NX
# → OK      ← 获取锁成功
# → (nil)   ← 锁被别人持有

# ═══ SETNX — 不存在才设（可被 SET NX 替代）═══
SETNX key value
# → 1 = 设成功（key 之前不存在）
# → 0 = 没设（key 已存在）

# ═══ SETEX — 设值 + 设过期（可被 SET EX 替代）═══
SETEX key seconds value
SETEX session:abc123 3600 "user:10086"

# ═══ PSETEX — 设值 + 毫秒级过期 ═══
PSETEX key milliseconds value
PSETEX captcha:user:10086 60000 "A3xQ9"  # 验证码 60 秒后过期

# ═══ MSET — 批量设值（原子的！）═══
MSET key1 value1 key2 value2 key3 value3 ...
MSET user:10086:name "张三" user:10086:age "28" user:10086:city "北京"
# 一次性设多个，减少网络 RTT，整个 MSET 是原子操作

# ═══ MSETNX — 批量设值（全部 key 都不存在才成功）═══
MSETNX key1 value1 key2 value2 ...
# → 1 = 全部设成功（所有 key 之前都不存在）
# → 0 = 全部没设（至少有一个 key 已存在）
# 原子操作：要么全成功，要么全失败

# ═══ APPEND — 追加内容到字符串末尾 ═══
SET desc "Hello"
APPEND desc " World"           # → (integer) 11（返回追加后总长度）
APPEND desc "!"                 # → (integer) 12
GET desc                        # → "Hello World!"
# 注意：APPEND 可能触发 embstr → raw 编码转换

# ═══ 初始化计数器 ═══
SET article:1001:pv 0           # 访问量初始化为 0
```

### 2.4 删

```bash
# ═══ DEL — 同步删除（阻塞）═══
DEL key [key ...]
DEL user:10086:name
DEL user:10086:name user:10086:age user:10086:city
# → (integer) 3  ← 成功删了 3 个
# 注意：如果删大 key（几 MB+），DEL 会阻塞 Redis → 应该用 UNLINK

# ═══ UNLINK — 异步删除（非阻塞，4.0+）═══
UNLINK key [key ...]
UNLINK big_cache_data           # 标记删除，后台线程慢慢回收内存

# ═══ EXPIRE/PEXPIRE/EXPIREAT — 设过期（到期自动删）═══
EXPIRE key 3600                 # 3600 秒后过期
PEXPIRE key 60000               # 60000 毫秒后过期
EXPIREAT key 1717800000         # 到 Unix 时间戳时过期

# ═══ PERSIST — 取消过期 ═══
PERSIST key                     # 移除过期时间，变成永久 key

# ═══ 续期行为说明 ═══
# EXPIRE 是「覆盖」不是「累加」！
# 设 EXPIRE key 10，到第 5 秒时再 EXPIRE key 10 → 回到 10 秒重新计时，不是变成 15 秒
# 如果想要累加：current_ttl = redis.ttl(key); redis.expire(key, current_ttl + 10)
```

### 2.5 改

```bash
# ═══ SET XX — 仅当 key 存在才更新 ═══
SET key new_value XX

# ═══ GETSET — 返回旧值 + 设新值（6.2+ 用 SET key value GET）═══
GETSET cron:last_run "2026-06-07 10:05:00"
# → "2026-06-07 10:00:00"  ← 返回旧值
# 6.2+ 推荐写法：
SET cron:last_run "2026-06-07 10:05:00" GET

# ═══ SETRANGE — 覆盖字符串的某个部分 ═══
SET greeting "Hello World"
SETRANGE greeting 6 "Redis"     # 从第 6 个字符开始覆盖
GET greeting                    # → "Hello Redis"

# ═══ RENAME/RENAMENX — 重命名 key ═══
RENAME old_key new_key          # 重命名（覆盖 new_key）
RENAMENX old_key new_key        # 仅当 new_key 不存在才重命名

# ═══ 数值增减（这些都是原子的！）═══
# 整数
INCR key                        # +1 → 返回新值
DECR key                        # -1 → 返回新值
INCRBY key 10                   # +10
DECRBY key 5                    # -5

# 浮点数
INCRBYFLOAT key 1.5             # +1.5
INCRBYFLOAT key -0.5            # -0.5

# 实战：
INCR article:1001:pv            # 文章阅读量 +1
INCRBY user:10086:coins -100    # 扣 100 金币（原子！）
INCRBYFLOAT account:10086:score 0.5
```

### 2.6 查

```bash
# ═══ GET — 取单个值 ═══
GET user:10086:name             # → "张三"
GET nonexist_key                # → (nil)

# ═══ MGET — 批量取值（减少 RTT）═══
MGET user:10086:name user:10086:age user:10086:city
# → 1) "张三"  2) "28"  3) "北京"  4) (nil) ← 不存在的返回 nil
# 注意：MGET 不是原子的"读取"，但每个 GET 本身是原子的

# ═══ GETRANGE — 取子串 ═══
SET long_text "Hello Redis World"
GETRANGE long_text 6 10         # → "Redis"
GETRANGE long_text 0 -1         # → 全部（等同于 GET）
GETRANGE long_text -5 -1        # → "World"

# ═══ STRLEN — 取字符串长度 ═══
STRLEN user:10086:name          # 中文字在 UTF-8 下 3 字节/字
# "张三" → STRLEN → 6（两个中文字 = 2 × 3 字节）

# ═══ GETEX — 取值 + 设过期（6.2+）═══
GETEX key EX 3600               # 取值同时设 3600 秒过期
GETEX key PERSIST               # 取值同时移除过期
GETEX session:abc123 EX 1800    # 取 session 且自动续期 30 分钟
# 「延期的同时拿值」，一个命令搞定，减少了 RTT

# ═══ GETDEL — 取值 + 删除（6.2+）═══
GETDEL temp_token
# → 返回旧值，同时删了 key。类似原子 LPOP——取出即消费
# 场景：一次性 Token、验证码只能验证一次
```

### 2.7 实战场景

#### 场景一：分布式锁

```python
import redis
import uuid

r = redis.Redis(decode_responses=True)

def acquire_lock(lock_name, expire=30):
    """获取分布式锁"""
    lock_value = str(uuid.uuid4())
    acquired = r.set(f"lock:{lock_name}", lock_value, ex=expire, nx=True)
    return lock_value if acquired else None

def release_lock(lock_name, lock_value):
    """释放锁（Lua 脚本保证原子：验证是持有者才删）"""
    script = """
    if redis.call('GET', KEYS[1]) == ARGV[1] then
        return redis.call('DEL', KEYS[1])
    else
        return 0
    end
    """
    return r.eval(script, 1, f"lock:{lock_name}", lock_value)
```

#### 场景二：接口限流（INCR + EXPIRE）

```python
import time

def rate_limit(user_id, max_requests=100, window_seconds=60):
    key = f"rate:{user_id}:{int(time.time() / window_seconds)}"
    count = r.incr(key)
    if count == 1:
        r.expire(key, window_seconds + 1)
    if count > max_requests:
        ttl = r.ttl(key)
        return False, f"超限！请在 {ttl} 秒后重试"
    return True, f"剩余 {max_requests - count} 次"
```

#### 场景三：分布式 ID 生成器

```python
def next_id(business="order"):
    return r.incr(f"idgen:{business}")
# 第一个订单→1，第二个→2，绝不重复，绝对原子
```

#### 场景四：缓存序列化对象

```python
import json

def cache_user(user_id, user_data):
    r.setex(f"user:{user_id}", 600, json.dumps(user_data, ensure_ascii=False))

def get_user(user_id):
    data = r.get(f"user:{user_id}")
    return json.loads(data) if data else None
# ⚠️ 如果需要频繁单字段更新 → 用 Hash 而不是 String JSON！
```

### 2.8 String vs 其他类型选择

```
场景                                  用哪种？

存一个简单的值（配置、开关）            String
计数器、限流                           String (INCR)
缓存 JSON（整体读写、不改字段）         String（JSON 序列化）
缓存对象（需频繁单字段更新）            Hash（HGET/HSET 一个字段）
存一个列表                            List / Set（看需不需要去重）
判断是否存在                           Set / Bloom Filter
```

---

## 第 3 章：List（列表）

### 3.1 是什么？

Redis 的 List 是一个**双向链表**。记住两句话就能掌握所有命令：

> - **L 开头 = 从左操作，R 开头 = 从右操作**
> - **Push = 塞进去，Pop = 取出来并删除**

### 3.2 记忆方法

#### 方法一：前缀 + 后缀拆解

```
┌──────┬──────────────────────────────────────────────────────┐
│      │  每个命令可以拆成：方向 + 动作                         │
├──────┼──────────────────────────────────────────────────────┤
│  L   │  Left（左边）                                        │
│  R   │  Right（右边）                                       │
│  B   │  Blocking（阻塞，前面加 L/R 组合：BLPOP/BRPOP）        │
├──────┼──────────────────────────────────────────────────────┤
│ PUSH │  推进去（增）                                         │
│ POP  │  弹出来（删+取）                                      │
│ SET  │  修改                                                │
│ RANGE│  范围查询                                            │
│ INDEX│  索引取                                              │
│ LEN  │  长度                                                │
│ REM  │  移除（删指定值）                                     │
│ TRIM │  修剪（保留区间）                                     │
│ INSERT│  插入到某元素前后                                    │
└──────┴──────────────────────────────────────────────────────┘
```

#### 方法二：管子类比

```
         LPUSH ──►  [  ]  ◄── RPUSH
         LPOP  ◄──       ──►  RPOP

        左端 ←─────────→ 右端
        (L)               (R)

把 List 想象成一根横着的管子：
  Push = 从管口塞进去
  Pop  = 从管口掏出来
  L    = 管子左边，R = 管子右边
```

#### 方法三：三个核心图案

```
作为【队列】（先进先出 FIFO）：
  LPUSH + RPOP  或  RPUSH + LPOP  → 一端进，另一端出

作为【栈】（后进先出 LIFO）：
  LPUSH + LPOP  或  RPUSH + RPOP  → 同端进出

作为【消息队列】（阻塞等待）：
  BLPOP / BRPOP  → 没数据就等着，有数据立即取
```

### 3.3 增

```bash
# ═══ 从左端插入 ═══
LPUSH queue "A"                    # 队列: ["A"]
LPUSH queue "B" "C"                # 队列: ["C", "B", "A"] ← 逐个从左边塞入

# ═══ 从右端插入 ═══
RPUSH queue "D"                    # 队列: ["C", "B", "A", "D"]
RPUSH queue "E" "F"                # 队列: ["C", "B", "A", "D", "E", "F"]

# ═══ 在指定值前/后插入 ═══
LINSERT queue BEFORE "B" "X"       # 在 B 前面插入 X
LINSERT queue AFTER  "B" "Y"       # 在 B 后面插入 Y

# ═══ 不存在就不插 ═══
LPUSHX queue "Z"                   # queue 存在才 LPUSH，不存在什么都不做
RPUSHX queue "Z"                   # 同理
```

### 3.4 删

```bash
# ═══ 从两端弹出 ═══
LPOP queue                         # 从左边弹出并返回
RPOP queue                         # 从右边弹出并返回
LPOP queue 2                       # 一次弹 2 个（Redis 6.2+）

# ═══ 阻塞弹出（队列为空时等待！消息队列常用）═══
BLPOP queue 5                      # 等 5 秒，没有消息就返回 nil
BRPOP queue 0                      # 等 0 秒 = 永久等待

# BLPOP 的返回格式：
# 1) "queue"                       ← 队列名
# 2) "弹出的值"

# ═══ 原子移动（可靠队列核心！）═══
RPOPLPUSH queue backup             # 从 queue 右边弹出 → 推到 backup 左边
# Redis 6.2+ 推荐用 LMOVE：
LMOVE queue backup RIGHT LEFT      # 更灵活，可以指定方向

# ═══ 删除指定值 ═══
LREM queue 2 "A"                   # 删除 2 个值为 "A" 的元素
# count > 0 → 从左往右删
# count < 0 → 从右往左删
# count = 0 → 全部删

# ═══ 修剪（只保留区间）═══
LTRIM queue 0 2                    # 只保留索引 0~2 的元素，其余全部删除
```

### 3.5 改

```bash
# ═══ 修改指定索引的值 ═══
LSET queue 0 "new_value"           # 把索引 0 的值改成 "new_value"
```

### 3.6 查

```bash
# ═══ 范围查询（最常用）═══
LRANGE queue 0 -1                  # 查全部（0=第一个, -1=最后一个）
LRANGE queue 0 2                   # 查前 3 个
LRANGE queue -3 -1                 # 查最后 3 个

# ═══ 按索引取单个 ═══
LINDEX queue 0                     # 第一个
LINDEX queue -1                    # 最后一个

# ═══ 列表长度 ═══
LLEN queue

# ═══ 查找元素位置（Redis 6.0.6+）═══
LPOS queue "A"                     # 从左找第一个 "A" 的索引
LPOS queue "A" RANK 2              # 找第二个 "A"
LPOS queue "A" COUNT 2             # 找所有 "A"，最多返回 2 个
```

### 3.7 实战场景

#### ① 消息队列

```bash
# 生产者：往队尾塞消息
RPUSH messages "msg1" "msg2" "msg3"
# 消费者：从队头取消息
LPOP messages
# 阻塞消费者：没消息就等着
BLPOP messages 0
```

#### ② 可靠队列模式（消息不丢失）

```bash
# 工作队列：取出消息的同时备份到另一个列表
RPOPLPUSH messages messages_backup
# 处理成功后再从 backup 中删除
LREM messages_backup 1 "msg"
# 如果处理失败，消息还在 backup 里，不会丢失
```

### 3.8 Stream vs Pub/Sub vs List 选型

| 特性 | Stream | Pub/Sub | List |
|------|--------|---------|------|
| 消息持久化 | ✅ 内存+可选磁盘 | ❌ | ✅（取出即删） |
| 消费确认 | ✅ XACK | ❌ | ❌ |
| 消费者组 | ✅ | ❌ | ❌（需自己做） |
| 消息回溯 | ✅ 按 ID | ❌ | ❌ |
| 一对多 | ✅ 不同消费组 | ✅ 所有订阅者 | ❌ |
| 阻塞读取 | ✅ | ✅ 天然 | ✅ BLPOP/BRPOP |
| 适用场景 | 可靠消息、事件溯源 | 实时广播 | 简单队列/栈 |

---

## 第 4 章：Set（集合）

### 4.1 是什么？

Set 是**无序、不重复**的字符串集合。记住核心：

> **S 开头 = Set 集合**
> 集合就是**一个麻袋里的玻璃球——没顺序、不能重复、只能整颗拿出来**

### 4.2 增

```bash
SADD tags "redis"                      # → 1（成功添加 1 个）
SADD tags "mongodb" "mysql" "redis"    # → 2（redis 已存在，实际只加了 2 个）
```

### 4.3 删

```bash
SREM tags "mysql"                      # → 1（删了 1 个）
SREM tags "oracle"                     # → 0（不存在）

# 随机弹出一个（抽奖！）
SPOP tags                              # 随机取走 1 个
SPOP tags 3                            # 随机取走 3 个（Redis 3.2+）

# 原子移动
SMOVE tags archived "redis"            # 从 tags 移到 archived
```

### 4.4 改

Set 没有直接的「修改」命令。因为元素就是值本身，改 = 删旧 + 加新：

```bash
SREM tags "mysql"
SADD tags "postgresql"
```

### 4.5 查

```bash
# 基础查询
SISMEMBER tags "redis"                 # 是否存在（1=在，0=不在，用最多）
SMEMBERS tags                          # 全部成员（慎用！大集合会慢）
SRANDMEMBER tags                       # 随机返回 1 个（不删除）
SRANDMEMBER tags 3                     # 随机返回 3 个
SCARD tags                             # 元素个数（CARDinality）
SSCAN tags 0                           # 游标扫描（适合大集合）
```

### 4.6 集合运算（精髓！）

```bash
# ═══ 交集 SINTER — 共同好友 ═══
SADD user:1:friends "A" "B" "C"
SADD user:2:friends "B" "C" "D"
SINTER user:1:friends user:2:friends      # → {"B", "C"}

# ═══ 并集 SUNION — 全部好友 ═══
SUNION user:1:friends user:2:friends      # → {"A", "B", "C", "D"}

# ═══ 差集 SDIFF — 我有他没有 ═══
SDIFF user:1:friends user:2:friends       # → {"A"}（user1 有而 user2 没有）

# ═══ 带 STORE — 结果存到新集合 ═══
SINTERSTORE common user:1:friends user:2:friends   # 交集存入 common
SUNIONSTORE  all    user:1:friends user:2:friends   # 并集存入 all
SDIFFSTORE   only   user:1:friends user:2:friends   # 差集存入 only
```

### 4.7 实战场景

#### ① 点赞（去重天然防刷）

```bash
SADD article:1001:likes "user:5"
SADD article:1001:likes "user:5"      # → 0，重复加不进去
SCARD article:1001:likes              # 点赞数
SISMEMBER article:1001:likes "user:5" # 我点过吗？
SREM article:1001:likes "user:5"      # 取消点赞
```

#### ② 抽奖

```bash
SADD pool "user:1" ... "user:1000"
SPOP pool                             # 随机抽 1 个（弹出即中奖，不会重复中）
SPOP pool 3                           # 随机抽 3 个
```

#### ③ 好友推荐

```bash
# 好友的好友，但不是我的好友 → 推荐
SDIFF user:2:friends user:1:friends   # user2 有而 user1 没有的
```

---

## 第 5 章：Sorted Set（有序集合）

### 5.1 是什么？

Sorted Set 是 **Set + 每个元素绑一个分数，按分数自动排序**。

> **Z 开头 = ZSet（有序集合）**
> 就像**班级成绩单**——每个人（元素）有分数（score），按分数高低自动排队。

```
元素（member）= 不能重复（和 Set 一样）
分数（score） = 可以重复，必须是数字（double）

  成绩单（key: "scores"）
┌──────────────────────────┐
│  Alice    95.0   ← 最高  │
│  Bob      87.5           │  分数相同 → 按元素名字典序排
│  Charlie  87.5           │
│  David    62.0   ← 最低  │
└──────────────────────────┘
     ↑       ↑
  member   score
```

### 5.2 增

```bash
ZADD scores 95 "Alice"                 # → 1（新增 1 个）
ZADD scores 87.5 "Bob" 62 "David"      # → 2（一次加多个）

# 更新分数（已存在 = 覆盖旧分数）
ZADD scores 96 "Alice"                 # 0（0 新增，因为 Alice 已存在）

# 条件添加
ZADD scores NX 88 "Eve"                # 不存在才加
ZADD scores XX 90 "Alice"              # 存在才更新
ZADD scores GT 90 "Alice"              # 新分数 > 旧分数才更新
ZADD scores LT 85 "Alice"              # 新分数 < 旧分数才更新
```

### 5.3 删

```bash
ZREM scores "Alice"                     # 删除指定元素

# 按排名删（索引 0=最低分, -1=最高分）
ZREMRANGEBYRANK scores 0 2             # 删排名 0~2（最低的 3 个）
ZREMRANGEBYRANK scores -3 -1           # 删排名最高的 3 个

# 按分数范围删
ZREMRANGEBYSCORE scores 0 60           # 删分数 0~60 的
ZREMRANGEBYSCORE scores -inf 60        # 和上面一样，-inf 表负无穷
ZREMRANGEBYSCORE scores 90 +inf        # 删 90 分以上的

# 区间开闭符号
ZREMRANGEBYSCORE scores (60 100        # (60 = 大于 60（不含 60）
ZREMRANGEBYSCORE scores 60 (100        # (100 = 小于 100（不含 100）
```

### 5.4 改

```bash
# 给已有元素增减分数（原子操作！）
ZINCRBY scores 5 "Alice"               # +5 分
ZINCRBY scores -3 "Bob"                # -3 分

# 如果元素不存在 → 相当于 ZADD
```

### 5.5 查（最丰富）

```bash
# ═══ 按排名查 ═══
ZRANGE scores 0 2                       # 最低分的 3 个
ZRANGE scores 0 -1                      # 所有人，从低到高
ZRANGE scores 0 2 WITHSCORES            # 带分数
ZREVRANGE scores 0 2                    # 最高分的 3 个
ZREVRANGE scores 0 -1 WITHSCORES        # 所有人，从高到低

# ═══ 查排名 ═══
ZRANK scores "Alice"                    # Alice 的排名（低→高，0 起步）
ZREVRANK scores "Alice"                 # Alice 的排名（高→低，0 起步）

# ═══ 按分数范围查 ═══
ZRANGEBYSCORE scores 80 100             # 80~100 分的
ZRANGEBYSCORE scores 80 100 WITHSCORES  # 带分数
ZRANGEBYSCORE scores 80 100 LIMIT 0 3   # 前 3 个（分页）
ZRANGEBYSCORE scores 80 (100            # (100 = 不含 100
ZRANGEBYSCORE scores -inf +inf          # 查全部

# ═══ 反向查 ═══
ZREVRANGEBYSCORE scores 100 80          # 100~80，从高到低
ZREVRANGEBYSCORE scores +inf -inf LIMIT 0 10  # 最高分 10 个

# ═══ 统计 ═══
ZCARD scores                            # 总人数
ZCOUNT scores 80 100                    # 80~100 分有几人
ZSCORE scores "Alice"                   # 查 Alice 的分数
ZSCAN scores 0                          # 游标扫描
```

### 5.6 集合运算

```bash
# 并集：合并两个班的成绩，相同元素取最高分
ZUNIONSTORE all 2 class1 class2 \
    WEIGHTS 1 2 \
    AGGREGATE MAX                        # SUM | MIN | MAX

# 交集：取两个班都有的
ZINTERSTORE common 2 class1 class2 \
    WEIGHTS 1 1 \
    AGGREGATE SUM
```

### 5.7 实战场景

#### ① 排行榜（最经典）

```bash
ZADD leaderboard 1000 "player1" 850 "player2"
# Top 10
ZREVRANGE leaderboard 0 9 WITHSCORES
# 我的排名
ZREVRANK leaderboard "player1"
```

#### ② 延迟队列

```bash
# 分数 = 执行时间戳，到期任务 = 分数 ≤ 当前时间
ZADD delay_queue 1717750000 "task:send_email:1001"
ZRANGEBYSCORE delay_queue 0 1717760000 LIMIT 0 10
ZREM delay_queue "task:send_email:1001"  # 执行完删掉
```

#### ③ 滑动窗口限流

```bash
# 分数 = 毫秒时间戳
ZADD ratelimit:user:1001 1717766200000 "req:uuid1"
# 删掉 1 秒前的请求
ZREMRANGEBYSCORE ratelimit:user:1001 0 1717766199000
# 统计窗口内请求数
ZCARD ratelimit:user:1001
```

---

## 第 6 章：Hash（哈希）

### 6.1 是什么？

Hash 是**键值对的集合**，像一个**微型字典**。记住核心：

> **H 开头 = Hash**
> 就像数据库里的一行记录——key 是表名+主键，field 是列名，value 是单元格值

```
表.主键        列名          值
  ↓            ↓            ↓
HSET user:1001 name "张三" age 28 city "北京"

Redis 中的存储：
user:1001 ──→ ┌───────────┐
              │ name  张三  │
              │ age   28    │
              │ city  北京  │
              └───────────┘

类比 SQL：
SELECT * FROM user WHERE id = 1001;
→ HGETALL user:1001

Hash 就是「一张表的某一行」存在 Redis 里
```

### 6.2 增

```bash
HSET user:1001 name "张三"                # → 1（新增 1 个字段）
HSET user:1001 age 28 city "北京"         # → 2（新增 2 个）
HMSET user:1001 email "zhang@test.com"    # 旧语法，仍可用，但不推荐

# 仅字段不存在时设置（原子！）
HSETNX user:1001 name "李四"              # → 0（已存在，不覆盖）
HSETNX user:1001 gender "男"              # → 1（不存在，设成功）

# Redis 4.0 之后：HSET 可以设多个字段
# 现在统一用 HSET，不需要 HMSET
```

### 6.3 删

```bash
HDEL user:1001 phone                      # 删一个字段
HDEL user:1001 phone email               # 删多个
DEL user:1001                             # 删整个 Hash
```

### 6.4 改

```bash
HSET user:1001 age 29                     # 修改 = 重新设值

# 数字增减（原子！
HINCRBY user:1001 age 1                   # +1 → 30
HINCRBY user:1001 age -5                  # -5 → 25

# 浮点数增减
HINCRBYFLOAT user:1001 score 1.5          # +1.5
HINCRBYFLOAT user:1001 score -0.5         # -0.5
```

### 6.5 查

```bash
HGET user:1001 name                       # 取单个字段
HMGET user:1001 name age city            # 取多个
HGETALL user:1001                         # 所有字段+值（逐对返回）
HKEYS user:1001                           # 所有字段名
HVALS user:1001                           # 所有值
HEXISTS user:1001 name                    # 字段是否存在
HLEN user:1001                            # 字段数量
HSTRLEN user:1001 name                    # 值的长度
HSCAN user:1001 0 MATCH "na*"            # 扫描
```

### 6.6 实战场景

#### ① 用户信息

```bash
HSET user:1001 name "张三" age 28 email "zhang@test.com"
HGET user:1001 name                       # 登录时取名字
HINCRBY user:1001 age 1                   # 过生日 +1 岁
HEXISTS user:1001 phone                   # 有没有填手机号
```

#### ② 购物车

```bash
# 商品 ID = field，数量 = value
HSET cart:user:1001 "prod:2001" 2         # 加 2 个
HINCRBY cart:user:1001 "prod:2001" 1      # 再加 1 个 → 3
HINCRBY cart:user:1001 "prod:2001" -1     # 减 1 个
HDEL cart:user:1001 "prod:2001"           # 移除商品
HLEN cart:user:1001                        # 几样东西
DEL cart:user:1001                         # 清空
```

#### ③ 比 String JSON 更好的对象缓存

```bash
# ❌ 做更复杂的做法：整个序列化
SET article:1001 '{"title":"...","views":100}'
# 每次改 views → GET → 反序列化 → 改 → 序列化 → SET（4 步）

# ✅ 更好的做法：用 Hash
HSET article:1001 title "..." content "..." views 100
HINCRBY article:1001 views 1             # 一步到位，原子操作！并发安全！
```

---

## 第 7 章：Stream（消息队列）

### 7.1 是什么？

Stream 是 Redis 5.0 引入的**持久化消息队列**，弥补了 Pub/Sub「消息不存、离线丢失」的缺陷。

> **Stream = 追加日志 + 消费者组**
> 就像**微信群聊 + 聊天记录永久保存**——消息不丢、能回溯、可多人分工消费

### 7.2 数据结构理解

```
Stream: "orders"
┌─────────────────────────────────────────────────┐
│  ID: 1717760000000-0    ← 消息 ID（时间戳-序号）  │
│  ┌─────────────────────┐                        │
│  │ user: "张三"         │   ← field-value 键值对 │
│  │ amount: 100          │                        │
│  │ item: "手机"          │                        │
│  └─────────────────────┘                        │
├─────────────────────────────────────────────────┤
│  ID: 1717760001000-0                            │
│  ┌─────────────────────┐                        │
│  │ user: "李四"         │                        │
│  │ amount: 50           │                        │
│  └─────────────────────┘                        │
└─────────────────────────────────────────────────┘

一条 Stream = 多条消息（Entry）
每条消息 = 唯一 ID + 一组 field-value（和 Hash 一样）
消息按 ID 排序，新消息追加到末尾
```

### 7.3 消息 ID 格式

```
格式：<毫秒时间戳>-<序号>

1717760000000-0
│             │
│             └─ 同一毫秒内的序号，从 0 开始
└─────────────── 毫秒级 Unix 时间戳

手动指定：新的必须 > 旧的（字典序）
用 * 自动生成：就是当前时间
```

### 7.4 增 — XADD

```bash
# 自动生成 ID（* 号）
XADD orders * user "张三" amount 100 item "手机"
# → "1717760000000-0"  ← 返回自动生成的 ID

# 手动指定 ID（必须严格递增，否则报错）
XADD orders 1717760005000-0 user "赵六" amount 80

# 限制长度（防止 Stream 无限增长，CAP 机制）
XADD orders MAXLEN 1000 * user "张三" amount 100
# 只保留最新的 1000 条

# 近似裁剪（效率更高，不保证精确到 1000，可能是 1010 条）
XADD orders MAXLEN ~ 1000 * user "张三" amount 100
```

### 7.5 查

```bash
# ═══ XRANGE/XREVRANGE — 按 ID 范围查 ═══
XRANGE orders - +                          # 所有（- 最小, + 最大）
XRANGE orders - + COUNT 10                 # 前 10 条
XRANGE orders 1717760000000-0 1717760001000-0  # ID 范围
XREVRANGE orders + - COUNT 5               # 最新 5 条（反序）

# ═══ XREAD — 阻塞/非阻塞读 ═══
# 非阻塞：从开头读 2 条
XREAD COUNT 2 STREAMS orders 0

# 只读新消息（$ = 当前最新，之后新来的）
XREAD STREAMS orders $

# 阻塞读取（等新消息）
XREAD BLOCK 5000 STREAMS orders $          # 等 5 秒
XREAD BLOCK 0 STREAMS orders $             # 永久等待

# 从上次消费位置继续
XREAD BLOCK 0 STREAMS orders 1717760000000-0

# 同时读多个 Stream
XREAD BLOCK 3000 STREAMS orders payments $ $

# ═══ 元信息 ═══
XLEN orders                                 # 消息条数
XINFO STREAM orders                         # 详细信息
XINFO GROUPS orders                         # 消费者组
XINFO CONSUMERS orders mygroup              # 组内消费者
```

### 7.6 消费者组 — 核心功能！

```
概念图：

              Stream: orders
         ┌─────────────────────┐
         │ msg1  msg2  msg3    │
         │ msg4  msg5  msg6    │
         └─────────┬───────────┘
                   │
        ┌──────────┴──────────┐
        │   消费者组: workers  │
        │  ┌───────┐ ┌───────┐│
        │  │ 消费A  │ │ 消费B  ││
        │  │msg1 ✓  │ │msg2 ✓ ││  竞争消费，消息只发给组内一个消费者
        │  │msg3 ✓  │ │msg4 ✗ ││  ← 挂了没 ACK → 留在 pending
        │  └───────┘ └───────┘│
        └─────────────────────┘

同一组内：每条消息只发给一个消费者（竞争消费）
不同组间：独立消费，互不影响
```

```bash
# ═══ 创建消费者组 ═══
XGROUP CREATE orders workers 0             # 从头开始消费
XGROUP CREATE orders workers $             # 只消费创建后的新消息
XGROUP CREATE orders workers $ MKSTREAM    # Stream 不存在也创建

# ═══ 消费者读取 ═══
# 消费者 A：读未处理的新消息
XREADGROUP GROUP workers consumer-A COUNT 2 STREAMS orders >
#               ↑组名    ↑消费者名                   ↑ ">" = 从未消费过的

# 消费者 B：读不同的消息（自动负载均衡！）
XREADGROUP GROUP workers consumer-B COUNT 2 STREAMS orders >

# 重试 pending 消息（消费者挂了，消息未被 ACK）
XPENDING orders workers                    # 概览
XPENDING orders workers - + 10             # 列出前 10 条 pending

# 消费者 A 重连后读 pending
XREADGROUP GROUP workers consumer-A COUNT 5 STREAMS orders 0
#                                                        ↑ 0 = 读 pending

# ═══ 确认完成 ═══
XACK orders workers 1717760000000-0
# → 1  ← 确认了 1 条
XACK orders workers 1717760000000-0 1717760001000-0  # 确认多条

# ═══ XCLAIM — 认领超时消息 ═══
# 消费者 A 挂了，B 认领 A 的 pending 消息
XCLAIM orders workers consumer-B 30000 1717760000000-0
#                         认领的超时消息 ↑    ↑ 超时毫秒数  ↑ 消息 ID
```

### 7.7 `>` vs `$` vs `0` — 最容易混淆的地方

```
XREAD STREAMS orders $
  → $ = 只读执行命令这一刻之后的新消息，历史的不读

XREADGROUP ... STREAMS orders >
  → > = 读从未分配给本组任何消费者的消息（新消息 + 历史未派发的）
    > 只能用在 XREADGROUP，XREAD 不支持

XREADGROUP ... STREAMS orders 0（或具体 ID）
  → 读已经分配过但没确认的 pending 消息（用于重试）

对比：
  $ → "从现在开始，之前的不看"（XREAD 用）
  > → "我要新任务"（XREADGROUP 用）
  0 → "我要重试之前没搞定的"（XREADGROUP 重试）
```

### 7.8 Python 消费者组完整实现

```python
import redis
import threading
import time

r = redis.Redis(decode_responses=True)

def consumer_worker(consumer_name):
    """消费者组的工作者"""
    # 确保消费者组存在
    try:
        r.xgroup_create("orders", "workers", id="0", mkstream=True)
    except redis.ResponseError as e:
        if "BUSYGROUP" not in str(e):
            raise

    while True:
        try:
            result = r.xreadgroup(
                groupname="workers",
                consumername=consumer_name,
                streams={"orders": ">"},
                count=2,
                block=5000
            )
            if result:
                for stream_name, messages in result:
                    for msg_id, fields in messages:
                        print(f"[{consumer_name}] 处理 {msg_id}: {fields['item']}")
                        if process_order(fields):
                            r.xack("orders", "workers", msg_id)
                            print(f"[{consumer_name}] ✓ {msg_id}")
                        else:
                            print(f"[{consumer_name}] ✗ {msg_id}（保留 pending 等重试）")
            else:
                print(f"[{consumer_name}] 无新消息...")
        except Exception as e:
            print(f"[{consumer_name}] 错误: {e}")
            time.sleep(1)

def process_order(fields):
    """模拟业务处理"""
    time.sleep(0.3)
    return True
```

---

## 第 8 章：Geospatial（地理空间）

### 8.1 是什么？

Redis Geospatial 是 **3.2** 引入的地理位置数据类型。

> **GEO = 基于 Sorted Set 的地理坐标系统**
> 底层就是 ZSet，经纬度通过 GeoHash 算法编码成 score，提供了地理专用的距离计算和范围查询

### 8.2 底层原理：ZSet 套壳

```bash
# GEO 本质上就是 Sorted Set
# 添加地理位置时，Redis 内部做了两件事：
#   1. member = 位置名称
#   2. score  = 经纬度通过 GeoHash 算法编码成 52 位整数

# 所以可以直接用 ZSet 命令操作 GEO 数据！
ZRANGE cities 0 -1          # 查所有城市名
ZREM cities "北京"           # 删一个位置
ZCARD cities                # 有多少个位置
```

### 8.3 GeoHash 编码原理（了解即可）

```
经纬度 → GeoHash 算法 → 52 位整数（Score）
                            ↓
    近似地把地球切成一个个小格子
    相邻的位置 → GeoHash 也相近（但不保证严格相邻！）

例如：
  (116.4, 39.9) 北京 → 4069885361618014
  (121.5, 31.2) 上海 → 4054793662317626

重要注意：GeoHash 前缀相同的 ≠ 一定在附近
  边界两边的点虽然近但前缀可能不同
  查附近时应该搜周围 8 个格子的前缀最稳妥
```

### 8.4 增 — GEOADD

```bash
# 语法：GEOADD key longitude latitude member [...]

GEOADD cities 116.4074 39.9042 "北京"

# 一次添加多个
GEOADD cities \
    121.4737 31.2304 "上海" \
    113.2644 23.1291 "广州" \
    114.0579 22.5431 "深圳" \
    120.1551 30.2741 "杭州" \
    104.0657 30.6599 "成都"

# 已存在的 member → 更新坐标
GEOADD cities 116.4100 39.9100 "北京"

# ⚠️ 经纬度限制（记住！）
#   经度：-180 ~ 180
#   纬度：-85.05112878 ~ 85.05112878（不是 ±90！）
#   两极附近 GeoHash 无效
```

### 8.5 删

```bash
# 没有专用删除命令，直接用 ZSet 的 ZREM
ZREM cities "北京"
ZREM cities "北京" "上海"
```

### 8.6 查

```bash
# 查坐标
GEOPOS cities "北京"
# → 1) 1) "116.4074005484581"
#       2) "39.90420075783584"

# 查 GeoHash（base32 编码字符串）
GEOHASH cities "北京"
# → 1) "wx4g0bmets4s0"
# 用途：前缀相同的 → 位置相近（粗筛）；可以存到关系数据库做简单地理索引

# 算距离
GEODIST cities "北京" "上海"
# → "1068153.1183"   ← 默认单位：米
GEODIST cities "北京" "上海" km   # → "1068.1531"
GEODIST cities "北京" "上海" mi   # → "663.7192"
GEODIST cities "北京" "上海" ft   # → "3504277.1619"

# 算不存在的 → (nil)
GEODIST cities "北京" "火星"       # → (nil)
```

### 8.7 范围查询（最核心的功能）

```bash
# ═══ GEORADIUS — 以某坐标为中心（6.2 之后已过时，用 GEOSEARCH）═══
GEORADIUS cities 116.4 39.9 2000 km WITHDIST ASC COUNT 5

# ═══ GEORADIUSBYMEMBER — 以已有位置为中心（也已过时）═══
GEORADIUSBYMEMBER cities "北京" 2000 km WITHDIST ASC COUNT 5

# ═══ GEOSEARCH（Redis 6.2+，推荐！统一语法）═══

# 替换 GEORADIUS：以坐标为中心
GEOSEARCH cities FROMLONLAT 116.4 39.9 BYRADIUS 2000 km

# 替换 GEORADIUSBYMEMBER：以已有成员为中心
GEOSEARCH cities FROMMEMBER "北京" BYRADIUS 2000 km

# 矩形范围
GEOSEARCH cities FROMMEMBER "上海" BYBOX 500 300 km
#                                                ↑宽  ↑高

# 完整语法
GEOSEARCH cities \
    FROMMEMBER "上海" \                          # 以"上海"为圆心
    BYRADIUS 500 km \                            # 半径 500km
    ASC \                                        # 近→远
    COUNT 5 \                                    # 最多 5 个
    WITHDIST \                                   # 带距离
    WITHCOORD                                    # 带坐标

# 存到新 key
GEOSEARCHSTORE nearby cities FROMMEMBER "上海" BYRADIUS 500 km ASC COUNT 10
# 结果存入 nearby（一个 ZSet）
```

### 8.8 重要限制和注意

```
1. GEO 底层是 ZSet
   → 可以用 ZCARD/ZRANGE/ZREM 等所有 ZSet 命令
   → 但注意 score 是 GeoHash 编码，不是可读的距离

2. GEORADIUS / GEORADIUSBYMEMBER 在 6.2+ 已过时
   → 新项目统一用 GEOSEARCH / GEOSEARCHSTORE

3. 经纬度范围
   经度：-180 ~ 180
   纬度：-85.05112878 ~ 85.05112878（不是 ±90！）
   两极附近 GeoHash 无效

4. 距离是球面直线距离（Haversine 公式）
   → 不考虑地形、道路，只是球面最短弧

5. ⚠️ 仅支持二维（经纬度），不支持三维（高度/海拔）
   因为底层 GeoHash 天然就是二维算法
   Redis GEO 设计目标很单一：LBS（附近的人/门店）
   三维空间搜索（无人机、楼层定位）→ 用 PostGIS/MongoDB

6. GeoHash 前缀相同的 ≠ 一定在附近
   → 查附近时搜周围 8 个格子的前缀最稳妥
```

### 8.9 为什么 Redis GEO 只支持二维？

Redis GEO 底层用的是 **GeoHash + Sorted Set**，GeoHash 算法天然就是二维的——把地球表面交叉切成格子。第三维（高度）GeoHash 本身就不支持。

如果你需要三维空间搜索：

| 方案 | 适用场景 |
|------|---------|
| Redis + 三个 ZSet 模拟 | 简单 3D 范围过滤 |
| PostgreSQL + PostGIS | 2D/3D 地理全支持 |
| MongoDB 3D 索引 | 文档型 3D 查询 |
| Redis 不是 GIS 系统 | 真 3D 用专业 GIS 引擎 |

Redis GEO 设计目标非常单一：做「附近的人 / 最近的门店」这类 LBS 服务。这种场景 99% 只需要经纬度，因为人在平面上移动。

---

## 第 9 章：Bitmap（位图）

### 9.1 是什么？

Bitmap 严格来说**不是一个独立数据类型**，而是 **String 上的一组位操作命令**。

> **Bitmap = 把 String 当成一个巨大的比特数组来用**
> 每个 bit 只存 0 或 1，一个 512MB 的 String 可以表示 **40 多亿个布尔状态**

### 9.2 为什么要用 Bitmap？—— 内存优势

```
场景：记录 1 亿用户今天是否签到

方案 A：Set 存 user_id
  SADD sign:20260607 user:1 user:2 ... user:100000000
  → 每个 user_id 平均 20 字节
  → 1 亿 × 20 字节 ≈ 2 GB

方案 B：Bitmap
  SETBIT sign:20260607 <user_id> 1
  → 1 亿 bit = 12.5 MB
  → 节省 99.4% 内存！

一年 365 天 × 12.5 MB = 4.5 GB（Set 方案是 730 GB）
```

### 9.3 增 / 改 — SETBIT

```bash
# 语法：SETBIT key offset value（value 只能是 0 或 1）

SETBIT sign:20260607 10086 1        # user:10086 签到
SETBIT sign:20260607 10087 1        # user:10087 签到

# 修改 = 重新设
SETBIT sign:20260607 10086 0        # 取消签到

# ⚠️ SETBIT 返回的是旧值！可以用来判断是否第一次签到
SETBIT sign:20260607 10086 1        # → 0（之前是 0）
SETBIT sign:20260607 10086 0        # → 1（之前是 1）

# offset 可以很大，Redis 自动扩展 String
SETBIT sign:20260607 99999999 1     # 1 亿 bit ≈ 12.5 MB
```

### 9.4 查 — GETBIT

```bash
GETBIT sign:20260607 10086          # → 1（签到了）
GETBIT sign:20260607 99999          # → 0（没签到）
# 不存在的 key → 返回 0（不是 nil）
```

### 9.5 统计 — BITCOUNT

```bash
BITCOUNT sign:20260607              # 今天签到人数

# ⚠️ 注意：可选范围参数是字节，不是 bit！
BITCOUNT sign:20260607 0 1249       # 前 10000 个 bit → 1250 字节
# offset 0~1249 是字节索引！
```

### 9.6 位运算 — BITOP

```bash
# ═══ AND — 连续两天都签到 ═══
BITOP AND consecutive sign:0606 sign:0607
BITCOUNT consecutive                 # 连续签到人数

# ═══ OR — 至少一天签到 ═══
BITOP OR any_day sign:0606 sign:0607

# ═══ XOR — 只签了一天 ═══
BITOP XOR irregular sign:0606 sign:0607

# ═══ NOT — 取反 ═══
BITOP NOT not_flag key              # 注意：NOT 只有一个源 key
```

### 9.7 查找 — BITPOS

```bash
BITPOS sign:20260607 1              # 第一个签到的用户 ID（第一个 1 的位置）
BITPOS sign:20260607 0              # 第一个没签到的（第一个 0 的位置）
BITPOS sign:20260607 1 0 1000       # 在 0~1000 字节范围找
```

### 9.8 实战场景

#### ① 签到系统

```python
from datetime import date

def sign_in(user_id):
    today = date.today().strftime("%Y%m%d")
    key = f"sign:{today}"
    old = r.setbit(key, user_id, 1)
    if old == 1:
        return "今天已经签到了"
    count = r.bitcount(key)
    return f"签到成功！你是第 {count} 个"

def is_signed(user_id, day_str):
    return r.getbit(f"sign:{day_str}", user_id) == 1

def consecutive_7_days(user_id):
    """判断是否连续 7 天签到"""
    from datetime import timedelta
    today = date.today()
    for i in range(7):
        day = (today - timedelta(days=i)).strftime("%Y%m%d")
        if not r.getbit(f"sign:{day}", user_id):
            return False
    return True
```

#### ② 活跃用户统计

```python
# 周活跃 = 7 天的 OR
days = [f"active:{d}" for d in last_7_days]
r.bitop("or", "wau", *days)
wau = r.bitcount("wau")
```

#### ③ 在线状态

```bash
SETBIT online 10086 1               # 上线
SETBIT online 10086 0               # 下线
BITCOUNT online                     # 在线人数
```

---

## 第 10 章：Bitfield（位域）

### 10.1 是什么？

Bitfield 是 **Bitmap 的进阶版**——不只看单个 bit，而是把 String 当成**自定义宽度的整数数组**来操作。

> **Bitmap = 每个 bit 独立看（0 和 1）**
> **Bitfield = 把连续 N 个 bit 打包成一个整数（计数器/状态码/小整数）**

### 10.2 思维升级

```
Bitmap 的视角：
  String: [0][1][0][0][0][0][0][1][1][0][1][0][0][1][1][1]...
          每个格子 = 1 bit，只有 0 和 1

Bitfield 的视角：
  String: [── u8 ──][── u4 ──][─── i12 ───][── u1 ──]...
          8位无符号  4位无符号  12位有符号   1位

  同一个 String
  Bitmap 看成一个一个的 bit
  Bitfield 看成一块一块的「位域」
```

### 10.3 类型系统

```bash
# 类型格式: uN 或 iN
#   u = 无符号（unsigned），0 ~ 2^N-1
#   i = 有符号（signed），-2^(N-1) ~ 2^(N-1)-1
#   N = 位数，1~64

u1   → 0~1           （1 个布尔值）
u4   → 0~15          （一个小状态码）
u8   → 0~255         （年龄、等级）
i8   → -128~127      （温度差值）
u16  → 0~65535       （分数、金币）
i16  → -32768~32767  （坐标偏移）
u32  → 0~43亿        （时间戳）
```

### 10.4 基本操作

```bash
# ═══ GET — 读 N 位整数 ═══
BITFIELD player:10086 GET u8 0       # 从 bit 0 开始读 8 位
# → (integer) 50

# 一次读多个
BITFIELD player:10086 GET u8 0 GET u16 8 GET u4 24 GET u1 28
# → 1) 50     ← 等级
#    2) 9999   ← 金币
#    3) 3      ← 生命
#    4) 1      ← VIP

# ═══ SET — 写 N 位整数 ═══
BITFIELD player:10086 SET u8 0 60           # 等级 = 60
BITFIELD player:10086 SET u8 0 60 SET u16 8 8000 SET u4 24 2
# 返回旧值

# ═══ INCRBY — 原子增减 ═══
BITFIELD player:10086 INCRBY u16 8 100      # 金币 +100
BITFIELD player:10086 INCRBY u16 8 -50      # 金币 -50
BITFIELD player:10086 INCRBY u4 24 -1       # 生命 -1
```

### 10.5 溢出控制（非常重要！）

当 INCRBY 超出类型的合法范围时，怎么办？

```bash
# 三种策略：

# ═══ WRAP（回绕，默认）═══
# 设 u4 当前 = 14，+2：
BITFIELD test OVERFLOW WRAP SET u4 0 14
BITFIELD test OVERFLOW WRAP INCRBY u4 0 2   # → 0（14+2=16 → 归零）

# BITFIELD test OVERFLOW WRAP INCRBY u4 0 -1 # → 15（0-1=-1 → 回绕到 15）
# 就像汽车里程表，满了归零

# ═══ SAT（饱和）═══
BITFIELD test OVERFLOW SAT SET u4 0 14
BITFIELD test OVERFLOW SAT INCRBY u4 0 2    # → 15（到顶了，不再涨）
BITFIELD test OVERFLOW SAT INCRBY u4 0 -20  # → 0（到底了，不再减）
# 就像杯子装满水，多了溢出不要了

# ═══ FAIL（失败）═══
BITFIELD test OVERFLOW FAIL SET u4 0 14
BITFIELD test OVERFLOW FAIL INCRBY u4 0 2   # → (nil)  ← 拒绝操作
```

### 10.6 内存布局设计实战

```
假设一个用户状态数据包：

字段：
  age:    0~150    →  u8   (8bit,  从 bit 0 开始)
  level:  1~100    →  u8   (8bit,  从 bit 8 开始)
  coins:  0~99999  →  u32  (32bit, 从 bit 16 开始)
  lives:  0~5      →  u4   (4bit,  从 bit 48 开始)
  vip:    0/1      →  u1   (1bit,  从 bit 52 开始)
  faction:0~2      →  u2   (2bit,  从 bit 53 开始)
  online: 0/1      →  u1   (1bit,  从 bit 55 开始)

共 56 bit = 7 字节

按 100 万用户算：7 MB（Hash 方案要几百 MB！）
```

```python
import redis

r = redis.Redis(decode_responses=True)

LAYOUT = {
    "age": ("u8", 0), "level": ("u8", 8), "coins": ("u32", 16),
    "lives": ("u4", 48), "vip": ("u1", 52), "faction": ("u2", 53), "online": ("u1", 55),
}

def init_player(player_id, age=18, level=1, coins=0, lives=3, vip=False):
    r.bitfield(f"p:{player_id}",
        "SET", "u8",  0,  age,
        "SET", "u8",  8,  level,
        "SET", "u32", 16, coins,
        "SET", "u4",  48, lives,
        "SET", "u1",  52, int(vip),
        "SET", "u2",  53, 0,
        "SET", "u1",  55, 0,
    )

def add_coins(player_id, amount):
    """加金币（饱和控制，不超上限）"""
    return r.bitfield(f"p:{player_id}", "OVERFLOW", "SAT",
        "INCRBY", "u32", 16, amount)

def lose_life(player_id):
    """扣一条命（不低于 0）"""
    result = r.bitfield(f"p:{player_id}", "OVERFLOW", "SAT",
        "INCRBY", "u4", 48, -1)
    new_val = result[0]
    return "游戏结束！" if new_val == 0 else f"剩余 {new_val} 条命"
```

### 10.7 与 Bitmap 的关系

```bash
# Bitfield 和 Bitmap 操作的是同一个 String！！
SETBIT player:10086 0 1             # Bitmap 设 bit
BITFIELD player:10086 SET u8 0 100  # Bitfield 设位域
GETBIT player:10086 0               # 结果会被 BITFIELD 影响！
# 它们可以混合使用
```

---

<!-- ═══════════════════════════════════════════════════════ -->
<!--  第四部分：概率数据类型 — 小内存做大统计                  -->
<!-- ═══════════════════════════════════════════════════════ -->

---

## 第 11 章：概率数据类型

> **核心理念：用极小的内存换取高精度的近似结果。**
>
> ```
> 内存对比：
> 统计 1 亿独立用户
> Set（精确）     → 3 GB
> HyperLogLog     → 12 KB（误差 0.81%）
> Bloon Filter   → 120 MB（误判 0.01%）
> ```

### 11.1 HyperLogLog — 基数统计

**解决问题：有多少个不同的东西？只数人头，不关心每个来了几次。**

#### 工作原理（简化版）

```
1. 对每个元素做哈希 → 64 位二进制串
2. 看二进制串前面有几个连续的 0
   - "0001..." → 3 个前导零
   - "000001..." → 5 个前导零
3. 记录"见过的最长前导零长度"
4. 如果见过最长是 N 个前导零 → 大概见过 2^N 个不同元素

为什么有效？
  哈希值是随机的，出现 1 个前导零的概率 = 1/2
  出现 2 个前导零的概率 = 1/4
  出现 K 个前导零的概率 = 1/2^K
  → 如果见过 K 个前导零，大概穷举了 2^K 次

实际上用了 16384 个桶 + 调和平均数来提高精度
```

#### 命令

```bash
# 添加元素
PFADD page:home:uv "user:10086"
PFADD page:home:uv "user:10086" "user:10087" "user:10088"
# → 1 = 至少一个元素是新的；→ 0 = 全部重复

# 查基数
PFCOUNT page:home:uv                # → 3（估算值）

# 合并多个 HLL（跨天合并 UV，自动去重！）
PFADD page:uv:0606 "user:1" "user:2" "user:3"
PFADD page:uv:0607 "user:2" "user:3" "user:4"
PFMERGE page:uv:total page:uv:0606 page:uv:0607
PFCOUNT page:uv:total               # → 4（user:1/2/3/4）
```

#### 关键参数

| 特性 | 值 |
|------|-----|
| 标准误差 | 0.81% |
| 内存占用 | 固定 12 KB（每个 key） |
| 计数上限 | 2^64（几乎无穷） |
| 能删元素吗 | ❌（只能加不能减） |
| 能查具体元素吗 | ❌（只知道总数） |
| 命令前缀 | PF = Philippe Flajolet（发明者） |

---

### 11.2 Bloom Filter — 布隆过滤器

**解决问题：判断一个元素「绝对不存在」还是「可能存在」。**

#### 核心原理

```
两个特性：
  ✅ 说「不存在」→ 100% 准确（绝对不会漏）
  ⚠️ 说「可能存在」→ 有小概率误判（误判率可配置）

工作原理：
  1. 一个很长的比特数组（全 0）
  2. K 个哈希函数
  3. 加入元素 → 算 K 个哈希 → 把 K 个比特位都设成 1
  4. 查询元素 → 算 K 个哈希 → 检查对应 K 个位是否全是 1
     - 全是 1 → 可能存在（可能别的元素碰巧也设了这些位）
     - 有 0 → 绝对不存在（100% 准确）
```

#### 命令

```bash
# 创建（需指定误判率和预计元素数量）
BF.RESERVE users 0.001 1000000        # 0.1% 误判，预计 100 万元
# → OK                                 # 一旦创建，容量锁定

# 添加
BF.ADD users "张三"
BF.MADD users "张三" "李四" "王五"    # 批量

# 查询
BF.EXISTS users "张三"                # → 1（可能存在）
BF.EXISTS users "赵六"                # → 0（绝对不存在）
BF.MEXISTS users "张三" "赵六" "王二"  # → [1, 0, 0]

# 查看信息
BF.INFO users
# ⚠️ 布隆过滤器不能删除！用 Cuckoo Filter
```

#### 容量计算参考

| 预计元素数 | 误判率 | 内存占用 |
|-----------|--------|---------|
| 100 万 | 1% | ~1.14 MB |
| 100 万 | 0.1% | ~1.71 MB |
| 100 万 | 0.01% | ~2.28 MB |
| 1 亿 | 0.01% | ~228 MB |
| 10 亿 | 0.01% | ~2.28 GB |

#### 实战：防止缓存穿透

```python
def login(username, password):
    # 第一关：布隆过滤器（内存检查）
    if not r.bf().exists("registered_users", username):
        return "用户不存在"  # ← 100% 准确，不查数据库！

    # 第二关：数据库（只有布隆说"可能存在"才查）
    user = db.query(username)
    if user and check_password(user, password):
        return "登录成功"
    return "密码错误"  # 或用户真的不存在（布隆误判，极少数情况）

# 攻击者想用大量不存在用户名拖垮 DB → 布隆全拦
```

---

### 11.3 Cuckoo Filter — 布谷鸟过滤器

**解决问题：Bloom 能做的都能做，还支持删除和计数。**

#### 为什么叫"布谷鸟"？

```
布谷鸟把自己的蛋下到别的鸟巢，把原来的蛋挤走。

Cuckoo Filter 类似：
  1. 对元素算哈希 → 找到两个候选「巢位」
  2. 任意一个巢位空着 → 放进去
  3. 两个巢位都满了 → 随机挤走一个旧元素，放到旧元素的另一个巢位
  4. 被挤走的如果也没位置 → 继续挤……直到找到空位
  5. 挤太多次还是没找到 → 插入失败（需要扩容）
```

#### 命令

```bash
CF.RESERVE users 1000000               # 预计 100 万
CF.RESERVE users 1000000 \
    BUCKETSIZE 4 \
    MAXITERATIONS 20 \
    EXPANSION 1

CF.ADD users "张三"                    # → 1（成功）
CF.ADD users "张三"                    # → 0（已存在）
CF.ADDNX users "张三"                  # 不存在才加
CF.MADD users "张三" "李四" "王五"
CF.EXISTS users "张三"                 # → 1
CF.DEL users "张三"                    # 可以删除！Bloom 做不到
CF.COUNT users "张三"                  # 比 CF.EXISTS 更准
CF.INFO users
```

#### Bloom vs Cuckoo

| | Bloom | Cuckoo |
|---|-------|--------|
| 能否删除 | ❌ | ✅ |
| 查询速度 | 快 | 更快（少量元素） |
| 插入速度 | 快 | 可能慢（需挤位） |
| 空间效率 | 更高 | 稍低 |
| 扩容 | ❌ 需重建 | ✅ 动态扩容 |

---

### 11.4 Count-Min Sketch — 频率估算

**解决问题：估算"某个元素出现了多少次"。**

#### 核心原理

```
想象一个矩阵：[深度 D 行] × [宽度 W 列]

1. 元素来了 → 用 D 个不同哈希函数各映射到一列 → 对应格子 +1
2. 查询频率 → 用 D 个哈希算出 D 列 → 取最小值为估算频率

为什么取最小值？
  因为哈希冲突只会让计数偏大（永远不会偏小！）
  取最小值 → 最接近真实值

重要性质：估算值 ≥ 真实值（永远不会低估）
  → 适合"上限判断"：估算值都没超过限制，真实值肯定也没超过
```

#### 命令

```bash
CMS.INITBYPROB views 0.001 0.01       # 误差率 置信度
CMS.INITBYDIM views 2000 10           # 宽度 深度
CMS.INCRBY views "video:1" 1          # 计数 +1
CMS.INCRBY views "video:1" 5          # +5
CMS.QUERY views "video:1"             # → 6（估算值，≥ 真实值）
CMS.MERGE total 2 views_day1 views_day2  # 合并
```

---

### 11.5 Top-K — 热门排行榜

**解决问题：只维护 K 个最热门的，用极小的恒定内存。**

```bash
TOPK.RESERVE trending 100
TOPK.ADD trending "hamburger" "pizza" "sushi"
TOPK.INCRBY trending pizza 5 sushi 3
TOPK.LIST trending                    # → ["pizza", "sushi", "hamburger"]
TOPK.QUERY trending "pizza"           # → 排名 + 近似计数
TOPK.COUNT trending "pizza"           # → 12（计数）
```

---

### 11.6 t-digest — 分位数估算

**解决问题：快速估算数据集的百分位数（P50/P95/P99），用极少内存。**

#### 核心原理

```
1. 把数据分布用很少的「质心」+ 权重来近似
2. 数据密集的地方 → 质心多、精度高
3. 数据稀疏的地方 → 质心少
4. 查询百分位 → 遍历质心累加权重

就像把直方图压缩成关键的几个柱子：
  直方图 1000 个柱子 → t-digest 100 个质心
  估算 P99 仍然很准（这个区域质心密度高）
```

#### 命令

```bash
TDIGEST.CREATE latencies 100           # 压缩因子（越大越准）
TDIGEST.ADD latencies 15.2 23.7 45.1
TDIGEST.QUANTILE latencies 0.5         # P50（中位数）
TDIGEST.QUANTILE latencies 0.95        # P95
TDIGEST.QUANTILE latencies 0.5 0.95 0.99  # 三个一起查

# 反向：这个值排在第几百分位
TDIGEST.CDF latencies 50               # 值 50 在 P72 左右

TDIGEST.MIN latencies / TDIGEST.MAX latencies
TDIGEST.TRIMMED_MEAN latencies 0.1 0.9 # 去掉首尾 10% 的均值
TDIGEST.MERGE all 2 day1 day2          # 合并
```

---

<!-- ═══════════════════════════════════════════════════════ -->
<!--  第三部分：扩展模块类型                                    -->
<!-- ═══════════════════════════════════════════════════════ -->

---

## 第 12 章：JSON

### 12.1 是什么？

JSON 是 Redis 的**文档数据类型**，让你像操作 MongoDB 那样在 Redis 里直接读写 JSON 文档。

> **JSON = 在 Redis 里存一棵 JSON 树，可以只读/改其中一个叶子节点**

### 12.2 和 String 存 JSON 的本质区别

```bash
# ❌ String 存 JSON 的问题
SET user:10086 '{"name":"张三","profile":{"age":28,"city":"北京"}}'
# 要改 city？
# → GET 整条 → 反序列化 → 改字段 → 序列化 → SET 整条
# 10KB JSON 改一个字段 → 网络传 20KB（取一遍改一遍）

# ✅ JSON 类型
JSON.SET user:10086 $ '{"name":"张三","profile":{"age":28,"city":"北京"}}'
JSON.SET user:10086 $.profile.city '"上海"'
# → OK，网络只传几十字节
# String 搬树，JSON 摘叶
```

### 12.3 JSONPath — JSON 的寻址语言

```
数据：
{
  "name": "张三",
  "profile": {"age": 28, "city": "北京"},
  "tags": ["redis", "python", "mongodb"],
  "orders": [
    {"id": 1, "amount": 100},
    {"id": 2, "amount": 200}
  ]
}

JSONPath：
  $                          → 根
  $.name                     → "张三"
  $.profile.age              → 28
  $.tags[0]                  → "redis"
  $.tags[-1]                 → "mongodb"
  $.tags[*]                  → 数组所有元素
  $.orders[*].amount         → [100, 200]
  $.orders[?(@.amount>150)]  → {"id":2,"amount":200}（条件过滤）
  $..city                    → 递归搜所有层级的 city
```

### 12.4 增

```bash
# 创建 JSON 文档
JSON.SET user:10086 $ '{"name":"张三","age":28,"city":"北京"}'

# 设置嵌套路径（中间节点自动创建）
JSON.SET user:10086 $.profile.age '28'
JSON.SET user:10086 $.profile.skills '["redis","python"]'

# 条件创建
JSON.SET user:99999 $ '{"name":"新用户"}' NX   # 不存在才创建
JSON.SET user:10086 $.age '29' XX              # 存在才更新

# 数组追加
JSON.ARRAPPEND store:1 $.products '"redis"'
JSON.ARRAPPEND store:1 $.products '"mongodb"' '"mysql"'

# 数组插入
JSON.SET colors $ '["红","绿","蓝"]'
JSON.ARRINSERT colors $ 1 '"黄"'               # 索引 1 插入，后面后移
```

### 12.5 删

```bash
JSON.DEL user:10086 $.temp_token              # 删除字段
JSON.ARRPOP user:10086 $.tags                  # 弹最后
JSON.ARRPOP user:10086 $.tags 0                # 弹第一个
JSON.ARRTRIM user:10086 $.tags 0 4             # 只保留索引 0~4
```

### 12.6 改

```bash
JSON.SET user:10086 $.name '"李四"'            # 更新值
JSON.NUMINCRBY user:10086 $.age -1             # 年龄 -1（原子！）
JSON.STRAPPEND user:10086 $.name "先生"        # 字符串追加
```

### 12.7 查

```bash
JSON.GET user:10086 $                          # 全部
JSON.GET user:10086 $.name                     # → ["张三"]（路径结果）
JSON.GET user:10086 $.name $.age               # 多个路径
JSON.MGET user:10086 user:10087 $.name         # 批量多 key
JSON.TYPE user:10086 $.name                    # → "string"
JSON.STRLEN user:10086 $.name                  # 字符串长度
JSON.ARRLEN user:10086 $.tags                   # 数组长度
JSON.OBJLEN user:10086 $                       # 对象字段数
JSON.OBJKEYS user:10086 $                      # 所有字段名
```

### 12.8 JSONPath 高级过滤

```bash
# 所有电子类产品
JSON.GET products '$[?(@.category=="电子")]'

# price > 100 的商品名
JSON.GET products '$[?(@.price>100)].name'

# price 在 50~100 之间的
JSON.GET products '$[?(@.price>=50 && @.price<=100)]'

# 递归搜索
JSON.GET store '$..手机'                       # 不管在哪层，找到手机
JSON.GET store '$..price'
```

### 12.9 JSON vs Hash 选型

```
扁平字段 → Hash（更快、更省内存）
嵌套结构/数组 → JSON（Hash 做不到）
需要数组操作（追加/插入/弹出）→ JSON
需要条件过滤 → JSON（JSONPath 过滤）
需要单字段原子增减 → 都可以（HINCRBY / JSON.NUMINCRBY）
```

---

## 第 13 章：Time Series（时序数据）

### 13.1 是什么？

> **Time Series = 专门为「按时间顺序排列的数据」设计的类型**
> 存一组带时间戳的数值，内置降采样、聚合、自动过期

### 13.2 和 Sorted Set/Stream 的本质区别

```
Sorted Set 存时序：
  ❌ 没降采样（想看每小时汇总？自己算）
  ❌ 没自动过期（旧数据手动删？）
  ❌ 相同时间戳会覆盖

Stream 存时序：
  ❌ 没聚合（AVG/MAX/MIN）
  ❌ 没降采样
  ❌ 空间占用相对大

Time Series：
  ✅ 自动降采样（原始→分钟→小时→天）
  ✅ 自动过期（RETENTION）
  ✅ 标签系统（多维查询）
  ✅ 11 种聚合类型
```

### 13.3 增 — TS.ADD / TS.MADD

```bash
# 最简单：* = 自动用当前时间
TS.ADD temperature:room1 * 23.5
# → (integer) 1717760000000  ← 返回写入的时间戳

# 指定时间戳
TS.ADD temperature:room1 1717760000000 23.5

# 创建时指定配置（只首次调用有效）
TS.ADD temperature:room1 * 23.5 \
    RETENTION 86400000 \                       # 保留 1 天（毫秒）
    ON_DUPLICATE last \                        # 同一毫秒多条→保留最后
    LABELS sensor "temp" room "101"            # 标签

# 批量添加
TS.MADD temperature:room1 * 23.5 \
          temperature:room2 * 24.0 \
          temperature:room3 * 22.8
```

### 13.4 保留策略（RETENTION）

```bash
# 保留时长单位：毫秒
1 秒     = 1000
1 分钟   = 60000
1 小时   = 3600000
1 天     = 86400000
7 天     = 604800000
30 天    = 2592000000
```

### 13.5 重复时间戳策略（ON_DUPLICATE）

```bash
ON_DUPLICATE last     # 保留最后一个值
ON_DUPLICATE first    # 保留第一个值
ON_DUPLICATE min      # 保留最小值
ON_DUPLICATE max      # 保留最大值
ON_DUPLICATE sum      # 求和
```

### 13.6 查

```bash
TS.GET temperature:room1                      # 最新值
TS.MGET FILTER sensor=temp                    # 按标签批量取最新
TS.RANGE temperature:room1 - + COUNT 5       # 最新 5 条
TS.REVRANGE temperature:room1 - + COUNT 5    # 反向
TS.INFO temperature:room1                     # 元信息
TS.QUERYINDEX sensor=temp                     # 按标签查 key 名

# ═══ 聚合查询（最核心！）═══
# 每小时平均温度
TS.RANGE temperature:room1 - + AGGREGATION avg 3600000

# 聚合类型：
avg    → 平均值           sum    → 总和
min    → 最小值           max    → 最大值
range  → max - min        count  → 样本数
first  → 第一个值          last   → 最后一个值
std.p  → 总体标准差        std.s  → 样本标准差
var.p  → 总体方差          var.s  → 样本方差
twa    → 时间加权平均（更准！非均匀采样时用 twa 而不是 avg）
```

### 13.7 自动降采样（最强功能！）

```bash
# 原始数据保留 1 天
TS.CREATE cpu:server1 RETENTION 86400000 LABELS host server1 metric cpu

# 小时聚合保留 30 天
TS.CREATE cpu:server1:hourly RETENTION 2592000000

# 天聚合保留 365 天
TS.CREATE cpu:server1:daily RETENTION 31536000000

# 建规则：每次写原始数据→自动聚合到降采样 key
TS.CREATERULE cpu:server1 cpu:server1:hourly AGGREGATION avg 3600000
TS.CREATERULE cpu:server1:hourly cpu:server1:daily AGGREGATION max 86400000

# 删除规则
TS.DELETERULE cpu:server1 cpu:server1:hourly

# 数据流：
#   原始(10秒) 保留 1 天
#       ↓ 自动
#   小时聚合   保留 30 天
#       ↓ 自动
#   天聚合     保留 365 天
```

### 13.8 标签系统

```bash
# 创建时打标签
TS.CREATE cpu:server1 LABELS host server1 region cn type cpu
TS.CREATE cpu:server2 LABELS host server2 region cn type cpu
TS.CREATE mem:server1 LABELS host server1 region cn type mem

# 按标签查
TS.MGET FILTER type=cpu                        # 所有 CPU 指标
TS.MGET FILTER host=server1                    # server1 所有指标
TS.MGET FILTER type=cpu region=cn              # 中国区所有 CPU
TS.MRANGE - + FILTER type=cpu                 # 按标签范围查
```

---

## 第 14 章：Vector Sets（向量集）

### 14.1 先理解"向量"—— 从傻瓜比喻开始

#### 比喻一：用数字打分来描述东西

```
我问你：苹果和橘子像不像？

传统方法（分类）：
  苹果 = "水果"，橘子 = "水果" → "一样！"
  太粗糙！橘子和苹果能一样吗？

向量方法（多维度打分）：
  苹果 = [甜度:7, 酸度:3, 脆度:8, 多汁:6, 大小:5]
  橘子 = [甜度:6, 酸度:5, 脆度:2, 多汁:8, 大小:4]

  每个维度比较 → 总体算相似度 → 苹果和橘子"有几分像"
```

#### 比喻二：高维空间坐标

```
把每个东西变成高维空间的一个点：

  苹果 = (7, 3, 8, 6, 5)
  橘子 = (6, 5, 2, 8, 4)
  椅子 = (0, 0, 0, 0, 1)

  苹果和橘子坐标近 → "有点像"
  苹果和椅子坐标远 → "完全不搭边"

  3 维你可以画出来：(2, 5, 1) → 三维空间的一个点
  768 维你画不出来，但数学上它就是高维空间的一个点
  高维坐标越近 → 语义越像
```

#### 比喻三：你无法名状的"像"

```
问题是这样的：
  你有一篇"Redis 持久化 RDB 和 AOF 详解"的文章
  用户问："请问 Redis 怎么把数据存到磁盘上？"

传统关键词搜索（字面匹配）：
  搜"存到磁盘" → 那篇文章里没有这五个字 → 搜不到！
  但文章就是在讲"持久化"！

向量搜索（语义匹配）：
  把问题和文章分别变成向量（768 个数字）→ 算距离 → 很近！
  因为语义相近，所以向量坐标相近 → 找到了
```

### 14.2 什么是 Redis Vector Sets？

```
Redis 里新的一种集合类型：

key: "kb:articles"
┌─────────────────────────────────────────────────────────┐
│  元素 doc:1                                             │
│  ├─ 向量: (0.1, -0.3, 0.7, -0.2, 0.5, ...  768个数字)  │
│  └─ 属性: {"title":"Redis持久化","category":"database"}  │
│                                                         │
│  元素 doc:2                                             │
│  ├─ 向量: (0.2, -0.1, 0.5, 0.3, -0.4, ...  768个数字)  │
│  └─ 属性: {"title":"Python异步编程","category":"编程"}    │
│                                                         │
│  元素 doc:3                                             │
│  ├─ 向量: (-0.1, 0.4, -0.2, 0.8, 0.1, ...  768个数字)  │
│  └─ 属性: {"title":"Redis集群","category":"database"}    │
└─────────────────────────────────────────────────────────┘

每个元素 = 一个名字 + 一个向量（N 个浮点数） + 可选的 JSON 属性

核心操作：VSIM →"谁离这个查询向量最近？"
```

### 14.3 VSIM 是怎么"找最像的"？

```
简化到 2 维理解：

  向量 A = (3, 4)
  向量 B = (0, 0)
  向量 C = (100, 200)

欧氏距离：
  A-B = √(3²+4²) = 5      ← 很近
  A-C = √(97²+196²) ≈ 218 ← 很远

Redis Vector Sets 用的相似度：
  - 默认用余弦相似度（cosine similarity）
  - 不看向量长度，看方向
  - 同一方向 → 1.0（最像）
  - 垂直 → 0（无关）
  - 相反 → -1.0（最不像）

实际用的是 HNSW 算法（Hierarchical Navigable Small World）
  - 不跟所有向量比（那样太慢），用图索引结构快速定位
  - 毫秒级返回，千万级向量也没问题
```

### 14.4 为什么需要向量数据库？—— AI 时代的刚需

```
RAG（检索增强生成）流程：

用户问："Redis 怎么做高可用？"
    │
    ▼
① Embedding 模型 → 把问题变成 768 个数字（向量）
    │
    ▼
② Redis VSIM → 找最相关的 5 篇文章（毫秒级）
    │
    ▼
③ VGETATTR → 拿到文章标题和内容
    │
    ▼
④ [问题 + 这些文章内容] → 拼成 Prompt → 喂给 LLM
    │
    ▼
⑤ LLM：基于这些真实资料回答（不是瞎编的）

Redis Vector Sets 负责的就是 ② 和 ③：
  从海量文档里毫秒级找到语义最相关的那几篇
```

### 14.5 增 — VADD

```bash
# 语法：VADD key element_name VALUES v1 v2 ... [ATTRIBUTES json]

# 添加向量
VADD articles doc:1001 \
    VALUES 0.1 -0.3 0.7 0.8 -0.2 -0.1 0.5 0.3

# 带属性（JSON 元数据）
VADD articles doc:1002 \
    VALUES 0.2 -0.1 1.5 0.3 0.6 -0.3 0.9 -0.2 \
    ATTRIBUTES '{"title":"Redis持久化","url":"/redis-persist","category":"database","score":95}'

# 如果元素已存在 → 更新向量和属性
```

### 14.6 删 — VREM

```bash
VREM articles doc:1001                    # → (integer) 1
VREM articles doc:1002 doc:1003           # → (integer) 2
```

### 14.7 查 — VCARD / VDIM / VEMB

```bash
VCARD articles                            # → 10234（多少向量）
VDIM articles                             # → 768（向量维数）
VEMB articles doc:1001                    # 取向量值
VEMB articles doc:1001 VALUES             # 浮点数格式
VEMB articles doc:1001 VALUES COUNT 3     # 前 3 维
VEMB articles doc:1001 BLOB               # 二进制精确值
```

### 14.8 属性 — VSETATTR / VGETATTR

```bash
VSETATTR articles doc:1001 \
    '{"title":"Redis持久化","author":"张三","tags":["redis","db"]}'

VGETATTR articles doc:1001                # 全部属性
VGETATTR articles doc:1001 $.title $.author  # 指定字段
```

### 14.9 VSIM — 相似度搜索（核心中的核心！）

```bash
# ═══ 基本搜索 ═══
# 方式 1：用库里已有的元素
VSIM articles ELE doc:1001
# → 返回和 doc:1001 最像的元素（按相似度从高到低）

# 方式 2：给原始向量值
VSIM articles VALUES 0.1 -0.3 0.7 0.8 -0.2 -0.1 0.5 0.3

# ═══ 带相似度分数 ═══
VSIM articles ELE doc:1001 WITHSCORES
# → 1) "doc:1001"  2) "1.000"     ← 自己和自己的相似度 = 1.0
#    2) "doc:1056"  2) "0.9234"
#    3) "doc:2031"  2) "0.8912"

# ═══ 限制数量 ═══
VSIM articles ELE doc:1001 COUNT 5 WITHSCORES

# ═══ 属性过滤（混合搜索！最强功能）═══
# 语义相似 + 精确筛选
VSIM articles ELE doc:1001 \
    COUNT 5 WITHSCORES \
    FILTER '@category == "database"'

VSIM articles ELE doc:1001 \
    COUNT 10 \
    FILTER '@category == "database" && @score > 80'

VSIM articles ELE doc:1001 \
    COUNT 10 \
    FILTER '@score >= 85 && @reviewed == true'

# ═══ 用原始向量 + 属性过滤 ═══
VSIM articles VALUES 0.1 -0.3 0.7 ... \
    COUNT 5 WITHSCORES \
    FILTER '@category == "database" && @year > 2023'
```

### 14.10 Filter Expressions 完整语法

```bash
# 比较运算符
==   !=   >   >=   <   <=

# 逻辑运算符
&&   ||   !

# 字符串
@name == "张三"                         # 精确匹配
@name IN ("张三", "李四", "王五")        # 在列表中
@name CONTAINS "三"                     # 包含子串
@name STARTSWITH "张"                   # 开头是

# 数字范围
@score BETWEEN 70 90                    # 70 ≤ score ≤ 90

# 数组
@tags CONTAINS "redis"                  # 数组包含某值
@tags LENGTH 3                          # 数组长度

# 空值
@field EXISTS / @field ISNULL
```

### 14.11 Python 完整实战：RAG 知识库

```python
import redis
import numpy as np
import hashlib
import json

r = redis.Redis(decode_responses=True)

def mock_embed(text):
    """模拟 embedding：把文字变成 768 维向量"""
    seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
    np.random.seed(seed)
    return np.random.randn(768).astype(np.float32).tolist()

# ═══════════ 1. 创建知识库 ═══════════
articles = [
    {"id": "art:1", "title": "Redis 持久化 RDB 和 AOF 详解",
     "content": "Redis 有两种持久化...", "category": "database", "score": 95},
    {"id": "art:2", "title": "Redis Cluster 分片原理",
     "content": "Redis Cluster 使用哈希槽...", "category": "database", "score": 90},
    {"id": "art:3", "title": "Python 异步编程入门",
     "content": "asyncio 是 Python 的...", "category": "programming", "score": 72},
    {"id": "art:4", "title": "如何选择 Redis 持久化方案",
     "content": "缓存用 RDB，核心数据用 AOF...", "category": "database", "score": 88},
]

for art in articles:
    vector = mock_embed(art["content"])
    attrs = {"title": art["title"], "category": art["category"],
             "tags": art.get("tags", []), "score": art["score"]}
    r.execute_command("VADD", "kb:articles", art["id"],
        "VALUES", *vector,
        "ATTRIBUTES", json.dumps(attrs))

print(f"知识库：{r.execute_command('VCARD', 'kb:articles')} 篇文章")
print(f"维度：{r.execute_command('VDIM', 'kb:articles')}")

# ═══════════ 2. 语义搜索 ═══════════
def semantic_search(query, top_k=3, category=None):
    """用户问问题 → 找最相关的文章"""
    query_vector = mock_embed(query)
    cmd = ["VSIM", "kb:articles", "VALUES", *query_vector,
           "COUNT", top_k, "WITHSCORES"]
    if category:
        cmd.extend(["FILTER", f'@category == "{category}"'])
    result = r.execute_command(*cmd)

    results = []
    for i in range(0, len(result), 2):
        element_name = result[i]
        score = float(result[i + 1])
        attrs = r.execute_command("VGETATTR", "kb:articles", element_name)
        results.append({"id": element_name, "similarity": round(score, 4),
                        "title": attrs.get("title", ""),
                        "category": attrs.get("category", "")})
    return results

# 测试
result = semantic_search("Redis 怎么把数据存到磁盘上？", top_k=3)
for r in result:
    print(f"  [{r['similarity']}] {r['title']} ({r['category']})")

# ═══════════ 3. 按已存元素推荐 ═══════════
def recommend_similar(article_id, top_k=3):
    """看了这篇文章 → 推荐和它最像的（不用重新 embed！）"""
    result = r.execute_command(
        "VSIM", "kb:articles", "ELE", article_id,
        "COUNT", top_k + 1, "WITHSCORES")
    # 跳过第一个（它自己）
    for i in range(2, len(result), 2):
        element_name = result[i]
        score = float(result[i + 1])
        attrs = r.execute_command("VGETATTR", "kb:articles", element_name)
        print(f"  [{score:.4f}] {attrs.get('title')}")
```

### 14.12 VSIM 四大参数

```
VSIM key
  ELE element              ← 用库里元素做查询（二选一）
  VALUES v1 v2 ...         ← 给原始向量做查询（二选一）
  COUNT n                  ← 返回几条
  WITHSCORES               ← 带相似度分数
  FILTER 'expression'      ← 属性过滤（混合搜索）
  EF_RUNTIME n             ← 搜索广度（越大越准但越慢）
  TIMEOUT ms               ← 超时时间
```

### 14.13 Redis Vector Sets vs 其他向量数据库

| | Redis | Milvus | Pinecone | Weaviate | Qdrant |
|---|-------|--------|----------|----------|--------|
| 速度 | ★★★★★ 最快 | ★★★★ | ★★★ | ★★★★ | ★★★★ |
|     | (内存原生)                |        |           |           |        |
| 部署 | ★★★★★ 已有 Redis 即可 | 另部署 | 云服务 | 另部署 | 另部署 |
| 混合搜索 | ★★★★★ VSIM+FILTER | ★★★★ | ★★★★ | ★★★★★ | ★★★★ |

Redis Vector Sets 最大优势：**如果你已经在用 Redis，加向量功能零额外成本。**

### 14.14 企业应用全景

```
🔍 智能客服    → 问题→向量→VSIM 找FAQ→AI回答
📚 RAG 知识库  → 文档→向量→用户提问→VSIM 检索→喂LLM
🛒 商品推荐    → 用户行为→向量→VSIM 找相似商品
🖼️ 以图搜图    → 图片→CLIP→向量→VSIM
🎵 内容推荐    → 内容特征→向量→VSIM 快速召回
🔐 人脸/声纹   → 生物特征→向量→VSIM 匹配
🧠 Agent 记忆  → 对话摘要→向量→VSIM 召回历史
```

---

## 第 15 章：Arrays

### 15.1 是什么？

Arrays 是 JSON 类型的补充，提供更便捷的 JSON 数组操作。

```
Arrays 不能独立存在，依附于 JSON 类型
命令前缀是 ARR.XXX，等价于 JSON.ARRXXX 系列
```

### 15.2 命令一览

```bash
ARR.APPEND key path value [value ...]   # 追加
ARR.INSERT key path index value [...]   # 插入
ARR.POP    key path [index]            # 弹出
ARR.TRIM   key path start stop         # 修剪
ARR.INDEX  key path value [start]      # 查找索引
ARR.LEN    key path                    # 数组长度
```

### 15.3 List vs JSON 数组选型

```
简单字符串列表/队列 → List（LPUSH/RPOP，最快）
对象列表 + 需要查字段 → JSON 数组 + JSONPath
需要数组内查找索引 → Arrays（ARR.INDEX）
需要嵌套结构 → JSON + Arrays
```

---

## 第 16 章：Pub/Sub（发布订阅）

### 16.1 是什么？

**PUBLISH = 广播消息，SUBSCRIBE = 收听频道。** 就像微信群聊——在群里发消息，群友都能收到，不在线就错过了。

### 16.2 三个关键特点（面试高频）

| 特性 | 说明 |
|------|------|
| 🔥 即发即忘 | 消息不持久化，发了就不管 |
| 📡 一对多广播 | 一个发布者 → 所有订阅者 |
| ⚡ 实时推送 | 阻塞等待，无需轮询 |
| 🚫 无历史消息 | 离线就收不到，没有回溯 |

### 16.3 命令

```bash
# 订阅
SUBSCRIBE news                    # 订阅频道（阻塞等待）
PSUBSCRIBE news.*                 # 模式订阅（通配符）
PSUBSCRIBE user:*:message         # 所有 user:*:message 频道

# 广播
PUBLISH news "消息内容"           # → (integer) 3 ← 3 个订阅者收到

# 退订
UNSUBSCRIBE news                  # 退订指定频道
UNSUBSCRIBE                       # 退订所有
PUNSUBSCRIBE news.*               # 退订模式

# 查询
PUBSUB CHANNELS                   # 活跃频道
PUBSUB NUMSUB news                # 频道订阅数
PUBSUB NUMPAT                     # 模式订阅数
```

### 16.4 重要限制

```
1. 订阅后连接进入"订阅模式"
   → 只能做 SUBSCRIBE/UNSUBSCRIBE/PING
   → 不能 GET/SET → 需要专用连接！

2. 消息不持久化 → 离线收不到

3. 缓冲区溢出 → 订阅者处理太慢 → 断开
   解决：订阅线程只负责收，扔给工作线程处理
```

---

<!-- ═══════════════════════════════════════════════════════ -->
<!--  第五部分：事务与持久化                                    -->
<!-- ═══════════════════════════════════════════════════════ -->

---

## 第 17 章：事务

### 17.1 是什么？

> **Redis 事务 = 把一组命令打包，排队执行，不被打断。**
> 它不是"出错就回滚"，而是**隔离性有，但没有回滚**。

### 17.2 基本流程

```bash
MULTI                   # 开启事务（进入队列模式）
SET account:A 100       # 排队，不执行
SET account:B 50        # 排队，不执行
INCRBY account:A -30    # 排队，不执行
INCRBY account:B 30     # 排队，不执行
EXEC                    # 一口气全部执行
# → 1) OK  2) OK  3) (integer) 70  4) (integer) 80

# 放弃
DISCARD                 # 清空队列，不执行
```

### 17.3 五种特殊情况

```bash
# ① 正常：全部成功
# ② 入队时语法错误：整个事务不执行！
# ③ 入队成功、执行时单个报错：报错的跳过，其余照常执行（不回滚！）
# ④ WATCH 被触发：EXEC 返回 nil，全部不执行
# ⑤ 连接断开：队列清空
```

### 17.4 WATCH — 乐观锁（CAS）

`WATCH` 监视 key，如果在 WATCH 之后、EXEC 之前 key 被其他客户端改过 → EXEC 返回 nil。

```python
def transfer(from_acc, to_acc, amount, max_retries=3):
    for attempt in range(max_retries):
        r.watch(from_acc, to_acc)
        balance = int(r.get(from_acc) or 0)
        if balance < amount:
            r.unwatch()
            return False, "余额不足"

        pipe = r.pipeline()          # pipeline 内部包含 MULTI
        try:
            pipe.decrby(from_acc, amount)
            pipe.incrby(to_acc, amount)
            pipe.execute()           # EXEC
            return True, "转账成功"
        except redis.WatchError:
            print(f"冲突！第 {attempt+1} 次重试...")
            continue
    return False, "转账失败"
```

### 17.5 事务 vs Lua 脚本

| | 事务 | Lua 脚本 |
|---|------|----------|
| 原子性 | ✅ | ✅ |
| 隔离性 | ✅ | ✅ |
| 回滚 | ❌ | ❌ |
| 条件判断 | ❌（MULTI 里不能读） | ✅（if/else） |
| 中间结果 | ❌ | ✅（变量传递） |

```
需要条件判断 → Lua 脚本
需要并发安全 → WATCH + 事务
需要简单批量写 → 裸事务
```

---

## 第 18 章：持久化

### 18.1 两种方式

| | RDB | AOF |
|---|-----|-----|
| 方式 | 定期全量快照 | 逐条写日志 |
| 文件 | dump.rdb（二进制压缩） | appendonly.aof（文本） |
| 恢复速度 | 快（直接加载） | 慢（逐条重放） |
| 丢数据 | 可能丢几分钟 | 最多 1 秒（everysec） |
| 性能影响 | fork 时短暂 | 持续 IO |
| 文件可读 | ❌ | ✅ |
| 备份友好 | ✅ 单文件 | 文件较大 |

### 18.2 RDB 工作原理

```bash
# 触发方式
save 900 1        # 900 秒内 ≥1 次修改
save 300 10       # 300 秒内 ≥10 次修改
save 60 10000     # 60 秒内 ≥10000 次修改

BGSAVE            # 子进程后台快照（生产用这个！）
SAVE              # 主进程快照（阻塞！生产禁用！）

# BGSAVE 的 Copy-On-Write：
# 1. fork 子进程
# 2. 父子共享同一块内存（COW）
# 3. 子进程把数据写磁盘
# 4. 期间主进程有写操作 → 触发 COW，复制被写的那一页
```

### 18.3 AOF 配置

```bash
appendonly yes
appendfsync everysec          # 每秒刷盘（推荐！平衡之选）
# always → 每条刷盘（最安全，最慢，QPS 受磁盘限制）
# no     → OS 决定（快但不安全，可能丢几十秒数据）

auto-aof-rewrite-percentage 100   # 文件翻倍时重写
auto-aof-rewrite-min-size 64mb    # 至少 64MB 才触发

# AOF 重写：把 SET a 1 → SET a 2 → DEL a → SET a 100
# 压缩成 SET a 100，去掉中间步骤
```

### 18.4 混合持久化（企业最佳实践 ⭐）

```bash
# Redis 4.0+
aof-use-rdb-preamble yes

# AOF 重写时：
#   RDB 格式存当前全量数据（快）
#   + AOF 格式存重写期间的增量（完整）

# 文件结构：
# ┌──────────┬──────────┐
# │ RDB 快照  │ AOF 增量 │
# └──────────┴──────────┘

# 恢复：RDB 速度 + AOF 完整性
```

### 18.5 企业场景方案

```
纯缓存 → 可以不持久化（或只开 RDB，用于快速预热）
缓存+少量持久数据 → RDB + AOF 混合模式（推荐！）
核心业务数据 → AOF always + RDB + 主从
大规模 → 主从架构中 Slave 承担 BGSAVE 任务
```

---

<!-- ═══════════════════════════════════════════════════════ -->
<!--  第六部分：高可用与扩展                                    -->
<!-- ═══════════════════════════════════════════════════════ -->

---

## 第 19 章：主从复制

### 19.1 核心概念

```
         ┌─────────────┐
         │   Master    │  ← 唯一写入点
         │  (读写)      │
         └──────┬──────┘
                │ 异步同步
        ┌───────┼───────┐
        ▼       ▼       ▼
    Slave1   Slave2   Slave3  ← 只读，数据副本
```

### 19.2 六大作用

```
① 读写分离（分摊读压力）
② 数据冗余（热备）
③ 高可用基础（Sentinel/Cluster 的前置条件）
④ 备份不阻塞主库（在 Slave 上 BGSAVE）
⑤ 水平扩展读能力
⑥ 地理分布（多地域就近访问）
```

### 19.3 复制的三个阶段

```
1. 首次全量同步（PSYNC ? -1）
   Master BGSAVE → 发 RDB → Slave 加载
   + 发 RDB 期间的增量命令

2. 增量同步（PSYNC replid offset）
   Slave 重连 → Master 从 repl_backlog 找差量补发

3. 持续复制（命令流）
   Master 每执行一个写命令 → 同步发给所有 Slave
```

### 19.4 配置

```bash
# Slave 配置
replicaof 192.168.1.100 6379
masterauth "password"
replica-read-only yes                    # 务必保持！

# Master 必改参数
repl-backlog-size 256mb                  # 默认 1MB 太小！
repl-backlog-ttl 3600                    # Slave 断开后保留 backlog 多久
repl-timeout 60                          # 复制超时

min-replicas-to-write 1                  # 至少 1 个 Slave 在线才写
min-replicas-max-lag 10                  # Slave 延迟 ≤ 10 秒

# repl-backlog-size 怎么定？
# = Master 每秒写入量 × 预期最长断连秒数 × 2
# 例：1MB/s × 60s × 2 = 120MB → 设 256MB 更安全
```

### 19.5 常见问题

```
复制延迟高 → 增大 repl-backlog-size、减少 Slave 数、同机房部署
频繁全量同步 → repl-backlog-size 太小 → 调大
复制风暴 → Master 重启后所有 Slave 同时全量同步 → 树状级联解决
```

---

## 第 20 章：Sentinel（哨兵模式）

### 20.1 是什么？

**一群哨兵盯着 Master，挂了自动选新 Master。**
解决主从复制最大的痛点——Master 挂了要人工处理。

```
至少 3 个 Sentinel，quorum = N/2+1

┌──────────┐ ┌──────────┐ ┌──────────┐
│ Sentinel │ │ Sentinel │ │ Sentinel │
│ :26379   │ │ :26379   │ │ :26379   │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     └─────────────┼─────────────┘
                   │
            ┌──────┴──────┐
            │   Master    │
            └──────┬──────┘
           ┌───────┴───────┐
           ▼               ▼
        Slave1           Slave2
```

### 20.2 故障转移全过程

```
T=0s    Master 进程崩溃
T=30s   down-after-milliseconds 到
        3 个 Sentinel 都标记 SDOWN
        互相确认 → quorum=2 → 标记 ODOWN
T=31s   选 Leader Sentinel
T=32s   Leader 从 Slave 中选新 Master（按优先级→数据最新→runid）
        → REPLICAOF NO ONE → 升级为新 Master
T=33s   通知其他 Slave → REPLICAOF 新 Master
T=34s   故障转移完成！业务恢复

原 Master 复活后 → 自动变成新 Master 的 Slave！
```

### 20.3 配置

```bash
# sentinel.conf（3 台机器同）
port 26379
sentinel monitor mymaster 192.168.1.100 6379 2    # quorum=2
sentinel auth-pass mymaster "password"
sentinel down-after-milliseconds mymaster 30000    # 30s 判定超时
sentinel failover-timeout mymaster 180000          # 3 分钟转移超时
sentinel parallel-syncs mymaster 1                 # 一次同步 1 个

# 启动
redis-sentinel /etc/redis/sentinel.conf
```

### 20.4 Python 客户端

```python
from redis.sentinel import Sentinel

sentinel = Sentinel([
    ('192.168.1.10', 26379),
    ('192.168.1.11', 26379),
    ('192.168.1.12', 26379),
])
master = sentinel.master_for('mymaster', password='xxx')
slave = sentinel.slave_for('mymaster', password='xxx')
# 故障转移自动发现新 Master，代码 0 改动！
```

### 20.5 Sentinel 不解决什么？

```
❌ 不解决分片（数据量太大 → Cluster）
❌ 不解决写扩展（写 QPS 太高 → Cluster）
❌ 不保证零丢失（异步复制）
✅ 解决的是：Master 挂了自动切换，秒级恢复
```

---

## 第 21 章：Redis Cluster（集群模式）

### 21.1 为什么需要 Cluster？— Sentinel 不解决的两个问题

**Sentinel 只解决高可用（Master 挂了自动切），不解决容量和写吞吐：**

```
Sentinel 主从架构的问题：

  1. ❌ 内存容量上限 = 单机内存
     一台机器 256GB → 你的数据集 500GB → Sentinel 救不了
     → 只能存一部分，或者换更大的机器（有上限）

  2. ❌ 写 QPS 上限 = 单机 Master 的写入能力
     Master 一个实例写 10 万 QPS → 业务需要 50 万 QPS → Sentinel 救不了
     → Slave 只能分担读，不能分担写

Cluster 的解法：
  把数据切碎（分片），每个分片各管一部分
  每个分片内部还是一主一从（用 Sentinel 的思路）

  数据分片 → 总容量 = 所有分片之和
  写分片 → 总写 QPS = 所有分片 Master 之和
```

**一张图看懂 Sentinel vs Cluster：**

```
  Sentinel 方案（一主多从）：         Cluster 方案（多分片）：
  
       ┌─────────┐                ┌────┬────┬────┐
       │ Master  │                │ M0 │ M1 │ M2 │  ← 3 个 Master 都能写
       └────┬────┘                └──┬─┘──┬─┘──┬─┘
      ┌─────┼─────┐                │    │    │
      ▼     ▼     ▼                S0   S1   S2   ← 每个 Master 有自己的 Slave
    S1     S2    S3
  
  写只能走 Master               写分散到 3 个 Master
  总容量 = 1 台机器             总容量 = 3 台机器之和
```

---

### 21.2 核心概念：哈希槽（Hash Slot）

**Cluster 不是按 key 名字分片，而是对 key 做哈希后映射到 16384 个槽。**

```
核心公式：slot = CRC16(key) % 16384

  每个 key 归属一个 slot（0~16383）
  每个 Master 节点负责一部分 slot
  客户端算 slot → 找对应的 Master → 发命令

为什么是 16384？
  - 16,384 = 2^14，足够分给 1000 个节点用了
  - 心跳消息里的 slot 位图占 2KB（16,384 bit = 2,048 bytes）
  - 如果是 65,536 → 位图变 8KB，心跳包太大

哈希标签（Hash Tag）— 让多个 key 落同一个 slot：
  user:{10086}:name
  user:{10086}:email
  user:{10086}:orders
  ↑ 只对 {} 里的内容做 CRC16，所以这三个 key 必然在同一个 slot

作用：多 key 操作（MGET/SINTER/ZUNIONSTORE）要求所有 key 在同一个 slot
      用 {} 强制它们在一起 → 多 key 操作才能成功
```

---

### 21.3 Cluster 架构图

```
              ┌──────────────────────────────────────┐
              │           Redis Cluster               │
              │                                       │
              │  ┌─────────┐ ┌─────────┐ ┌─────────┐ │
              │  │ Master0 │ │ Master1 │ │ Master2 │ │
              │  │slot:    │ │slot:    │ │slot:    │ │
              │  │0~5460  │ │5461~   │ │10923~   │ │
              │  │         │ │10922   │ │16383   │ │
              │  └────┬────┘ └────┬────┘ └────┬────┘ │
              │       │          │          │        │
              │  ┌────┴────┐┌────┴────┐┌────┴────┐   │
              │  │ Slave0  ││ Slave1  ││ Slave2  │   │
              │  └─────────┘└─────────┘└─────────┘   │
              │                                       │
              │  每个节点之间互相连接（Gossip 协议）     │
              │  每个节点都知道：谁负责哪些 slot        │
              └──────────────────────────────────────┘

  工作原理：
    1. 客户端连任意一个节点
    2. 发命令 SET user:10086:name "张三"
    3. 节点算 slot = CRC16("user:10086:name") % 16384 = 12345
    4. slot 12345 归 Master1 管 → 返回 MOVED 错误（告诉客户端去 Master1）
    5. 客户端连接 Master1，重发命令 → OK
    6. 客户端缓存 slot 路由表，下次直接连对
```

---

### 21.4 搭建 Cluster（实战）

**最简方式：6 个节点，3 主 3 从。**

```bash
# ═══ 步骤 1：准备 6 个 Redis 实例的配置 ═══
# 假设 6 台机器/6 个端口，以端口为例：
# 7000, 7001, 7002 → Master
# 7003, 7004, 7005 → Slave

# 每个实例的 redis.conf 核心配置：
port 7000
cluster-enabled yes                      # ← 开启集群模式！
cluster-config-file nodes-7000.conf      # 集群拓扑信息文件
cluster-node-timeout 5000                # 节点超时（毫秒）
appendonly yes
requirepass "password"
masterauth "password"

# 每个节点单独启动
redis-server redis-7000.conf
redis-server redis-7001.conf
redis-server redis-7002.conf
redis-server redis-7003.conf
redis-server redis-7004.conf
redis-server redis-7005.conf

# ═══ 步骤 2：创建集群 ═══
# Redis 5.0+ 推荐用 redis-cli：
redis-cli --cluster create \
    192.168.1.10:7000 \
    192.168.1.11:7001 \
    192.168.1.12:7002 \
    192.168.1.13:7003 \
    192.168.1.14:7004 \
    192.168.1.15:7005 \
    --cluster-replicas 1 \
    -a "password"

# --cluster-replicas 1 → 每个 Master 配 1 个 Slave
# redis-cli 自动分配 slot 和主从关系：
#   Master    → 7001/7002/7003，各负责约 5461 个 slot
#   Slave     → 7004/7005/7006，分别对应上面的 Master

# ═══ 步骤 3：验证 ═══
redis-cli -p 7000 -a "password"
127.0.0.1:7000> CLUSTER INFO
# cluster_state:ok
# cluster_slots_assigned:16384
# cluster_slots_ok:16384
# cluster_known_nodes:6
# cluster_size:3

127.0.0.1:7000> CLUSTER NODES
# 列出所有节点：谁负责哪些 slot，谁是 Master 谁是 Slave
```

---

### 21.5 客户端连接 Cluster

**连 Cluster 不能用普通连接方式，要用专门的 Cluster 客户端。**

```python
# ❌ 错误：用普通 Redis 客户端连 Cluster
r = redis.Redis(host='192.168.1.10', port=7000)
r.set('key', 'value')
# → (error) MOVED 12345 192.168.1.11:7001  ← 重定向错误！

# ✅ 正确：用 Cluster 客户端
from redis.cluster import RedisCluster

rc = RedisCluster(
    host='192.168.1.10',   # 种子节点（连一个就行，自动发现全部）
    port=7000,
    password='password',
    # 或者给多个种子节点防止单点故障
    # startup_nodes=[
    #     {'host': '192.168.1.10', 'port': 7000},
    #     {'host': '192.168.1.11', 'port': 7001},
    # ]
)

# 无需关心 slot 路由，客户端自动处理 MOVED 重定向
rc.set('user:10086:name', '张三')
rc.get('user:10086:name')           # → "张三"

# 批量操作：客户端自动按 slot 分组 → 发到对应节点 → 合并结果
rc.mget('user:10086:name', 'user:10087:name', 'user:10088:name')
```

**Cluster 客户端的职责：**

```
1. 连种子节点 → 获取完整的路由表（CLUSTER SLOTS）
2. 每个命令 → 算 key 的 slot → 找对应节点 → 发命令
3. 收到 MOVED → 更新路由表 → 重发命令
4. 缓存路由表在本地 → 避免每次都做路由查找
```

---

### 21.6 MOVED 与 ASK — 重定向机制

```
MOVED（永久重定向）：
  客户端连错节点了
  slot 永久归属另一个节点
  → 客户端应该更新路由表
  → 后续请求直接发给对的节点

ASK（临时重定向）：
  slot 正在从节点 A 迁移到节点 B
  迁移中的 key 暂时在 B，但还没完全迁移完
  → 客户端只对当前这个 key 临时发给 B
  → 不要更新路由表（其他 key 还在 A）

客户端看到的流程：
  SET key value
  → -MOVED 3999 192.168.1.11:7001         ← slot 永久在 7001
  → -ASK 3999 192.168.1.12:7002           ← slot 正在迁移中
```

---

### 21.7 故障转移 — Cluster 自带 Sentinel

**Cluster 不依赖外部 Sentinel，故障转移功能内建在节点之间。**

```
每个节点都在监控其他节点（Gossip 协议）

故障流程：
  1. Master1 宕机
  2. 其他 Master 通过 Gossip 发现 Master1 无响应
  3. 超过 cluster-node-timeout（默认 15 秒）→ 标记为 PFAIL（疑似下线）
  4. 多数 Master 都确认 → 标记为 FAIL（确认下线）
  5. Master1 的 Slave（Slave1）发起选举
  6. 多数 Master 投票同意 → Slave1 升级为新 Master
  7. Slave1 接管 Master1 的 slot
  8. 集群恢复，继续服务

整个过程自动，无需人工介入
和 Sentinel 的思路一样，但内建在节点通信里
```

---

### 21.8 数据迁移与扩缩容

```bash
# ═══ 加新 Master 节点 ═══
# 1. 启动新节点（cluster-enabled yes）
redis-server redis-7006.conf

# 2. 加入集群
redis-cli --cluster add-node 192.168.1.16:7006 192.168.1.10:7000
#              新节点                       现有节点

# 3. 迁移 slot 给新节点
redis-cli --cluster reshard 192.168.1.10:7000
# 交互式：要迁移多少 slot？从哪些节点迁？迁给谁？

# 或者一次性指定：
redis-cli --cluster reshard 192.168.1.10:7000 \
    --cluster-from <source-node-id> \
    --cluster-to <target-node-id> \
    --cluster-slots 1000

# ═══ 加新 Slave 节点 ═══
redis-cli --cluster add-node 192.168.1.17:7007 192.168.1.10:7000 \
    --cluster-slave \
    --cluster-master-id <master-node-id>

# ═══ 删除节点 ═══
# 先迁移走它的 slot（如果是 Master）
redis-cli --cluster reshard ...
# 再删除
redis-cli --cluster del-node 192.168.1.10:7000 <node-id>

# ═══ 在线重分片（reshard）的关键特性 ═══
# 迁移过程中集群照常服务！
# 迁移中的 key 通过 ASK 重定向保证正确访问
```

---

### 21.9 Cluster 的限制

```
1. ❌ 多 key 操作必须在同一 slot
   以下命令只有所有 key 在同一 slot 才能成功：
     MGET / MSET / SINTER / SUNION / SDIFF
     ZINTERSTORE / ZUNIONSTORE
     RENAME（两个 key 要同 slot）
   解决：使用哈希标签 {same_group} 强制同 slot

2. ❌ 不支持多数据库
   SELECT 0 → OK
   SELECT 1 → (error) SELECT is not allowed in cluster mode
   → 只能用 db0

3. ❌ 事务受限
   MULTI/EXEC 只能在同一个节点
   不能跨 slot 的事务

4. ❌ Lua 脚本受限
   EVAL 里的所有 key 必须在同一个 slot
   不能用脚本操作跨 slot 的多个 key

5. ❌ 批量操作不自动分组
   客户端要自己做 slot 分组
   Cluster 客户端（redis-py-cluster）已处理好，不用自己写

6. ❌ Pub/Sub 跨节点广播
   发布到任意节点 → 广播到所有节点
   有额外的网络开销

7. ⚠️ 至少 3 个 Master（建议）
   少于 3 个 Master → 部分 slot 集中 → 单点压力大
   生产建议 3 Master + 3 Slave 起步
```

---

### 21.10 Cluster 命令速查

```bash
# ═══ 集群信息 ═══
CLUSTER INFO                          # 集群状态概览
CLUSTER NODES                         # 所有节点详情
CLUSTER SLOTS                         # slot 分配表
CLUSTER KEYSLOT <key>                 # 算 key 属于哪个 slot
CLUSTER COUNTKEYSINSLOT <slot>        # 某 slot 里有多少 key
CLUSTER GETKEYSINSLOT <slot> <count>  # 取某 slot 的 key 样本

# ═══ 运维操作 ═══
CLUSTER MEET <ip> <port>              # 手动加入集群
CLUSTER FORGET <node-id>              # 踢掉节点
CLUSTER REPLICATE <master-node-id>    # 当前节点成为某 Master 的 Slave
CLUSTER FAILOVER                      # 手动触发故障转移
CLUSTER FAILOVER FORCE               # 强制转移（即使 Master 正常）
CLUSTER RESET [SOFT|HARD]             # 重置集群状态
CLUSTER SETSLOT <slot> IMPORTING/MIGRATING/NODE/STABLE  # 手动迁移 slot

# ═══ redis-cli 集群管理 ═══
redis-cli --cluster create ...        # 创建集群
redis-cli --cluster check <ip:port>   # 检查集群健康
redis-cli --cluster info <ip:port>    # 查看集群信息
redis-cli --cluster reshard ...       # 在线重分片
redis-cli --cluster add-node ...      # 加节点
redis-cli --cluster del-node ...      # 删节点
redis-cli --cluster rebalance ...     # 自动均衡 slot
redis-cli --cluster fix ...           # 修复集群问题
```

---

## 第 22 章：企业架构演进

```
阶段 1：单机
    Redis 单实例 + RDB 持久化
    → 适合开发/小项目

阶段 2：一主一从
    Master + 1 Slave（读写分离 + 备份）
    → 初创期

阶段 3：一主多从
    Master + N 个 Slave（水平扩展读）
    → 增长期

阶段 4：Sentinel 高可用
    3 台 Sentinel + 一主多从（自动故障转移）
    → 成熟期

阶段 5：Cluster 分片
    多分片 + 每分片一主一从（突破内存/写 QPS 上限）
    → 大规模

阶段 6：多地域
    不同地区 Slave + 就近访问
    → 全球化
```

---

## 第 23 章：快速上手 — 四种使用场景

> 根据 Redis 官方 Quick Start 指南，Redis 在现代应用中主要有四种典型使用场景。你已经学过的所有数据类型和功能，最终都是为这四种场景服务的。

### 23.1 场景一：当做数据结构存储（Data Structure Store）

**这是 Redis 最经典、最传统的用法。**

```
把 Redis 当做「内存中的数据结构工具箱」：

你的应用需要什么数据结构 → Redis 提供什么
  - 需要缓存 → String + EXPIRE
  - 需要计数器 → String INCR
  - 需要队列 → List LPUSH/RPOP 或 Stream
  - 需要去重 → Set SADD
  - 需要排行榜 → Sorted Set ZADD/ZREVRANGE
  - 需要存对象 → Hash HSET/HGET
  - 需要实时通知 → Pub/Sub
  - 需要消息队列 → Stream + XREADGROUP
  - 需要签到统计 → Bitmap SETBIT/BITCOUNT
  - 需要附近的人 → Geospatial GEOSEARCH
  - 需要限流 → String INCR + EXPIRE
  - 需要分布式锁 → SET NX EX

关键思路：
  把 Redis 当成内存中的瑞士军刀
  不要把所有数据塞进同一个数据结构
  为每种数据选最合适的 Redis 类型
```

**典型架构：**

```
  ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ 应用服务器 │    │ 应用服务器 │    │ 应用服务器 │
  └─────┬────┘    └─────┬────┘    └─────┬────┘
        └───────────────┼───────────────┘
                        │
              ┌─────────┴─────────┐
              │   Redis 主从/Sentinel│
              │  String + Hash +     │
              │  List + Set + ZSet   │
              └─────────────────────┘
                        │
              ┌─────────┴─────────┐
              │   MySQL / PG      │ ← 持久化存储
              └───────────────────┘

  Redis 负责热数据（缓存/计数/状态/排行榜）
  数据库负责冷数据（历史订单/用户信息/日志）
```

---

### 23.2 场景二：当做文档数据库（Document Database）

**如果你之前用 MongoDB，Redis 可以用 JSON 类型实现类似的体验。**

```
把 Redis 当做文档数据库：

关键类型：JSON + Search（Redis Stack 支持二级索引）

使用方式：
  - JSON.SET 存储文档
  - JSON.GET 查询文档（支持 JSONPath 条件过滤）
  - 用 Search 模块的 FT.CREATE/FT.SEARCH 做全文搜索和聚合

适合数据特征：
  - 文档结构灵活（字段可变）
  - 嵌套层级深（JSON 对嵌套天然支持）
  - 需要部分更新（只改某个嵌套字段）
  - 需要按字段搜索
```

**示例：**

```bash
# 存储商品文档
JSON.SET product:1001 $ '{
  "name": "无线耳机",
  "price": 299,
  "category": "电子产品",
  "specs": {"color": "黑色", "battery": "30小时"},
  "reviews": [
    {"user": "张三", "rating": 5, "comment": "音质很好"},
    {"user": "李四", "rating": 4, "comment": "佩戴舒适"}
  ]
}'

# 只查价格
JSON.GET product:1001 $.price

# 只查评论
JSON.GET product:1001 $.reviews[*]

# 按条件搜索（需要 Redis Stack 的 Search 模块）
FT.SEARCH idx:products '@category:{电子产品} @price:[0 500]'
```

**与 MongoDB 对比：**

| | Redis JSON | MongoDB |
|---|-----------|---------|
| 速度 | 内存级，微秒 | 内存+磁盘，毫秒 |
| 查询能力 | JSONPath + 简单搜索 | 完整的聚合管道 |
| 数据量 | 受内存限制 | 受磁盘限制 |
| 持久化 | RDB + AOF | 原生支持 |
| 适合场景 | 热文档、低延迟 | 海量文档、复杂查询 |

---

### 23.3 场景三：当做向量数据库（Vector Database）

**这是 AI 时代 Redis 最重要的新定位。**

```
把 Redis 当做向量数据库：

关键类型：Vector Sets（VADD / VSIM）

使用方式：
  1. 用 Embedding 模型把非结构化数据（文本/图片/音频）转成向量
  2. VADD 存入 Redis
  3. VSIM 做语义搜索

为什么选 Redis 而不是专用向量数据库？
  - 已有 Redis 部署 → 零额外运维成本
  - 内存原生 → 延迟最低（毫秒级 vs 专用数据库的几十毫秒）
  - 混合搜索 → VSIM + FILTER（语义 + 精确条件一起查）
  - 生态统一 → 用同一套技术栈做缓存、队列、向量搜索
```

**典型向量搜索架构：**

```
  ┌──────────────────────────────────────┐
  │         离线建库（非实时）             │
  │                                      │
  │  海量文档 → Embedding模型 → 向量      │
  │     │                            │    │
  │     └─── VADD 存入 Redis ────────┘    │
  └──────────────────────────────────────┘

  ┌──────────────────────────────────────┐
  │         在线查询（实时）               │
  │                                      │
  │  用户搜索 "轻便耳机推荐"               │
  │     │                                │
  │     ▼                                │
  │  Embedding 模型 → 查询向量            │
  │     │                                │
  │     ▼                                │
  │  Redis VSIM → Top 10 最相似商品       │
  │     │                                │
  │     ▼                                │
  │  返回给用户                           │
  └──────────────────────────────────────┘
```

---

### 23.4 场景四：搭建 RAG（检索增强生成）

**RAG = 先搜资料，再让大模型基于资料回答。**

```
RAG 的核心流程：

  用户问："Redis 怎么做高可用？"
      │
      ▼
  ① 问题 → Embedding → 向量
      │
      ▼
  ② Redis VSIM → 找最相关的 5 篇文档
      │
      ▼
  ③ 取文档内容
      │
      ▼
  ④ 拼 Prompt：
     "根据以下参考资料回答用户问题：
      [文档1内容]
      [文档2内容]
      ...
      用户问题：Redis 怎么做高可用？"
      │
      ▼
  ⑤ 发给 LLM（GPT/Claude）
      │
      ▼
  ⑥ LLM 基于资料回答（非瞎编，有据可查）

Redis 在 RAG 中的位置：
  文档向量存储 → VADD
  语义检索 → VSIM
  属性过滤 → VSIM FILTER
  对话记忆 → 历史对话摘要→向量→VSIM 召回
```

**RAG 的 Redis 技术栈：**

```
  ┌─────────────────────────────────────────────┐
  │                 RAG 架构                     │
  │                                              │
  │  离线索引层                                  │
  │  ┌──────────────────────────────────────┐    │
  │  │ 文档 → Embedding → VADD 写入 Vector Set │   │
  │  └──────────────────────────────────────┘    │
  │                                              │
  │  在线检索层                                  │
  │  ┌──────────────────────────────────────┐    │
  │  │ 问题 → Embedding → VSIM → 文档列表      │   │
  │  └──────────────────────────────────────┘    │
  │                                              │
  │  对话记忆层                                  │
  │  ┌──────────────────────────────────────┐    │
  │  │ 历史对话 → 摘要→向量 → VSIM 召回上下文  │   │
  │  └──────────────────────────────────────┘    │
  └─────────────────────────────────────────────┘
```

**四种场景的选型指南：**

| 你的需求 | 用 Redis 的什么功能 |
|---------|-------------------|
| 缓存/计数/排行/队列 | String + List + Set + ZSet + Hash |
| 存文档/JSON 数据 | JSON + Search 模块 |
| 语义搜索/推荐/以图搜图 | Vector Sets (VADD + VSIM) |
| RAG 问答/智能客服 | Vector Sets + LLM |
| 以上全部 | Redis Stack（一次性部署，兼收并蓄） |

---

## 第 24 章：常见问题 FAQ（官方）

> 以下内容来源于 Redis 官方文档 FAQ，结合中文社区常见疑问进行了解析和补充。

---

### 23.1 Redis 和其他 KV 存储有什么不同？

**官方回答（翻译+解析）：**

Redis 走了一条不同的进化路线：它的 value 不只是简单字符串，而是**复杂数据类型 + 原生原子操作**。不像其他 KV 存储在 value 上加抽象层，Redis 直接暴露给程序员的是基础数据结构。

核心区别有三点：

```
1. 数据类型丰富
   其他 KV：key → string，上限是存个 JSON
   Redis：key → String/List/Set/ZSet/Hash/Stream/JSON/Vector...
   而且每种类型有专属的原子操作命令

2. 内存 + 磁盘混合
   其他 KV（如 RocksDB）：以磁盘为主，内存做缓存
   Redis：以内存为主，磁盘做持久化（RDB 快照 + AOF 日志）
   取舍：数据集不能超过内存，但读写极快

3. 数据结构在内存中操作更简单
   相同的数据结构在内存和在磁盘上操作，复杂度天差地别
   内存里的 List 插入 = O(1) 指针操作
   磁盘上的 List 插入 = 寻道 + 移动数据块

设计哲学：
  Redis 选择「内存优先 + 磁盘做备份」
  而不是「磁盘优先 + 内存做缓存」
  这带来了极致的速度，也带来了内存容量的限制
```

---

### 23.2 Redis 的内存占用有多大？

**官方数据（64 位系统实测）：**

```
空实例               → ~3 MB
100 万个小 key（String）→ ~85 MB
100 万个 Hash（5 个字段）→ ~160 MB

测试方法：
  redis-benchmark 生成随机数据
  INFO memory 查看内存占用
```

**64 位 vs 32 位：**

```
64 位系统占用更多内存（指针 8 字节 vs 4 字节）
但能用更大的内存 → 要跑生产环境必须 64 位
替代方案：分片（Cluster）让每个实例的内存可控
```

---

### 23.3 为什么 Redis 要把数据全放在内存？

**官方回答（翻译）：**

Redis 团队实验过虚拟内存（Virtual Memory）方案，让数据集超过物理内存。但最终的选择是：**把一件本质的事情做到极致——数据从内存服务，磁盘只做持久化存储。**

```
Redis 的定位：
  不是「大而全」的数据库
  而是「快而专」的数据结构服务器

如果你的问题不是总内存，而是需要分片：
  用 Redis Cluster 把数据分散到多个实例
  而不是期望一个 Redis 实例装下所有数据

Redis 公司开发的「Redis on Flash」：
  混合 RAM + Flash 存储，适合冷热不均的数据
  这是企业版功能，不是开源版的一部分
```

**这句话本质上也是对我们学的「概率数据结构」的最好解释——Redis 的哲学就是能用算法换内存的地方绝不堆内存。**

---

### 23.4 Redis 能和磁盘数据库一起用吗？

**官方回答（翻译+解析）：**

**能，而且这是最常见的架构模式。**

```
经典设计模式：

  ┌─────────────┐     ┌─────────────┐
  │   Redis     │     │  MySQL/PG   │
  │  (热数据)    │     │  (冷数据)    │
  │             │     │             │
  │ 计数器      │     │ 用户表       │
  │ 排行榜      │     │ 订单表       │
  │ Session     │     │ 日志表       │
  │ 实时状态    │     │ 历史数据     │
  └─────────────┘     └─────────────┘

关键区别（比纯缓存更高级）：
  纯缓存模式：Redis 数据 = 数据库数据的子集
           缓存放冷了就从数据库重新加载

  高级模式：Redis 数据和数据库数据同步更新
          不是 cache-aside，是 write-through/write-behind
          Redis 的数据始终和数据库保持一致
          这样缓存命中率 = 100%（热点数据永远不会被淘汰）
```

---

### 23.5 怎么减少 Redis 的内存占用？

**官方回答（翻译 + 你学到的方法汇总）：**

```
1. 设计阶段就要考虑内存
   把逻辑数据模型映射到 Redis 物理模型时，选择最省内存的类型
   例：存用户签到 → Bitmap（12MB/亿用户）而不是 Set（2GB/亿用户）
   例：存用户信息 → Hash 而不是 String JSON（字段可以单独编码）

2. 选对数据类型
   布尔状态 → Bitmap
   计数 → HyperLogLog（12KB）
   存在性判断 → Bloom Filter
   排行榜 → Top-K（恒定 O(K) 内存）

3. 用 Hash 的 ziplist 编码（小 Hash 自动压缩）
   字段少 + 值短 → Redis 自动用 ziplist 编码（省 50% 内存）

4. 控制 key 过期时间
   不是所有数据都要永久保留
   用完就设 EXPIRE，让 Redis 自动回收

5. 更多参考
   Redis 官方 Memory Optimization 文档
```

---

### 23.6 Redis 内存用完了怎么办？

**官方回答（翻译+解析）：**

```
Redis 有内置的内存上限保护：

maxmemory 配置：
  在 redis.conf 里设置 Redis 最大内存
  达到上限后：

  默认行为：写命令返回错误
    SET key value
    → (error) OOM command not allowed when used memory > 'maxmemory'

   读命令不受影响，GET/EXISTS 等照常工作

淘汰策略（maxmemory-policy）：
  noeviction     → 不淘汰，写命令直接报错（默认）
  allkeys-lru    → 淘汰最近最少用的 key（适合缓存）
  allkeys-lfu    → 淘汰最不常用的 key（4.0+）
  volatile-lru   → 只淘汰设了过期时间的 key 中 LRU 的
  volatile-lfu   → 只淘汰设了过期时间的 key 中 LFU 的
  allkeys-random → 随机淘汰
  volatile-random→ 随机淘汰有 TTL 的
  volatile-ttl   → 淘汰 TTL 最短的

企业选择：
  纯缓存 → allkeys-lru
  有持久数据 → volatile-lru 或 volatile-ttl
  核心数据 → noeviction（宁可不可用也不丢数据）
```

---

### 23.7 BGSAVE 因 fork() 报错怎么办？

**这是 Redis 运维最高频的问题之一。**

```
现象：
  BGSAVE 时报错：
  Can't save in background: fork: Cannot allocate memory

原因：
  Linux 的 overcommit_memory 设置为 0（默认）
  → fork 时系统检查：空闲内存够不够复制整个父进程？
  → 你的 Redis 用 3GB，但只剩 2GB 空闲 → Linux 拒绝 fork

  但实际上 Redis 的 fork 靠 COW（写时复制），
  子进程不会真的复制全部内存！
  Linux 在 fork 的时候过于保守了

解决：
  echo 1 > /proc/sys/vm/overcommit_memory

  overcommit_memory 的三个值：
  0 → 启发式判断（默认），fork 时保守估计
  1 → 总是允许 overcommit，Redis 最需要的模式
  2 → 不允许超过 swap + 物理内存百分比

永久生效：
  echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf
  sysctl -p
```

---

### 23.8 Redis 磁盘快照是原子的吗？

**官方回答（翻译）：**

**是的。** Redis 的 BGSAVE 过程总是在服务端没有执行命令时 fork，所以**每一个在内存中是原子的命令，在磁盘快照中也是原子的。**

```
换句话说：
  BGSAVE 拍快照的瞬间，Redis 不在任何命令的中间状态
  所以快照文件里的数据是「一致」的
  不会有"SET 执行了一半"的状态被写进 RDB 文件
```

---

### 23.9 Redis 怎么利用多核 CPU？

**官方回答（翻译+解析）：**

```
Redis 绝大多数场景下 CPU 不是瓶颈。
瓶颈通常是内存大小或网络带宽。

一个 Redis 实例在普通 Linux 上就能跑 100 万 QPS
如果你的命令主要是 O(1) 或 O(log N) 的，CPU 不会满。

如果真的需要利用多核：

方案 1：同一台机器跑多个 Redis 实例
  实例 A 绑核 0-3
  实例 B 绑核 4-7
  → 手动分配，每个实例还是单线程

方案 2：Redis Cluster 分片
  每个分片一个进程
  分片分布在多核/多机上

方案 3：等待 Redis 逐步多线程化
  Redis 4.0 → 后台删除对象异步化
  Redis 6.0 → 网络 IO 多线程
  未来的版本 → 更多多线程支持
```

---

### 23.10 单个 Redis 实例最多存多少 key？

**官方回答（翻译）：**

```
理论上限：2^32 个 key（约 43 亿）
实践验证：单个实例至少 2.5 亿个 key

每个 Hash / List / Set / Sorted Set
最多元素数：2^32 个（约 43 亿）

所以真正的上限不是 Redis，是你机器的内存
```

**场景参考：**

```
2.5 亿个 String key → 约 20-30 GB 内存
5000 万个 Hash（5 字段）→ 约 80 GB 内存
```

---

### 23.11 为什么 Slave 的 key 数量和 Master 不一样？

**官方回答（翻译+解析）：**

```
正常现象！如果你用了带 TTL 的 key（EXPIRE），这是预期行为。

原因：
  1. Master 在做第一次全量同步（RDB）给 Slave 时
  2. RDB 文件不会包含「逻辑上已过期但物理上还在内存」的 key
  3. 这些 key 在 Master 内存里还存在：
     - 逻辑上已经过期（GET 返回 nil）
     - 但物理内存还没回收（惰性删除或定期删除没扫到）
     - INFO 和 DBSIZE 会统计到它们
  4. Slave 加载 RDB 时不会加载这些 key
     → Slave 的 DBSIZE 比 Master 小

但逻辑上两个节点的数据集是完全相同的：
  你在 Master 上 GET 不到的 key，在 Slave 上同样 GET 不到
  DBSIZE 的差异只是统计口径的问题
```

---

### 23.12 Redis 这个名字怎么来的？

```
Redis 是 REmote DIctionary Server 的首字母缩写
—— 远程字典服务器

发音：/ˈrɛd-ɪs/
用中文近音记："red"（红色）+ "iss"（kiss 去掉 k）
不是"瑞迪斯"，不是"瑞迪艾斯"

创始人：Salvatore Sanfilippo（社区昵称 antirez）
最初创建 Redis 是为了扩展 LLOOGG（一个实时日志分析工具）
在把基础服务器做出来后，决定开源分享给更多人
```

---

> 📌 **以上 FAQ 来源于 Redis 官方文档，结合学习中的常见疑问进行了解析。更多细节参见：https://redis.io/docs/latest/develop/get-started/faq/**

---

<!-- ═══════════════════════════════════════════════════════ -->
<!--  第七部分：附录                                        -->
<!-- ═══════════════════════════════════════════════════════ -->

---

## 附录 A：完整命令速查

### A.1 通用命令

```bash
KEYS pattern       # ⚠️ 生产慎用！用 SCAN
SCAN cursor [MATCH pattern] [COUNT n] [TYPE type]
TYPE key
EXISTS key
DEL key / UNLINK key
EXPIRE key seconds / PEXPIRE key ms / EXPIREAT key timestamp
TTL key / PTTL key
PERSIST key
RENAME old new / RENAMENX old new
DBSIZE
INFO [section]
OBJECT ENCODING key
```

### A.2 String

```bash
SET/GET  MSET/MGET  SETNX  SETEX  PSETEX
INCR/DECR  INCRBY/DECRBY  INCRBYFLOAT
APPEND  GETRANGE  SETRANGE  STRLEN
GETSET  GETEX  GETDEL
```

### A.3 List

```bash
LPUSH/RPUSH  LPOP/RPOP  BLPOP/BRPOP
LLEN  LRANGE  LINDEX  LSET  LINSERT
LREM  LTRIM  LPOS  RPOPLPUSH  LMOVE
```

### A.4 Set

```bash
SADD  SREM  SMEMBERS  SISMEMBER  SCARD
SPOP  SRANDMEMBER  SMOVE  SSCAN
SINTER/SUNION/SDIFF  SINTERSTORE/SUNIONSTORE/SDIFFSTORE
```

### A.5 Sorted Set

```bash
ZADD  ZREM  ZCARD  ZCOUNT  ZSCORE
ZRANGE/ZREVRANGE/ZRANGEBYSCORE/ZREVRANGEBYSCORE
ZRANK/ZREVRANK  ZINCRBY  ZSCAN
ZREMRANGEBYRANK/ZREMRANGEBYSCORE
ZUNIONSTORE/ZINTERSTORE
```

### A.6 Hash

```bash
HSET  HGET  HMSET  HMGET  HGETALL
HKEYS  HVALS  HEXISTS  HDEL
HLEN  HSTRLEN  HINCRBY  HINCRBYFLOAT
HSETNX  HSCAN
```

### A.7 Stream

```bash
XADD  XREAD  XRANGE/XREVRANGE  XLEN
XGROUP CREATE/DESTROY  XREADGROUP  XACK
XPENDING  XCLAIM  XDEL  XTRIM
XINFO STREAM/GROUPS/CONSUMERS
```

### A.8 Geospatial

```bash
GEOADD  GEOPOS  GEOHASH  GEODIST
GEOSEARCH  GEOSEARCHSTORE
```

### A.9 Bitmap & Bitfield

```bash
SETBIT  GETBIT  BITCOUNT  BITPOS  BITOP
BITFIELD ... GET/SET/INCRBY ...
```

### A.10 概率类型

```bash
# HyperLogLog
PFADD  PFCOUNT  PFMERGE

# Bloom Filter
BF.RESERVE  BF.ADD  BF.MADD  BF.EXISTS  BF.MEXISTS

# Cuckoo Filter
CF.RESERVE  CF.ADD  CF.ADDNX  CF.EXISTS  CF.DEL  CF.COUNT

# Count-Min Sketch
CMS.INITBYDIM  CMS.INITBYPROB  CMS.INCRBY  CMS.QUERY  CMS.MERGE

# Top-K
TOPK.RESERVE  TOPK.ADD  TOPK.INCRBY  TOPK.LIST  TOPK.QUERY

# t-digest
TDIGEST.CREATE  TDIGEST.ADD  TDIGEST.QUANTILE
TDIGEST.CDF  TDIGEST.MIN/MAX  TDIGEST.MERGE
```

### A.11 JSON

```bash
JSON.SET  JSON.GET  JSON.MGET  JSON.DEL
JSON.TYPE  JSON.STRLEN  JSON.ARRLEN  JSON.OBJLEN  JSON.OBJKEYS
JSON.NUMINCRBY  JSON.STRAPPEND
JSON.ARRAPPEND  JSON.ARRINSERT  JSON.ARRPOP  JSON.ARRTRIM  JSON.ARRINDEX
```

### A.12 Time Series

```bash
TS.CREATE  TS.ADD  TS.MADD  TS.GET  TS.MGET
TS.RANGE  TS.REVRANGE  TS.MRANGE  TS.MREVRANGE
TS.CREATERULE  TS.DELETERULE
TS.INFO  TS.QUERYINDEX  TS.DEL  TS.ALTER
```

### A.13 Vector Sets

```bash
VADD  VREM  VCARD  VDIM  VEMB
VSETATTR  VGETATTR
VSIM [ELE|VALUES] [COUNT n] [WITHSCORES] [FILTER 'expr'] [EF_RUNTIME n] [TIMEOUT ms]
```

### A.14 Pub/Sub

```bash
SUBSCRIBE  PSUBSCRIBE  PUBLISH
UNSUBSCRIBE  PUNSUBSCRIBE
PUBSUB CHANNELS/NUMSUB/NUMPAT
```

### A.15 事务

```bash
MULTI  EXEC  DISCARD  WATCH  UNWATCH
```

---

## 附录 B：数据类型选型决策树

```
你的需求是什么？

存一个值
├── 简单值、配置、计数器 → String
├── 嵌套 JSON、对象带数组 → JSON
└── 扁平字段、需单独更新 → Hash

存一串值
├── 简单队列/栈              → List
├── 消息队列（不能丢消息）    → Stream + 消费者组
├── 实时广播（丢了无所谓）    → Pub/Sub
└── 有序、需要排序            → Sorted Set

需要判断"在不在"
├── 精确去重/标签             → Set
├── 判断存在（海量）          → Bloom Filter（不能删）
├── 判断存在+能删            → Cuckoo Filter
└── 签到/在线状态            → Bitmap

需要统计
├── 数人头（UV）              → HyperLogLog
├── 出现次数                  → Count-Min Sketch
├── 热门排行                  → Top-K
└── 延迟分位数                → t-digest

需要位置
├── 附近的人/门店             → Geospatial（只二维！）
└── 三维空间                  → PostgreSQL PostGIS

需要时序数据
└── 监控指标/IoT 传感器       → Time Series

需要 AI/语义搜索
└── RAG/相似搜索/Agent 记忆   → Vector Sets

需要打包存大量小整数
└── 游戏状态/IoT/紧凑编码    → Bitfield
```

---

## 附录 C：常用工具

> 官方提供三种工具连接 Redis，日常学习中 `redis-cli` 足够，生产环境用 GUI 浏览更方便。

### C.1 redis-cli（命令行）

```bash
# 连接
redis-cli                           # 本机 6379
redis-cli -h 192.168.1.100 -p 6379 -a "password"
redis-cli -u redis://user:pass@host:6379

# 两种模式
# ① 交互 REPL 模式
redis-cli
127.0.0.1:6379> SET key value

# ② 命令模式（脚本/一行命令）
redis-cli SET key value
redis-cli GET key
redis-cli --scan --pattern "user:*" | head -20
redis-cli INFO memory

# 常用技巧
redis-cli MONITOR              # 实时看所有命令（调试用，生产慎用）
redis-cli --latency            # 测延迟
redis-cli --stat               # 实时看 QPS
redis-cli --bigkeys            # 扫描大 key
redis-cli --rdb /data/dump.rdb # 分析 RDB 文件
```

### C.2 Redis Insight（官方免费 GUI）

```
免费桌面工具，Redis 官方出品
功能：
  - 树形浏览 key（按冒号折叠）
  - 可视化增删改查
  - 实时监控（QPS/内存/CPU）
  - 慢日志分析
  - RedisJSON/TimeSeries/Vector 可视化

下载：https://redis.io/insight/
```

### C.3 第三方工具

```
DataGrip / Navicat   — 你已经在用的，支持 Redis 连接
Redis Commander     — 开源 Web 管理界面（npm install -g redis-commander）
Another Redis Desktop Manager — 开源桌面客户端
medis               — macOS 专用
```

### C.4 redis-benchmark（性能压测）

```bash
# 自带压测工具
redis-benchmark -q -n 100000 -c 50
# -q 简洁输出
# -n 请求总数
# -c 并发连接数
# -t set,get  只测指定命令
```

---

> 📌 **核心哲学：Redis 的每种数据类型都是为特定场景「量身定做」的。理解场景才能选对类型。**
>
> 🔗 官方文档：https://redis.io/docs/latest/develop/
>
> 📝 复习建议：每章配合 `redis-cli` 动手敲一遍命令，遇到实际问题再回来查对应的章节。
