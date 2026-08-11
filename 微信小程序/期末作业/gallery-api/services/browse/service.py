"""
浏览记录服务

浏览记录嵌入在 User.browse_records 数组中。
使用 MongoDB $push + $slice 保持最多 1000 条，按 image_id 降序（新→旧）。
查询时用 $slice 分页，不会一次性拉取全部数据。
"""
# 内置库
from datetime import datetime, timezone
# 三方库
from bson import ObjectId
from pymongo import DESCENDING
# 自己的模块
from services.database.mongodb import get_collection
from data_models.database import BrowseItem
from logger import info


MAX_BROWSE = 1000


"""批量插入"""

async def add_browse_records(
    user_id: str,
    images: list[dict],
) -> int:
    """批量记录浏览，嵌入到用户文档

    使用 $push + $each + $sort + $slice:
    - 按 image_id 降序排列（新→旧）
    - 超过 1000 条自动裁剪最旧的数据

    Args:
        user_id: 用户 MongoDB ObjectId 字符串
        images: [{"image_id": "...", "image_url": "..."}, ...]

    Returns:
        实际新增条数
    """
    if not images:
        return 0

    now = datetime.now(timezone.utc)
    items = [
        {"image_id": img["image_id"], "image_url": img["image_url"], "browse_time": now}
        for img in images
    ]

    collection = get_collection("users")
    result = await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {
            "browse_records": {
                "$each": items,
                "$sort": {"image_id": DESCENDING},
                "$slice": -MAX_BROWSE,
            }
        }},
    )
    info(f"浏览记录已写入: user={user_id}, 新增={len(items)} 条")
    return len(items) if result.modified_count else 0


"""查询"""

async def get_user_browse_records(
    user_id: str,
    limit: int = 20,
    skip: int = 0,
) -> list[BrowseItem]:
    """获取用户浏览记录（分页，新→旧）

    使用 MongoDB $slice 在服务端做分页，只返回指定范围内的数据，
    不会把全部 1000 条拉回应用层再切片。

    Args:
        user_id: 用户 MongoDB ObjectId 字符串
        limit: 返回条数，默认 20
        skip: 跳过条数
    """
    collection = get_collection("users")
    doc = await collection.find_one(
        {"_id": ObjectId(user_id)},
        {"browse_records": {"$slice": [skip, limit]}},
    )
    if not doc or "browse_records" not in doc:
        return []
    return [BrowseItem(**item) for item in doc["browse_records"]]


"""删除"""

async def delete_all_browse_records(user_id: str) -> int:
    """清空用户全部浏览记录"""
    collection = get_collection("users")
    result = await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"browse_records": []}},
    )
    count = result.modified_count
    info(f"浏览记录已清空: user={user_id}")
    return count
