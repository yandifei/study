"""
用户数据模型

纯 pydantic BaseModel。浏览和收藏以嵌入式数组存储于用户文档中。
"""
# 内置库
from datetime import datetime, timezone
from typing import Optional
# 三方库
from pydantic import BaseModel, Field
# 自己的模块
from data_models.database.browse import BrowseItem
from data_models.database.favorite import FavoriteItem


class User(BaseModel):
    """用户模型

    MongoDB 文档结构:
    {
      "_id": ObjectId("..."),   ← 数据访问层转为 id: str
      "email": "user@qq.com",
      "username": "用户名",
      "browse_records": [       ← 嵌入式数组，最多 1000 条，按 image_id 排序
        { "image_id": "20250610120000", "image_url": "https://...", "browse_time": ISODate }
      ],
      "favorite_records": [     ← 嵌入式数组，无上限，按 image_id 排序
        { "image_id": "20250610120000", "image_url": "https://...", "favorite_time": ISODate }
      ],
      "created_at": ISODate("..."),
      "updated_at": ISODate("...")
    }
    """

    id: Optional[str] = Field(
        default=None,
        description="用户唯一标识（MongoDB ObjectId → str）",
    )
    email: str = Field(..., description="用户邮箱，业务唯一标识（登录凭证）")
    username: str = Field(..., description="用户昵称/显示名称")
    browse_records: list[BrowseItem] = Field(
        default_factory=list,
        description="浏览记录（嵌入式数组，最多 1000 条，按 image_id 排序）",
    )
    favorite_records: list[FavoriteItem] = Field(
        default_factory=list,
        description="收藏记录（嵌入式数组，无上限，按 image_id 排序）",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="账号创建时间",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="最近一次信息更新时间",
    )
