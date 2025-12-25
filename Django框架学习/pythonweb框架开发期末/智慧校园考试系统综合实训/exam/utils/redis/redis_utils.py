# utils/redis_utils.py
import redis
from django.conf import settings
import json

def get_redis_connection():
    """获取Redis连接"""
    return redis.Redis(
        host=getattr(settings, 'REDIS_HOST', 'localhost'),
        port=getattr(settings, 'REDIS_PORT', 6379),
        db=getattr(settings, 'REDIS_DB', 0),
        password=getattr(settings, 'REDIS_PASSWORD', None),
        decode_responses=True  # 自动解码为字符串
    )

def get_signcode(sign):
    """从Redis获取邮箱验证码"""
    try:
        redis_conn = get_redis_connection()
        email = redis_conn.get(f'email_sign:{sign}')
        return email
    except Exception as e:
        print(f"Redis获取signcode失败: {e}")
        return None

def set_signcode(sign, email, expire_time=3600):
    """设置邮箱验证码到Redis"""
    try:
        redis_conn = get_redis_connection()
        redis_conn.setex(f'email_sign:{sign}', expire_time, email)
        return True
    except Exception as e:
        print(f"Redis设置signcode失败: {e}")
        return False

def delete_signcode(sign):
    """删除已使用的验证码"""
    try:
        redis_conn = get_redis_connection()
        redis_conn.delete(f'email_sign:{sign}')
        return True
    except Exception as e:
        print(f"Redis删除signcode失败: {e}")
        return False