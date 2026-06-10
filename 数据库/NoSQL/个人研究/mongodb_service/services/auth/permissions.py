"""
权限检查模块

提供基于 FastAPI Depends 的声明式权限控制。

使用示例:
    # 需要特定角色
    @app.delete("/users/{user_id}")
    async def delete_user(
        user_id: str,
        current_user: User = Depends(require_role("admin"))
    ):
        ...

    # 只能操作自己的资源
    @app.put("/users/{user_id}/profile")
    async def update_profile(
        user_id: str,
        current_user: User = Depends(check_resource_owner("user_id"))
    ):
        ...
"""

from typing import Callable, Optional

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from data_models.database import User
from services.auth.dependencies import get_current_user
from logger import warning


# ============================================================================
#  角色权限检查
# ============================================================================

def require_role(*allowed_roles: str) -> Callable:
    """
    检查当前用户是否拥有指定角色之一

    这是一个工厂函数，返回一个 FastAPI 依赖:
        Depends(require_role("admin"))
        Depends(require_role("admin", "moderator"))

    使用前需要确保 User 模型有 role 字段。

    Args:
        *allowed_roles: 允许的角色列表

    Returns:
        依赖函数，验证通过后返回 User 对象
    """

    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        user_role: Optional[str] = getattr(current_user, "role", None)

        if user_role is None:
            warning(f"用户 {current_user.email} 无角色信息")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="用户未分配角色",
            )

        if user_role not in allowed_roles:
            warning(f"用户 {current_user.email} 角色 {user_role} 不在 {allowed_roles} 中")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要以下角色之一: {allowed_roles}",
            )

        return current_user

    return role_checker


# ============================================================================
#  资源所有权检查
# ============================================================================

def check_resource_owner(path_param: str) -> Callable:
    """
    检查当前用户是否是指定资源的所有者

    使用方式:
        @app.put("/users/{user_id}/profile")
        async def update_profile(
            user_id: str,
            current_user: User = Depends(check_resource_owner("user_id"))
        ):
            # current_user.id == user_id 才能继续执行
            ...

    Args:
        path_param: 路由路径参数名（如 "user_id"）

    Returns:
        依赖函数
    """
    from fastapi import Request

    async def owner_checker(
        request: Request,
        current_user: User = Depends(get_current_user),
    ) -> User:
        resource_owner_id = request.path_params.get(path_param)

        if resource_owner_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"路径参数 '{path_param}' 不存在",
            )

        if str(current_user.id) != str(resource_owner_id):
            warning(
                f"用户 {current_user.email} 尝试访问 {path_param}={resource_owner_id} 的资源"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问此资源",
            )

        return current_user

    return owner_checker
