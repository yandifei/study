"""
认证路由模块

验证码登录 + JWT 双 Token 体系。

端点:
    POST /auth/send-code → 发送6位验证码到邮箱（60s冷却，5min有效）
    POST /auth/login     → 验证码校验 + 新用户自动注册 + 签发双 Token
    POST /auth/refresh   → 使用 Refresh Token 换取新的 Token 对（无感刷新）
    POST /auth/logout    → 登出，撤销 Refresh Token
    GET  /auth/me        → 获取当前登录用户信息（受保护接口示例）
"""
# 内置库
import os
# 三方库
from fastapi import APIRouter, Depends, HTTPException, status
# 自己的模块
from bson import ObjectId
from data_models.database import User
from data_models.auth_model import (
    SendCodeRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    LogoutRequest,
    UserInfoResponse,
)
from services.database.mongodb import get_collection
from services.auth.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token,
    decode_token,
    TokenExpiredError,
    TokenInvalidError,
    TokenTypeError,
)
from services.auth.session_service import (
    save_refresh_token,
    exists_refresh_token,
    revoke_all_user_tokens,
    rotate_refresh_token,
    delete_refresh_token,
)
from services.auth.dependencies import get_current_user
from services.auth.verification import send_code, verify_and_consume_code
from logger import info, warning


"""Router 定义"""

router = APIRouter(
    prefix="/auth",
    tags=["认证"],
    responses={
        401: {"description": "未认证"},
        403: {"description": "权限不足"},
    },
)


"""签发 Token 的内部函数"""

async def _issue_tokens(user_id: str) -> TokenResponse:
    """为用户签发双 Token 并持久化 refresh token 到 Redis"""
    # 生成双 Token
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)

    # 解码 refresh token 获取 jti，存入 Redis
    refresh_payload = verify_token(refresh_token, token_type="refresh")
    expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    await save_refresh_token(
        user_id=user_id,
        jti=refresh_payload["jti"],
        expire_seconds=expire_days * 24 * 60 * 60,
    )

    # 获取 access token 有效期
    access_payload = decode_token(access_token, token_type="access")
    expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    info(f"Token 签发完成: user={user_id}")

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=expire_minutes * 60,
    )


"""发送验证码"""

@router.post(
    "/send-code",
    summary="发送验证码",
    description="向指定邮箱发送6位数字验证码，60秒内禁止重复发送，5分钟内有效",
)
async def send_verification_code(request: SendCodeRequest):
    """
    发送验证码流程:
    ① 检查冷却期（60秒内禁止重复）
    ② 生成6位随机码
    ③ 存入 Redis（5分钟有效）
    ④ 通过 QQ 邮箱发送
    ⑤ 设置冷却期
    """
    success, message = await send_code(request.email)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
            if "秒后再试" in message
            else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )
    return {"code": 200, "msg": message, "data": None}


"""验证码登录"""

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="验证码登录",
    description="验证邮箱和验证码，新用户自动注册，返回 Access Token 和 Refresh Token",
)
async def login(request: LoginRequest):
    """
    验证码登录流程:
    ① 校验验证码（一次性消费，验证后立即删除）
    ② 查找用户 → 不存在则自动创建（验证码即注册）
    ③ 签发双 Token
    """
    # ① 验证码校验
    if not await verify_and_consume_code(request.email, request.code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="验证码错误或已过期",
        )

    # ② 查找或创建用户（验证码即注册）
    users = get_collection("users")
    doc = await users.find_one({"email": request.email})

    if doc:
        # 已有用户：_id → id
        doc["id"] = str(doc.pop("_id"))
        user = User(**doc)
    else:
        # 新用户：自动注册
        user = User(email=request.email, username=request.email)
        result = await users.insert_one(user.model_dump(exclude={"id"}))
        user.id = str(result.inserted_id)
        info(f"新用户注册: {request.email}")

    # ③ 签发 Token
    info(f"用户登录成功: {user.email}")
    return await _issue_tokens(str(user.id))


"""刷新 Token"""

@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="刷新 Token",
    description="使用 Refresh Token 换取新的 Access Token + Refresh Token 对（无感刷新）",
)
async def refresh(request: RefreshRequest):
    """
    刷新流程（Token Rotation）:
    ① 验证 Refresh Token 签名和有效期
    ② 检查 Token 是否已被撤销（防重放）
    ③ 签发新的双 Token
    ④ 旧的 Refresh Token 作废，新的生效

    前端无感刷新模式:
    - 请求 API → 返回 401 → 自动调 /auth/refresh → 拿到新 token → 重试原请求
    """
    # ① 验证 Refresh Token
    try:
        refresh_payload = verify_token(request.refresh_token, token_type="refresh")
    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token 已过期，请重新登录",
            headers={"X-Token-Error": "expired"},
        )
    except (TokenInvalidError, TokenTypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token 无效",
            headers={"X-Token-Error": "invalid"},
        )

    user_id = refresh_payload["sub"]
    old_jti = refresh_payload["jti"]

    # ② 检查是否已被撤销
    if not await exists_refresh_token(user_id, old_jti):
        warning(f"Refresh Token 重放检测: user={user_id}")
        await revoke_all_user_tokens(user_id)  # 安全措施：全部撤销
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="检测到可疑的 Token 重用，请重新登录",
            headers={"X-Token-Error": "reused"},
        )

    # 验证用户是否还存在
    users = get_collection("users")
    doc = await users.find_one({"_id": ObjectId(user_id)})
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
        )

    # ③ 签发新 Token
    new_access_token = create_access_token(user_id)
    new_refresh_token = create_refresh_token(user_id)
    new_refresh_payload = verify_token(new_refresh_token, token_type="refresh")

    # ④ Token Rotation
    expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    rotated = await rotate_refresh_token(
        user_id=user_id,
        old_jti=old_jti,
        new_jti=new_refresh_payload["jti"],
        expire_seconds=expire_days * 24 * 60 * 60,
    )
    if not rotated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 刷新失败，请重新登录",
        )

    expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=expire_minutes * 60,
    )


"""登出"""

@router.post(
    "/logout",
    summary="用户登出",
    description="撤销 Refresh Token，使当前会话失效",
)
async def logout(
    request: LogoutRequest,
    current_user: User = Depends(get_current_user),
):
    """
    登出流程:
    ① 验证 Access Token（确保合法用户操作）
    ② 提供 refresh_token → 单设备登出
       未提供 refresh_token → 全设备登出
    """
    user_id = str(current_user.id)

    if request.refresh_token:
        # 单设备登出
        try:
            refresh_payload = verify_token(request.refresh_token, token_type="refresh")
            await delete_refresh_token(user_id, refresh_payload["jti"])
            info(f"用户 {current_user.email} 单设备登出成功")
        except (TokenExpiredError, TokenInvalidError, TokenTypeError):
            pass  # Token 已无效，无需操作
    else:
        # 全设备登出
        count = await revoke_all_user_tokens(user_id)
        info(f"用户 {current_user.email} 全设备登出成功，撤销了 {count} 个会话")

    return {"code": 200, "msg": "登出成功", "data": None}


"""获取当前用户信息"""

@router.get(
    "/me",
    response_model=UserInfoResponse,
    summary="获取当前用户信息",
    description="返回当前登录用户的详细信息（需要有效的 Access Token）",
)
async def get_me(current_user: User = Depends(get_current_user)):
    """受保护接口示例：在路由中声明 ``Depends(get_current_user)`` 即可完成认证"""
    return UserInfoResponse(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )
