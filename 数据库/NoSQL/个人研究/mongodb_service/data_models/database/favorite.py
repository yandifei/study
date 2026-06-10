"""
收藏记录数据模型

对应 MongoDB 中的 favorite_records 集合，记录用户收藏图片的行为。
通过唯一复合索引 (user_id, image_id) 保证同一用户不会重复收藏同一图片。

查询模式分析：
  1. 某用户的收藏列表 → (user_id, favorite_time DESC)
  2. 防重复收藏校验 → 唯一复合 (user_id, image_id)
  3. 某图片的收藏用户列表 / 收藏总量 → (image_id, favorite_time DESC)
"""

from beanie import Document
from pydantic import Field
from datetime import datetime, timezone
from pymongo import IndexModel, ASCENDING, DESCENDING


class Favorite(Document):
    """收藏记录文档模型

    Attributes:
        id: MongoDB 自动生成的代理主键（ObjectId），由 Beanie 自动管理
        user_id: 收藏用户的邮箱（对应 users 集合的 email 字段）
        image_id: 被收藏图片的 MongoDB ObjectId 字符串（对应 images 集合的 _id）
        favorite_time: 收藏发生的时间
    """

    # 收藏用户的邮箱（对应 users 集合的 email 字段）
    user_id: str

    # 被收藏图片对应的 MongoDB ObjectId 字符串
    image_id: str

    # 收藏发生的时间，插入文档时自动填充
    favorite_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        """Beanie 文档配置"""

        # MongoDB 集合名称
        name = "favorite_records"

        # 索引定义
        indexes = [
            # 唯一复合索引 (user_id, image_id)
            # 保证同一用户不会重复收藏同一张图片
            # 插入重复收藏记录时会触发 DuplicateKeyError
            IndexModel(
                [
                    ("user_id", ASCENDING),
                    ("image_id", ASCENDING)
                ],
                unique=True,
                name="idx_user_image_unique"
            ),
            # 复合索引 (user_id, favorite_time DESC)
            # 覆盖查询：「我的收藏」列表，按收藏时间倒序排列
            # 这是最高频的查询——用户查看自己的收藏列表
            IndexModel(
                [
                    ("user_id", ASCENDING),
                    ("favorite_time", DESCENDING)
                ],
                name="idx_user_favorite_time"
            ),
            # 复合索引 (image_id, favorite_time DESC)
            # 覆盖查询：「某图片被哪些用户收藏过」，按时间倒序
            # 同时支持统计某图片的收藏总量
            IndexModel(
                [
                    ("image_id", ASCENDING),
                    ("favorite_time", DESCENDING)
                ],
                name="idx_image_favorite_time"
            ),
        ]


"""
# 示例文档结构
{
  "_id": ObjectId("..."),
  "user_id": "admin@qq.com",
  "image_id": "507f1f77bcf86cd799439011",
  "favorite_time": ISODate("2025-01-01T12:00:00Z")
}

# 我的收藏列表（按收藏时间倒序）
records = await Favorite.find(
    Favorite.user_id == "admin@qq.com"
).sort(-Favorite.favorite_time).limit(20).to_list()

# 检查用户是否已收藏某图片（利用唯一索引，查询极快）
existing = await Favorite.find_one(
    Favorite.user_id == "admin@qq.com",
    Favorite.image_id == "507f1f77bcf86cd799439011"
)

# 添加收藏（重复添加会抛出 DuplicateKeyError）
try:
    await Favorite(
        user_id="admin@qq.com",
        image_id="507f1f77bcf86cd799439011"
    ).insert()
except Exception:
    pass  # 已收藏，忽略

# 某图片的收藏总量
count = await Favorite.find(
    Favorite.image_id == "507f1f77bcf86cd799439011"
).count()
"""
