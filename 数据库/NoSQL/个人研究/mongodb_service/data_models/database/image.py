"""
图片数据模型

对应 MongoDB 中的 images 集合，存储图片的元信息。
通过 URL 唯一索引保证同一图片不会重复入库。
"""

from beanie import Document
from pydantic import Field
from datetime import datetime
from pymongo import IndexModel, ASCENDING


class Image(Document):
    """图片文档模型

    Attributes:
        url: 图片资源的网络地址
        created_at: 图片入库时间
    """

    # 图片资源的网络地址（例如 OSS/CDN 地址）
    url: str

    # 图片入库时间，插入文档时自动填充
    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    class Settings:
        """Beanie 文档配置"""

        # MongoDB 集合名称
        name = "images"

        # 索引定义
        indexes = [
            # url 唯一索引：防止同一 URL 的图片被重复入库
            IndexModel(
                [("url", ASCENDING)],
                unique=True
            )
        ]