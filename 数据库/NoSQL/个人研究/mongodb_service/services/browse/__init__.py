"""
浏览记录服务包 (services.browse)

浏览记录嵌入在 User.browse_records 数组中。
"""
from services.browse.service import (
    add_browse_records,
    get_user_browse_records,
    delete_all_browse_records,
)
from services.browse.router import router as browse_router

__all__ = [
    "add_browse_records",
    "get_user_browse_records",
    "delete_all_browse_records",
    "browse_router",
]
