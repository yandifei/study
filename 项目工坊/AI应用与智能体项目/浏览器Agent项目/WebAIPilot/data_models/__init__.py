"""
ConfigModel是最根本的模型
使用pydantic库构建合法模型
"""

__author__ = "yandifei"
__package__ = "models"
# 顶层封装
from data_models.config_model import ConfigModel
from data_models.ask_model import AskModel
from data_models.playwright.context_options import ContextOptions
from data_models.playwright.launch_options import LaunchOptions
# 允许的外部导出
__all__ = [
    "ConfigModel",
    "AskModel",
    "ContextOptions",
    "LaunchOptions"
]
