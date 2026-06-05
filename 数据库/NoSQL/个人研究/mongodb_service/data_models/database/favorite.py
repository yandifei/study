"""
收藏记录数据模型

对应 MongoDB 中的 favorite_records 集合，记录用户收藏图片的行为。
通过唯一复合索引保证同一用户不会重复收藏同一图片。
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from pymongo import IndexModel, ASCENDING, DESCENDING


class Favorite(Document):
    """收藏记录文档模型

    Attributes:
        user_id: 收藏用户的邮箱（对应 users 集合的 _id）
        image_id: 被收藏图片的 MongoDB ObjectId（对应 images 集合的 _id）
        favorite_time: 收藏发生的时间
    """

    # 收藏用户的邮箱
    user_id: str

    # 被收藏图片对应的 MongoDB ObjectId
    image_id: str

    # 收藏发生的时间，插入文档时自动填充
    favorite_time: datetime = Field(
        default_factory=datetime.utcnow
    )

    class Settings:
        """Beanie 文档配置"""

        # MongoDB 集合名称
        name = "favorite_records"

        # 索引定义
        indexes = [
            # 复合索引 (user_id + favorite_time 降序)
            # 用于「我的收藏」查询：按用户过滤并按收藏时间倒序排列
            IndexModel(
                [
                    ("user_id", ASCENDING),
                    ("favorite_time", DESCENDING)
                ]
            ),
            # 唯一复合索引 (user_id + image_id)
            # 保证同一用户不会重复收藏同一张图片，重复插入会触发 DuplicateKeyError
            IndexModel(
                [
                    ("user_id", ASCENDING),
                    ("image_id", ASCENDING)
                ],
                unique=True
            )
        ]


"""
# 我的收藏查询示例
await Favorite.find(
    Favorite.user_id == email
).sort(-Favorite.favorite_time).to_list()
"""