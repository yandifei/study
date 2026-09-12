"""
ConfigModel是最根本的模型
使用pydantic库构建合法模型
"""

__author__ = "yandifei"
__package__ = "models"
# 顶层封装
from data_models.config_model import ConfigModel

# 允许的外部导出
__all__ = [
    "ConfigModel",
]
