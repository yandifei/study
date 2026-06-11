"""
浏览记录路由

端点:
    POST   /browse/  → 批量插入浏览记录
    GET    /browse/  → 查询当前用户浏览记录（最多 1000 条）
    DELETE /browse/  → 清空当前用户浏览记录
"""
# 三方库
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
# 自己的模块
from data_models.database import User
from services.browse.service import (
    add_browse_records,
    get_user_browse_records,
    delete_all_browse_records,
)
from services.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/browse",
    tags=["浏览记录"],
)


class BrowseImageItem(BaseModel):
    """单张图片"""
    image_id: str = Field(..., description="图片唯一标识（时间戳）")
    image_url: str = Field(..., description="图片 URL")


class BrowseBatchRequest(BaseModel):
    """批量浏览请求"""
    images: list[BrowseImageItem] = Field(
        ...,
        min_length=1,
        description="浏览的图片列表",
    )


"""批量插入"""

@router.post("/", summary="批量记录浏览")
async def batch_insert(
    request: BrowseBatchRequest,
    current_user: User = Depends(get_current_user),
):
    images = [{"image_id": img.image_id, "image_url": img.image_url} for img in request.images]
    await add_browse_records(str(current_user.id), images)
    return {"code": 200, "msg": f"已记录 {len(images)} 条浏览", "data": None}


"""查询"""

@router.get("/", summary="我的浏览记录（分页）")
async def my_records(
    limit: int = 20,
    skip: int = 0,
    current_user: User = Depends(get_current_user),
):
    """默认返回最近 20 条，最大 100 条"""
    limit = min(limit, 100)  # 硬限制，防止一次拉太多
    records = await get_user_browse_records(str(current_user.id), limit=limit, skip=skip)
    return {
        "code": 200,
        "msg": "success",
        "data": {
            "limit": limit,
            "skip": skip,
            "records": [r.model_dump() for r in records],
        },
    }


"""删除"""

@router.delete("/", summary="清空我的浏览记录")
async def delete_all(
    current_user: User = Depends(get_current_user),
):
    await delete_all_browse_records(str(current_user.id))
    return {"code": 200, "msg": "浏览记录已清空", "data": None}
