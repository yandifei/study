"""
MongoDB 数据库初始化模块

使用 pymongo 原生异步（AsyncMongoClient）管理连接。
不依赖 ODM，直接操作 collections，通过 pydantic BaseModel 做数据校验。
"""
# 内置库
import os
# 三方库
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.collection import AsyncCollection
# 自己的模块
from utils.path_utils import get_root
from logger import info

"""数据库实例（模块级单例）"""
_client: AsyncMongoClient | None = None
_db: AsyncDatabase | None = None


async def init_db(
    uri: str = "",
    db_name: str = "",
):
    """初始化 MongoDB 连接

    Args:
        uri: 连接字符串，为空则从环境变量自动拼接
        db_name: 数据库名称，为空则使用 APP_NAME 环境变量

    Returns:
        (client, db) 元组
    """
    global _client, _db

    if not uri:
        uri = os.getenv("MONGODB_URL", "mongodb://localhost:27017/?directConnection=true")
    if not db_name:
        db_name = os.getenv("APP_NAME", "test")

    _client = AsyncMongoClient(uri)
    _db = _client[db_name]
    info(f"MongoDB 连接数据库成功: {db_name}")

    return _client, _db


async def close_db(client: AsyncMongoClient | None = None):
    """关闭 MongoDB 连接"""
    global _client
    c = client or _client
    if c:
        await c.close()
        info("MongoDB 连接已关闭")


def get_db() -> AsyncDatabase:
    """获取数据库实例，未初始化则抛异常"""
    if _db is None:
        raise RuntimeError("数据库未初始化，请先调用 init_db()")
    return _db


def get_collection(name: str) -> AsyncCollection:
    """获取指定集合"""
    return get_db()[name]


if __name__ == '__main__':
    import asyncio
    asyncio.run(init_db())
