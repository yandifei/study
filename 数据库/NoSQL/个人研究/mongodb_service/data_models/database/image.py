"""
图片数据模型

对应 MongoDB 中的 images 集合，存储图片的元信息。
通过 URL 唯一索引保证同一图片不会重复入库，
通过 type 索引加速按格式筛选。
"""

from beanie import Document
from pydantic import Field
from datetime import datetime, timezone
from pymongo import IndexModel, ASCENDING, DESCENDING


class Image(Document):
    """图片文档模型

    Attributes:
        id: MongoDB 自动生成的代理主键（ObjectId），由 Beanie 自动管理
        url: 图片资源的网络地址（例如 OSS/CDN 地址）
        type: 图片格式（如：jpg, png, webp, gif 等）
        created_at: 图片入库时间
    """

    # 图片资源的网络地址（例如 OSS/CDN 地址）
    url: str

    # 图片格式（如：jpg, png, webp, gif 等）
    type: str

    # 图片入库时间，插入文档时自动填充
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        """Beanie 文档配置"""

        # MongoDB 集合名称
        name = "images"

        # 索引定义
        indexes = [
            # url 唯一索引：防止同一 URL 的图片被重复入库
            # 同时加速「根据 URL 查找图片」的查询
            IndexModel(
                [("url", ASCENDING)],
                unique=True,
                name="idx_url_unique"
            ),
            # type 普通索引：加速「按图片格式筛选」的查询
            # 例如：查询所有 png 格式的图片
            IndexModel(
                [("type", ASCENDING)],
                name="idx_type"
            ),
            # created_at 降序索引：加速「最新入库图片」列表查询
            # 用于首页瀑布流、图片列表分页等场景
            IndexModel(
                [("created_at", DESCENDING)],
                name="idx_created_at_desc"
            ),
        ]


"""
# 示例文档结构
{
  "_id": ObjectId("..."),
  "url": "https://example.com/images/photo.jpg",
  "type": "jpg",
  "created_at": ISODate("2025-01-01T00:00:00Z")
}

# 根据 URL 查找图片（用于去重）
image = await Image.find_one(Image.url == "https://example.com/images/photo.jpg")

# 查询指定格式的图片
images = await Image.find(
    Image.type == "png"
).sort(-Image.created_at).to_list()
"""
