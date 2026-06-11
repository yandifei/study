"""
收藏记录服务包 (services.favorite)

收藏记录嵌入在 User.favorite_records 数组中。
"""
from services.favorite.service import (
    add_favorite,
    get_user_favorites,
    delete_favorite,
    delete_all_favorites,
)
from services.favorite.router import router as favorite_router

__all__ = [
    "add_favorite",
    "get_user_favorites",
    "delete_favorite",
    "delete_all_favorites",
    "favorite_router",
]
