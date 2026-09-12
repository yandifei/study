"""__init__.py"""
# 只暴露公共 API
# from .browser_factory import Browser
from .logger import LoggerManager, logger_manager, debug, info, warning, error, critical, exception  # <--- (A)
from .config_manager import ConfigManager
from .path_utils import get_root, is_path_exist, get_parent_path, mkdir
# import logger
# __all__ = ['public_function', 'PublicClass']


__author__ = 'yandifei'
