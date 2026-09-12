"""
图片数据模型

纯 pydantic BaseModel，对应 MongoDB 中 images 集合。
"""
# 内置库
from datetime import datetime, timezone
# 三方库
from pydantic import BaseModel, Field


class Image(BaseModel):
    """图片模型

    MongoDB 文档结构:
    {
      "_id": "20250610120000",         ← 时间戳作为主键
      "url": "https://...",
      "type": "jpg",
      "created_at": ISODate("...")
    }
    """

    id: str = Field(
        ...,
        description="图片唯一标识（时间戳字符串，如 20250610120000）",
    )
    url: str = Field(..., description="图片资源的网络地址（OSS/CDN）")
    type: str = Field(..., description="图片格式（jpg, png, webp, gif 等）")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="图片入库时间",
    )
