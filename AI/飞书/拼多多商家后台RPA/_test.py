"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
# 内置库
import asyncio
# 自己的模块
from logger import logger_manager, info, critical    # 导入日志记录器模块
from utils.config_manager import ConfigManager # 导入配置管理模块

# 创建配置管理器实例（这是个单例）
config_manager = ConfigManager(debug=True)
# 层叠覆盖原来的日志配置
config_manager.config_override()    # 层叠覆盖原来的配置
info("日志模块加载完成，全局异常捕获开启")

