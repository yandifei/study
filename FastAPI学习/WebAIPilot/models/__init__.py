"""请求模型
使用pydantic库构建合法模型
"""

__author__ = "yandifei"
__package__ = "models"
# 顶层封装
from .ask_model import AskModel
# 允许的外部导出
__all__ = [
    "AskModel"
]
