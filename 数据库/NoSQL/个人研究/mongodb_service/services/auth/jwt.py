"""
JWT 令牌工具模块

实现企业级双 Token 体系:
- Access Token: 短期 (默认15分钟)，放在前端内存，每次 API 请求通过 Authorization Header 携带
- Refresh Token: 长期 (默认30天)，jti 存储在 Redis 中，用于换取新的 Access Token

安全设计:
- 每个 Token 有唯一 jti (JWT ID)，实现精确撤销能力
- 签发者 (iss) 校验，防止跨应用 Token 滥用
- 类型 (type) 校验，防止 Access/Refresh Token 互换攻击
- 自定义异常体系，让 FastAPI 异常处理器返回精确的 HTTP 状态码
"""

# 内置库
import os
from datetime import datetime, timedelta, timezone
from typing import Literal, Any
from uuid import uuid4

# 第三方库
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWSSignatureError, JWTError, JWTClaimsError

# 自己的模块
from logger import debug, info, warning


# ============================================================================
#  自定义异常体系
#  为什么不用 return False？
#  因为 FastAPI 的 Depends() 依赖注入需要在异常传播链上捕获特定异常，
#  从而返回不同的 HTTP 状态码（401, 403 等），这是企业级 API 的标准做法。
# ============================================================================

class AuthException(Exception):
    """认证异常基类 —— 所有认证相关异常都继承此类"""
    def __init__(self, message: str = "认证失败"):
        self.message = message
        super().__init__(self.message)


class TokenExpiredError(AuthException):
    """Token 已过期 → HTTP 401"""
    def __init__(self, message: str = "Token 已过期，请刷新"):
        super().__init__(message)


class TokenInvalidError(AuthException):
    """Token 无效（签名错误、被篡改等） → HTTP 401"""
    def __init__(self, message: str = "Token 无效"):
        super().__init__(message)


class TokenMissingError(AuthException):
    """Token 缺失 → HTTP 401"""
    def __init__(self, message: str = "缺少认证令牌"):
        super().__init__(message)


class TokenTypeError(AuthException):
    """Token 类型错误（用 refresh token 访问 API 等） → HTTP 401"""
    def __init__(self, message: str = "Token 类型不正确"):
        super().__init__(message)


