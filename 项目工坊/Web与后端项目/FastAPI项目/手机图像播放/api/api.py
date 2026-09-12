"""聚合v1版本的所有API路由"""

from fastapi import APIRouter

# 导入各个路由模块
from . import users, items, system

# 创建API路由器
api_router = APIRouter()

# 包含各个端点的路由
api_router.include_router(users.router)
api_router.include_router(items.router)
api_router.include_router(system.router)