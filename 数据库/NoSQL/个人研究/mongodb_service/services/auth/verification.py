"""
邮件验证码服务模块

独立的验证码生成、存储、校验、发送功能。
通过 Redis 管理验证码生命周期（5分钟有效 + 60秒发送冷却），
不直接修改 utils/message_util.py，仅通过调用其公开函数完成邮件发送。

Redis Key 设计:
    email_code:{email}      → 6位验证码，TTL 300s（5分钟）
    email_cooldown:{email}  → "1"，TTL 60s（发送冷却期）
"""
# 内置库
import os
import random
# 三方库
# 无三方依赖，仅使用 redis_client 和 send_verification_email
# 自己的模块
from services.database.redis import redis_client
from utils.message_util import send_verification_email
from logger import info, warning


"""Key 生成"""

def _code_key(email: str) -> str:
    """验证码 Redis key"""
    return f"email_code:{email}"


def _cooldown_key(email: str) -> str:
    """冷却期 Redis key"""
    return f"email_cooldown:{email}"


"""验证码生成"""

def generate_code() -> str:
    """生成6位随机数字验证码"""
    return ''.join(random.choices('0123456789', k=6))


"""验证码存储与校验"""

async def save_verification_code(email: str, code: str) -> None:
    """将验证码存入 Redis，TTL 后自动过期"""
    key = _code_key(email)
    await redis_client.set(key, code, ex=int(os.getenv("VERIFICATION_CODE_TTL", "300")))


async def verify_and_consume_code(email: str, code: str) -> bool:
    """
    校验验证码并立即消费（一次性使用）

    验证成功 → 删除 Redis 中的验证码 → 返回 True
    验证失败 → 返回 False
    """
    key = _code_key(email)
    stored = await redis_client.get(key)

    if stored is None:
        warning(f"验证码不存在或已过期: {email}")
        return False

    if stored != code:
        warning(f"验证码不匹配: {email}")
        return False

    # 一次性消费，删除验证码防止重用
    await redis_client.delete(key)
    info(f"验证码校验成功并已消费: {email}")
    return True


"""冷却期控制"""

async def check_send_cooldown(email: str) -> bool:
    """
    检查是否在冷却期内

    Returns:
        True  → 可以发送（不在冷却期）
        False → 不能发送（冷却期内，须等待）
    """
    key = _cooldown_key(email)
    if await redis_client.exists(key):
        ttl = await redis_client.ttl(key)
        warning(f"发送冷却期内: {email}, 剩余 {ttl}s")
        return False
    return True


async def set_send_cooldown(email: str) -> None:
    """设置发送冷却期标记"""
    key = _cooldown_key(email)
    await redis_client.set(key, "1", ex=int(os.getenv("COOLDOWN_TTL", "60")))


"""核心业务：发送验证码"""

async def send_code(email: str) -> tuple[bool, str]:
    """
    向指定邮箱发送验证码

    编排完整流程:
    ① 检查冷却期 → 60秒内禁止重复发送
    ② 生成6位验证码
    ③ 存入 Redis（5分钟有效）
    ④ 调用邮件服务发送
    ⑤ 设置冷却期标记

    Args:
        email: 接收验证码的邮箱地址

    Returns:
        (success, message)
        - (True,  "验证码已发送")    → 发送成功
        - (False, "请 X 秒后再试")   → 冷却期内
        - (False, "邮件发送失败: ...") → 邮件服务异常
    """
    # ① 冷却期检查
    if not await check_send_cooldown(email):
        ttl = await redis_client.ttl(_cooldown_key(email))
        return False, f"请 {ttl} 秒后再试"

    # ② 生成验证码
    code = generate_code()

    # ③ 存入 Redis
    await save_verification_code(email, code)

    # ④ 发送邮件（调用已有的邮件工具，不动 message_util.py）
    try:
        send_verification_email(email, code)
    except Exception as e:
        warning(f"邮件发送失败: {email}, 错误: {e}")
        return False, f"邮件发送失败: {e}"

    # ⑤ 设置冷却期
    await set_send_cooldown(email)
    return True, "验证码已发送"

if __name__ == '__main__':
    import asyncio
    asyncio.run(send_code("3058439878@qq.com"))