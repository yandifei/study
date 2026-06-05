"""
浏览记录数据模型

对应 MongoDB 中的 browse_records 集合，记录用户每次浏览图片的行为。
同一用户可以多次浏览同一图片，每次产生一条独立记录。
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from pymongo import IndexModel, ASCENDING, DESCENDING


class Browse(Document):
    """浏览记录文档模型

    Attributes:
        user_id: 浏览用户的邮箱（对应 users 集合的 _id）
        image_id: 被浏览图片的 MongoDB ObjectId（对应 images 集合的 _id）
        browse_time: 浏览发生的时间
    """

    # 浏览用户的邮箱
    user_id: str

    # 被浏览图片对应的 MongoDB ObjectId
    image_id: str

    # 浏览发生的时间，插入文档时自动填充
    browse_time: datetime = Field(
        default_factory=datetime.utcnow
    )

    class Settings:
        """Beanie 文档配置"""

        # MongoDB 集合名称
        name = "browse_records"

        # 索引定义
        indexes = [
            # 复合索引 (user_id + browse_time 降序)
            # 用于「最近浏览」查询：按用户过滤并按时间倒序排列
            IndexModel(
                [
                    ("user_id", ASCENDING),
                    ("browse_time", DESCENDING)
                ]
            ),
            # 单字段索引 (image_id)
            # 用于统计某张图片的浏览总量或查询某图片的浏览用户
            IndexModel(
                [
                    ("image_id", ASCENDING)
                ]
            )
        ]


"""
# 最近浏览查询示例
await Browse.find(
    Browse.user_id == email
).sort(-Browse.browse_time).to_list()
"""