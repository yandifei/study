"""
service.database 包

MongoDB 连接管理 + Redis 客户端。
"""
from services.database.mongodb import init_db, close_db, get_db, get_collection

__all__ = [
    "init_db",
    "close_db",
    "get_db",
    "get_collection",
]
