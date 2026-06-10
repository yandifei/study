"""
用户数据模型

纯 pydantic BaseModel，不依赖 Beanie ODM。
ObjectId ↔ str 转换在数据访问层处理，模型保持干净。
"""
# 内置库
from datetime import datetime, timezone
from typing import Optional
# 三方库
from pydantic import BaseModel, Field


class User(BaseModel):
    """用户模型

    MongoDB 文档结构:
    {
      "_id": ObjectId("..."),   ← 数据访问层转为 id: str
      "email": "user@qq.com",
      "username": "用户名",
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
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="账号创建时间",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="最近一次信息更新时间",
    )
