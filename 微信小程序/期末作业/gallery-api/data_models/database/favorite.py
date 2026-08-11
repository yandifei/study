"""
收藏记录子文档模型

嵌入在 User.favorite_records 数组中，不作为独立集合。
"""
# 内置库
from datetime import datetime, timezone
# 三方库
from pydantic import BaseModel, Field


class FavoriteItem(BaseModel):
    """收藏记录子文档

    嵌入在 User 文档中:
    {
      "image_id": "20250610120000",
      "image_url": "https://cdn.example.com/photo.jpg",
      "favorite_time": ISODate("2025-06-10T12:00:00Z")
    }
    """

    image_id: str = Field(..., description="图片唯一标识（时间戳）")
    image_url: str = Field(..., description="图片 URL（冗余存储）")
    favorite_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="收藏时间",
    )
