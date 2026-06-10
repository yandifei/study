"""
MongoDB 索引管理模块

提供索引创建、验证和状态查询功能，用于生产环境部署。
虽然 Beanie 在 init_beanie() 时会自动创建索引，但在以下场景中仍需要此模块：
  - 生产环境预热：在应用开始接收流量前预先创建索引，避免冷启动时索引构建阻塞查询
  - CI/CD 验证：确认所有预期索引已正确创建
  - 性能诊断：查看索引使用统计，识别未被使用的冗余索引
  - 手动控制：精细控制索引创建时机（例如在低峰期创建大型索引）

索引设计总览
============

┌──────────────────┬─────────────────────────────────────────┬──────────────────────────────┐
│ 集合             │ 索引                                    │ 覆盖的查询模式               │
├──────────────────┼─────────────────────────────────────────┼──────────────────────────────┤
│ users            │ _id (PK, 自动)                          │ 按主键精确查找               │
│                  │ email UNIQUE                            │ 邮箱登录、邮箱唯一性校验     │
│                  │ username                                │ 按用户名搜索用户             │
├──────────────────┼─────────────────────────────────────────┼──────────────────────────────┤
│ images           │ _id (PK, 自动)                          │ 按主键精确查找               │
│                  │ url UNIQUE                              │ URL 去重、按 URL 查找图片    │
│                  │ type                                    │ 按图片格式筛选               │
│                  │ created_at DESC                         │ 最新入库图片列表（瀑布流）   │
├──────────────────┼─────────────────────────────────────────┼──────────────────────────────┤
│ browse_records   │ _id (PK, 自动)                          │ 按主键精确查找               │
│                  │ (user_id, browse_time DESC)             │ 用户的最近浏览历史           │
│                  │ (image_id, browse_time DESC)            │ 某图片的浏览用户/浏览次数    │
│                  │ browse_time DESC                        │ 全局最近浏览记录             │
├──────────────────┼─────────────────────────────────────────┼──────────────────────────────┤
│ favorite_records │ _id (PK, 自动)                          │ 按主键精确查找               │
│                  │ (user_id, image_id) UNIQUE              │ 防重复收藏、查询收藏状态     │
│                  │ (user_id, favorite_time DESC)           │ 我的收藏列表（按时间倒序）   │
│                  │ (image_id, favorite_time DESC)          │ 某图片的收藏用户/收藏总量    │
└──────────────────┴─────────────────────────────────────────┴──────────────────────────────┘
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import IndexModel, ASCENDING, DESCENDING
from typing import List, Dict

from logger import info, warning


# ── 索引定义 ──────────────────────────────────────────────

# 所有预期索引的声明性定义，按集合分组
EXPECTED_INDEXES: Dict[str, List[IndexModel]] = {
    "users": [
        IndexModel(
            [("email", ASCENDING)],
            unique=True,
            name="idx_email_unique"
        ),
        IndexModel(
            [("username", ASCENDING)],
            name="idx_username"
        ),
    ],
    "images": [
        IndexModel(
            [("url", ASCENDING)],
            unique=True,
            name="idx_url_unique"
        ),
        IndexModel(
            [("type", ASCENDING)],
            name="idx_type"
        ),
        IndexModel(
            [("created_at", DESCENDING)],
            name="idx_created_at_desc"
        ),
    ],
    "browse_records": [
        IndexModel(
            [
                ("user_id", ASCENDING),
                ("browse_time", DESCENDING)
            ],
            name="idx_user_browse_time"
        ),
        IndexModel(
            [
                ("image_id", ASCENDING),
                ("browse_time", DESCENDING)
            ],
            name="idx_image_browse_time"
        ),
        IndexModel(
            [("browse_time", DESCENDING)],
            name="idx_browse_time_desc"
        ),
    ],
    "favorite_records": [
        IndexModel(
            [
                ("user_id", ASCENDING),
                ("image_id", ASCENDING)
            ],
            unique=True,
            name="idx_user_image_unique"
        ),
        IndexModel(
            [
                ("user_id", ASCENDING),
                ("favorite_time", DESCENDING)
            ],
            name="idx_user_favorite_time"
        ),
        IndexModel(
            [
                ("image_id", ASCENDING),
                ("favorite_time", DESCENDING)
            ],
            name="idx_image_favorite_time"
        ),
    ],
}


async def create_all_indexes(db: AsyncIOMotorDatabase) -> Dict[str, List[str]]:
    """为所有集合创建预期索引（幂等操作）

    在应用启动时、接收流量之前调用此函数，
    确保所有索引已就绪，避免冷启动时的索引构建延迟。

    Args:
        db: Motor 异步数据库实例

    Returns:
        { 集合名: [已创建的索引名列表] } 的字典
    """
    result = {}

    for collection_name, indexes in EXPECTED_INDEXES.items():
        collection = db[collection_name]
        created_names = await collection.create_indexes(indexes)
        result[collection_name] = created_names
        info(
            "索引创建完成: 集合=%s, 新建索引=%s",
            collection_name,
            created_names if created_names else "无需新建（已存在）"
        )

    return result


async def verify_indexes(db: AsyncIOMotorDatabase) -> Dict[str, Dict]:
    """验证所有预期索引是否已存在

    用于 CI/CD 流程中的前置检查，确保索引部署正确。

    Args:
        db: Motor 异步数据库实例

    Returns:
        {
            集合名: {
                "expected": int,    # 预期索引数量（不含 _id）
                "actual": int,      # 实际索引数量
                "missing": [...],   # 缺失的索引名列表
                "extra": [...]      # 多余的索引名列表
            }
        }
    """
    report = {}

    for collection_name, expected_indexes in EXPECTED_INDEXES.items():
        # 获取集合中当前所有索引
        existing_indexes = await db[collection_name].list_indexes().to_list(length=None)
        # 提取索引名（排除 _id_ 主键索引）
        existing_names = {idx["name"] for idx in existing_indexes if idx["name"] != "_id_"}
        expected_names = {idx.document["name"] for idx in expected_indexes}

        missing = sorted(expected_names - existing_names)
        extra = sorted(existing_names - expected_names)

        report[collection_name] = {
            "expected": len(expected_names),
            "actual": len(existing_names),
            "missing": missing,
            "extra": extra,
            "healthy": len(missing) == 0 and len(extra) == 0,
        }

        if not report[collection_name]["healthy"]:
            if missing:
                warning("索引缺失: 集合=%s, 缺失=%s", collection_name, missing)
            if extra:
                warning("冗余索引: 集合=%s, 多余=%s", collection_name, extra)

    return report


async def list_indexes(db: AsyncIOMotorDatabase,
                       collection_name: str | None = None) -> Dict[str, List[Dict]]:
    """列出数据库中所有（或指定集合的）索引及其详细信息

    Args:
        db: Motor 异步数据库实例
        collection_name: 指定集合名，为 None 时列出所有集合

    Returns:
        { 集合名: [索引信息字典列表] }
    """
    collections = [collection_name] if collection_name else list(EXPECTED_INDEXES.keys())
    result = {}

    for name in collections:
        indexes = await db[name].list_indexes().to_list(length=None)
        result[name] = indexes
        info("集合 %s 共有 %d 个索引", name, len(indexes))

    return result


async def drop_extra_indexes(db: AsyncIOMotorDatabase) -> Dict[str, List[str]]:
    """删除未在预期定义中的多余索引

    危险操作：仅在确认多余索引确实需要删除时调用。

    Args:
        db: Motor 异步数据库实例

    Returns:
        { 集合名: [已删除的索引名列表] }
    """
    result = {}

    for collection_name, expected_indexes in EXPECTED_INDEXES.items():
        existing = await db[collection_name].list_indexes().to_list(length=None)
        expected_names = {idx.document["name"] for idx in expected_indexes}
        dropped = []

        for idx in existing:
            name = idx["name"]
            if name == "_id_":
                continue  # 永远不删除主键索引
            if name not in expected_names:
                await db[collection_name].drop_index(name)
                dropped.append(name)
                warning("已删除冗余索引: 集合=%s, 索引=%s", collection_name, name)

        result[collection_name] = dropped

    return result


async def warmup_indexes(db: AsyncIOMotorDatabase):
    """预热：创建索引并验证，用于应用启动流程

    结合 create_all_indexes 和 verify_indexes 的一站式启动函数。

    Args:
        db: Motor 异步数据库实例
    """
    info("开始数据库索引预热...")
    created = await create_all_indexes(db)
    total_created = sum(len(v) for v in created.values())
    info("索引创建阶段完成，共新建 %d 个索引", total_created)

    report = await verify_indexes(db)
    all_healthy = all(v["healthy"] for v in report.values())
    if all_healthy:
        info("索引验证通过：所有预期索引均已就绪")
    else:
        warning("索引验证未通过，请检查上方警告信息")

    return report
