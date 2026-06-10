"""
Refresh Token 会话管理模块

使用 Redis 管理 Refresh Token 的生命周期，实现以下企业级安全能力:

1. Token 存储:
   - Key 格式: ``refresh:{user_id}:{jti}``
   - Value: ``"1"`` (简单存在标记)
   - TTL: 与 Refresh Token JWT 过期时间一致

2. Token Rotation (防重放攻击):
   - 每次刷新时，旧的 Refresh Token 立即作废
   - 同时发放新的 Refresh Token
   - 如果攻击者窃取并使用旧的 Token，服务端能检测到异常

3. 登出:
   - 单设备登出: 删除指定 jti 的 Token
   - 全设备登出: 删除该用户所有 Refresh Token (使用 SCAN 避免 KEYS 阻塞)

Redis Key 设计:
    refresh:{user_id}:{jti}  →  "1"
    例如: refresh:507f1f77bcf86cd799439011:a1b2c3d4-... → "1"
"""

import os
from typing import Optional

from services.database.redis import redis_client
from logger import info, warning


# ============================================================================
#  配置
# ============================================================================

def _get_refresh_ttl() -> int:
    """获取 Refresh Token 的 Redis TTL (秒)"""
    days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    return days * 24 * 60 * 60  # 转换为秒


def _make_key(user_id: str, jti: str) -> str:
    """生成 Redis key"""
    return f"refresh:{user_id}:{jti}"


# ============================================================================
#  Token 存储 (CRUD)
# ============================================================================

async def save_refresh_token(user_id: str, jti: str, expire_seconds: Optional[int] = None) -> None:
    """
    保存 Refresh Token 到 Redis

    Args:
        user_id: 用户 ID
        jti: JWT 唯一标识
        expire_seconds: TTL (秒)，默认使用环境变量中的 REFRESH_TOKEN_EXPIRE_DAYS

    Raises:
        redis.exceptions.RedisError: Redis 写入失败
    """
    if expire_seconds is None:
        expire_seconds = _get_refresh_ttl()

    key = _make_key(user_id, jti)
    await redis_client.set(key, "1", ex=expire_seconds)
    info(f"Refresh Token 已存储: user={user_id}, jti={jti[:8]}...")


async def exists_refresh_token(user_id: str, jti: str) -> bool:
    """
    检查 Refresh Token 是否在 Redis 中存在且有效

    Args:
        user_id: 用户 ID
        jti: JWT 唯一标识

    Returns:
        True 如果 Token 有效，False 如果已被撤销或过期
    """
    key = _make_key(user_id, jti)
    return bool(await redis_client.exists(key))


async def delete_refresh_token(user_id: str, jti: str) -> bool:
    """
    删除单个 Refresh Token (用于单设备登出)

    Args:
        user_id: 用户 ID
        jti: JWT 唯一标识

    Returns:
        True 如果成功删除，False 如果 Token 已不存在
    """
    key = _make_key(user_id, jti)
    deleted = await redis_client.delete(key)
    if deleted:
        info(f"Refresh Token 已删除: user={user_id}, jti={jti[:8]}...")
    return bool(deleted)


# ============================================================================
#  Token Rotation (核心安全机制)
# ============================================================================

async def rotate_refresh_token(
    user_id: str,
    old_jti: str,
    new_jti: str,
    expire_seconds: Optional[int] = None,
) -> bool:
    """
    Refresh Token Rotation —— 用旧 Token 换新 Token

    安全原理:
    1. 删除旧的 Refresh Token (使其立即失效)
    2. 创建新的 Refresh Token
    3. 如果旧的 Token 已被使用过 (不存在于 Redis)，说明可能发生了重放攻击

    这个操作不是原子性的 (Redis 事务)，但在实际场景中:
    - 即使步骤2失败，旧的已删除也是安全的 (强制用户重新登录)
    - 步骤1和2之间的窗口极小 (毫秒级)

    Args:
        user_id: 用户 ID
        old_jti: 旧的 JWT 唯一标识 (即将被作废)
        new_jti: 新的 JWT 唯一标识 (即将生效)
        expire_seconds: 新 Token 的 TTL

    Returns:
        True 如果轮换成功，False 如果旧 Token 已失效 (可能被重放攻击)

    Raises:
        RefreshTokenReuseError: 检测到旧 Token 可能被重放
    """
    # 步骤 1: 验证旧 Token 是否还存在
    old_key = _make_key(user_id, old_jti)
    if not await redis_client.exists(old_key):
        warning(f"⚠️ 疑似 Refresh Token 重放攻击: user={user_id}, jti={old_jti[:8]}...")
        # 安全措施: 删除该用户的所有 Refresh Token，强制全部重新登录
        await revoke_all_user_tokens(user_id)
        return False

    # 步骤 2: 删除旧 Token
    await redis_client.delete(old_key)

    # 步骤 3: 创建新 Token
    new_key = _make_key(user_id, new_jti)
    if expire_seconds is None:
        expire_seconds = _get_refresh_ttl()
    await redis_client.set(new_key, "1", ex=expire_seconds)

    info(f"Refresh Token 轮换完成: user={user_id}, old={old_jti[:8]}... → new={new_jti[:8]}...")
    return True


# ============================================================================
#  登出操作
# ============================================================================

async def revoke_all_user_tokens(user_id: str) -> int:
    """
    撤销某用户的所有 Refresh Token (全设备强制登出)

    使用 SCAN 而非 KEYS，因为:
    - KEYS 会阻塞 Redis 主线程（在生产环境中是灾难性的）
    - SCAN 是增量迭代，不会阻塞其他请求

    Args:
        user_id: 用户 ID

    Returns:
        被删除的 Token 数量
    """
    pattern = f"refresh:{user_id}:*"
    deleted_count = 0

    # 使用 SCAN 增量迭代，避免阻塞 Redis
    cursor = 0
    while True:
        cursor, keys = await redis_client.scan(
            cursor=cursor,
            match=pattern,
            count=100,  # 每次扫描 100 个 key
        )
        if keys:
            deleted_count += await redis_client.delete(*keys)
        if cursor == 0:
            break

    info(f"用户 {user_id} 的所有 Refresh Token 已撤销，共 {deleted_count} 个")
    return deleted_count


async def count_user_sessions(user_id: str) -> int:
    """
    统计某用户当前有效的 Refresh Token 数量 (即活跃会话数)

    Args:
        user_id: 用户 ID

    Returns:
        活跃会话数
    """
    pattern = f"refresh:{user_id}:*"
    count = 0

    cursor = 0
    while True:
        cursor, keys = await redis_client.scan(
            cursor=cursor,
            match=pattern,
            count=100,
        )
        count += len(keys)
        if cursor == 0:
            break

    return count
