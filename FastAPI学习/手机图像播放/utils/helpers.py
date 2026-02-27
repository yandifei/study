"""通用工具函数"""

import hashlib
import uuid
from datetime import datetime
from typing import Any, Dict, List, Generator


def generate_uuid() -> str:
    """生成UUID"""
    return str(uuid.uuid4())

def hash_string(text: str) -> str:
    """对字符串进行MD5哈希"""
    return hashlib.md5(text.encode()).hexdigest()

def format_datetime(dt: datetime) -> str:
    """格式化日期时间"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def snake_to_camel(snake_str: str) -> str:
    """蛇形命名转驼峰命名"""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def camel_to_snake(camel_str: str) -> str:
    """驼峰命名转蛇形命名"""
    return ''.join(['_' + c.lower() if c.isupper() else c for c in camel_str]).lstrip('_')

def safe_get_nested_dict(data: Dict, keys: List[str], default: Any = None) -> Any:
    """安全获取嵌套字典的值"""
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data

def chunk_list(lst: List, chunk_size: int) -> Generator[list[Any], Any, None]:
    """将列表分块"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def is_valid_email(email: str) -> bool:
    """验证邮箱格式"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def mask_sensitive_data(data: str, show_chars: int = 4) -> str:
    """遮蔽敏感数据"""
    if len(data) <= show_chars * 2:
        return "*" * len(data)
    return data[:show_chars] + "*" * (len(data) - show_chars * 2) + data[-show_chars:]