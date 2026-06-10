"""
浏览记录数据模型

对应 MongoDB 中的 browse_records 集合，记录用户每次浏览图片的行为。
同一用户可以多次浏览同一图片，每次产生一条独立记录。

查询模式分析：
  1. 某用户的最近浏览历史 → (user_id, browse_time DESC)
  2. 某图片的浏览用户列表 / 浏览总量 → (image_id, browse_time DESC)
  3. 全局最近浏览记录 → (browse_time DESC)
"""

from beanie import Document
from pydantic import Field
from datetime import datetime, timezone
from pymongo import IndexModel, ASCENDING, DESCENDING


class Browse(Document):
    """浏览记录文档模型

    Attributes:
        id: MongoDB 自动生成的代理主键（ObjectId），由 Beanie 自动管理
        user_id: 浏览用户的邮箱（对应 users 集合的 email 字段）
        image_id: 被浏览图片的 MongoDB ObjectId 字符串（对应 images 集合的 _id）
        browse_time: 浏览发生的时间
    """

    # 浏览用户的邮箱（对应 users 集合的 email 字段）
    user_id: str

    # 被浏览图片对应的 MongoDB ObjectId 字符串
    image_id: str

    # 浏览发生的时间，插入文档时自动填充
    browse_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        """Beanie 文档配置"""

        # MongoDB 集合名称
        name = "browse_records"

        # 索引定义
        indexes = [
            # 复合索引 (user_id, browse_time DESC)
            # 覆盖查询：「某用户的最近浏览历史」，按时间倒序排列
            # 这是最高频的查询——用户查看自己的浏览记录
            IndexModel(
                [
                    ("user_id", ASCENDING),
                    ("browse_time", DESCENDING)
                ],
                name="idx_user_browse_time"
            ),
            # 复合索引 (image_id, browse_time DESC)
            # 覆盖查询：「某图片被哪些用户浏览过」，按时间倒序
            # 同时支持按时间范围统计某图片的浏览次数
            IndexModel(
                [
                    ("image_id", ASCENDING),
                    ("browse_time", DESCENDING)
                ],
                name="idx_image_browse_time"
            ),
            # browse_time 降序索引
            # 覆盖查询：「全局最近浏览记录」
            # 用于首页动态、最近活动等场景
            IndexModel(
                [("browse_time", DESCENDING)],
                name="idx_browse_time_desc"
            ),
        ]


"""
# 示例文档结构
{
  "_id": ObjectId("..."),
  "user_id": "admin@qq.com",
  "image_id": "507f1f77bcf86cd799439011",
  "browse_time": ISODate("2025-01-01T12:00:00Z")
}

# 某用户的最近浏览历史
records = await Browse.find(
    Browse.user_id == "admin@qq.com"
).sort(-Browse.browse_time).limit(20).to_list()

# 某图片的浏览用户列表（最近 20 条）
records = await Browse.find(
    Browse.image_id == "507f1f77bcf86cd799439011"
).sort(-Browse.browse_time).limit(20).to_list()

# 某图片的浏览次数（30 天内）
from datetime import timedelta
thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
count = await Browse.find(
    Browse.image_id == "507f1f77bcf86cd799439011",
    Browse.browse_time >= thirty_days_ago
).count()
"""
