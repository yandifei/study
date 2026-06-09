"""
service.database 包

封装 MongoDB 数据库初始化和索引管理功能。
"""

from service.database.mongodb import init_db, close_db
from service.database.index_manager import (
    create_all_indexes,
    verify_indexes,
    list_indexes,
    drop_extra_indexes,
    warmup_indexes,
)

__all__ = [
    "init_db",
    "close_db",
    "create_all_indexes",
    "verify_indexes",
    "list_indexes",
    "drop_extra_indexes",
    "warmup_indexes",
]
