"""
用户数据模型

对应 MongoDB 中的 users 集合，存储用户基本信息。
使用邮箱作为文档主键（_id），每个用户仅有一条记录。
"""

from beanie import Document
from pydantic import Field
from datetime import datetime


class User(Document):
    """用户文档模型

    Attributes:
        id: 用户邮箱，映射为 MongoDB 的 _id 字段
        username: 用户昵称/显示名称
        created_at: 账号创建时间
        updated_at: 最近一次信息更新时间
    """

    # 用户邮箱，作为 MongoDB 文档主键（_id）
    id: str = Field(alias="_id")

    # 用户昵称/显示名称
    username: str

    # 账号创建时间，插入文档时自动填充
    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    # 最近一次信息更新时间，每次修改时需手动刷新
    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    class Settings:
        """Beanie 文档配置"""

        # MongoDB 集合名称
        name = "users"


"""
# 示例文档结构
{
  "_id": "admin@qq.com",
  "username": "admin"
}
"""