"""
FastAPI 认证依赖注入模块

提供声明式的用户认证依赖，让任何路由函数只需在参数中声明
``current_user: User = Depends(get_current_user)`` 即可获取当前用户。

企业实践:
- OAuth2PasswordBearer: FastAPI 标准方式，自动从 Authorization Header 提取 Bearer token
- get_current_user: 核心依赖，验证 token → 查数据库 → 返回 User 对象
- get_optional_user: 可选认证，未登录的用户也能访问，但可以区分登录态
- require_permission: 基于角色的权限检查工厂函数

使用示例:
    @app.get("/me")
    async def my_profile(current_user: User = Depends(get_current_user)):
        return {"user_id": str(current_user.id), "email": current_user.email}

    @app.get("/admin")
    async def admin_only(
        current_user: User = Depends(require_permission("admin"))
    ):
        return {"msg": "欢迎管理员"}
"""

# 内置库
from typing import Optional, Callable

# 第三方库
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel

# 自己的模块
from bson import ObjectId
from data_models.database import User
from services.database.mongodb import get_collection
from services.auth.jwt import (
    extract_user_id_from_access_token,
    TokenExpiredError,
    TokenInvalidError,
    TokenMissingError,
    TokenTypeError,
    InsufficientPermissionError,
)
from logger import info, warning


# ============================================================================
#  OAuth2 安全方案定义
#  tokenUrl 指向登录接口，FastAPI 自动生成的 Swagger 文档中会出现认证按钮
# ============================================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",      # Swagger UI 中"Authorize"按钮会调用此地址
    scheme_name="JWT",            # 显示名称
    description="输入 Access Token（格式: Bearer <token>）"
)


# ============================================================================
#  核心依赖: 获取当前登录用户
# ============================================================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    从请求中提取并验证 Access Token，返回对应的 User 对象

    执行流程:
    1. FastAPI 从 Authorization: Bearer <token> 中提取 token 字符串
    2. 验证 JWT 签名、有效期、类型
    3. 提取 sub 字段（用户 ID）
    4. 从 MongoDB 查找用户
    5. 返回 User 对象，路由函数可直接使用

    Raises:
        TokenMissingError: 请求头中没有 Authorization
        TokenExpiredError: Access Token 已过期 → HTTP 401
        TokenInvalidError: Token 无效 → HTTP 401
    """
    user_id = extract_user_id_from_access_token(token)

    # 从 MongoDB 查找用户
    users = get_collection("users")
    doc = await users.find_one({"_id": ObjectId(user_id)})
    if doc is None:
        warning(f"Token 有效但用户不存在: user_id={user_id}")
        raise TokenInvalidError("用户不存在或已被删除")

    # MongoDB dict → User 对象
    doc["id"] = str(doc.pop("_id"))
    user = User(**doc)
    return user


# ============================================================================
#  可选认证: 用户可以不登录，但登录后会注入 User 对象
# ============================================================================

async def get_optional_user(
    request: Request,
) -> Optional[User]:
    """
    可选认证依赖 —— 用户登录与否都能访问，但返回的 User 可能为 None

    使用场景:
    - 公开内容页面（登录用户看到个性化内容，未登录用户看到通用内容）
    - 统计/日志类接口（记录用户行为但不强制登录）

    使用方式:
        @app.get("/public-content")
        async def content(user: Optional[User] = Depends(get_optional_user)):
            if user:
                return {"msg": f"你好 {user.username}，这里是个性化内容"}
            return {"msg": "你好游客，这里是通用内容"}
    """
    # 手动从 Authorization Header 提取 token
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.removeprefix("Bearer ").strip()
    if not token:
        return None

    try:
        user_id = extract_user_id_from_access_token(token)
        users = get_collection("users")
        doc = await users.find_one({"_id": ObjectId(user_id)})
        if doc:
            doc["id"] = str(doc.pop("_id"))
            return User(**doc)
        return None
    except (TokenExpiredError, TokenInvalidError, TokenTypeError):
        return None


# ============================================================================
#  基于角色的权限检查（工厂函数模式）
# ============================================================================

def require_role(*allowed_roles: str) -> Callable:
    """
    角色权限检查工厂函数

    企业实践:
    - 工厂函数模式：require_role("admin", "moderator") 返回一个新的依赖函数
    - 在路由中声明式使用: Depends(require_role("admin"))
    - 权限逻辑与业务逻辑分离

    使用方式:
        # 管理员专用接口
        @app.delete("/users/{user_id}")
        async def delete_user(
            user_id: str,
            current_user: User = Depends(require_role("admin"))
        ):
            ...

        # 管理员和版主都可以访问
        @app.get("/reports")
        async def view_reports(
            current_user: User = Depends(require_role("admin", "moderator"))
        ):
            ...

    注意:
    - 当前 User 模型没有 role 字段，你需要先在 User 模型中添加 role: str 字段
    - 如果暂时不需要角色系统，可以只用 get_current_user 做基础认证
    """

    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        # 检查用户是否有 role 属性
        user_role = getattr(current_user, "role", None)

        if user_role is None:
            warning(f"用户 {current_user.email} 没有角色信息")
            raise InsufficientPermissionError("用户没有分配角色")

        if user_role not in allowed_roles:
            warning(f"用户 {current_user.email} 角色 {user_role} 不在允许列表 {allowed_roles} 中")
            raise InsufficientPermissionError(
                f"需要 {allowed_roles} 角色，当前角色为 {user_role}"
            )

        return current_user

    return role_checker
