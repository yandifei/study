"""项目相关API路由"""
from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
async def get_items():
    """获取项目列表"""
    return {"items": []}

@router.get("/{item_id}")
async def get_item(item_id: int):
    """获取特定项目"""
    return {"item_id": item_id, "name": "test item"}