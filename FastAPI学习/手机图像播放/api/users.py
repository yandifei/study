"""用户相关API路由"""
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def get_users():
    """获取用户列表"""
    return {"users": []}

@router.get("/{user_id}")
async def get_user(user_id: int):
    """获取特定用户"""
    return {"user_id": user_id, "name": "test user"}