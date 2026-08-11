"""__init__.py"""
# 只暴露公共 API
from .logger import LoggerManager, logger_manager, debug, info, warning, error, critical, exception  # <--- (A)
# import logger
# __all__ = ['public_function', 'PublicClass']


__author__ = 'yandifei'

