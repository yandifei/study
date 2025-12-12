"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
import json

import yaml

# 导入日志记录器模块（第一行主程序代码就是启动日志记录器）
from utils import logger_manager, info, critical
# 导入配置管理模块
from utils import ConfigManager
# 导入日志记录器(启动并解析日志配置)

# 创建配置管理器实例（这是个单例）
config_manager = ConfigManager()
# 层叠覆盖原来的日志配置
logger_manager.use_logging_config(config_manager)
info("程序启动，全局异常捕获完成，日志记录器成功开启")