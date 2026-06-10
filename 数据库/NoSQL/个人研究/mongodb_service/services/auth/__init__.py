"""
认证服务包 (services.auth)

提供完整的企业级 JWT 认证体系:

核心模块:
    jwt.py              → JWT 创建、验证、异常定义
    session_service.py  → Redis 会话管理 (Refresh Token 存储/轮换/撤销)
    verification.py     → 邮件验证码服务 (生成/存储/校验/发送)
    dependencies.py     → FastAPI 依赖注入 (get_current_user 等)
    router.py           → 认证路由 (/auth/send-code, /auth/login, /auth/refresh, /auth/logout, /auth/me)
    permissions.py      → 权限检查装饰器

快速使用:
    from services.auth import router as auth_router
    app.include_router(auth_router)

    from services.auth import get_current_user, require_role
"""

from services.auth.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token,
    decode_token,
    extract_user_id_from_access_token,
    AuthException,
    TokenExpiredError,
    TokenInvalidError,
    TokenMissingError,
    TokenTypeError,
    InsufficientPermissionError,
)

from services.auth.dependencies import (
    get_current_user,
    get_optional_user,
    require_role,
    oauth2_scheme,
)

from services.auth.session_service import (
    save_refresh_token,
    exists_refresh_token,
    delete_refresh_token,
    rotate_refresh_token,
    revoke_all_user_tokens,
    count_user_sessions,
)

from services.auth.router import router as auth_router

__all__ = [
    # JWT 核心
    "create_access_token",
    "create_refresh_token",
    "verify_token",
    "decode_token",
    "extract_user_id_from_access_token",
    # 异常
    "AuthException",
    "TokenExpiredError",
    "TokenInvalidError",
    "TokenMissingError",
    "TokenTypeError",
    "InsufficientPermissionError",
    # 依赖注入
    "get_current_user",
    "get_optional_user",
    "require_role",
    "oauth2_scheme",
    # Redis 会话管理
    "save_refresh_token",
    "exists_refresh_token",
    "delete_refresh_token",
    "rotate_refresh_token",
    "revoke_all_user_tokens",
    "count_user_sessions",
    # 路由
    "auth_router",
]
