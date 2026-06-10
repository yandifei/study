"""
认证模块请求/响应数据模型

FastAPI 接口的 Pydantic 模型定义，包括邮箱验证、Token、用户信息等。
从 services/auth/router.py 中抽离，方便统一管理。
"""
# 内置库
from datetime import datetime
# 三方库
from pydantic import BaseModel, Field, EmailStr


"""发送验证码"""

class SendCodeRequest(BaseModel):
    """发送验证码请求"""
    email: EmailStr = Field(
        ...,
        examples=["user@qq.com"],
        description="接收验证码的邮箱",
    )


"""验证码登录"""

class LoginRequest(BaseModel):
    """验证码登录请求"""
    email: EmailStr = Field(
        ...,
        examples=["user@qq.com"],
        description="用户邮箱",
    )
    code: str = Field(
        ...,
        min_length=6,
        max_length=6,
        examples=["123456"],
        description="6位数字验证码",
    )


"""Token"""

class TokenResponse(BaseModel):
    """Token 响应"""
    access_token: str = Field(..., description="Access Token (短期，用于 API 请求)")
    refresh_token: str = Field(..., description="Refresh Token (长期，用于刷新)")
    token_type: str = Field(default="bearer", description="Token 类型 (固定为 bearer)")
    expires_in: int = Field(..., description="Access Token 有效期 (秒)")


class RefreshRequest(BaseModel):
    """刷新请求"""
    refresh_token: str = Field(..., description="已持有的 Refresh Token")


"""登出"""

class LogoutRequest(BaseModel):
    """登出请求（单设备登出）"""
    refresh_token: str = Field(
        default="",
        description="要撤销的 Refresh Token，为空则登出所有设备",
    )


"""用户信息"""

class UserInfoResponse(BaseModel):
    """用户信息响应"""
    id: str
    email: EmailStr
    username: str
    created_at: datetime
    updated_at: datetime
