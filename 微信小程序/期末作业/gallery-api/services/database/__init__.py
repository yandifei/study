"""
service.database 包

MongoDB 连接管理 + 索引管理 + Redis 客户端。
"""
from services.database.mongodb import init_db, close_db, get_db, get_collection
from services.database.index_manager import (
    create_all_indexes,
    verify_indexes,
    list_indexes,
    drop_extra_indexes,
    warmup_indexes,
)

__all__ = [
    "init_db",
    "close_db",
    "get_db",
    "get_collection",
    "create_all_indexes",
    "verify_indexes",
    "list_indexes",
    "drop_extra_indexes",
    "warmup_indexes",
]
