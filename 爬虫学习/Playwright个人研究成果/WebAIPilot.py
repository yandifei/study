"""WebAIPilot.py
程序主入口
优先加载日志记录器
"""
import json

# 导入配置管理模块
from utils import ConfigManager
# 导入日志记录器(启动并解析日志配置)
from utils import info
# 导入日志记录器模块

# 创建配置管理器实例（这是个单例）
config_manager = ConfigManager()
# print(config_manager.config_data)
# print(json.dumps(config_manager.config_data))
info("程序启动，全局异常捕获完成，日志记录器成功开启")

data = config_manager.load_logging_config()

# print(json.dumps(data))