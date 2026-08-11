"""
收藏记录服务

收藏记录嵌入在 User.favorite_records 数组中。
使用 MongoDB $push / $pull / $set 操作，按 image_id 排序，无上限。
"""
# 内置库
from datetime import datetime, timezone
# 三方库
from bson import ObjectId
from pymongo import DESCENDING
# 自己的模块
from services.database.mongodb import get_collection
from data_models.database import FavoriteItem
from logger import info


"""插入"""

async def add_favorite(
    user_id: str,
    image_id: str,
    image_url: str,
) -> bool:
    """添加收藏（幂等——先 $pull 再 $push，保证不重复）

    Args:
        user_id: 用户 MongoDB ObjectId 字符串
        image_id: 图片唯一标识（时间戳）
        image_url: 图片 URL

    Returns:
        True 已添加
    """
    collection = get_collection("users")
    now = datetime.now(timezone.utc)
    item = {"image_id": image_id, "image_url": image_url, "favorite_time": now}

    # 先删除同 image_id 的旧记录（幂等），再 push 新记录
    await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"favorite_records": {"image_id": image_id}}},
    )
    await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"favorite_records": {"$each": [item], "$sort": {"image_id": DESCENDING}}}},
    )
    info(f"收藏成功: user={user_id}, image={image_id}")
    return True


"""查询"""

async def get_user_favorites(
    user_id: str,
    limit: int = 20,
    skip: int = 0,
) -> list[FavoriteItem]:
    """获取用户收藏（分页，新→旧）

    Args:
        user_id: 用户 MongoDB ObjectId 字符串
        limit: 返回条数，默认 20
        skip: 跳过条数
    """
    collection = get_collection("users")
    doc = await collection.find_one(
        {"_id": ObjectId(user_id)},
        {"favorite_records": {"$slice": [skip, limit]}},
    )
    if not doc or "favorite_records" not in doc:
        return []
    return [FavoriteItem(**item) for item in doc["favorite_records"]]


"""删除"""

async def delete_favorite(user_id: str, image_id: str) -> bool:
    """删除单条收藏"""
    collection = get_collection("users")
    result = await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"favorite_records": {"image_id": image_id}}},
    )
    info(f"取消收藏: user={user_id}, image={image_id}")
    return result.modified_count > 0


async def delete_all_favorites(user_id: str) -> int:
    """清空用户全部收藏"""
    collection = get_collection("users")
    result = await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"favorite_records": []}},
    )
    info(f"收藏已清空: user={user_id}")
    return result.modified_count
