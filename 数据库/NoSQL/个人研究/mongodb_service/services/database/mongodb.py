"""
MongoDB 数据库初始化模块

负责创建异步 MongoDB 连接并初始化 Beanie ODM。
所有文档模型的索引在 init_beanie() 调用时自动创建。
"""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from data_models.database import User, Image, Browse, Favorite


async def init_db(uri: str = "mongodb://root:root@localhost:27017",
                  db_name: str = "graduation_project"):
    """初始化 MongoDB 连接和 Beanie ODM

    Args:
        uri: MongoDB 连接字符串
        db_name: 数据库名称

    Returns:
        (client, db) 元组，调用方可用于后续操作或关闭连接
    """
    client = AsyncIOMotorClient(uri)
    db = client[db_name]

    await init_beanie(
        database=db,
        document_models=[
            User,
            Image,
            Browse,
            Favorite,
        ]
    )

    return client, db


async def close_db(client: AsyncIOMotorClient):
    """关闭 MongoDB 连接"""
    client.close()
