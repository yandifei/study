"""
收藏记录路由

端点:
    POST   /favorite/            → 添加收藏
    GET    /favorite/            → 查询当前用户全部收藏
    DELETE /favorite/{image_id}  → 删除单条收藏
    DELETE /favorite/            → 清空当前用户全部收藏
"""
# 三方库
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
# 自己的模块
from data_models.database import User
from services.favorite.service import (
    add_favorite,
    get_user_favorites,
    delete_favorite,
    delete_all_favorites,
)
from services.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/favorite",
    tags=["收藏记录"],
)


class AddFavoriteRequest(BaseModel):
    """添加收藏请求"""
    image_id: str = Field(..., description="图片唯一标识（时间戳）")
    image_url: str = Field(..., description="图片 URL")


"""添加"""

@router.post("/", summary="添加收藏")
async def add(
    request: AddFavoriteRequest,
    current_user: User = Depends(get_current_user),
):
    await add_favorite(str(current_user.id), request.image_id, request.image_url)
    return {"code": 200, "msg": "收藏成功", "data": None}


"""查询"""

@router.get("/", summary="我的收藏列表（分页）")
async def my_favorites(
    limit: int = 20,
    skip: int = 0,
    current_user: User = Depends(get_current_user),
):
    """默认返回最近 20 条，最大 100 条"""
    limit = min(limit, 100)
    records = await get_user_favorites(str(current_user.id), limit=limit, skip=skip)
    return {
        "code": 200,
        "msg": "success",
        "data": {
            "limit": limit,
            "skip": skip,
            "records": [r.model_dump() for r in records],
        },
    }


"""删除单条"""

@router.delete("/{image_id}", summary="取消收藏")
async def remove(
    image_id: str,
    current_user: User = Depends(get_current_user),
):
    await delete_favorite(str(current_user.id), image_id)
    return {"code": 200, "msg": "已取消", "data": None}


"""删除全部"""

@router.delete("/", summary="清空我的收藏")
async def remove_all(
    current_user: User = Depends(get_current_user),
):
    await delete_all_favorites(str(current_user.id))
    return {"code": 200, "msg": "收藏已清空", "data": None}