class InsufficientPermissionError(AuthException):
    """权限不足 → HTTP 403"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(message)


# ============================================================================
#  JWT 载荷类型定义
# ============================================================================

# Access Token 的载荷字段
AccessPayload = dict[str, Any]
# Refresh Token 的载荷字段
RefreshPayload = dict[str, Any]
# 解码后的通用载荷
DecodedPayload = dict[str, Any]


# ============================================================================
#  Token 创建函数
# ============================================================================

def _now_utc() -> datetime:
    """获取当前 UTC 时间 —— 确保每次调用 iat/nbf/exp 使用一致的时间基准"""
    return datetime.now(timezone.utc)


def create_access_token(user_id: str) -> str:
    """
    生成 Access Token

    企业实践:
    - Access Token 短期有效（默认 15 分钟），即使泄露影响也有限
    - 放在前端内存（React state / Vue reactive），不存 localStorage（防 XSS）
    - 每次 API 请求通过 Header: Authorization: Bearer <token> 携带

    Args:
        user_id: 用户唯一标识（对应 MongoDB 中 User 文档的 _id）

    Returns:
        编码后的 JWT 字符串
    """
    now = _now_utc()
    expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))

    payload = {
        "iss": os.getenv("APP_NAME", "default-app"),   # 签发者
        "sub": user_id,                                  # 主体（用户 ID）
        "jti": str(uuid4()),                             # Token 唯一标识（用于撤销）
        "type": "access",                                # Token 类型（防止与 refresh 互换）
        "iat": now,                                      # 签发时间
        "nbf": now,                                      # 生效时间（即签即用）
        "exp": now + timedelta(minutes=expire_minutes),  # 过期时间
    }

    token = jwt.encode(
        claims=payload,
        key=os.environ["ACCESS_TOKEN_SECRET_KEY"],
        algorithm=os.environ["ACCESS_TOKEN_ALGORITHM"],
    )

    info(f"Access Token 已签发: sub={user_id}, jti={payload['jti']}")
    return token


def create_refresh_token(user_id: str) -> str:
    """
    生成 Refresh Token

    企业实践:
    - Refresh Token 长期有效（默认 30 天），用于在 Access Token 过期后换取新的
    - 前端放 httpOnly Secure SameSite Cookie 中（防 XSS + CSRF）
    - 服务端将 jti 存入 Redis，可实现精确撤销

    Args:
        user_id: 用户唯一标识

    Returns:
        编码后的 JWT 字符串
    """
    now = _now_utc()
    expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))

    payload = {
        "iss": os.getenv("APP_NAME", "default-app"),   # 签发者（refresh 也应有 iss）
        "sub": user_id,
        "jti": str(uuid4()),
        "type": "refresh",
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(days=expire_days),
    }

    token = jwt.encode(
        claims=payload,
        key=os.environ["REFRESH_TOKEN_SECRET_KEY"],
        algorithm=os.environ["REFRESH_TOKEN_ALGORITHM"],
    )

    info(f"Refresh Token 已签发: sub={user_id}, jti={payload['jti']}")
    return token


# ============================================================================
#  Token 验证函数
# ============================================================================

def _get_key_and_algorithm(token_type: Literal["access", "refresh"]) -> tuple[str, str]:
    """根据 token 类型获取对应的密钥和算法"""
    if token_type == "refresh":
        return (
            os.environ["REFRESH_TOKEN_SECRET_KEY"],
            os.environ["REFRESH_TOKEN_ALGORITHM"],
        )
    else:
        return (
            os.environ["ACCESS_TOKEN_SECRET_KEY"],
            os.environ["ACCESS_TOKEN_ALGORITHM"],
        )


def verify_token(
    token: str,
    token_type: Literal["access", "refresh"] = "access",
) -> DecodedPayload:
    """
    验证 JWT 并返回解码后的载荷

    企业实践:
    - 使用 jose 库的 options 参数强制要求必要字段存在
    - 验证失败时抛出明确的自定义异常（而非返回 False）
    - 上游调用者（如 FastAPI 依赖注入）可以捕获特定异常
      并返回对应的 HTTP 状态码

    Args:
        token: JWT 字符串
        token_type: Token 类型 ("access" 或 "refresh")

    Returns:
        解码后的 JWT 载荷字典

    Raises:
        TokenExpiredError: Token 已过期
        TokenInvalidError: Token 无效（签名错误/字段缺失/非法）
        TokenTypeError: Token 类型不匹配
    """
    key, algorithm = _get_key_and_algorithm(token_type)

    # 第 1 层：加密验证（签名、过期时间、必要字段）
    try:
        payload = jwt.decode(
            token=token,
            key=key,
            algorithms=[algorithm],
            options={
                "require_sub": True,   # sub 必须存在
                "require_jti": True,   # jti 必须存在
                "require_type": True,  # type 必须存在
                "require_exp": True,   # exp 必须存在
                "verify_signature": True,  # 验证签名
                "verify_exp": True,        # 验证过期
            },
        )
    except ExpiredSignatureError:
        info(f"Token 已过期: type={token_type}")
        raise TokenExpiredError("Token 已过期，请刷新") from None
    except JWTClaimsError as e:
        info(f"Token 声明不完整: {str(e)}")
        raise TokenInvalidError("Token 格式不完整") from None
    except (JWSSignatureError, JWTError) as e:
        info(f"Token 无效: {str(e)}")
        raise TokenInvalidError("Token 无效") from None

    # 第 2 层：业务验证（签发者、用户 ID、类型匹配）
    expected_iss = os.getenv("APP_NAME", "default-app")

    if payload.get("iss") != expected_iss:
        warning(f"Token 签发者不匹配: 期望={expected_iss}, 实际={payload.get('iss')}")
        raise TokenInvalidError("Token 签发者无效")

    if not payload.get("sub"):
        warning("Token 中用户 ID 为空")
        raise TokenInvalidError("Token 用户标识缺失")

    if payload.get("type") != token_type:
        warning(f"Token 类型不匹配: 期望={token_type}, 实际={payload.get('type')}")
        raise TokenTypeError(f"期望 {token_type} token，但收到 {payload.get('type')} token")

    return payload


# ============================================================================
#  便捷函数：一步完成验证 + 提取用户 ID
# ============================================================================

def decode_token(
    token: str,
    token_type: Literal["access", "refresh"] = "access",
) -> DecodedPayload:
    """
    轻量解码 JWT —— 不做完整业务校验，仅解码并验证签名+过期

    使用场景:
    - 刚创建的 token，只需读取载荷字段（如 jti、exp）
    - 不需要重复做 issuer/type 等业务校验

    与 verify_token 的区别:
    - verify_token: 完整校验（签名+过期+iss+sub+type），用于外部请求
    - decode_token:  轻量解码（签名+过期），用于内部读取载荷

    Args:
        token: JWT 字符串
        token_type: Token 类型

    Returns:
        解码后的 JWT 载荷字典

    Raises:
        TokenExpiredError: Token 已过期
        TokenInvalidError: Token 无效
    """
    key, algorithm = _get_key_and_algorithm(token_type)

    try:
        payload = jwt.decode(
            token=token,
            key=key,
            algorithms=[algorithm],
            options={
                "verify_signature": True,
                "verify_exp": True,
            },
        )
    except ExpiredSignatureError:
        raise TokenExpiredError("Token 已过期") from None
    except (JWSSignatureError, JWTError) as e:
        raise TokenInvalidError("Token 无效") from None

    return payload


def extract_user_id_from_access_token(token: str) -> str:
    """
    从 Access Token 中提取用户 ID

    这是 API 请求中最常用的函数：
    1. 验证 token 签名和有效期
    2. 提取 sub 字段（用户 ID）

    Args:
        token: Access Token 字符串

    Returns:
        用户 ID (MongoDB ObjectId 的字符串形式)

    Raises:
        TokenExpiredError / TokenInvalidError / TokenTypeError
    """
    payload = verify_token(token, token_type="access")
    return payload["sub"]
