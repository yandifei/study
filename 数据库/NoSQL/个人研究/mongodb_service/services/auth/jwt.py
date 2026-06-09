# 内置库
import os
from datetime import datetime, timedelta, timezone
from typing import Literal
from uuid import uuid4
# 第三方库
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWSSignatureError, JWTError, JWTClaimsError
# 自己的模块
from logger import debug, info, warning

def create_access_token(user_id: str)-> str:
    """
    生成access的JWT，这个放前端
    """
    # access默认15分钟有效期
    exp = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)))
    # JWT载荷(Payload)
    payload = {
        "iss": os.getenv("APP_NAME"),           # 签发者
        "sub": user_id,                         # 用户ID
        "jti": str(uuid4()),                    # Token唯一ID
        "type": "access",                       # token类型
        "iat": datetime.now(timezone.utc),      # 签发时间
        "nbf": datetime.now(timezone.utc),      # 生效时间
        "exp": exp                              # 过期时间
    }

    # 生成JWT
    return jwt.encode(
        claims=payload,
        # JWT密钥
        key=os.environ["ACCESS_TOKEN_SECRET_KEY"],
        # 加密算法
        algorithm=os.environ["ACCESS_TOKEN_ALGORITHM"]
    )

def create_refresh_token(user_id: str)-> str:
    """
    生成refresh的JWT，这个放redis
    """
    # refresh默认30天有效期
    exp = datetime.now(timezone.utc) + timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30)))
    # JWT载荷(Payload)
    payload = {
        "sub": user_id,                         # 用户ID
        "jti": str(uuid4()),                    # Token唯一ID
        "type": "refresh",                      # token类型
        "exp": exp                              # 过期时间
    }

    # 生成JWT
    return jwt.encode(
        claims=payload,
        # JWT密钥
        key=os.environ["REFRESH_TOKEN_SECRET_KEY"],
        # 加密算法
        algorithm=os.environ["REFRESH_TOKEN_ALGORITHM"]
    )


def verify_token(token: str, token_type: Literal["access", "refresh"] ="access"):
    """校验JWT是否有效，如果无效则返回False """
    if token_type == "refresh":
        algorithm = os.environ["REFRESH_TOKEN_ALGORITHM"]
        key = os.environ["REFRESH_TOKEN_SECRET_KEY"]
    else:
        algorithm = os.environ["ACCESS_TOKEN_ALGORITHM"]
        key = os.environ["ACCESS_TOKEN_SECRET_KEY"]

    try:
        payload = jwt.decode(
            token=token,
            # JWT密钥
            key=key,
            # 加密算法
            algorithms=[algorithm],
            # 仅仅只能保证字段出现在token中，无法保证字段是否为空
            options={
                "require_sub": True,  # 要求用户ID必须存在
                "require_jti": True,  # 要求Token唯一ID必须存在
                "require_type": True,  # 要求type必须存在
                "require_exp": True,  # 要求exp必须存在
            }
        )
        # 验证签发者
        if payload.get("iss") != os.getenv("APP_NAME"):
            info("token签发者错误")
            return False
        # 验证用户ID
        if payload.get("sub") == "" or payload.get("sub") is None or  payload.get("sub") is False:
            info("token用户ID为空")
            return False
        return payload
    except ExpiredSignatureError:
        info("Token已过期")
        return False
    except JWTClaimsError:
        info("Token声明错误(token字段缺失)")
        return False
    except JWTError:
        info("Token无效")
        return False
    except Exception as e:
        # 捕获意外异常
        warning(f"token校验存在未知错误: {str(e)}")
        return False